---
name: web3-chain-radar-en
description: Use the web3-chain-radar MCP server to scan on-chain tokens, narrative labels, momentum signals, liquidity, volume, and basic safety risks. Use when users ask about Web3 token radar, on-chain narratives, GMGN rankings, meme token momentum, or basic token risk checks.
---

# web3-chain-radar

## When To Use

Use this skill when the user wants to:

- Scan new or trending tokens on ETH, BSC, Base, or Solana
- Classify token narratives such as Musk/Trump, Binance/CZ, celebrity/viral, or emerging themes
- Inspect GMGN-ranked tokens for momentum, liquidity, volume, buys, and sells
- Run basic safety checks through RugCheck or GoPlus
- Get structured candidates for research instead of trade execution

## Tools

### `scan_onchain_narratives`

Scan on-chain tokens and return structured candidates.

Common parameters:

- `chains`: comma-separated chain names, for example `eth,bsc,base,sol`
- `limit_per_chain`: max GMGN rows per endpoint
- `include_safety`: whether to check RugCheck or GoPlus
- `strict_safety`: whether to drop unsafe or unchecked tokens
- `include_profiles`: whether to fetch DexScreener social links
- `max_results`: maximum number of candidates to return

Recommended default:

```text
scan_onchain_narratives(chains="eth,bsc,base,sol", include_safety=true, strict_safety=false, max_results=20)
```

### `classify_token_narrative`

Classify a token name, symbol, and chain into the radar narrative taxonomy.

## Behavior

This skill only scans and analyzes:

- It does not trade
- It does not connect wallets
- It does not store private keys
- It does not submit transactions
- It does not send Telegram messages by default

If the user asks to buy, sell, swap, or place an order, do not use this skill to execute the trade. Treat the output as research context only.

## Response Guidance

When summarizing results, include:

- Token name, chain, and address
- Narrative category and star rating
- Market cap, liquidity, 1h/24h change
- Whether safety checks succeeded and whether hard risks appeared
- Why a candidate ranked highly

Do not present scan results as guaranteed profit or financial advice.

