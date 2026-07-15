# SolarEdge 储能逆变器：Smart Meter 还是逆变器决定充放电？

> **日期**: 2026-07-15
> **问题**: SolarEdge 电池逆变器 + 自己品牌 Smart Meter，无光伏板。开机后自动从电网取电给电池充电，无法控制。
> **SOC**: >50%

---

## 一、一句话结论

**逆变器的 Energy Manager 决定充放电，不是 Smart Meter。Smart Meter 只是个尺子——它只会量，不会管。**

---

## 二、用白话讲清楚架构

| 组件 | 类比 | 实际功能 |
|------|------|---------|
| **Smart Meter** | 温度计 | 只负责读数——"现在电网关口功率是 +3kW" |
| **逆变器的 Energy Manager** | 恒温器控制器 | 读到温度计的数据 → 做判断 → 下指令 |
| **逆变器的功率电路** | 空调/暖气 | 执行指令——充电或放电 |

Smart Meter 本质上是一个 **Modbus RTU 传感器**，每秒钟通过 RS485 发一条报文给逆变器：

```
" 现在电网关口：P = -2.5kW, Q = 0.3kVAr, V = 231V, I = 10.9A "
```

仅此而已。它没有任何逻辑芯片去判断"该不该充电"——这个判断 100% 在逆变器的 CPU 里完成。

---

## 三、谁做哪些事的对照表

| 决策/动作 | 谁做的 | 说明 |
|----------|--------|------|
| 测量电网关口功率 | Smart Meter | RS485 报文，每秒一次 |
| 测量电池 SOC | 逆变器（BMS 通讯） | 通过 CAN/RS485 读电池 BMS |
| 测量 PV 功率 | 逆变器（DC-DC 单元） | 内置传感器 |
| **充电/放电判断** | **逆变器 Energy Manager** | 读到的数据→对比策略→决定充/放/待机 |
| **充电功率大小** | **逆变器 Energy Manager** | 例如"现在以 2kW 充" |
| 执行充电 | 逆变器功率电路 | DC-AC 双向变换器执行 |
| 执行放电 | 逆变器功率电路 | 同上 |
| **没有人读得懂时** | **逆变器 Energy Manager** | **进入安全兜底→自动充电** |

---

## 四、你的问题出在哪

你的系统链路：

```
Smart Meter（自己品牌）→ 逆变器
             ↑
       协议不通！
```

逆变器 Energy Manager 每隔 1 秒问一次："Smart Meter，关口功率多少？"

没有回应。问 3 次 → 判定 **"Meter Communication Lost"**。

这个故障码不只是"尺子坏了所以没法量"——

而是 **"我不知道家里用电状况，所以不敢让电池闲着。"**

安全兜底逻辑说：万一现在家里正在用电，电池没电 → 电费飙升；电池有电 → 至少能顶一阵。

于是开机就自动从电网取电充电。**SOC 大于 50% 也没用**——因为逆变器不知道你现在是"不需要电的静止状态"，它只知道"我看不见外面发生了什么，先把电池充满以策安全"。

---

## 五、解决方案

| 方案 | 原理 | 费用 |
|------|------|------|
| **买 SolarEdge 原厂 Modbus Meter** | 协议兼容，逆变器收到正确报文 → 安全兜底关闭 → 你说了算 | ~€150 |
| **让你的 Smart Meter 仿冒 SolarEdge 协议** | 在 RS485 总线上发送 SolarEdge 格式的 Modbus 报文 | 开发成本高 |
| **Modbus TCP 写寄存器强控** | 绕过 Energy Manager，直接写充放电功率寄存器（地址 0xE004-0xE00A） | 需要外置控制器 |

**推荐方案：买 SolarEdge 原厂 Modbus Meter。** 装上去 5 分钟后，逆变器 Energy Manager 收到正确关口数据，安全兜底关闭，你就能在 SetApp / mySolarEdge 里自由设置充放电策略。

---

## 六、额外需要关注的设置

即使 Meter 就位，还需要确认以下配置：

1. **SetApp → Storage Mode** 设为 "Backup Only" 或 "Remote Control"（而非 "Maximize Self Consumption"）
2. **SetApp → AC Charge / Grid Charging** 设为 "Disabled"
3. **SetApp → Status → Communication → Meter Status** 确认显示 "OK"

因为你的场景是无光伏、纯电池储能，错误的 Storage Mode 设置（如 "Maximize Self Consumption"）即使 Meter 正常，也可能导致逆变器主动从电网买电给电池充电。
