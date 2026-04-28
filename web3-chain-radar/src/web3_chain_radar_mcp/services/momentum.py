from __future__ import annotations

import time
from dataclasses import dataclass, field

from web3_chain_radar_mcp.models import TokenCandidate


@dataclass
class MomentumState:
    snapshots: dict[str, list[dict[str, float]]] = field(default_factory=dict)
    pushed: dict[str, dict[str, float]] = field(default_factory=dict)

    def update(self, token: TokenCandidate, rounds: int = 3) -> tuple[bool, float, list[str]]:
        now = time.time()
        key = f"{token.chain}:{token.address.lower()}"
        snapshots = self.snapshots.setdefault(key, [])

        if snapshots and snapshots[-1]["market_cap"] == token.market_cap and snapshots[-1]["volume"] == token.volume:
            return False, 0, ["GMGN data unchanged since previous scan"]

        snapshots.append(
            {
                "ts": now,
                "market_cap": token.market_cap,
                "volume": token.volume,
                "buys": float(token.buys_1h),
            }
        )
        if len(snapshots) > 20:
            self.snapshots[key] = snapshots[-20:]
            snapshots = self.snapshots[key]

        if len(snapshots) < rounds:
            return False, 0, [f"needs {rounds} changing snapshots for strict momentum"]

        recent = snapshots[-rounds:]
        for previous, current in zip(recent, recent[1:]):
            if current["market_cap"] <= previous["market_cap"]:
                return False, 0, ["market cap is not rising consecutively"]

        first = recent[0]["market_cap"]
        last = recent[-1]["market_cap"]
        gain = ((last - first) / first * 100) if first > 0 else 0
        if gain < 5:
            return False, gain, ["consecutive rise is below 5%"]

        last_push = self.pushed.get(key)
        if last_push and last <= last_push.get("market_cap", 0):
            return False, gain, ["market cap has not exceeded previous alert"]

        self.pushed[key] = {"ts": now, "market_cap": last}
        return True, gain, [f"strict momentum: {rounds} rising snapshots, +{gain:.1f}%"]


def heuristic_score(token: TokenCandidate, narrative_stars: int) -> tuple[float, list[str]]:
    score = float(narrative_stars * 20)
    reasons: list[str] = [f"narrative stars: {narrative_stars}/3"]

    if token.price_change_1h > 5:
        score += min(token.price_change_1h, 30)
        reasons.append(f"1h price change is positive: {token.price_change_1h:.1f}%")
    if token.price_change_24h > 20:
        score += min(token.price_change_24h / 2, 25)
        reasons.append(f"24h price change is strong: {token.price_change_24h:.1f}%")
    if token.volume > 50_000:
        score += 10
        reasons.append("volume is above $50k")
    if token.liquidity > 10_000:
        score += 10
        reasons.append("liquidity is above $10k")
    if token.smart_money_count > 0:
        score += min(token.smart_money_count * 5, 20)
        reasons.append(f"smart money count: {token.smart_money_count}")
    if token.buys_1h > token.sells_1h and token.buys_1h > 0:
        score += 10
        reasons.append("1h buys exceed sells")

    return round(score, 2), reasons


STATE = MomentumState()

