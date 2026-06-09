# 本机硬件配置

## CPU

| 项目 | 详情 |
|------|------|
| 型号 | 11th Gen Intel Core **i9-11900H** |
| 基础频率 | 2.50 GHz（睿频最高 4.90 GHz） |
| 核心 | 8 核 16 线程 |

## 内存

| 项目 | 详情 |
|------|------|
| 总容量 | **64 GB** DDR4 |

## 显卡

| 项目 | 详情 |
|------|------|
| 集显 | Intel UHD Graphics（共享系统内存） |
| 独显 | NVIDIA GeForce **RTX 3080 Laptop GPU** |
| 显存 | **16 GB** (16384 MiB) GDDR6 |
| 驱动 | 30.0.14.7219 |

> **注**：WMI `Win32_VideoController.AdapterRAM` 为 32 位字段，超过 4GB 会溢出。以 `nvidia-smi` 输出的 16384 MiB 为准。

## 系统

| 项目 | 详情 |
|------|------|
| 操作系统 | Windows 10 Pro 19043 |
| 时区 | (UTC+01:00) Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna（德国 CEST/CET） |

---

*采集日期: 2026-06-06*
*采集命令: `Get-CimInstance Win32_Processor` / `Win32_PhysicalMemory` / `Win32_VideoController` / `nvidia-smi`*
