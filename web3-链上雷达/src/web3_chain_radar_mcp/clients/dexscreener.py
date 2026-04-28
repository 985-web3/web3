from __future__ import annotations

from typing import Any

import httpx


class DexScreenerClient:
    def __init__(self, timeout: float = 10) -> None:
        self.timeout = timeout

    async def fetch_token_profile(self, address: str) -> dict[str, Any]:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{address}"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                payload = response.json()
        except httpx.HTTPError:
            return {"description": "", "twitter": "", "telegram": "", "website": ""}

        pairs = payload.get("pairs") or []
        if not pairs:
            return {"description": "", "twitter": "", "telegram": "", "website": ""}

        info = pairs[0].get("info") or {}
        socials = info.get("socials") or []
        websites = info.get("websites") or []

        twitter = ""
        telegram = ""
        website = ""
        for item in socials:
            if item.get("type") == "twitter":
                twitter = item.get("url", "")
            elif item.get("type") == "telegram":
                telegram = item.get("url", "")

        for item in websites:
            if item.get("label", "").lower() == "website":
                website = item.get("url", "")
                break

        return {
            "description": "",
            "twitter": twitter,
            "telegram": telegram,
            "website": website,
        }

