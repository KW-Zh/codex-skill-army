# 贡献指南

欢迎围绕科研工作流改进本 skill。优先贡献以下内容：

- 更真实的科研压力测试场景。
- 更清晰的军制角色边界。
- 对常见科研工具链的安全、隐私和安装说明。
- 能减少 token 消耗或误触发的调度规则。

## 基本要求

1. 不提交个人隐私、凭据、真实聊天记录或未授权论文全文。
2. 新增协议必须能被压力测试覆盖。
3. 新增脚本默认只读；写入、删除、覆盖必须显式说明。
4. 中文说明优先，必要时补充英文摘要。
5. 不复制第三方 skill 的正文、脚本、示例、表格或独特表达；只允许抽象化总结能力类别、触发场景和风险边界。

## 可以贡献什么

- 新增科研 workflow：先说明触发场景、主将/副将、监军验收，再补压力测试。
- 新增 example：提供完整用户 prompt、预期调度令、禁止事项和验收清单。
- 新增 pressure case：覆盖一个真实失败模式，例如隐私保存、过度军制、缺兵乱装、Word 排版遗漏。
- 新增工具说明：只写调度视角和安全边界，不重新分发外部工具源码。

## Pull Request 清单

- [ ] 改动面向普通用户或贡献者，不包含维护者临时话术。
- [ ] 已更新相关压力测试。
- [ ] 已运行结构、隐私、内容、防侵权和 quick validate 检查。
- [ ] 新增第三方名称时已更新 `THIRD_PARTY_NOTICES.md`。
- [ ] 没有复制第三方 skill 的大段文本或脚本。

## 提交前检查

```powershell
py -3 .\scripts\check_structure.py .
py -3 .\scripts\privacy_scan.py .
py -3 .\scripts\content_audit.py .
py -3 .\scripts\source_audit.py .
py -3 .\scripts\run_pressure_tests.py .
py -3 .\scripts\quick_validate_ci.py .
py -3 -X utf8 "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .
```
