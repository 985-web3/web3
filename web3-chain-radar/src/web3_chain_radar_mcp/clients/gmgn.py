from __future__ import annotations

import time
from typing import Any

import httpx

from web3_chain_radar_mcp.models import TokenCandidate


GMGN_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "application/json",
    "Referer": "https://gmgn.ai/",
}


def _as_float(value: Any, default: float = 0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


class GMGNClient:
    def __init__(self, timeout: float = 15) -> None:
        self.timeout = timeout

    async def _get_data(self, client: httpx.AsyncClient, url: str) -> dict[str, Any]:
        response = await client.get(url, headers=GMGN_HEADERS)
        response.raise_for_status()
        payload = response.json()
        data = payload.get("data", {})
        return data if isinstance(data, dict) else {}

    async def fetch_ranked_tokens(
        self,
        chains: list[str],
        limit_per_endpoint: int = 50,
        min_market_cap: float = 1_000,
        max_market_cap: float = 10_000_000,
        min_liquidity: float = 500,
    ) -> list[TokenCandidate]:
        all_tokens: list[TokenCandidate] = []
        seen: set[tuple[str, str]] = set()

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for chain in chains:
                chain = chain.lower().strip()
                if not chain:
                    continue

                urls = [
                    f"https://gmgn.ai/defi/quotation/v1/rank/{chain}/swaps/1h"
                    f"?orderby=open_timestamp&direction=desc&limit={limit_per_endpoint}",
                    f"https://gmgn.ai/defi/quotation/v1/rank/{chain}/swaps/1h"
                    f"?orderby=swaps&direction=desc&limit={max(20, limit_per_endpoint // 2)}",
                ]

                for url in urls:
                    try:
                        data = await self._get_data(client, url)
                    except httpx.HTTPError:
                        continue

                    rows = data.get("rank", [])
                    if not isinstance(rows, list):
                        continue

                    for row in rows:
                        token = self._row_to_token(chain, row)
                        if not token:
                            continue
                        identity = (token.chain, token.address.lower())
                        if identity in seen:
                            continue
                        if token.market_cap < min_market_cap:
                            continue
                        if token.market_cap > max_market_cap:
                            continue
                        if token.liquidity < min_liquidity:
                            continue
                        seen.add(identity)
                        all_tokens.append(token)

        return all_tokens

    def _row_to_token(self, chain: str, row: dict[str, Any]) -> TokenCandidate | None:
        address = str(row.get("address") or "").strip()
        if not address:
            return None

        market_cap = _as_float(row.get("market_cap")) or _as_float(row.get("fdv"))
        liquidity = _as_float(row.get("liquidity"))
        opened_at = _as_float(row.get("open_timestamp"))
        age_hours = (time.time() - opened_at) / 3600 if opened_at > 0 else 999

        return TokenCandidate(
            address=address,
            chain=chain,
            name=str(row.get("name") or "?"),
            symbol=str(row.get("symbol") or "?"),
            market_cap=market_cap,
            liquidity=liquidity,
            volume=_as_float(row.get("volume")),
            holders=_as_int(row.get("holder_count")),
            smart_money_count=_as_int(row.get("smart_degen_count")),
            price_change_1h=_as_float(row.get("price_change_percent1h")),
            price_change_24h=_as_float(row.get("price_change_percent")),
            age_hours=age_hours,
            price=_as_float(row.get("price")),
            buys_1h=_as_int(row.get("buys")),
            sells_1h=_as_int(row.get("sells")),
            source="gmgn",
        )

