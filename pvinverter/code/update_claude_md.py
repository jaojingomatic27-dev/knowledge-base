# -*- coding: utf-8 -*-
with open(r"C:\AI\cc\CLAUDE.md", "r", encoding="utf-8") as f:
    old = f.read()

new_rules = """
11. **中文信息图首选 HTML+Playwright 截图**：需要生成含大量中文文字的图片（如小红书封面、知识卡片、速查图）时，首选方案：① Write 工具写 HTML 文件（`<meta charset="UTF-8">`）→ ② 用 `playwright` 库截图转 PNG（`device_scale_factor=2` 保证清晰度）。Pillow 仅用于无中文或极少量中文的纯色块图片。原因：HTML 的中文渲染不受 Python 编码问题影响，且 CSS 排版灵活度远超 Pillow。
12. **中文文本写入**：含中文的文本文件（markdown、日志等）**禁止**用 PowerShell 的 `Set-Content`/`Out-File` 写入（UTF-8 编码在管道传递中会损坏）。必须用 Python `open(path, "w", encoding="utf-8")` 写入。原因：PowerShell 5.1 对管道中含中文变量的编码处理有 bug，输出文件会产生乱码。
"""

with open(r"C:\AI\cc\CLAUDE.md", "w", encoding="utf-8") as f:
    f.write(old.rstrip() + new_rules)
print("CLAUDE.md updated OK")
