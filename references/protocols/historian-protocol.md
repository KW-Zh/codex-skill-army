# 史官记忆协议

史官负责长期经验沉淀，推荐使用 `agentmemory`。本项目不强制依赖它；没有史官时，任务仍可完成。

## 推荐保存

- 研究方向、项目目标、长期偏好。
- 用户确认过的论文写作风格、引用风格、Word 排版规范。
- 项目中反复出现的方法选择、实验约束、失败经验。
- 常用工具链、环境限制、已安装关键 skills。
- 用户明确要求“以后记住”的结论。

## 不默认保存

- 原始论文全文、未授权数据集、审稿机密。
- 凭据、API key、账号、Cookie。
- 邮件、聊天记录、会议纪要中的个人隐私。
- 身份证、电话、住址、财务和医疗信息。
- 未脱敏的客户或合作方资料。

## token 控制

推荐保守配置：

```env
AGENTMEMORY_AUTO_COMPRESS=false
AGENTMEMORY_INJECT_CONTEXT=false
AGENTMEMORY_REFLECT=false
AGENTMEMORY_TOOLS=core
```

只有当用户明确需要自动回忆上下文，且理解 token 成本时，才考虑开启自动注入。

## 读写规则

- 写入前先判断是否具有长期价值。
- 对敏感内容先脱敏或摘要。
- 只在长期项目、重复任务、科研偏好稳定时写入。
- 读取记忆后要说明它只是历史上下文，不替代当前证据。

## 确认话术

写入前使用类似提示：

```text
这条信息适合长期复用。我建议史官仅保存脱敏摘要：“……”。是否写入长期记忆？
```

读取后使用类似提示：

```text
我参考了史官中的历史偏好：“……”。这只是历史上下文，当前任务仍以你本轮提供的材料为准。
```

拒绝敏感写入：

```text
这包含凭据、隐私或未授权材料，我不会写入长期记忆。可以改为保存脱敏规则或非敏感偏好。
```

## agentmemory 命令模板

不同版本的工具命令可能变化，执行前先用 `agentmemory --help` 或 MCP 工具列表确认。

```powershell
agentmemory status
agentmemory doctor --dry-run
agentmemory mcp
agentmemory remove --keep-data
```

通过 MCP 使用时，优先选择语义清晰的 core 工具，例如 search/save/session/governance delete；不要直接操作数据库文件。

## 失效和删除

用户要求删除记忆时，优先使用史官系统提供的治理/删除命令；不要手动删除未知数据库文件，除非用户明确批准并确认路径。
