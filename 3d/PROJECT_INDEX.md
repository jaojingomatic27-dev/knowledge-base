# 3D — 项目索引

生成各种 3D 模型文件（STL 等格式）。

## 目录结构

| 目录 | 说明 |
|------|------|
| `code/` | 生成脚本 |
| `data/` | 输出 STL 文件 |
| `image/` | 渲染预览图 |

## 文件清单

| 文件 | 说明 |
|------|------|
| `code/generate_half_pipe.py` | 半圆管 STL 生成器 |
| `code/generate_half_pipe_slotted.py` | 带扎带槽半圆管 STL 生成器 |
| `data/half_pipe.stl` | 半圆管 STL（OD=40mm, ID=35mm, L=50mm） |
| `data/half_pipe_slotted.stl` | 带扎带槽半圆管 STL（ID=15mm, wall=6mm, L=60mm） |
| `input/hook.stl` | 原始壁挂钩子模型（180×80×63mm） |
| `data/hook_with_box.stl` | 钩子+挂载盒子组合（200×100×30mm 盒子，底部开槽卡在钩子顶部） |
| `code/analyze_hook.py` | hook.stl 结构分析脚本 |
| `code/analyze_hook2.py` | hook.stl 详细几何截面分析脚本 |
| `code/generate_hook_box.py` | 钩子+盒子组合 STL 生成器 |
| `code/verify_hook_box.py` | hook_with_box.stl 验证脚本 |
