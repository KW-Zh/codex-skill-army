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

## 提交前检查

```powershell
py -3 .\scripts\check_structure.py .
py -3 .\scripts\privacy_scan.py .
py -3 .\scripts\run_pressure_tests.py .
py -3 -X utf8 "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .
```
