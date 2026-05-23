# Abaqus/FEA 工作流

## 触发

用户要求 Abaqus 脚本建模、材料、边界条件、载荷、网格、接触、静力/动力/热分析、ODB 结果提取或优化。

## 点将

- 主将：最匹配的 Abaqus 专用 skill。
- 副将：材料、几何、网格、载荷、边界条件、ODB、可视化。
- 监军：检查单位、约束、网格收敛、接触定义和结果解释。

## 最小流程

1. 明确分析目标：应力、位移、频率、热场、疲劳或优化。
2. 明确单位制，不混用。
3. 确认材料模型：线弹性、塑性、超弹性、损伤、热属性等。
4. 确认单元类型：实体、壳、梁、热单元、减缩积分和 hourglass 风险。
5. 先建最小可运行模型，再扩展接触、非线性和复杂边界。
6. 设置载荷步：静力、动力、频率、热分析，说明增量、稳定化和非线性开关。
7. 网格收敛：至少给出网格尺寸、关键响应量和收敛判断。
8. 输出脚本时说明 Abaqus/abqpy 版本假设。
9. 结果提取要包括字段、位置和单位。

## 最小脚本骨架

```python
from abaqus import mdb
from abaqusConstants import *

model = mdb.Model(name="research_model")
# 1. geometry
# 2. material and section
# 3. assembly
# 4. step
# 5. boundary conditions and loads
# 6. mesh
# 7. output requests
# 8. job submit
```

## ODB 提取模板

```python
from odbAccess import openOdb

odb = openOdb("Job-1.odb")
step = odb.steps["Step-1"]
frame = step.frames[-1]
stress = frame.fieldOutputs["S"]
disp = frame.fieldOutputs["U"]
# 提取位置、单位和统计方式必须随结果一起说明。
odb.close()
```

## 验收

- 脚本语法和 API 名称尽量可核验。
- Job、Step、BC、Load、Mesh、Output 均有合理设置。
- 材料、单元、接触、网格和载荷步假设明确。
- 遇到收敛失败时，优先检查边界约束、接触、材料非线性、网格质量和增量设置。
- 不把有限元结果当作无需工程判断的最终结论。
