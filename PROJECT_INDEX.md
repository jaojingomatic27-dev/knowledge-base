# 项目文件索引

> 生成于 2026-06-03 | 更新于 2026-06-04（新增4组轮动+6组总图）

## 根目录 C:\AI\cc

| 类型 | 路径 | 说明 |
|------|------|------|
| 📋 | `CLAUDE.md` | 全局规则 |
| 📋 | `PROJECT_INDEX.md` | 本索引文件 |
| 📋 | `PROJECT_LOG.md` | 全局项目日志 |
| 📋 | `account.txt` | GitHub 账号信息 |

---

## 📁 stock/ — 量化回测项目

**GitHub**: https://github.com/jaojingomatic27-dev/stock

### 📂 stock/code/ — 脚本代码

| 文件 | 大小 | 功能 |
|------|------|------|
| `all6_backtest.py` | 13KB | 6 资产综合回测（MA交叉+动量） |
| `chart_4stock_comparison.py` | 7.6KB | 4 只股票对比图 |
| `chart_threshold_scan.py` | 8.4KB | 阈值扫描图表 |
| `check_googl_amzn.py` | 294B | GOOGL/AMZN 数据检查 |
| `check_nvda.py` | 583B | NVDA 数据检查 |
| `dca_2000_2016.py` | 15.8KB | DCA 2000-2016 三时代回测 |
| `dca_backtest.py` | 10.6KB | DCA 基础回测 |
| `dca_equal_invested.py` | 18.7KB | DCA 等额投资对比 |
| `dca_optimize.py` | 14.2KB | DCA 规则优化 |
| `dca_optimize_v2.py` | 15.5KB | DCA 优化 v2 |
| `debug_test.py` | 768B | 调试测试 |
| `download_google.py` | 718B | 下载 GOOGL 数据 |
| `download_orcl_amzn_gld.py` | 629B | 下载 ORCL/AMZN/GLD |
| `download_shy.py` | 356B | 下载 SHY 数据 |
| `download_sp500.py` | 974B | 下载 S&P 500 数据 |
| `download_stocks.py` | 916B | 批量下载股票数据 |
| `download_warrant_data.py` | 792B | 下载权证数据 |
| `googl_backtest.py` | 10.5KB | GOOGL 回测 |
| `googl_backtest_2010.py` | 13.7KB | GOOGL 2010年起回测 |
| `leverage_optimize.py` | 5.6KB | 杠杆 ETF 优化 |
| `leverage_optimize_googl_amzn.py` | 13.4KB | GOOGL/AMZN 杠杆优化 |
| `nvda_backtest.py` | 4.5KB | NVDA 回测 |
| `nvda_chart.py` | 1.2KB | NVDA 图表 |
| `nvda_momentum.py` | 8.3KB | NVDA 动量策略 |
| `rotation_backtest.py` | 16.3KB | 板块轮动回测 |
| `rotation_backtest_googl_amzn.py` | 16.5KB | GOOGL/AMZN 轮动回测 |
| `rotation_threshold_scan.py` | 4.8KB | 轮动阈值扫描 |
| `rotation_threshold_scan_googl_amzn.py` | 4.9KB | GOOGL/AMZN 轮动阈值扫描 |
| `shy_backtest.py` | 28KB | SHY 债券回测 |
| `spy_2000_bear.py` | 7.1KB | SPY 2000 熊市分析 |
| `spy_backtest.py` | 12.6KB | SPY 回测 |
| `volatility_decay_demo.py` | 7.2KB | 波动率衰减演示 |
| `warrants_backtest.py` | 18.6KB | 权证回测 |
| `warrants_full_backtest.py` | 21.5KB | 权证完整回测 |
| `warrant_3x_vs_5x.py` | 5.2KB | 3倍 vs 5倍权证对比 |
| `warrant_5x_compare.py` | 6.4KB | 5倍权证对比 |
| `rotation_vs_worst_stock.py` | 7.4KB | 轮动 vs 表现差股票对比 |
| `leverage_2016_all4.py` | 8.9KB | 4只股票10年杠杆优化 |
| `leverage_optimize_googl_amzn.py` | 13.4KB | GOOGL/AMZN 杠杆优化 |
| `threshold_2016_nvda_mu.py` | 8.1KB | NVDA/MU 10年阈值扫描 |
| `threshold_2016_googl_amzn.py` | 7.2KB | GOOGL/AMZN 10年阈值扫描 |
| `rotation_2016_nvda_mu.py` | 6.8KB | NVDA/MU 10年轮动 |
| `rotation_2016_googl_amzn.py` | 6.7KB | GOOGL/AMZN 10年轮动 |
| `annual_rolling.py` | 8.2KB | 年度滚动回测（两对） |
| `chart_annual_rotation_vs_bh.py` | 4.6KB | 年度轮动 vs B&H 图表 |
| `threshold_scan_4pairs.py` | 11.3KB | 4组新股对阈值+杠杆扫描 |
| `chart_6pairs_annual.py` | 9.1KB | 6组年度轮动 vs B&H 总图 |

### 📂 stock/data/ — 已下载数据

| 文件 | 大小 | 内容 |
|------|------|------|
| `AMZN_daily.csv` | 22.9KB | 亚马逊日线 |
| `GLD_daily.csv` | 374.8KB | 黄金 ETF 日线 |
| `GOOG_daily.csv` | 509.1KB | Google 日线 |
| `GOOGL_daily.csv` | 23.3KB | Alphabet A 日线 |
| `GOOGL_ma_cross.csv` | 162.5KB | GOOGL MA交叉信号 |
| `GOOGL_ma_trades.csv` | 18.4KB | GOOGL MA交易记录 |
| `GOOGL_momentum_12M.csv` | 32.1KB | GOOGL 12月动量 |
| `GSPC_daily.csv` | 364KB | S&P 500 指数日线 |
| `MU_5min.csv` | 462.5KB | 美光 5分钟线 |
| `MU_daily.csv` | 23.2KB | 美光日线 |
| `NVDA_daily.csv` | 23.6KB | 英伟达日线 |
| `NVDA_equity.csv` | 269.8KB | NVDA 权益曲线 |
| `NVDA_momentum_12M.csv` | 23.6KB | NVDA 12月动量 |
| `NVDA_trades.csv` | 14.6KB | NVDA 交易记录 |
| `ORCL_daily.csv` | 23.4KB | 甲骨文日线 |
| `SHY_daily.csv` | 534.2KB | 短期国债 ETF 日线 |
| `SMCI_daily.csv` | 374.7KB | 超微电脑日线 |
| `SPY_daily.csv` | 382.2KB | SPY ETF 日线 |
| `SPY_full.csv` | 768.5KB | SPY 完整历史 |
| `stocks_daily.csv` | 759.1KB | 多股票合并数据 |
| `NVDA_2016_daily.csv` | — | NVDA 2016-2026 日线 |
| `MU_2016_daily.csv` | — | MU 2016-2026 日线 |
| `GOOGL_2016_daily.csv` | — | GOOGL 2016-2026 日线 |
| `AMZN_2016_daily.csv` | — | AMZN 2016-2026 日线 |

### 📂 stock/image/ — 生成的图表

| 文件 | 大小 | 内容 |
|------|------|------|
| `ALL6_risk_return.png` | 117.3KB | 6 资产风险收益散点图 |
| `ALL6_strategies.png` | 617KB | 6 资产策略对比 |
| `DCA_2000_2016.png` | 335.5KB | DCA 三时代对比 |
| `DCA_equal_invested.png` | 398.2KB | DCA 等额投资图 |
| `DCA_optimized.png` | 332.6KB | DCA 优化结果 |
| `DCA_optimized_v2.png` | 419.7KB | DCA 优化 v2 |
| `DCA_SPY_vs_NVDA.png` | 298.2KB | SPY vs NVDA DCA 对比 |
| `GOOGL_backtest_chart.png` | 652.2KB | GOOGL 回测图 |
| `GOOGL_vs_NVDA_2010.png` | 383.3KB | GOOGL vs NVDA 对比 |
| `NVDA_chart.png` | 139.8KB | NVDA K线图 |
| `NVDA_momentum_chart.png` | 451.5KB | NVDA 动量策略图 |
| `SHY_comparison.png` | 900.8KB | SHY 对比图 |
| `SPY_GOOGL_NVDA_chart.png` | 381KB | SPY/GOOGL/NVDA 对比 |
| `chart_4stock_comparison.png` | 301.8KB | 4 股对比图 |
| `threshold_scan_chart.png` | 293.5KB | 阈值扫描图 |
| `chart_annual_rotation_vs_bh.png` | — | 年度轮动 3x/20% vs B&H |
| `threshold_scan_4pairs.png` | — | 4组新股对阈值扫描总图 |
| `chart_6pairs_annual.png` | — | 全部6组年度轮动总图 |

### 📂 stock/ — 其他文件

| 文件 | 说明 |
|------|------|
| `CLAUDE.md` | stock 项目专用规则 |
| `PROJECT_LOG.md` | stock 项目日志 |
| `DCA_RULES_FINAL.txt` | DCA 策略最终结论报告 |
| `.gitignore` | Git 忽略规则 |

---

## 📁 mail/

待开发

## 📁 roof/

待开发
