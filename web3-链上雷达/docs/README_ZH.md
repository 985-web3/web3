<p align="center">
  <b>web3-链上雷达</b><br>
  链上叙事雷达 · MCP 服务 · 安全信号 · 动量排序
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="./README_ZH.md">中文</a>
</p>

---

`web3-链上雷达` 是一个 Web3 链上扫描 MCP 服务。它来自原始的单文件雷达脚本，但已经被拆成可安装的模块、客户端和 MCP 工具，便于 AI 调用、维护和继续扩展。

这个项目负责：

- 扫描 GMGN 排行里的新币和活跃币
- 识别叙事分类，例如马斯克/川普、币安/CZ、名人热点、普通新叙事
- 检查基础安全信号，例如 RugCheck 和 GoPlus
- 返回结构化候选列表给 AI

这个项目不会：

- 自动买卖
- 连接钱包
- 保存私钥
- 提交交易

## 可用工具

### `scan_onchain_narratives`

扫描链上代币并返回结构化结果。

常用参数：

- `chains`：链名，默认 `eth,bsc,base,sol`
- `limit_per_chain`：每条链每个 GMGN 端点最多抓多少条
- `include_safety`：是否检查基础安全风险
- `strict_safety`：是否直接过滤不安全或检查失败的代币
- `include_profiles`：是否补充 DexScreener 社交链接
- `max_results`：最多返回多少条候选

### `classify_token_narrative`

只根据代币名称、符号、链来判断叙事分类。

## 项目结构

```text
web3-链上雷达/
  pyproject.toml
  .env.example
  docs/
    README_ZH.md
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

## 安装

```bash
cd web3-链上雷达
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 启动 MCP

```bash
web3-chain-radar-mcp
```

示例 MCP 配置：

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

## 环境变量

如果你想保留本地默认配置，可以把 `.env.example` 复制为 `.env`：

```bash
cp .env.example .env
```

当前版本不需要钱包私钥，也不需要交易权限。`TG_BOT_TOKEN` 和 `TG_CHAT_ID` 只是为后续可选的 Telegram 推送预留。

## 说明

- 安全接口可能限流或暂时不可用，使用时要检查 `safety.checked`
- 严格动量判断依赖同一个 MCP 进程内的连续多次调用
- 这是研究工具，不构成投资建议
