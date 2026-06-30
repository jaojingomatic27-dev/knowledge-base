# -*- coding: utf-8 -*-
"""Generate cheatsheets using HTML -> screenshot approach (no-Pillow, just HTML)"""

import os
import subprocess

OUT = r"C:\AI\cc\pvinverter\output"

def write_html(path, html):
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

# ── Cheatsheet 1: Solution Engineer ──
html1 = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { width: 1080px; font-family: "Microsoft YaHei", "SimHei", sans-serif; background: #fff; padding: 80px 60px 60px 60px; }
  h1 { text-align: center; font-size: 48px; color: #1a1a1a; margin-bottom: 8px; }
  .sub { text-align: center; font-size: 26px; color: #999; margin-bottom: 40px; }
  hr { border: none; border-top: 2px solid #e0e0e0; margin-bottom: 36px; }
  .section-title { font-size: 32px; color: #e74c3c; font-weight: 700; margin: 36px 0 16px 0; }
  .item { font-size: 26px; color: #333; margin: 10px 0 10px 24px; line-height: 1.5; }
  .item b { color: #1a1a1a; }
  .footer { margin-top: 40px; font-size: 26px; color: #e74c3c; font-weight: 700; text-align: center; }
  .tags { text-align: center; font-size: 22px; color: #ccc; margin-top: 30px; }
</style>
</head>
<body>
<h1>PCS 技术方案 / 售前工程师</h1>
<p class="sub">核心职责 · 所需能力 · 为什么必须在德国</p>
<hr>

<div class="section-title">核心职责 (70%)</div>
<div class="item"><b>投标技术方案</b> — 读德语招标书 → PCS配置 / 单线图</div>
<div class="item"><b>并网兼容性分析</b> — VDE 4105 / 4110 / 4120 / EN 50549</div>
<div class="item"><b>系统方案设计</b> — PCS + 变压器 + BESS + EMS/SCADA</div>
<div class="item"><b>FAT / SAT 技术支持</b> — 工厂 + 现场验收技术代表</div>

<div class="section-title">延伸职责 (30%)</div>
<div class="item"><b>竞品技术对标</b> → 向中国研发反馈市场技术需求</div>
<div class="item"><b>新品本地化验证</b> → 德国电网仿真 / 现场试点</div>
<div class="item"><b>培训销售团队</b> → 储能PCS 101 技术培训</div>

<div class="section-title">硬技能（必须）</div>
<div class="item"><b>电力电子拓扑</b> / 单线图 / 变压器选型</div>
<div class="item"><b>VDE 4105/4110/4120</b> + EN 50549 并网标准</div>
<div class="item"><b>BESS系统集成：</b>电池 ↔ PCS ↔ EMS 链路</div>
<div class="item"><b>Modbus / IEC 61850</b> / CANbus 通信协议</div>
<div class="item"><b>德语技术文档读写 C1+</b> 英语商务 B2+</div>

<div class="section-title">软技能（同样必须）</div>
<div class="item"><b>跨文化沟通</b> — 中国研发 ↔ 德国客户</div>
<div class="item"><b>客户服务</b> — 快速响应 + 技术有据</div>
<div class="item"><b>压力承受</b> — 投标截止前48小时的冷静</div>
<div class="item"><b>结构化表达</b> — 逻辑 + 数据 + 图示</div>

<div class="section-title">为什么必须在德国 (5个理由)</div>
<div class="item"><b>1. 时差</b> — 30分钟响应 vs 6小时延迟</div>
<div class="item"><b>2. 法域</b> — § StromNEV/EEG 不是语言，是Jurisdiction</div>
<div class="item"><b>3. 现场</b> — 并网评估/技术答辩/FAT不可能是Zoom</div>
<div class="item"><b>4. 跨文化中介</b> — 两国技术逻辑的唯一翻译器</div>
<div class="item"><b>5. 信任</b> — 电网是国安级，必须见过人握过手</div>

<div class="footer">底线：与客户直接沟通的技术角色，必须在德国本地</div>
<div class="tags">#储能出海 #技术方案 #售前工程师 #德国招聘</div>
</body>
</html>
"""

# ── Cheatsheet 2: Sales vs Presales ──
html2 = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { width: 1080px; font-family: "Microsoft YaHei", "SimHei", sans-serif; background: #fff; padding: 80px 60px 60px 60px; color: #1a1a1a; }
  h1 { text-align: center; font-size: 46px; margin-bottom: 6px; }
  .sub { text-align: center; font-size: 26px; color: #999; margin-bottom: 36px; }
  hr { border: none; border-top: 2px solid #e0e0e0; margin-bottom: 30px; }
  .sec { font-size: 30px; color: #e74c3c; font-weight: 700; margin: 30px 0 14px 0; }
  p { font-size: 24px; color: #333; margin: 8px 0 8px 20px; line-height: 1.5; }
  table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 22px; }
  th { background: #f5f5f5; color: #999; padding: 10px 12px; text-align: left; font-weight: 600; }
  td { padding: 9px 12px; border-bottom: 1px solid #f0f0f0; color: #333; }
  .reason { font-size: 24px; color: #333; font-weight: 600; margin: 8px 0 8px 20px; }
  .warn { text-align: center; font-size: 28px; color: #e74c3c; font-weight: 700; margin: 30px 0 8px 0; }
  .warn2 { text-align: center; font-size: 24px; color: #1a1a1a; font-weight: 600; margin-bottom: 4px; }
  .warn3 { text-align: center; font-size: 22px; color: #999; }
  .footer { text-align: center; font-size: 18px; color: #ccc; margin-top: 20px; }
</style>
</head>
<body>
<h1>销售 vs 售前 vs 方案工程师</h1>
<p class="sub">同一链条 · 不同角色 · 不能合并</p>
<hr>

<div class="sec">一、称呼澄清</div>
<p>方案工程师 = 售前工程师 = Solution Engineer</p>
<p>储能PCS行业最准确的叫法：<b>Solution Engineer</b></p>
<p>卖的不是单一设备，是 PCS+变压器+并网+通信 的系统级方案</p>

<div class="sec">二、8个维度的核心差异</div>
<table>
<tr><th>维度</th><th>销售 Sales</th><th>售前 / 方案 Pre-Sales</th></tr>
<tr><td>核心KPI</td><td>签了多少MW / 多少钱</td><td>技术标得分 / 技术澄清完成数</td></tr>
<tr><td>工作产出</td><td>合同（签字经过谈判）</td><td>技术标书 / 单线图 / 配置表 / 合规报告</td></tr>
<tr><td>沟通对象</td><td>采购总监 / VP / 财务</td><td>电网工程师 / 系统集成 / 电气设计</td></tr>
<tr><td>语言</td><td>商业：ROI IRR TCO 付款 违约金</td><td>技术：kW kVAr ms % IEC 61850 Modbus</td></tr>
<tr><td>性格</td><td>外向 关系驱动 抗拒绝 谈判型</td><td>内向中向 逻辑驱动 细节强迫 分析型</td></tr>
<tr><td>知识结构</td><td>三成技术 七成商务 满级人脉</td><td>七成技术 三成商务 足够沟通</td></tr>
<tr><td>出差</td><td>展会 客户拜访 签约仪式</td><td>技术澄清会 FAT SAT 电网对接</td></tr>
<tr><td>收入</td><td>底薪+提成 高风险高回报</td><td>底薪+项目奖金 低风险稳定</td></tr>
</table>

<div class="sec">三、为什么不能合并成一个人？</div>
<div class="reason">1. 写技术标书是全职工种 — 200页德语标书需2-3周逐条回复</div>
<div class="reason">2. 能力的天然矛盾 — 人际关系 vs 逻辑深度，两个极端</div>
<div class="reason">3. 客户有两个接口 — 采购部门(销售) + 工程部门(方案)</div>
<div class="reason">4. 签字责任不同 — 技术参数承诺 vs 商务条款承诺</div>

<div class="warn">中国公司常见误区：招一个有技术背景的销售就行</div>
<div class="warn2">在德语区储能行业 这不成立 — 技术严谨度全球最高</div>
<div class="warn3">RWE会要求你用MATLAB做并网仿真 + 附FGH独立测试报告</div>

<div class="footer">文件: data/sales_vs_presales_vs_solution_engineer.md &nbsp;|&nbsp; #储能出海 #售前 #销售 #方案工程师 #德国招聘</div>
</body>
</html>
"""

write_html(os.path.join(OUT, "_cheatsheet1.html"), html1)
write_html(os.path.join(OUT, "_cheatsheet2.html"), html2)
print("HTML files written. Open in browser and screenshot via browser devtools (Ctrl+Shift+S) or Print -> Save as PDF -> convert.")
print("Since no headless Chrome is available, opening them in the default browser now.")
