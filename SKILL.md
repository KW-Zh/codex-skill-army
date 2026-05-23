---
name: codex-skill-army
description: Use when the user asks for skill orchestration, 技之军团, 技之将, choosing or combining Codex skills, research workflows, task decomposition, subagent coordination, missing skill recruitment, skill audits, or long-running scientific projects.
license: MIT
metadata:
  short-description: 科研向 Codex 技能军团总控
---

# codex-skill-army：技之军团

## 核心定位

`codex-skill-army` 是一个单体总控 skill。它不替代领域 skill，而是用“军制”把用户本地已有和未来新增的 skills 组织起来：先轻量预检，再按任务需要点将、分兵、合围、验收。

目标用户偏科研方向：研究生、科研人员、论文写作者、科研代码维护者、仿真建模用户。简单问题直接回答，不因为本 skill 存在就制造流程。

## 轻量预检

每轮先判断：

1. 用户是否点名 skill、工具、插件、子代理或“技之军团”。
2. 任务是否属于已安装专用 skill 的明确领域。
3. 是否需要科研检索、论文写作、Word 排版、公式、引用、代码图谱、Abaqus/仿真、计划拆解或多阶段验收。
4. 是否涉及删除、批量整理、非项目目录、隐私外发、凭据、账号写入或联网安装。

低风险小任务直接完成。复杂、跨领域或长期任务才进入完整军制。

## 调度令

进入完整军制时，先形成简短调度令：

```text
主线：本轮真正要交付什么。
军师：是否需要澄清、计划、取舍或任务拆解。
斥候：是否需要查本地 skills、联网找高分 skill、审计来源。
主将：承担交付物核心规则的领域 skill。
副将：0 到 4 个辅助 skills，负责检索、格式、图表、验证、部署等补位。
分兵：是否派子代理；每个子代理的边界和禁止事项。
监军：验证命令、质量门槛、隐私和发布风险。
史官：是否需要读取或写入长期科研记忆。
缺兵：本地无合适 skill 时，是否出征召令。
```

## 军制角色

- 总帅：本 skill，负责统一调度、点将、分兵、合围、验收。
- 军师：目标澄清、任务拆解、路线选择和取舍判断。
- 斥候：本地盘点、外部搜索、来源审计、技能评分、征召令。
- 主将：最匹配的领域 skill，负责核心交付物。
- 副将：辅助领域 skill，负责格式、检索、图表、测试、部署等。
- 监军：质量、安全、隐私、引用、测试和开源发布检查。
- 军需官：维护能力地图，发现重复、失效、悬空引用和缺口。
- 史官：长期记忆系统，推荐 `agentmemory`；默认只保存用户确认的长期科研偏好和项目决策。
- 工部：CodeGraph、MCP、CLI、安装器、自动化脚本等基础设施。

需要角色边界时读取 `references/roles/role-taxonomy.md`。

## 科研优先规则

科研任务必须重视证据链：

- 文献综述、论文写作、审稿回复：优先选择论文检索、阅读、引用、写作和 Word/PDF 类 skills。
- Word 学术文档：必须尊重用户给定排版规范；公式、编号、交叉引用交给对应 Office/Docx skill。
- 科研代码：先判断是否需要 CodeGraph；大型结构问题优先代码图谱，再读文件。
- 仿真建模：Abaqus/FEA 任务先选专用 Abaqus skill，再由监军检查建模假设、边界条件和结果提取。
- 引用和事实：能核验就核验；不能核验时明确标注不确定性。

科研流程模板见 `references/workflows/`。

## 缺兵征召

本地没有合适主将或副将时，不要泛化硬做。读取 `references/protocols/recruitment-protocol.md`，输出征召令：

- 缺口说明。
- 已有 skills 为什么不足。
- 候选来源、路径、评分、风险。
- 安装或创建建议。
- 校验方式。

默认只提方案；用户明确要求自动安装时，仍要排除隐私外发、凭据、批量整理和高风险候选。

## 史官记忆

史官用于长期科研连续性，不用于无边界记录隐私。

默认只建议保存：

- 研究方向、项目目标、长期偏好。
- 论文格式、引用风格、Word 排版要求。
- 已确认的方法选择、失败经验、实验约束。
- 用户明确希望复用的写作和工作流偏好。

不要默认保存原始论文全文、聊天隐私、凭据、客户资料、财务数据或未脱敏个人信息。具体规则见 `references/protocols/historian-protocol.md`。

## 子代理

只有任务能拆成独立子任务、结果可由主代理复核时才分兵。主代理始终保留最终集成、冲突检查和验收责任。分兵规则见 `references/protocols/subagent-protocol.md`。

## 验收

完成前必须做与任务相称的验证：

- Skill 本体：运行 `scripts/check_structure.py`、`scripts/privacy_scan.py`、`scripts/run_pressure_tests.py`，并用 Codex 的 `quick_validate.py` 校验。
- 科研交付：检查引用、事实、格式、图表、公式、Word/PDF 渲染。
- 代码交付：运行测试、构建、静态检查或最小复现场景。
- 开源发布：检查许可证、README、安装说明、路径泄露和第三方来源。

验收协议见 `references/protocols/validation-protocol.md`。
