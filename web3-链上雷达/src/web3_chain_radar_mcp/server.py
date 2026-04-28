from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from web3_chain_radar_mcp.tools.onchain import (
    classify_token_narrative_impl,
    scan_onchain_narratives_impl,
)


mcp = FastMCP("web3-chain-radar")


@mcp.tool()
async def scan_onchain_narratives(
    chains: str = "eth,bsc,base,sol",
    limit_per_chain: int = 50,
    include_safety: bool = True,
    strict_safety: bool = False,
    include_profiles: bool = False,
    max_results: int = 20,
) -> dict[str, Any]:
    """Scan GMGN ranked tokens and return narrative, momentum, and safety signals.

    Args:
        chains: Comma-separated chain names. Supported: eth,bsc,base,sol.
        limit_per_chain: Max rows per GMGN endpoint.
        include_safety: Check RugCheck for Solana and GoPlus for EVM chains.
        strict_safety: Drop tokens when safety is unavailable or unsafe.
        include_profiles: Fetch social links from DexScreener.
        max_results: Maximum ranked candidates to return.
    """
    return await scan_onchain_narratives_impl(
        chains=chains,
        limit_per_chain=limit_per_chain,
        include_safety=include_safety,
        strict_safety=strict_safety,
        include_profiles=include_profiles,
        max_results=max_results,
    )


@mcp.tool()
def classify_token_narrative(name: str, symbol: str, chain: str = "eth") -> dict[str, Any]:
    """Classify a token name and symbol into the radar narrative taxonomy."""
    return classify_token_narrative_impl(name=name, symbol=symbol, chain=chain)


def main() -> None:
    mcp.run()

