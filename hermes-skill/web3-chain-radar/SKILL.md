---
name: web3-chain-radar
description: Use the web3-chain-radar MCP server to scan on-chain tokens, classify narratives, inspect momentum, liquidity, and basic safety risks. 当用户想查链上新币、GMGN 排行、叙事分类、动量信号或基础安全风险时使用。 Requires the `web3-chain-radar` MCP server to be configured first.
---

# web3-chain-radar

## What This Skill Is

This is a thin Hermes-style skill wrapper for the `web3-chain-radar` MCP server.

It is meant to be dropped into a `skills` directory so the assistant knows:

- when to use the radar
- which MCP tools to call
- how to present the results
- what not to do

This skill does not replace the MCP server. It depends on the `web3-chain-radar` MCP service being installed and connected.

## Prerequisite

Before using this skill, make sure the MCP server is available as `web3-chain-radar`.

If the MCP server is missing, explain that this skill needs the `web3-chain-radar-mcp` service installed and configured first.

## When To Use

Use this skill when the user wants to:

- scan new or active tokens on ETH, BSC, Base, or Solana
- inspect GMGN-ranked tokens
- classify narratives such as Musk/Trump, Binance/CZ, celebrity or viral themes, or emerging themes
- check momentum, liquidity, buys and sells, and basic safety signals
- get ranked research candidates instead of direct trading execution

## Tools

### `scan_onchain_narratives`

Use this as the primary tool.

Recommended default call:

```text
scan_onchain_narratives(
  chains="eth,bsc,base,sol",
  include_safety=true,
  strict_safety=false,
  include_profiles=false,
  max_results=20
)
```

Adjust parameters only when the user narrows scope.

### `classify_token_narrative`

Use this when the user asks about a token name, symbol, or theme classification without needing a full market scan.

## Output Guidance

When summarizing results, prioritize:

- token name, chain, and address
- narrative category and star level
- market cap, liquidity, and short-term price change
- safety result and whether the check succeeded
- why the token ranked highly

Keep the output concise and structured for decision support.

## Boundaries

This skill is for scanning and analysis only.

- Do not trade
- Do not connect wallets
- Do not handle private keys
- Do not present results as guaranteed profit

If the user asks to buy, sell, or place trades, treat the radar output as research context only.

