from __future__ import annotations

from typing import Any

import httpx

from web3_chain_radar_mcp.models import SafetyResult


CHAIN_IDS = {
    "eth": "1",
    "ethereum": "1",
    "bsc": "56",
    "base": "8453",
}


class SafetyClient:
    def __init__(self, timeout: float = 10) -> None:
        self.timeout = timeout

    async def check(self, chain: str, address: str) -> SafetyResult:
        chain = chain.lower()
        if chain in ("sol", "solana"):
            return await self._check_sol(address)
        return await self._check_evm(chain, address)

    async def _check_sol(self, address: str) -> SafetyResult:
        url = f"https://api.rugcheck.xyz/v1/tokens/{address}/report"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                data: dict[str, Any] = response.json()
        except httpx.HTTPError as exc:
            return SafetyResult(False, False, "rugcheck", f"rugcheck unavailable: {exc}")

        mint = data.get("mintAuthority")
        freeze = data.get("freezeAuthority")
        safe = not mint and not freeze
        reason = "ok" if safe else "mint or freeze authority is present"
        return SafetyResult(
            checked=True,
            safe=safe,
            source="rugcheck",
            reason=reason,
            details={
                "score": data.get("score"),
                "mint_authority": bool(mint),
                "freeze_authority": bool(freeze),
            },
        )

    async def _check_evm(self, chain: str, address: str) -> SafetyResult:
        chain_id = CHAIN_IDS.get(chain)
        if not chain_id:
            return SafetyResult(False, False, "goplus", f"unsupported chain: {chain}")

        url = (
            f"https://api.gopluslabs.io/api/v1/token_security/{chain_id}"
            f"?contract_addresses={address}"
        )
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                payload = response.json()
        except httpx.HTTPError as exc:
            return SafetyResult(False, False, "goplus", f"goplus unavailable: {exc}")

        result = payload.get("result") or {}
        data = result.get(address.lower()) or result.get(address) or {}
        if not data:
            return SafetyResult(False, False, "goplus", "no security data")

        honeypot = data.get("is_honeypot", "0") == "1"
        mintable = data.get("is_mintable", "0") == "1"
        proxy = data.get("is_proxy", "0") == "1"
        sell_tax = _float(data.get("sell_tax"))
        buy_tax = _float(data.get("buy_tax"))
        safe = not honeypot and not mintable

        reason = "ok"
        if honeypot:
            reason = "honeypot"
        elif mintable:
            reason = "mintable contract"

        return SafetyResult(
            checked=True,
            safe=safe,
            source="goplus",
            reason=reason,
            details={
                "honeypot": honeypot,
                "mintable": mintable,
                "proxy": proxy,
                "buy_tax": buy_tax,
                "sell_tax": sell_tax,
            },
        )


def _float(value: Any) -> float:
    try:
        if value is None or value == "":
            return 0
        return float(value)
    except (TypeError, ValueError):
        return 0

