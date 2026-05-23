# Pull Request

## Summary

请说明本次改动解决什么问题。

## Checklist

- [ ] 面向用户或贡献者，不包含维护者临时话术。
- [ ] 不包含本机路径、个人邮箱、凭据、聊天记录、审稿材料或未授权论文全文。
- [ ] 没有复制第三方 skill 的正文、脚本、示例或独特表格。
- [ ] 已更新相关压力测试或说明无需更新的原因。
- [ ] 已运行本地验证：

```powershell
py -3 .\scripts\check_structure.py .
py -3 .\scripts\privacy_scan.py .
py -3 .\scripts\content_audit.py .
py -3 .\scripts\source_audit.py .
py -3 .\scripts\run_pressure_tests.py .
py -3 .\scripts\quick_validate_ci.py .
```
