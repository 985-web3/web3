from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class TokenCandidate:
    address: str
    chain: str
    name: str
    symbol: str
    market_cap: float
    liquidity: float
    volume: float
    holders: int
    smart_money_count: int
    price_change_1h: float
    price_change_24h: float
    age_hours: float
    price: float
    buys_1h: int
    sells_1h: int
    source: str = "gmgn"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class NarrativeResult:
    category: str
    label: str
    stars: int
    matched_keywords: list[str]
    theme: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SafetyResult:
    checked: bool
    safe: bool
    source: str
    reason: str = ""
    details: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ScanResult:
    token: TokenCandidate
    narrative: NarrativeResult
    safety: SafetyResult | None
    score: float
    reasons: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "token": self.token.to_dict(),
            "narrative": self.narrative.to_dict(),
            "safety": self.safety.to_dict() if self.safety else None,
            "score": self.score,
            "reasons": self.reasons,
        }

