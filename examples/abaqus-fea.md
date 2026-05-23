# 示例：Abaqus/FEA

## 用户提示

```text
调用 $codex-skill-army：帮我用 Abaqus Python 建一个钢梁三点弯曲模型，输出脚本，并提取最大 Mises 应力和跨中位移。
```

## 预期调度

- 主将：Abaqus 静力分析或几何/材料/网格/ODB 专用 skill。
- 副将：材料、边界条件、载荷、网格、结果提取。
- 监军：检查单位、材料模型、单元类型、载荷步、网格收敛和 ODB 字段。

## 输入清单

- 几何尺寸和单位。
- 钢材参数。
- 支座和加载方式。
- 网格尺寸和单元类型。
- 输出字段和结果位置。

## 验收重点

- 脚本包含 Model、Part、Material、Section、Assembly、Step、BC、Load、Mesh、Job。
- 结果提取说明字段 `S`、`U`、位置和单位。
- 不把一次网格结果当最终工程结论。
