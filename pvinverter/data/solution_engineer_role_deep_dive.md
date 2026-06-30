# PCS 技术方案/售前工程师 — 德国本地招聘详解

> **适用行业**: 大型储能/商用储能 PCS 逆变器
> **岗位对标**: 盛弘德国 "DACH 储能销售经理" JD 中隐含的技术能力要求，拆出独立岗位
> **分析日期**: 2026-06-30

---

## 一、岗位定义

**技术方案工程师 / 售前工程师（Pre-Sales Engineer / Solution Engineer）**

这个职位是销售团队和客户之间的**技术翻译器**——把客户说的"我需要一个 50MW 储能电站，在萨克森-安哈特接入 110kV"翻译成"你需要 30 台 PWS1-1725KTL、3 台 10kV/110kV 变压器、按 VDE-AR-N 4120 做并网方案"。

---

## 二、职责范围

### 2.1 核心职责（日常 70%）

| 职责 | 具体工作内容 | 交付物 |
|------|------------|--------|
| **投标技术方案** | 读客户招标书（德语 200 页+），提取技术需求，配置 PCS 型号、数量、连接方式 | 技术标书 / 配置清单 / 单线图 |
| **并网兼容性分析** | 根据项目所在地电网规范（VDE 4105/4110/4120 / EN 50549），判断 PCS 是否需要额外认证或参数调整 | 并网合规评估报告 |
| **系统级方案设计** | PCS + 变压器 + 集装箱/BESS 外壳 + EMS/SCADA 的接口对接方案 | 系统架构图 / 接口规范表 |
| **客户技术答疑** | 陪同销售拜访客户，解答电网运营商、EPC 技术团队、IPP 技术顾问的一切技术问题 | 会议纪要 / 技术澄清函 |
| **FAT/SAT 技术支持** | 在工厂验收（FAT）和现场验收（SAT）时做技术代表，确保测试结果符合合同承诺 | 测试报告审核 |

### 2.2 延伸职责（日常 30%）

| 职责 | 具体工作内容 |
|------|------------|
| **竞品技术分析** | 对比 SMA/Siemens/阳光电源等竞品 PCS 在效率、并网能力、认证范围上的差异，形成 technical battlecard |
| **向研发反馈需求** | VDE 标准更新、客户定制化需求、现场发现的 bug → 翻译为中文技术需求，提交中国研发团队 |
| **新品本地化验证** | 中国总部出的新机型，在德国做本地并网仿真、现场试点，确认符合 DACH 电网实际 |
| **培训销售团队** | 给纯销售背景的同事做"101 储能 PCS 技术培训"：并网标准、系统架构、关键指标解读 |

---

## 三、应聘者需要具备的能力

### 3.1 硬技能（必须）

| 能力维度 | 具体要求 | 面试中如何验证 |
|---------|---------|-------------|
| **电气工程基础** | 电力电子拓扑（三电平/模块化多电平）、变压器选型、功率计算、单线图绘制 | 给一张空白纸，让他画一个 50MW BESS 的单线图 |
| **并网标准** | VDE-AR-N 4105 / 4110 / 4120、EN 50549-1/-2、IEC 61850 通信协议。LVRT/HVRT、Q-V 曲线、P-f 下垂 | 给一个具体项目参数，让他判断用什么并网标准、需要哪些 TR 认证 |
| **储能系统集成** | 理解电池（容量 C-rate、SOC/SOH）、PCS、EMS/SCADA、变压器、保护装置之间的逻辑关系 | 问：BESS 从收到 AGC 指令到 PCS 出力变化，信号链路是什么？ |
| **通信协议** | Modbus TCP/RTU、IEC 61850 MMS/GOOSE、CANbus。知道怎么配置 PCS 与 EMS 之间的点表 | 给一份真实的 Modbus 寄存器表部分截图，让他解释 |
| **德语技术文档** | 能**用德语**阅读并书写技术标书。德语母语或 C1+，英语至少 B2 | 现场给一段德国电网运营商的 VDE 合规要求（德语），让他翻译并总结 |
| **投标经验** | 至少 2 年 PV/BESS 项目技术投标经验，参与过 >10MW 级项目 | 问：上一个你负责技术标的大型项目是什么？你的具体贡献？ |

### 3.2 软技能（同样必须）

| 能力 | 为什么重要 |
|------|----------|
| **跨文化沟通** | 你是中国工厂/研发团队和德国客户之间的唯一技术接口。中国人说"差不多"，德国人理解成"不需要"。你要两边翻译得不能让任何一方误解 |
| **客户服务意识** | 客户半夜发邮件问"你们的 PCS 为什么在频率 49.8Hz 时无功出力跟我仿真的不一样"，你要能在第二天上班前给他一个技术上有依据的回复 |
| **压力承受** | 投标截止前 48 小时发现方案里变压器选型有误 → 需要你跟中国团队一起熬夜改 |
| **结构化表达** | 你的方案要有逻辑、有数据、有图示，让客户的电网部门、采购部门、管理层三个层次的人看完都服气 |

### 3.3 加分项

- 有 **SMA / Siemens / ABB / KACO / Fronius / 阳光电源 / 华为** 等同行业背景
- 有 **电网运营商（VNB/ÜNB）从业经验**——最了解并网审批内部逻辑
- 有 **DACH 地区电气工程学位**（TU München、RWTH Aachen、TU Berlin、ETH Zürich 等）
- 中文能力（能和深圳总部直接用中文沟通，飞跃级加分）

---

## 四、这个职位为什么必须在德国，不能在中国？

这不是"nice to have"——是**战略级必须**。五个不可替代的理由：

### 理由 1：时差是物理定律，不是流程能解决的

| 场景 | 在中国做 | 在德国做 |
|------|---------|---------|
| 德国客户上午 10:00 发来紧急技术问题 | 北京时间下午 5:00，中国团队准备下班 | 德国时间上午 10:00，立刻回复 |
| 中国研发下午 3:00 需要确认一个德国电网参数 | 可以直接问 | 德国凌晨——等他回消息是 6 小时后 |
| 投标截止前通宵改方案 | 德国时间夜间，客户联系不上 | 随时可电话沟通 |

500MW 级的项目——客户在德国、招标方在德国、电网在德国——**技术响应时效从 6 小时延迟变成 30 分钟，这个差别决定你拿不拿得到标。**

### 理由 2：德语技术文档不是在中国的双语工程师就能搞定的

一个德国的 Utility 招标书通常 200-300 页，全部德文，包含：
- 电网运营商的**技术连接条件（TAB）**引用
- VDE 标准的**条款级引用**
- 德国本地的**法律法规条款**（EEG、EnWG、StromNEV）

让你在深圳的双语工程师读这个东西？他会卡在"§ 19 StromNEV i.V.m. § 8 EEG 2023"这种法律条款引用上。而这是德国电气工程师在读书期间就在课堂上讨论的内容。

**不是语言问题，是法域（jurisdiction）问题。** 你的技术方案写错了某个并网参数，后果不是客户投诉——是电网运营商拒绝给你并网许可。

### 理由 3：现场就是一切

客户说"我要去你们现场看看"，你说"我们的技术负责人在深圳，我帮你视频连线"——这单已经丢了。

德国的 EPC 和 Utility 非常看重**本地存在感**：
- 项目前期：客户的技术团队会要求供应商到项目现场做**并网可行性评估**
- 投标阶段：技术答辩（technical clarification meeting）通常是**面对面**
- 交付阶段：FAT/SAT 必须有技术负责人在场签字

你不能让一个深圳工程师每两周飞一次德国——成本+签证+时差+身体损耗完全不可行。

### 理由 4：跨文化技术沟通需要"中间人"

中国研发说"这个问题不大"——德国客户听到的是"你不重视我的问题"。
德国客户说"我们要求功率响应时间 ≤ 150ms"——中国研发在 PDF 里翻到底都找不到这句德语是什么意思。

**技术方案工程师就是这个"中间人"。** 他不能只懂技术——他必须懂两边的文化逻辑：
- 知道德国人说"ich hätte eine kleine Anmerkung"其实是一个非常严重的反对意见
- 知道中国研发说"已经优化了"需要追问"优化后的具体测试数据是什么"

这不可能在深圳培养出来。必须是在 DACH 地区生活工作过、和中国团队有长期合作经验的人。

### 理由 5：客户信任是当面建立，不是 Zoom 建立的

这是德国能源行业的底层逻辑：**电网是国家安全级基础设施。** 你卖给 RWE 的 PCS 如果出了故障，可能导致整个变电站跳闸。RWE 的电网总监必须见过你的人、看过你的脸、跟你握过手——才敢在采购决策上签字。

一个在深圳远程工作的技术方案工程师，永远不可能建立这种级别的信任。

---

## 五、如果仍然想在中国培养人替代 —— 现实方案

在德国本地团队站稳之前（前 12-18 个月），可以考虑**渐进过渡方案**：

| 阶段 | 德国本地 | 中国支持 | 过渡目标 |
|------|---------|---------|---------|
| 第 1-6 月 | 1 个德国方案工程师 | 1 个中国海归（德语 C1+电气背景）常驻德国 3 个月 | 中方人员熟悉德国客户和标准 |
| 第 6-12 月 | 同上 | 中方回国，远程支持标准化的技术文档撰写 | 基础文档剥离到中国 |
| 第 12 月+ | 2 个德国方案工程师 | 中国只做内部技术分析，不与客户直接沟通 | 德国团队完全独立面对客户 |

**底线不可动摇：与客户直接沟通的技术角色，必须在德国本地。**

---

## 六、招聘 JD 草稿

**Position**: Solution Engineer / Pre-Sales Engineer — Energy Storage PCS (DACH)

**Location**: Düsseldorf / Frankfurt / Munich, Germany

**Responsibilities**:
- Lead technical proposal preparation for utility-scale BESS projects (>10MW), including PCS configuration, single-line diagrams, and grid compliance analysis
- Serve as primary technical interface between customers (utilities, IPPs, EPCs) and the China-based R&D/manufacturing team
- Perform grid code compliance assessment per VDE-AR-N 4105/4110/4120 and EN 50549
- Support FAT/SAT on-site and resolve technical deviations during commissioning
- Conduct competitive technical benchmarking and feed market requirements back to product development
- Deliver technical training to the sales team and customer workshops

**Requirements — Must-have**:
- B.Sc. or M.Sc. in Electrical Engineering, Power Systems, Power Electronics, or related field
- 3+ years in a technical/pre-sales role in renewable energy, preferably energy storage, PV, or wind
- Proven experience preparing technical bids for projects >10MW
- Deep understanding of grid connection requirements in DACH: VDE 4105/4110/4120 and EN 50549
- Hands-on experience with PCS/inverter system integration, EMS/SCADA interfaces, and industrial communication protocols (Modbus, IEC 61850)
- Native or C1 German; fluent business English (B2 minimum)
- Willingness to travel within DACH (~30-40%)

**Nice-to-have**:
- Experience at a PCS/inverter manufacturer (SMA/Siemens/ABB/Huawei/Sungrow etc.)
- Prior employment at a DACH grid operator (VNB/ÜNB)
- Chinese language ability (Mandarin)

**What we offer**:
- A key role in building the European technical team from the ground up
- Competitive compensation with project-based bonus
- Flexible remote work within Germany with regular team meetings
- Direct interface with the global R&D team in Shenzhen
