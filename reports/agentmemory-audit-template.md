# agentmemory 史官审计模板

本模板用于维护者或用户在自己的机器上审计 `agentmemory`。不要把本地安装记录、记忆数据库、`.env` 或个人路径提交到公开仓库。

## 基本信息

- 审计日期：
- 审计人：
- agentmemory 版本：
- iii-engine 版本：
- 安装方式：
- 许可证：

## 来源核验

- GitHub 仓库：
- npm 包：
- MCP shim：
- release 或 commit：

## 保守配置

```env
AGENTMEMORY_AUTO_COMPRESS=false
AGENTMEMORY_INJECT_CONTEXT=false
AGENTMEMORY_REFLECT=false
AGENTMEMORY_TOOLS=core
```

## 健康检查

```powershell
agentmemory status
agentmemory doctor --dry-run
```

记录：

- 服务是否 reachable：
- Provider：
- Embeddings：
- 自动压缩是否关闭：
- 自动上下文注入是否关闭：

## 风险判断

- 是否会默认保存隐私：
- 是否会默认注入上下文：
- 是否依赖外部 LLM provider：
- 是否需要凭据：
- 是否提供删除或导出机制：

## 结论

- [ ] 可作为可选史官使用。
- [ ] 暂不建议启用。
- [ ] 需要进一步审计。
