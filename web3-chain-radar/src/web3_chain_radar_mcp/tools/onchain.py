from __future__ import annotations

import asyncio
from typing import Any

from web3_chain_radar_mcp.clients.dexscreener import DexScreenerClient
from web3_chain_radar_mcp.clients.gmgn import GMGNClient
from web3_chain_radar_mcp.clients.safety import SafetyClient
from web3_chain_radar_mcp.config import load_settings
from web3_chain_radar_mcp.models import ScanResult
from web3_chain_radar_mcp.services.momentum import STATE, heuristic_score
from web3_chain_radar_mcp.services.narrative import classify_token


def parse_chains(chains: str | None) -> list[str]:
    settings = load_settings()
    if not chains:
        return list(settings.default_chains)
    return [chain.strip().lower() for chain in chains.split(",") if chain.strip()]


async def scan_onchain_narratives_impl(
    chains: str | None = None,
    limit_per_chain: int = 50,
    include_safety: bool = True,
    strict_safety: bool = False,
    include_profiles: bool = False,
    max_results: int = 20,
) -> dict[str, Any]:
    settings = load_settings()
    selected_chains = parse_chains(chains)
    gmgn = GMGNClient(timeout=settings.request_timeout)
    safety_client = SafetyClient()
    profile_client = DexScreenerClient()

    tokens = await gmgn.fetch_ranked_tokens(
        chains=selected_chains,
        limit_per_endpoint=limit_per_chain,
        min_market_cap=settings.min_market_cap,
        max_market_cap=settings.max_market_cap,
        min_liquidity=settings.min_liquidity,
    )

    results: list[ScanResult] = []
    for token in tokens:
        narrative = classify_token(token)
        if narrative.category == "spam":
            continue

        safety = None
        if include_safety:
            safety = await safety_client.check(token.chain, token.address)
            if strict_safety and (not safety.checked or not safety.safe):
                continue

        score, reasons = heuristic_score(token, narrative.stars)
        strict_signal, gain, momentum_reasons = STATE.update(token)
        if strict_signal:
            score += 30
            reasons.extend(momentum_reasons)
        elif gain > 0:
            reasons.append(f"partial momentum gain: {gain:.1f}%")
        else:
            reasons.extend(momentum_reasons[:1])

        if safety and safety.checked:
            if safety.safe:
                score += 10
                reasons.append(f"safety check passed via {safety.source}")
            else:
                score -= 30
                reasons.append(f"safety risk: {safety.reason}")

        results.append(
            ScanResult(
                token=token,
                narrative=narrative,
                safety=safety,
                score=round(score, 2),
                reasons=reasons,
            )
        )

    results.sort(key=lambda item: item.score, reverse=True)
    results = results[: max(1, max_results)]

    profiles: dict[str, dict[str, Any]] = {}
    if include_profiles and results:
        profile_tasks = [
            asyncio.create_task(profile_client.fetch_token_profile(item.token.address))
            for item in results
        ]
        fetched = await asyncio.gather(*profile_tasks, return_exceptions=True)
        for item, profile in zip(results, fetched):
            if isinstance(profile, Exception):
                continue
            token = item.token
            profiles[f"{token.chain}:{token.address}"] = profile

    return {
        "name": "web3-链上雷达",
        "chains": selected_chains,
        "scanned_tokens": len(tokens),
        "returned": len(results),
        "profile_data": profiles,
        "results": [item.to_dict() for item in results],
        "notes": [
            "This MCP tool only scans and ranks tokens. It does not trade.",
            "Strict momentum needs multiple calls in the same MCP server process.",
            "Safety APIs can be unavailable or rate-limited; inspect safety.checked before relying on it.",
        ],
    }


def classify_token_narrative_impl(name: str, symbol: str, chain: str = "eth") -> dict[str, Any]:
    from web3_chain_radar_mcp.models import TokenCandidate

    token = TokenCandidate(
        address="",
        chain=chain,
        name=name,
        symbol=symbol,
        market_cap=0,
        liquidity=0,
        volume=0,
        holders=0,
        smart_money_count=0,
        price_change_1h=0,
        price_change_24h=0,
        age_hours=0,
        price=0,
        buys_1h=0,
        sells_1h=0,
    )
    return classify_token(token).to_dict()
