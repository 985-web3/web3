# web3-链上雷达

Web3 on-chain narrative radar packaged as an MCP server. It is based on the original single-file radar script, but reorganized into installable modules and MCP tools.

This project scans token rankings, classifies narratives, checks basic safety signals, and returns ranked candidates for an AI agent. It does not trade, hold private keys, or submit transactions.

## Tools

### `scan_onchain_narratives`

Scans GMGN ranked tokens across selected chains and returns narrative, momentum, liquidity, volume, and safety signals.

Parameters:

- `chains`: comma-separated chains, default `eth,bsc,base,sol`
- `limit_per_chain`: max GMGN rows per endpoint, default `50`
- `include_safety`: use RugCheck for Solana and GoPlus for EVM chains
- `strict_safety`: drop tokens when safety is unavailable or unsafe
- `include_profiles`: fetch social links from DexScreener
- `max_results`: number of candidates returned

### `classify_token_narrative`

Classifies a token name and symbol into the radar narrative taxonomy.

## Project Structure

```text
web3-链上雷达/
  pyproject.toml
  .env.example
  src/web3_chain_radar_mcp/
    server.py
    config.py
    clients/
      gmgn.py
      dexscreener.py
      safety.py
    services/
      narrative.py
      momentum.py
    tools/
      onchain.py
  openclaw-skill/
    web3-chain-radar-zh/
      SKILL.md
      package.json
    web3-chain-radar-en/
      SKILL.md
      package.json
```

## Install

```bash
cd web3-链上雷达
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run MCP Server

```bash
web3-chain-radar-mcp
```

Example MCP config:

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

## Environment

Copy `.env.example` to `.env` if you want local defaults.

```bash
cp .env.example .env
```

Current scanning works without private keys or wallet access. Telegram variables are reserved for a later optional delivery feature.

## Notes

- Safety APIs can be rate-limited or unavailable. Check `safety.checked` before relying on a safety result.
- Strict momentum needs repeated calls in the same running MCP server process.
- This is research tooling, not financial advice.

