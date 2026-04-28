<p align="center">
  <b>web3-链上雷达</b><br>
  On-chain narrative radar for AI agents
</p>

<p align="center">
  <a href="./README.md">English</a> | <a href="./docs/README_ZH.md">中文</a>
</p>

---

Web3 on-chain narrative radar packaged as an MCP server.

It scans token rankings, classifies narratives, checks basic safety signals, and returns ranked candidates for an AI agent.

## Quick Install

```bash
cd web3-chain-radar
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run

```bash
web3-chain-radar-mcp
```

## MCP Config

```json
{
  "mcpServers": {
    "web3-chain-radar": {
      "command": "web3-chain-radar-mcp",
      "env": {
        "WEB3_RADAR_DEFAULT_CHAINS": "eth,bsc,base,sol"
      }
    }
  }
}
```

## Tools

### `scan_onchain_narratives`

Scan GMGN-ranked tokens across selected chains and return narrative, momentum, liquidity, volume, and safety signals.

Common parameters:

- `chains`: `eth,bsc,base,sol`
- `include_safety`: `true` or `false`
- `strict_safety`: `true` or `false`
- `include_profiles`: `true` or `false`
- `max_results`: number of candidates returned

### `classify_token_narrative`

Classify a token name and symbol into the radar narrative taxonomy.

## Notes

- No private keys
- No wallet access
- No trading execution
- Safety APIs may be rate-limited
- Strict momentum needs repeated calls in the same MCP process
