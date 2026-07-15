# pvinverter 项目日志

## 20260604-22

- **新增**: `data/EU_policy_knowledge_base_2026.md` — 欧洲针对中国大储/光储企业政策知识库
  - 覆盖2024-2026年欧盟七重政策壁垒：NZIA、IAA、电池法规、FSR、CBAM、CRMA、光伏关税、PCS限制
  - 来源：WebSearch × 11轮全网搜索，涵盖官方法规、行业分析、法律评论
  - 约2000行，含13个章节，关键时间线汇总至2030+
- **新增**: `PROJECT_INDEX.md`, `PROJECT_LOG.md` — 项目初始化

## 20260604-23

- **新增**: `data/EU_policy_portal.html` — 交互式政策知识库网页
  - 功能：侧边栏索引导航 / 全文关键字搜索（Ctrl+K） / 滚动高亮当前位置 / 时间线可视化
  - 设计：深色主题 / 七色政策标签系统 / 响应式（桌面+移动端）/ 打印友好
  - 内容：13个章节完整呈现，含政策卡片网格、风险等级标注、量化影响数据
  - 纯静态 HTML，无需服务器，浏览器直接打开即可使用

## 20260606-01

- **新增**: `data/xiaohongshu_style_analysis.md` — 小红书专业账户风格分析文档
  - Top 5 类账户拆解：海外储能老番薯（一线实战）、商业小纸条（情绪钩子）、Freddy商业笔记（结构化知识）、出海老船长（避坑清单）、36氪（资讯快报）
  - 爆款内容公式：5类高转化标题公式、CES算法权重、封面黄金法则、"三段式"正文结构
  - 风格适配度评估：结构化知识向 > 情绪钩子向 > 避坑清单向 > 实战向 > 快报向
  - 推荐组合：情绪钩子标题 + 结构化正文 + 避坑清单收尾
- **新增**: `data/xiaohongshu_notes.md` — 欧盟政策知识库小红书笔记（10页）
  - 基于 EU_policy_knowledge_base_2026.md 改编
  - 每页含封面设计、正文文案、互动设计
  - 5个标题建议（按点击率排序），首推"欧盟对中国储能动手了，比关税狠100倍"
  - 附发布策略：每天2篇/早晚各1篇/5天发完

## 20260607-01

- **新增**: `data/sinexcel_research.md` — Sinexcel（盛弘股份 300693）公司调研
  - 覆盖五大业务板块、财务数据（2024年营收30.36亿）、PCS产品矩阵
  - 欧洲布局：德国总部+VDE认证+拉脱维亚/乌克兰/捷克项目
  - 创始人方兴背景：宝洁→捷普→中欧EMBA→35岁创业
  - PCS技术深度：模块化/多簇管理/VSG构网/98.5%效率/全球认证矩阵
- **新增**: `terminal/output.md` — 长输出落盘，记录Sinexcel调研和Pillow卡片生成

## 20260616-01

- **新增**: `data/sinexcel_germany_jd_analysis.md` — 盛弘德国子公司招聘 JD 深度分析
  - 职位: 德语区储能销售经理 DACH / Düsseldorf
  - 逐条拆解 11 项任职要求，导出"50%商务 + 30%技术 + 20%人脉"复合型人才画像
  - 全网评价搜索: Kununu/Glassdoor/Google Maps/Indeed 均无评价条目（公司太新规模太小）
  - 正面: Brandon Hall 奖项 / VDE认证 / 菲尼克斯战略合作 / 拉脱维亚项目落地
  - 发现: JD要求极其全面，说明德国子公司在0→1攻坚阶段

## 20260616-02

- **新增**: `data/dach_energy_industry_players.md` — 德语区储能行业玩家全解
  - EPC: BELECTRIC / maxsolar / Greentech 等 6 家
  - 系统集成商: Siemens / Fluence / Nidec / Tesvolt 等 6 家
  - 开发商: ABO Wind / JUWI / BayWa r.e. 等 7 家
  - Utility: E.ON / RWE / EnBW / Vattenfall / Stadtwerke 等 9 家
  - IPP: Aquila Capital / Encavis / KGAL / SUSI Partners 等 10 家
  - C-level 人脉解读：Utility VP / IPP Investment Director / EPC CTO / 开发商 CEO

## 20260616-03

- **新增**: `data/pcs_export_certification_guide.md` — 中国储能PCS逆变器出口德国认证全指南
  - 必须认证: CE(LVD+EMC+RoHS+REACH) + VDE 4105/4110/4120 + EN 50549-1/-2/-10
  - 推荐认证: IEC 62619 / VDE 2510-50 / ErP / 功能安全 / C5防腐
  - 全部实验室认证可在中国完成（TÜV南德广州/莱茵中国有DAkkS资质）
  - 必须在德国的只有: ZEREZ在线注册 + 电网运营商现场验收（项目环节）
  - 认证路径: 6-8个月 / ¥40-90万 / 0次出差德国
  - 原理: DAkkS认可=德国法律效力，中国实验室出具的DAkkS证书与德国本土等效

## 20260616-04

- **新增**: `data/germany_subsidiary_500mw_plan.md` — 500MW目标：在德国建分支机构的必要性分析与方案
  - 核心判断: 必须建——500MW级买家不会把框架协议签给没有德国实体的公司
  - 核心团队: 销售BD(2-3)+技术方案(2-3)+项目交付(3-5)+法务合规(1-2) = 8-13人
  - 三阶段路线: M1-6最小可行→M6-12交付能力→Y2+规模化
  - 第一年费用: €600,000-900,000，占目标收入(€40M)的1.5-2.3%
  - 同行对标: 盛弘/阳光电源/海博思创/比亚迪/华为均已有德国实体

## 20260630-01

- **新增**: `data/solution_engineer_role_deep_dive.md` — PCS技术方案/售前工程师岗位详解
  - 职责范围: 投标技术方案、并网兼容性分析、系统方案设计、FAT/SAT技术支持、竞品分析
  - 硬技能: 电力电子拓扑、VDE/EN并网标准、储能系统集成、Modbus/IEC 61850、德语技术文档
  - 软技能: 跨文化沟通、客户服务意识、压力承受、结构化表达
  - 必须在德国的5个理由: 时差、德语法域、现场存在、跨文化中介、客户信任
  - 附完整英文JD草稿 + 过渡期方案（12-18个月渐进本地化）

## 20260630-02

- **新增**: `data/sales_vs_presales_vs_solution_engineer.md` — 销售 vs 售前 vs 方案工程师：区别与协作
  - 称呼澄清: 方案工程师 = 售前工程师 = Solution Engineer（同岗位不同叫法）
  - 核心差异表: KPI/工作产出/面对的人/语言/性格/知识结构/出差模式/赚钱方式 8个维度
  - 500MW项目从线索到售后的8阶段协作流程

## 20260630-10

- **新增**: `data/intersolar_2026_contacts_analysis.md` — Intersolar Europe 2026 名片整理分析
  - 解析 17 条 OCR 名片记录，识别 15 家独立公司
  - 按产品分类: 光伏组件5家、逆变器2家(FORTUNES SOLAR/VDS)、支架1家(MG SOLAR)、材料1家、便携式太阳能1家
  - 关键发现: ELECWAY(德国杜塞尔多夫实体)可能是本地渠道伙伴；无大型EPC/Utility/IPP名片
  - 建议后续参加 E-World(Essen)/Energy Storage Europe(Dusseldorf)接触本地项目方

## 20260715-01

- **新增**: `data/solaredge_smart_meter_charge_control.md` — SolarEdge电池逆变器无PV场景自动充电问题
  - 诊断: 自己品牌Smart Meter协议不兼容 → Meter通信丢失 → Energy Manager安全兜底 → 自动充电
  - 结论: 逆变器Energy Manager决定充放电，Smart Meter只负责测量
  - 三套方案: 买原厂Meter(€150/推荐) / 仿冒协议 / Modbus TCP强控
  - Energy Manager 工作原理：每秒轮询传感器 → 优先级排序（负载>充电>卖电网）→ 输出功率指令
  - 典型场景举例：德国户用 PV 5kW + 负载 2kW + SOC 60% → EM 算出差值 3kW 拿去充电池
