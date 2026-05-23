# 监军验收协议

## Skill 本体验收

必须通过：

```powershell
py -3 .\scripts\check_structure.py .
py -3 .\scripts\privacy_scan.py .
py -3 .\scripts\run_pressure_tests.py .
py -3 -X utf8 "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .
```

## 科研交付验收

- 引用是否能追溯到来源。
- 事实是否经过核验或明确标注不确定性。
- 图表、公式、编号、单位是否一致。
- Word/PDF 是否渲染正常。
- 是否保留用户指定排版规则。

## 代码交付验收

- 运行与改动相称的测试。
- 大型代码库先确认架构证据。
- 不用“看起来正确”代替命令输出。
- 说明未能运行的验证和原因。

## 开源发布验收

- README 读者能在 5 分钟内理解价值。
- 安装步骤可以复现。
- 许可证和第三方来源清楚。
- 无本机绝对路径、私密文件名、凭据。
- 示例覆盖主要目标用户。
