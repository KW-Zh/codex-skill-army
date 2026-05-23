# 快速开始

## 1. 安装 skill

```powershell
py -3 "$env:USERPROFILE\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" --repo KW-Zh/codex-skill-army --ref main --method download
```

重启 Codex 后使用：

```text
调用 $codex-skill-army：帮我规划一个科研写作任务，并选择需要的 skills。
```

## 2. 可选安装史官

史官推荐 `agentmemory`，但它是可选增强。安装前应自行审计来源和许可证，不安装史官也能使用本 skill 的调度协议。

```powershell
npm install -g @agentmemory/agentmemory
agentmemory init
agentmemory
```

建议保持自动压缩、自动上下文注入和自动反思关闭，避免隐私和 token 成本失控。

保守配置建议见 `docs/privacy-and-historian.md`。

## 3. 本地开发

```powershell
.\scripts\install-local.ps1 -WhatIf
py -3 .\scripts\check_structure.py .
py -3 .\scripts\privacy_scan.py .
py -3 .\scripts\content_audit.py .
py -3 .\scripts\source_audit.py .
py -3 .\scripts\run_pressure_tests.py .
py -3 .\scripts\quick_validate_ci.py .
```
