---
name: web3-chain-radar-zh
description: 使用 web3-链上雷达 MCP 扫描链上新币、叙事标签、动量信号和基础安全风险。适合用户询问 Web3 新币雷达、链上热点、GMGN 排行、Meme 币叙事、是否有动量或基础风险时使用。
---

# web3-链上雷达

## 什么时候使用

当用户想要：

- 扫描 ETH、BSC、Base、Solana 上的新币或热门币
- 判断代币属于什么叙事，例如马斯克/川普、币安/CZ、名人热点、普通新叙事
- 查看 GMGN 排行中的动量、流动性、成交量、买卖情况
- 做基础安全检查，例如 RugCheck 或 GoPlus
- 让 AI 返回候选列表，而不是直接交易

## 可用工具

### `scan_onchain_narratives`

扫描链上代币并返回结构化结果。

常用参数：

- `chains`: 链名，用英文逗号分隔，例如 `eth,bsc,base,sol`
- `limit_per_chain`: 每条链每个 GMGN 端点最多拉取多少条
- `include_safety`: 是否检查安全风险
- `strict_safety`: 是否过滤掉无法检查或不安全的代币
- `include_profiles`: 是否从 DexScreener 补充社交链接
- `max_results`: 最多返回多少个候选

建议默认调用：

```text
scan_onchain_narratives(chains="eth,bsc,base,sol", include_safety=true, strict_safety=false, max_results=20)
```

### `classify_token_narrative`

只根据代币名称、符号、链来判断叙事分类。

## 工作方式

这个技能只做扫描和分析：

- 不买卖
- 不连接钱包
- 不保存私钥
- 不提交交易
- 不默认发送 Telegram 消息

如果用户要求交易、买入、卖出、下单，不能用这个技能执行交易，只能把扫描结果作为研究参考。

## 输出建议

回答用户时优先说明：

- 候选币名称、链、地址
- 叙事分类和星级
- 市值、流动性、1h/24h 涨幅
- 安全检查是否成功，以及是否发现硬风险
- 为什么排在前面

不要把扫描结果表达成确定收益或投资建议。

