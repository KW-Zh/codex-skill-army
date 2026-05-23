# 隐私与史官策略

史官用于长期科研连续性，但记忆系统本身具有隐私风险。本项目建议把 `agentmemory` 作为可选增强，而非硬依赖。

## 推荐配置

```env
AGENTMEMORY_AUTO_COMPRESS=false
AGENTMEMORY_INJECT_CONTEXT=false
AGENTMEMORY_REFLECT=false
AGENTMEMORY_TOOLS=core
```

这样可以避免默认 LLM 压缩、默认上下文注入和过宽工具面。

## 推荐记录

- 研究方向和长期目标。
- 用户确认的格式规范。
- 方法取舍和失败经验。
- 已安装关键工具和技能偏好。

## 不应默认记录

- 凭据、API key、Cookie。
- 邮件、聊天、会议中的隐私。
- 未授权论文全文或审稿材料。
- 身份信息、财务、医疗或客户资料。

## 发布提醒

公开仓库不得包含 `.agentmemory/`、`.env`、本机路径、真实研究隐私或记忆数据库。
