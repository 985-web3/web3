<p align="center">
  <b>web3-链上雷达</b><br>
  给 AI 用的链上叙事雷达
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="./README_ZH.md">中文</a>
</p>

---

`web3-链上雷达` 是一个 Web3 链上扫描 MCP 服务。

它会扫描代币排行、识别叙事、检查基础安全信号，并把候选结果返回给 AI。

## 快速安装

```bash
cd web3-链上雷达
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 启动

```bash
web3-chain-radar-mcp
```

## MCP 配置

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

## 可用工具

### `scan_onchain_narratives`

扫描 GMGN 排行代币，返回叙事、动量、流动性、成交量和基础安全信号。

常用参数：

- `chains`：默认 `eth,bsc,base,sol`
- `include_safety`：是否检查安全
- `strict_safety`：是否过滤不安全代币
- `include_profiles`：是否补充社交链接
- `max_results`：最多返回多少条

### `classify_token_narrative`

只根据名称、符号和链判断叙事分类。

## 说明

- 不需要私钥
- 不连接钱包
- 不执行交易
- 安全接口可能限流
- 严格动量判断依赖同一个 MCP 进程内的连续多次调用
