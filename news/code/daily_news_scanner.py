#!/usr/bin/env python3
"""
每日盘前新闻扫描器 — Pre-Market News Scanner
=============================================
美股开盘前 1 小时自动搜索全网 24 小时内关于持仓公司的新闻，
进行情感分析（利多/利空），并通过 Gmail 发送汇总报告。

覆盖标的：
  铁三角:   NVDA, MSFT, ORCL
  窜天猴:   PLTR, SMCI, TSLA
  DCA均衡型: SPY, AVGO (NVDA 已覆盖)

用法：
  python daily_news_scanner.py              # 标准模式
  python daily_news_scanner.py --dry-run    # 只生成报告，不发送邮件
  python daily_news_scanner.py --output     # 保存 HTML 到 data/ 目录
"""

import os
import sys
import io

# ── Windows 编码修复 ──────────────────────────────────────────
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
import re
import json
import hashlib
import smtplib
import ssl
import time
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from collections import defaultdict
from typing import Optional
from xml.etree import ElementTree

# ── 第三方库 ──────────────────────────────────────────────────
try:
    import yfinance as yf
except ImportError:
    yf = None
    print("[WARN] yfinance not installed; falling back to RSS only")

try:
    import feedparser
except ImportError:
    feedparser = None
    print("[WARN] feedparser not installed; RSS search disabled")

try:
    from deep_translator import GoogleTranslator
    TRANSLATOR = GoogleTranslator(source='en', target='zh-CN')
except ImportError:
    TRANSLATOR = None
    print("[WARN] deep-translator not installed; translation disabled")

# ── 路径配置 ──────────────────────────────────────────────────
PROJECT_ROOT = Path(r"C:\AI\cc\news")
# 确保工作目录正确（Task Scheduler 环境下必要）
os.chdir(str(PROJECT_ROOT))
CODE_DIR = PROJECT_ROOT / "code"
DATA_DIR = PROJECT_ROOT / "data"
ACCOUNT_FILE = PROJECT_ROOT / "account.txt"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ── 读取邮箱账号 ──────────────────────────────────────────────
def load_account():
    """从 account.txt 读取邮箱和密码"""
    lines = ACCOUNT_FILE.read_text(encoding="utf-8").strip().splitlines()
    email = lines[0].strip()
    password = lines[1].strip()
    return email, password

EMAIL, APP_PASSWORD = load_account()

# ── 投资组合配置 ──────────────────────────────────────────────
PORTFOLIOS = {
    "铁三角 (NVDA+MSFT+ORCL)": {
        "tickers": ["NVDA", "MSFT", "ORCL"],
        "type": "Turbo 权证多单",
        "emoji": "🔺",
        "priority": 1,  # 最高优先级
    },
    "窜天猴 (PLTR+SMCI+TSLA)": {
        "tickers": ["PLTR", "SMCI", "TSLA"],
        "type": "Turbo 权证多单",
        "emoji": "🚀",
        "priority": 2,
    },
    "DCA 均衡型 (SPY+NVDA+AVGO)": {
        "tickers": ["SPY", "AVGO"],  # NVDA 已在上方覆盖
        "type": "DCA 定投",
        "emoji": "⚖️",
        "priority": 3,
    },
}

# 去重后的所有 ticker
ALL_TICKERS = sorted(set(
    ticker for pf in PORTFOLIOS.values() for ticker in pf["tickers"]
))

# ── 公司全名映射 ──────────────────────────────────────────────
COMPANY_NAMES = {
    "NVDA": "NVIDIA",
    "MSFT": "Microsoft",
    "ORCL": "Oracle",
    "PLTR": "Palantir",
    "SMCI": "Super Micro Computer",
    "TSLA": "Tesla",
    "SPY": "S&P 500 ETF",
    "AVGO": "Broadcom",
}

# ── 搜索关键词 (用于 Google News RSS) ─────────────────────────
SEARCH_QUERIES = {
    "NVDA": "NVIDIA NVDA stock",
    "MSFT": "Microsoft MSFT stock",
    "ORCL": "Oracle ORCL stock",
    "PLTR": "Palantir PLTR stock",
    "SMCI": "Super Micro SMCI stock",
    "TSLA": "Tesla TSLA stock",
    "SPY": "SPY S&P 500 ETF market",
    "AVGO": "Broadcom AVGO stock",
}

# ═══════════════════════════════════════════════════════════════
#  金融情感词典 — Financial Sentiment Lexicon
# ═══════════════════════════════════════════════════════════════

# 利多关键词 (Bullish)
BULLISH_PATTERNS = [
    # 业绩相关
    (r'\b(beat|beats|beating)\s+(earnings|estimates?|expectations?|revenue|forecast)', 3.0),
    (r'\b(record|all.time.high|ATH)\s+(revenue|profit|quarter|sales|high)', 3.0),
    (r'\b(revenue|earnings|profit|sales)\s+(surge[d]?|soar|jump|climb|rise|grew|grow)', 2.5),
    (r'\b(raised?|raises?|raising)\s+(guidance|outlook|forecast|target|dividend)', 2.5),
    (r'\b(exceed|beat|top|surpass)\w*\s+(estimate|forecast|expectation|target)', 2.5),

    # 分析师评级
    (r'\b(upgrade[d]?|upgrading)\b', 2.0),
    (r'\b(bullish|outperform|overweight|strong buy|buy rating)\b', 2.0),
    (r'\b(price\s*target)\s*(raised|increase|boost|hiked|lifted)', 2.0),
    (r'\b(initiate[d]?\s*(coverage\s*)?with\s*(buy|outperform|overweight))\b', 2.0),

    # 业务/产品
    (r'\b(new\s*(product|chip|platform|partnership|contract|deal|launch))\b', 2.0),
    (r'\b(breakthrough|innovation|revolutionary|game.chang)', 1.5),
    (r'\b(AI\s*(boom|demand|growth|expansion|revolution))\b', 1.5),
    (r'\b(chip\s*shortage\s*(easing|improving|resolved))\b', 2.0),
    (r'\b(expanding|expansion|scaling)\s*(production|capacity|manufacturing)', 1.5),
    (r'\b(supply\s*deal|major\s*contract|won\s*contract)\b', 2.0),

    # 市场/宏观
    (r'\b(rally|surge[d]?|soar|skyrocket|boom)\b', 1.5),
    (r'\b(bull\s*(market|run|trend))\b', 1.5),
    (r'\b(Fed\s*(cut|cuts|cutting|ease|dovish))\b', 1.5),
    (r'\b(rate\s*cut|monetary\s*easing)\b', 1.5),

    # 通用利多
    (r'\b(strong|robust|impressive)\s+(demand|growth|result|quarter|performance|report)\b', 2.0),
    (r'\b(optimistic|positive|promising|bright)\s*(outlook|forecast|future)\b', 1.5),
    (r'\b(stock\s*(surge|jump|rally|climb|rise|gain))\b', 1.5),
    (r'\b(share\s*buyback|stock\s*repurchase)\b', 2.0),
    (r'\b(dividend\s*(increase|hike|boost|raise))\b', 2.0),
]

# 利空关键词 (Bearish)
BEARISH_PATTERNS = [
    # 业绩相关
    (r'\b(miss|misses|missed)\s+(earnings|estimates?|expectations?|revenue|forecast)', 3.0),
    (r'\b(revenue|earnings|profit|sales)\s+(drop|fell|decline|plunge|slump|tumble)', 2.5),
    (r'\b(loss|losses|net\s*loss)\b', 2.0),
    (r'\b(lowered?|lowers?|lowering|cut|cutting)\s+(guidance|outlook|forecast|target)', 3.0),

    # 分析师评级
    (r'\b(downgrade[d]?|downgrading)\b', 2.5),
    (r'\b(bearish|underperform|underweight|sell rating|strong sell)\b', 2.5),
    (r'\b(price\s*target)\s*(cut|lower|reduce|slash)', 2.0),

    # 业务/产品风险
    (r'\b(delay|postpone|push\s*back)\s*(product|chip|launch|shipment)', 2.0),
    (r'\b(recall|defect|bug|vulnerability|security\s*flaw)\b', 2.5),
    (r'\b(chip\s*ban|export\s*control|sanction|restriction)\b', 2.5),
    (r'\b(supply\s*chain\s*(disruption|issue|problem|shortage))\b', 2.0),
    (r'\b(production\s*(halt|stop|issue|problem|cut))\b', 2.0),
    (r'\b(ceo\s*(resign|step\s*down|depart|fired))\b', 2.5),

    # 监管/法律
    (r'\b(lawsuit|litigation|sue|suing|class\s*action)\b', 2.5),
    (r'\b(DOJ|FTC|SEC|EU)\s*(investigation|probe|fine|penalty|antitrust)\b', 2.5),
    (r'\b(regulation|regulatory)\s*(crackdown|risk|concern|issue)\b', 2.0),
    (r'\b(antitrust\s*(lawsuit|case|probe|investigation|breakup))\b', 2.5),

    # 竞争/市场
    (r'\b(losing|loss|lost)\s*(market\s*share|customer|contract)\b', 2.0),
    (r'\b(competition|competitive)\s*(threat|pressure|intensif)', 1.5),
    (r'\b(deepseek|Chinese\s*AI\s*(rival|threat|competition))\b', 1.5),

    # 宏观利空
    (r'\b(recession|downturn|slowdown|contraction)\b', 1.5),
    (r'\b(Fed\s*(hike|hawkish|tighten))\b', 1.5),
    (r'\b(tariff|trade\s*war)\b', 1.5),
    (r'\b(inflation\s*(surge|spike|accelerat|hotter))\b', 1.5),

    # 通用利空
    (r'\b(weak|poor|disappointing)\s+(demand|result|quarter|performance|report)\b', 2.0),
    (r'\b(stock\s*(drop|fall|plunge|crash|tumble|sink|decline))\b', 1.5),
    (r'\b(layoff|job\s*cut|workforce\s*reduction)\b', 2.0),
]

# 修饰词 — 增强或减弱信号
AMPLIFIERS = [
    r'\b(significantly|substantially|dramatically|massively|huge)\b',
    r'\b(record|historic|unprecedented)\b',
]

DIMINISHERS = [
    r'\b(slightly|modestly|marginally|minor)\b',
    r'\b(despite|although|however)\b',
]


def analyze_sentiment(text: str) -> dict:
    """
    对新闻标题+摘要进行金融情感分析。
    返回: {"score": float, "label": str, "bullish_hits": list, "bearish_hits": list}
    """
    text_lower = text.lower()
    bull_score = 0.0
    bear_score = 0.0
    bull_hits = []
    bear_hits = []

    # 扫描利多模式
    for pattern, weight in BULLISH_PATTERNS:
        matches = re.findall(pattern, text_lower)
        if matches:
            # 检查修饰词
            for amp in AMPLIFIERS:
                if re.search(amp, text_lower):
                    weight *= 1.3
                    break
            for dim in DIMINISHERS:
                if re.search(dim, text_lower):
                    weight *= 0.7
                    break
            bull_score += weight * len(matches)
            bull_hits.append(str(matches[0]) if isinstance(matches[0], tuple) else matches[0])

    # 扫描利空模式
    for pattern, weight in BEARISH_PATTERNS:
        matches = re.findall(pattern, text_lower)
        if matches:
            for amp in AMPLIFIERS:
                if re.search(amp, text_lower):
                    weight *= 1.3
                    break
            for dim in DIMINISHERS:
                if re.search(dim, text_lower):
                    weight *= 0.7
                    break
            bear_score += weight * len(matches)
            bear_hits.append(str(matches[0]) if isinstance(matches[0], tuple) else matches[0])

    net_score = bull_score - bear_score

    # 分类
    if net_score >= 3.0:
        label = "🟢 强烈利多"
    elif net_score >= 1.0:
        label = "🟢 利多"
    elif net_score > -1.0:
        label = "🟡 中性"
    elif net_score > -3.0:
        label = "🔴 利空"
    else:
        label = "🔴 强烈利空"

    return {
        "score": round(net_score, 2),
        "label": label,
        "bull_score": round(bull_score, 2),
        "bear_score": round(bear_score, 2),
        "bullish_hits": bull_hits[:5],
        "bearish_hits": bear_hits[:5],
    }


# ═══════════════════════════════════════════════════════════════
#  新闻获取 — News Fetching
# ═══════════════════════════════════════════════════════════════

def fetch_yfinance_news(ticker: str) -> list[dict]:
    """通过 yfinance 获取个股新闻"""
    if yf is None:
        return []
    try:
        t = yf.Ticker(ticker)
        raw_news = t.news or []
    except Exception as e:
        print(f"  [WARN] yfinance news failed for {ticker}: {e}")
        return []

    results = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    for item in raw_news:
        try:
            content = item.get("content", {})
            title = content.get("title", "")
            summary = content.get("summary", "") or content.get("description", "")
            pub_date_str = content.get("pubDate", "")
            url = content.get("canonicalUrl", {}).get("url", "") or \
                  content.get("clickThroughUrl", {}).get("url", "")
            provider = content.get("provider", {}).get("displayName", "")

            # 解析时间
            if pub_date_str:
                try:
                    pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
                except ValueError:
                    pub_date = datetime.now(timezone.utc)
            else:
                pub_date = datetime.now(timezone.utc)

            # 只保留 24 小时内的
            if pub_date < cutoff:
                continue

            if not title:
                continue

            results.append({
                "ticker": ticker,
                "title": title,
                "summary": summary,
                "url": url,
                "provider": provider,
                "pub_date": pub_date,
                "source": "yfinance",
            })
        except Exception:
            continue

    return results


def fetch_google_news_rss(ticker: str) -> list[dict]:
    """通过 Google News RSS 搜索新闻"""
    if feedparser is None:
        return []

    query = SEARCH_QUERIES.get(ticker, f"{ticker} stock")
    rss_url = (
        f"https://news.google.com/rss/search?"
        f"q={query.replace(' ', '%20')}&hl=en-US&gl=US&ceid=US:en"
    )

    try:
        feed = feedparser.parse(rss_url)
    except Exception as e:
        print(f"  [WARN] RSS parse failed for {ticker}: {e}")
        return []

    if feed.get("bozo", 0) and not feed.entries:
        return []

    results = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

    for entry in feed.entries:
        try:
            title = entry.get("title", "")
            summary = entry.get("summary", "") or entry.get("description", "")
            link = entry.get("link", "")
            source = entry.get("source", {}).get("title", "Google News")

            # 解析发布时间
            published_parsed = entry.get("published_parsed")
            if published_parsed:
                pub_date = datetime(*published_parsed[:6], tzinfo=timezone.utc)
            else:
                pub_date = datetime.now(timezone.utc)

            if pub_date < cutoff:
                continue

            if not title:
                continue

            # 清理 HTML 标签
            title = re.sub(r'<[^>]+>', '', title)
            summary = re.sub(r'<[^>]+>', '', summary)

            results.append({
                "ticker": ticker,
                "title": title,
                "summary": summary[:500] if summary else "",
                "url": link,
                "provider": source,
                "pub_date": pub_date,
                "source": "Google News RSS",
            })
        except Exception:
            continue

    return results


def fetch_reuters_news(ticker: str) -> list[dict]:
    """通过 Google News RSS 搜索 Reuters 来源新闻"""
    if feedparser is None:
        return []

    company = COMPANY_NAMES.get(ticker, ticker)
    query = f"{company} {ticker} site:reuters.com"
    rss_url = (
        f"https://news.google.com/rss/search?"
        f"q={query.replace(' ', '%20')}&hl=en-US&gl=US&ceid=US:en"
    )

    try:
        feed = feedparser.parse(rss_url)
    except Exception as e:
        print(f"  [WARN] Reuters RSS failed for {ticker}: {e}")
        return []

    if feed.get("bozo", 0) and not feed.entries:
        return []

    results = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

    for entry in feed.entries:
        try:
            title = entry.get("title", "")
            link = entry.get("link", "")
            published_parsed = entry.get("published_parsed")
            if published_parsed:
                pub_date = datetime(*published_parsed[:6], tzinfo=timezone.utc)
            else:
                pub_date = datetime.now(timezone.utc)

            if pub_date < cutoff:
                continue
            if not title:
                continue

            title = re.sub(r'<[^>]+>', '', title)
            # 提取真正来源 (Google News 格式: "标题 - Reuters")
            source_name = "Reuters"
            source_title = entry.get("source", {}).get("title", "")
            if "reuters" in source_title.lower():
                source_name = "Reuters"

            results.append({
                "ticker": ticker,
                "title": title.replace(" - Reuters", "").replace(" - Reuters.com", ""),
                "summary": "",
                "url": link,
                "provider": source_name,
                "pub_date": pub_date,
                "source": "Reuters",
            })
        except Exception:
            continue

    return results


def fetch_all_news() -> list[dict]:
    """获取所有 ticker 的新闻并去重"""
    all_news = []
    seen = set()

    for ticker in ALL_TICKERS:
        print(f"  搜索 {ticker} ({COMPANY_NAMES.get(ticker, '')})...")

        # 三源获取
        yf_news = fetch_yfinance_news(ticker)
        rss_news = fetch_google_news_rss(ticker)
        reuters_news = fetch_reuters_news(ticker)

        combined = yf_news + rss_news + reuters_news
        print(f"    共 {len(combined)} 条 (yfinance: {len(yf_news)}, RSS: {len(rss_news)}, Reuters: {len(reuters_news)})")

        for item in combined:
            # 用 URL 去重，无 URL 则用标题 hash
            dedup_key = item["url"] or hashlib.md5(item["title"].encode()).hexdigest()
            if dedup_key in seen:
                continue
            seen.add(dedup_key)

            # 情感分析
            sentiment_text = f"{item['title']} {item['summary']}"
            item["sentiment"] = analyze_sentiment(sentiment_text)
            all_news.append(item)

    # 按情感分数排序（利空在前，利多在后 — 关注风险优先）
    all_news.sort(key=lambda x: x["sentiment"]["score"])

    # 批量翻译标题
    print(f"\n  正在翻译 {len(all_news)} 条标题...")
    batch_translate(all_news)

    return all_news


# ═══════════════════════════════════════════════════════════════
#  翻译 + 公司名高亮
# ═══════════════════════════════════════════════════════════════

# 翻译缓存（避免重复翻译相同标题）
_translation_cache: dict = {}
TRANSLATION_CACHE_FILE = DATA_DIR / "translation_cache.json"

def _load_translation_cache():
    """从磁盘加载翻译缓存"""
    global _translation_cache
    if TRANSLATION_CACHE_FILE.exists():
        try:
            _translation_cache = json.loads(TRANSLATION_CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            _translation_cache = {}

def _save_translation_cache():
    """保存翻译缓存到磁盘"""
    try:
        TRANSLATION_CACHE_FILE.write_text(
            json.dumps(_translation_cache, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    except Exception:
        pass

# 公司名 → 高亮颜色映射（含 ticker 代码和常见别名）
COMPANY_HIGHLIGHT_MAP = {
    # NVIDIA
    "NVIDIA": "NVIDIA", "Nvidia": "NVIDIA", "nvidia": "NVIDIA", "NVDA": "NVIDIA",
    # Microsoft
    "Microsoft": "Microsoft", "microsoft": "Microsoft", "MSFT": "Microsoft",
    # Oracle
    "Oracle": "Oracle", "oracle": "Oracle", "ORCL": "Oracle",
    # Palantir
    "Palantir": "Palantir", "palantir": "Palantir", "PLTR": "Palantir",
    # Tesla
    "Tesla": "Tesla", "tesla": "Tesla", "TSLA": "Tesla",
    # Broadcom
    "Broadcom": "Broadcom", "broadcom": "Broadcom", "AVGO": "Broadcom",
    # Super Micro
    "Super Micro": "Super Micro", "Supermicro": "Super Micro",
    "super micro": "Super Micro", "SMCI": "Super Micro",
    # SPY
    "S&P 500": "SPY", "SPDR": "SPY",
    # 不映射的通用词
    "ETF": "",
}

# 中文公司名 → 英文 tag 映射（用于中文翻译文本高亮）
CN_COMPANY_NAMES = {
    "英伟达": "NVIDIA", "辉达": "NVIDIA",
    "微软": "Microsoft",
    "甲骨文": "Oracle",
    "帕兰提尔": "Palantir", "帕兰蒂尔": "Palantir", "帕兰泰尔": "Palantir",
    "帕拉提尔": "Palantir", "帕拉蒂尔": "Palantir",
    "特斯拉": "Tesla",
    "博通": "Broadcom",
    "超微": "Super Micro", "超微电脑": "Super Micro",
    "标普": "SPY", "标普500": "SPY", "标准普尔": "SPY",
}

COMPANY_HIGHLIGHT_COLORS = {
    "NVIDIA":    ("#76b900", "#1a2e0a"),
    "Microsoft": ("#00a4ef", "#0a1a2e"),
    "Oracle":    ("#f80000", "#2e0a0a"),
    "Palantir":  ("#c0c0c0", "#1a1a1a"),
    "Tesla":     ("#e82127", "#2e0a0a"),
    "Broadcom":  ("#cc0000", "#2e0a0a"),
    "Super Micro":("#1e90ff", "#0a1a2e"),
    "SPY":       ("#ff9800", "#2e1a0a"),
}

def translate_title(title: str) -> str:
    """翻译英文标题为中文（带缓存 + 重试）"""
    if TRANSLATOR is None:
        return ""
    if title in _translation_cache:
        return _translation_cache[title]
    text = title[:150]
    for attempt in range(2):
        try:
            result = TRANSLATOR.translate(text)
            if result and result != text:  # 确保翻译成功且不同于原文
                _translation_cache[title] = result
                return result
        except Exception:
            pass
        time.sleep(0.3)  # 重试前等待
    # 两次都失败，缓存空字符串避免重复尝试
    _translation_cache[title] = ""
    return ""

def highlight_companies(text: str) -> str:
    """在文本中高亮公司名（HTML span 标签，中英文均支持）"""
    result = text

    # 1. 英文公司名高亮
    en_names = sorted(COMPANY_HIGHLIGHT_MAP.keys(), key=len, reverse=True)
    for name in en_names:
        tag = COMPANY_HIGHLIGHT_MAP[name]
        if not tag:
            continue
        colors = COMPANY_HIGHLIGHT_COLORS.get(tag)
        if not colors:
            continue
        color, bg = colors
        replacement = f'<span style="color:{color};font-weight:600;">{name}</span>'
        result = result.replace(name, replacement)

    # 2. 中文公司名高亮
    cn_names = sorted(CN_COMPANY_NAMES.keys(), key=len, reverse=True)
    for cn_name in cn_names:
        tag = CN_COMPANY_NAMES[cn_name]
        colors = COMPANY_HIGHLIGHT_COLORS.get(tag)
        if not colors:
            continue
        color, bg = colors
        replacement = f'<span style="color:{color};font-weight:600;">{cn_name}</span>'
        result = result.replace(cn_name, replacement)

    return result

def batch_translate(news_list: list[dict]) -> None:
    """批量翻译新闻标题（修改传入的 news_list）"""
    if TRANSLATOR is None:
        for item in news_list:
            item["title_cn"] = ""
        return

    # 加载磁盘缓存
    _load_translation_cache()

    total = len(news_list)
    success_count = 0
    new_translations = 0
    for i, item in enumerate(news_list):
        title = item["title"]
        was_cached = title in _translation_cache
        cn = translate_title(title)
        item["title_cn"] = cn
        if cn:
            success_count += 1
            if not was_cached:
                new_translations += 1
        # 限速：每 5 条暂停 0.5 秒，避免触发 Google 反爬
        if (i + 1) % 5 == 0:
            time.sleep(0.5)
        if (i + 1) % 20 == 0:
            print(f"    翻译进度: {i+1}/{total} (成功: {success_count}, 新增: {new_translations})")

    # 保存磁盘缓存
    _save_translation_cache()
    print(f"    翻译完成: {total} 条, 成功: {success_count}, 新增翻译: {new_translations}, 缓存总量: {len(_translation_cache)} 条")

# ═══════════════════════════════════════════════════════════════
#  报告生成 — Report Generation (简报风格)
# ═══════════════════════════════════════════════════════════════

def format_time(dt: datetime) -> str:
    """格式化为北京时间"""
    bj_time = dt.astimezone(timezone(timedelta(hours=8)))
    return bj_time.strftime("%m-%d %H:%M")

def extract_themes(items: list[dict], top_n: int = 5) -> list[str]:
    """从新闻标题中提取高频主题词"""
    theme_keywords = [
        ("earnings|财报|earnings report|Q\\d|quarterly", "财报季"),
        ("beat|beat.*estimate|beat.*expect|surpass", "业绩超预期"),
        ("miss|miss.*estimate|below.*expect|disappoint", "业绩不及预期"),
        ("upgrade|upgraded|raise.*target|bullish", "分析师看多"),
        ("downgrade|downgraded|cut.*target|bearish|selloff|sell-off", "分析师看空"),
        ("AI|artificial intelligence|artificial.intelligence", "AI人工智能"),
        ("chip|semiconductor|GPU|processor|foundry", "芯片/半导体"),
        ("cloud|cloud.*infrastructure|cloud.*computing", "云计算"),
        ("revenue.*surge|revenue.*growth|revenue.*jump|record.*revenue", "收入激增"),
        ("backlog|pipeline|contract|deal|partnership", "订单/合作"),
        ("regulation|regulatory|probe|investigation|antitrust|DOJ|FTC", "监管风险"),
        ("layoff|job.*cut|workforce.*reduc", "裁员"),
        ("tariff|trade.*war|export.*control|sanction|chip.*ban", "贸易/制裁"),
        ("Fed|rate.*cut|rate.*hike|monetary|inflation", "美联储/利率"),
        ("rally|surge|soar|jump|record.*high", "股价上涨"),
        ("drop|fall|plunge|crash|decline|sink", "股价下跌"),
        ("Tesla|Musk|Elon", "特斯拉/马斯克"),
        ("Nvidia|NVDA|Jensen.*Huang", "英伟达"),
        ("Broadcom|AVGO|Hock.*Tan", "博通"),
        ("Oracle|ORCL|Ellison", "甲骨文"),
        ("Palantir|PLTR", "Palantir"),
        ("Super.*Micro|SMCI", "超微电脑"),
        ("Microsoft|MSFT", "微软"),
        ("robot|robotics|autonomous|self.driving|FSD", "机器人/自动驾驶"),
        ("data.*center|server|infrastructure", "数据中心"),
        ("ETF|index.*fund|S&P 500|VOO|SPY", "指数基金"),
    ]

    all_text = " ".join(item["title"] for item in items).lower()
    themes = []
    for pattern, label in theme_keywords:
        if re.search(pattern, all_text, re.IGNORECASE):
            themes.append(label)
    return themes[:top_n]


# ═══════════════════════════════════════════════════════════════
#  天气 + 时区 + 心灵鸡汤
# ═══════════════════════════════════════════════════════════════

def fetch_weather(city: str, city_cn: str) -> dict:
    """通过 wttr.in 获取天气（免费，无需 API key）"""
    try:
        import urllib.request
        url = f"https://wttr.in/{city}?format=j1"
        req = urllib.request.Request(url, headers={"User-Agent": "curl/7.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
        current = data.get("current_condition", [{}])[0]
        return {
            "city": city_cn,
            "temp_c": current.get("temp_C", "?"),
            "weather_desc": current.get("weatherDesc", [{}])[0].get("value", "?"),
            "weather_code": current.get("weatherCode", "?"),
            "humidity": current.get("humidity", "?"),
            "wind_kmh": current.get("windspeedKmph", "?"),
        }
    except Exception as e:
        return {"city": city_cn, "temp_c": "?", "weather_desc": "?", "weather_code": "?", "humidity": "?", "wind_kmh": "?", "error": str(e)}

def weather_soup(weather_list: list[dict]) -> str:
    """根据天气生成心灵鸡汤"""
    # 综合判断：优先看天气代码
    codes = [w.get("weather_code", "?") for w in weather_list]
    temps = []
    for w in weather_list:
        try:
            temps.append(int(w.get("temp_c", 15)))
        except (ValueError, TypeError):
            temps.append(15)
    avg_temp = sum(temps) / len(temps) if temps else 15

    # 天气代码: 113=晴, 116/119/122=多云, 176~=雨, 179~=雪, 200~=雷
    has_rain = any(str(c) in ["176", "179", "182", "185", "200", "227", "230", "248", "260", "263", "266", "281", "284", "293", "296", "299", "302", "305", "308", "311", "314", "317", "320", "323", "326", "329", "332", "335", "338", "341", "344", "347", "350", "353", "356", "359", "362", "365", "368", "371", "374", "377", "386", "389", "392", "395"] for c in codes)
    has_sun = any(str(c) == "113" for c in codes)
    has_cloud = any(str(c) in ["116", "119", "122"] for c in codes)

    if has_sun and avg_temp >= 20:
        return "☀️ 德国阳光正好，莱茵河畔元气满满。投资如天气，阴晴圆缺皆常态，守得云开见月明。"
    elif has_sun:
        return "🌤️ 德国晴空万里，虽带凉意却明朗清澈。市场短期是投票机，长期是称重机——好公司终会发光。"
    elif has_rain:
        return "🌧️ 法兰克福的雨冲刷不掉你的坚持。市场也会有阴雨天，每一次回调都是为下一次上涨蓄力。"
    elif has_cloud:
        return "☁️ 云层之上，阳光从未缺席。短期波动如同云层，遮不住长期向上的趋势。"
    elif avg_temp >= 25:
        return "🔥 德国今天热情似火。别让市场的狂热冲昏头脑——别人贪婪时恐惧，别人恐惧时贪婪。"
    elif avg_temp <= 5:
        return "❄️ 杜塞尔多夫的寒风提醒我们：熊市如冬，但冬天来了，春天还会远吗？坚持定投，静待花开。"
    else:
        return "📈 每一天都是新的开始。市场无法预测，但纪律可以坚守。慢慢变富，来日方长。"

def get_germany_weather() -> tuple[list[dict], str]:
    """获取法兰克福和杜塞尔多夫天气，返回 (天气列表, 鸡汤)"""
    cities = [
        ("Frankfurt", "法兰克福"),
        ("Duesseldorf", "杜塞尔多夫"),
    ]
    weather = []
    for city, cn in cities:
        w = fetch_weather(city, cn)
        weather.append(w)
        desc = w.get("weather_desc", "?")
        temp = w.get("temp_c", "?")
        print(f"    天气 {cn}: {temp}°C, {desc}")

    soup = weather_soup(weather)
    return weather, soup


def generate_briefing(news_list: list[dict]) -> dict:
    """生成简报数据：每个持仓组合的综合评估"""
    # 按投资组合分组
    portfolio_news = defaultdict(list)
    for item in news_list:
        ticker = item["ticker"]
        for pf_name, pf_info in PORTFOLIOS.items():
            if ticker in pf_info["tickers"]:
                portfolio_news[pf_name].append(item)

    # 按 ticker 分组
    ticker_news = defaultdict(list)
    for item in news_list:
        ticker_news[item["ticker"]].append(item)

    briefing = {}
    for pf_name, pf_info in PORTFOLIOS.items():
        items = portfolio_news.get(pf_name, [])
        if not items:
            continue

        # 计算平均情感分
        scores = [n["sentiment"]["score"] for n in items]
        avg_score = sum(scores) / len(scores)

        # 提取主题
        themes = extract_themes(items, 6)

        # 挑最重要的新闻（按情感绝对值排序，每 ticker 最多 2 条）
        key_headlines = []
        seen_titles = set()
        for item in sorted(items, key=lambda x: abs(x["sentiment"]["score"]), reverse=True):
            if item["ticker"] not in seen_titles and len(key_headlines) < 4:
                seen_titles.add(item["ticker"])
            elif len(key_headlines) >= 4:
                break
            title_short = item["title"][:80]
            if title_short not in seen_titles:
                seen_titles.add(title_short)
                key_headlines.append(item)

        # 限制最多 5 条关键标题
        key_headlines = key_headlines[:5]

        # 确定信号
        if avg_score >= 1.5:
            signal, signal_color, signal_bg = "偏多", "#4caf50", "#0d3320"
        elif avg_score >= 0.3:
            signal, signal_color, signal_bg = "中性偏多", "#8bc34a", "#1a2e1a"
        elif avg_score > -0.3:
            signal, signal_color, signal_bg = "中性", "#ff9800", "#2e2a1a"
        elif avg_score > -1.5:
            signal, signal_color, signal_bg = "偏空", "#ff5722", "#331a10"
        else:
            signal, signal_color, signal_bg = "偏空", "#f44336", "#331010"

        # 各 ticker 的简短结论
        ticker_summaries = []
        for ticker in pf_info["tickers"]:
            t_items = ticker_news.get(ticker, [])
            if not t_items:
                continue
            t_avg = sum(n["sentiment"]["score"] for n in t_items) / len(t_items)
            t_bull = sum(1 for n in t_items if "利多" in n["sentiment"]["label"])
            t_bear = sum(1 for n in t_items if "利空" in n["sentiment"]["label"])
            ticker_summaries.append({
                "ticker": ticker,
                "name": COMPANY_NAMES.get(ticker, ticker),
                "avg_score": t_avg,
                "bullish_count": t_bull,
                "bearish_count": t_bear,
                "total": len(t_items),
            })

        briefing[pf_name] = {
            "info": pf_info,
            "avg_score": round(avg_score, 1),
            "signal": signal,
            "signal_color": signal_color,
            "signal_bg": signal_bg,
            "themes": themes,
            "key_headlines": key_headlines,
            "tickers": ticker_summaries,
            "total_news": len(items),
        }

    # 整体市场
    all_scores = [n["sentiment"]["score"] for n in news_list]
    market_score = sum(all_scores) / len(all_scores) if all_scores else 0

    return {
        "briefing": briefing,
        "market_score": round(market_score, 1),
        "total_news": len(news_list),
        "strong_bull": sum(1 for n in news_list if "强烈利多" in n["sentiment"]["label"]),
        "bull": sum(1 for n in news_list if n["sentiment"]["label"] == "🟢 利多"),
        "neutral": sum(1 for n in news_list if "中性" in n["sentiment"]["label"]),
        "bear": sum(1 for n in news_list if n["sentiment"]["label"] == "🔴 利空"),
        "strong_bear": sum(1 for n in news_list if "强烈利空" in n["sentiment"]["label"]),
    }


def generate_html_report(news_list: list[dict], weather: list[dict] = None, soup: str = "") -> str:
    """生成简报风格 HTML 邮件"""
    now = datetime.now(timezone.utc)
    bj_now = now.astimezone(timezone(timedelta(hours=8)))
    et_now = now.astimezone(timezone(timedelta(hours=-4)))
    de_now = now.astimezone(timezone(timedelta(hours=2)))  # CEST (夏季) / CET  +1 (冬季)

    data = generate_briefing(news_list)
    bf = data["briefing"]

    # ── 天气翻译映射 ──
    WEATHER_CN = {
        "Sunny": "晴", "Clear": "晴",
        "Partly cloudy": "多云", "Partly Cloudy": "多云", "Cloudy": "阴", "Overcast": "阴",
        "Mist": "薄雾", "Fog": "雾", "Freezing fog": "冻雾",
        "Light drizzle": "毛毛雨", "Drizzle": "毛毛雨",
        "Light rain": "小雨", "Moderate rain": "中雨", "Heavy rain": "大雨",
        "Light rain shower": "阵雨", "Moderate or heavy rain shower": "大阵雨",
        "Heavy Rain Shower": "大阵雨", "Torrential rain shower": "暴雨",
        "Light sleet": "雨夹雪", "Sleet": "雨夹雪",
        "Light snow": "小雪", "Moderate snow": "中雪", "Heavy snow": "大雪",
        "Patchy rain possible": "局地雨", "Patchy rain nearby": "局地雨",
        "Thunderstorm": "雷暴", "Heavy Rain With Thunderstorm": "雷暴雨",
        "Light snow showers": "阵雪",
        "Blizzard": "暴风雪",
        "Blowing snow": "吹雪",
    }

    def _weather_cn(desc: str) -> str:
        for en, cn in WEATHER_CN.items():
            if en.lower() in desc.lower():
                return cn
        return desc

    # ── 天气行 ──
    weather_html = ""
    if weather:
        weather_parts = []
        for w in weather:
            icon_map = {"113": "☀️", "116": "⛅", "119": "☁️", "122": "☁️", "176": "🌦️", "179": "🌧️", "200": "⛈️"}
            icon = icon_map.get(str(w.get("weather_code", "")), "🌡️")
            desc_cn = _weather_cn(w.get("weather_desc", ""))
            weather_parts.append(
                f'{icon} {w["city"]} {w["temp_c"]}°C {desc_cn}'
            )
        weather_line = "  ·  ".join(weather_parts)
        soup_line = f'<div style="color:#c0a060;font-size:12px;margin-top:4px;font-style:italic;">{soup}</div>' if soup else ""
        weather_html = f"""
        <div style="background:#1a1f2e;border-radius:8px;padding:10px 16px;margin-bottom:14px;text-align:center;">
          <div style="color:#a0b0c0;font-size:13px;">{weather_line}</div>
          {soup_line}
        </div>"""

    # ── 整体市场判断 ──
    ms = data["market_score"]
    if ms >= 1.0:
        market_mood = "整体偏乐观"
        market_color = "#4caf50"
    elif ms >= -0.5:
        market_mood = "整体中性"
        market_color = "#ff9800"
    else:
        market_mood = "整体需谨慎"
        market_color = "#f44336"
    market_badge = f'<span style="background:{market_color}22;color:{market_color};padding:2px 10px;border-radius:10px;font-weight:bold;">{market_mood}</span>'

    # ── 渲染单个持仓组合卡片 ──
    def render_briefing_card(pf_name: str, b: dict) -> str:
        # Ticker 标签行
        ticker_tags = "".join(
            f"""<span style="display:inline-block;background:#1a1a2e;padding:4px 10px;margin:2px;
            border-radius:4px;font-size:13px;">
            {t['ticker']} <span style="color:{'#4caf50' if t['avg_score']>0 else '#f44336' if t['avg_score']<0 else '#888'};">
            {t['avg_score']:+.1f} ({t['bullish_count']}多{t['bearish_count']}空/{t['total']}条)</span></span>"""
            for t in b["tickers"]
        )

        # 关键标题（最多 3 条）
        headlines_html = ""
        if b["key_headlines"]:
            headlines_html = '<div style="margin-top:10px;">'
            for h in b["key_headlines"][:3]:
                s = h["sentiment"]
                sc = "#4caf50" if s["score"] > 0 else ("#f44336" if s["score"] < 0 else "#888")
                url = h.get("url", "")

                # 中文翻译 + 公司名高亮
                title_cn = highlight_companies(h.get("title_cn", "")) if h.get("title_cn") else ""
                # 英文原文 + 公司名高亮
                title_en = highlight_companies(h["title"][:120])

                title_html = ""
                if url:
                    if title_cn:
                        title_html += f'<a href="{url}" style="color:#e0e0e0;text-decoration:none;font-weight:500;">{title_cn}</a>'
                        title_html += f' <span style="color:#666;font-size:11px;">|</span> '
                    title_html += f'<a href="{url}" style="color:#888;text-decoration:none;font-size:11px;">{title_en}</a>'
                else:
                    if title_cn:
                        title_html += f'<span style="color:#e0e0e0;font-weight:500;">{title_cn}</span>'
                        title_html += f' <span style="color:#666;font-size:11px;">|</span> '
                    title_html += f'<span style="color:#888;font-size:11px;">{title_en}</span>'

                headlines_html += f"""
                <div style="padding:5px 0;border-bottom:1px solid #1a1a2e;line-height:1.5;">
                  <span style="color:{sc};margin-right:4px;font-size:12px;">{s['label']}</span>
                  {title_html}
                  <span style="color:#555;font-size:11px;">— {h['provider'][:25]}</span>
                </div>"""
            headlines_html += "</div>"

        # 主题标签
        theme_tags = "".join(
            f'<span style="display:inline-block;background:#1f2937;color:#9ca3af;padding:2px 8px;margin:2px;border-radius:3px;font-size:11px;">{t}</span>'
            for t in b["themes"]
        )

        return f"""
        <div style="background:#161b22;border:1px solid #30363d;border-radius:10px;padding:18px;margin-bottom:16px;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
            <h3 style="color:#e0e0e0;margin:0;font-size:16px;">
              {b['info']['emoji']} {pf_name}
            </h3>
            <span style="background:{b['signal_bg']};color:{b['signal_color']};padding:4px 14px;border-radius:12px;font-weight:bold;font-size:14px;">
              {b['signal']} {b['avg_score']:+.1f}
            </span>
          </div>
          <div style="margin-bottom:8px;">{ticker_tags}</div>
          <div style="margin-bottom:8px;">{theme_tags}</div>
          {headlines_html}
        </div>"""

    # ── 组装 HTML ──
    portfolio_cards = []
    for pf_name in ["铁三角 (NVDA+MSFT+ORCL)", "窜天猴 (PLTR+SMCI+TSLA)", "DCA 均衡型 (SPY+NVDA+AVGO)"]:
        if pf_name in bf:
            portfolio_cards.append(render_briefing_card(pf_name, bf[pf_name]))

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="utf-8"></head>
<body style="background:#0d1117;color:#c9d1d9;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:20px;max-width:700px;margin:0 auto;">

  <!-- 标题 -->
  <div style="text-align:center;padding:15px 0;border-bottom:1px solid #30363d;margin-bottom:18px;">
    <h1 style="color:#58a6ff;margin:0;font-size:22px;">盘前简报</h1>
    <p style="color:#8b949e;margin:4px 0 0 0;font-size:13px;">
      德国时间 {de_now.strftime('%Y-%m-%d %H:%M')} | 北京时间 {bj_now.strftime('%Y-%m-%d %H:%M')} | 美东时间 {et_now.strftime('%Y-%m-%d %H:%M')} | {market_badge}
    </p>
  </div>

  <!-- 德国天气 + 鸡汤 -->
  {weather_html}

  <!-- 概览数字 -->
  <div style="display:flex;justify-content:center;gap:14px;margin-bottom:18px;flex-wrap:wrap;">
    <div style="text-align:center;min-width:60px;">
      <div style="font-size:26px;font-weight:bold;color:#58a6ff;">{data['total_news']}</div>
      <div style="font-size:11px;color:#888;">条新闻</div>
    </div>
    <div style="text-align:center;min-width:60px;">
      <div style="font-size:26px;font-weight:bold;color:#4caf50;">{data['strong_bull'] + data['bull']}</div>
      <div style="font-size:11px;color:#888;">利多</div>
    </div>
    <div style="text-align:center;min-width:60px;">
      <div style="font-size:26px;font-weight:bold;color:#f44336;">{data['strong_bear'] + data['bear']}</div>
      <div style="font-size:11px;color:#888;">利空</div>
    </div>
    <div style="text-align:center;min-width:60px;">
      <div style="font-size:26px;font-weight:bold;color:{market_color};">{data['market_score']:+.1f}</div>
      <div style="font-size:11px;color:#888;">综合评分</div>
    </div>
  </div>

  <!-- 组合卡片 -->
  {"".join(portfolio_cards)}

  <!-- 页脚 -->
  <div style="margin-top:20px;padding:12px;border-top:1px solid #30363d;font-size:11px;color:#555;text-align:center;">
    来源: Yahoo Finance + Google News RSS | 情感分析基于关键词 | 仅供参考不构成投资建议<br>
    {bj_now.strftime('%Y-%m-%d %H:%M:%S')} CST
  </div>

</body>
</html>"""

    return html


# ═══════════════════════════════════════════════════════════════
#  邮件发送 — Email Sending
# ═══════════════════════════════════════════════════════════════

def send_email(html_content: str, dry_run: bool = False):
    """通过 Gmail SMTP 发送邮件报告"""
    bj_now = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))
    subject = f"📊 盘前新闻扫描 — {bj_now.strftime('%Y-%m-%d')}"

    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL
    msg["To"] = EMAIL  # 发送给自己
    msg["Subject"] = subject

    # 纯文本回退
    text_fallback = f"盘前新闻扫描报告\n{bj_now.strftime('%Y-%m-%d %H:%M')} CST\n请用 HTML 邮件客户端查看完整报告。"
    msg.attach(MIMEText(text_fallback, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    if dry_run:
        print("\n[Dry-run] 邮件内容已生成，不发送。")
        # 保存到文件
        report_path = DATA_DIR / f"report_{bj_now.strftime('%Y%m%d_%H%M')}.html"
        report_path.write_text(html_content, encoding="utf-8")
        print(f"  报告已保存到: {report_path}")
        return True

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(EMAIL, APP_PASSWORD)
            server.sendmail(EMAIL, EMAIL, msg.as_string())
        print(f"✅ 邮件已发送至 {EMAIL}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP 认证失败！请检查 account.txt 中的应用专用密码。")
        print("   确保 Gmail 已开启两步验证，并使用「邮件」应用专用密码。")
        return False
    except Exception as e:
        print(f"❌ 发送邮件失败: {e}")
        return False


# ═══════════════════════════════════════════════════════════════
#  数据持久化
# ═══════════════════════════════════════════════════════════════

def save_news_data(news_list: list[dict]):
    """保存新闻数据到 JSON（用于历史回溯）"""
    bj_now = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))
    date_str = bj_now.strftime("%Y%m%d")

    # 精简数据结构用于存储
    slim_data = []
    for item in news_list:
        slim_data.append({
            "ticker": item["ticker"],
            "title": item["title"],
            "title_cn": item.get("title_cn", ""),
            "summary": item["summary"][:300],
            "url": item["url"],
            "provider": item["provider"],
            "pub_date": item["pub_date"].isoformat(),
            "source": item["source"],
            "sentiment": item["sentiment"],
        })

    data_path = DATA_DIR / f"news_{date_str}.json"
    data_path.write_text(json.dumps(slim_data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"📁 新闻数据已保存: {data_path} ({len(slim_data)} 条)")


# ═══════════════════════════════════════════════════════════════
#  主流程
# ═══════════════════════════════════════════════════════════════

def main():
    dry_run = "--dry-run" in sys.argv
    save_output = "--output" in sys.argv or dry_run

    print("=" * 60)
    print("  每日盘前新闻扫描器 — Pre-Market News Scanner")
    print(f"  启动时间: {datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')} CST")
    print(f"  覆盖标的: {', '.join(ALL_TICKERS)}")
    print(f"  模式: {'Dry-run (仅生成)' if dry_run else '正式 (发送邮件)'}")
    print("=" * 60)

    # 1. 搜索新闻
    print("\n🔍 正在搜索新闻...")
    news_list = fetch_all_news()
    print(f"\n📊 共获取 {len(news_list)} 条去重新闻")

    if not news_list:
        print("⚠️ 未获取到任何新闻，退出。")
        return

    # 2. 统计
    sentiment_counts = defaultdict(int)
    for item in news_list:
        sentiment_counts[item["sentiment"]["label"]] += 1
    print("   情感分布:", dict(sentiment_counts))

    # 2.5. 获取德国天气
    print("\n🌤️  获取德国天气...")
    weather, soup = get_germany_weather()

    # 3. 生成报告
    print("\n📝 正在生成 HTML 报告...")
    html = generate_html_report(news_list, weather=weather, soup=soup)

    # 4. 保存数据
    save_news_data(news_list)

    # 5. 保存/发送报告
    if save_output or dry_run:
        bj_now = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))
        report_path = DATA_DIR / f"report_{bj_now.strftime('%Y%m%d_%H%M')}.html"
        report_path.write_text(html, encoding="utf-8")
        print(f"📁 HTML 报告已保存: {report_path}")

    if not dry_run:
        print("\n📧 正在发送邮件...")
        success = send_email(html)
        if success:
            print("\n✅ 完成！")
        else:
            print("\n⚠️ 邮件发送失败，报告已保存到 data/ 目录")
    else:
        print("\n✅ Dry-run 完成！")

    print("=" * 60)


if __name__ == "__main__":
    main()
