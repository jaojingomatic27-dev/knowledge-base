#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2ndhand Auto-Pipeline
=====================
流程：input/ 照片 → bl omni 识别物品 → 生成报告 + 德语文案 + YAML → output/

输出：
  - output/items_report.md          # 中文鉴定报告
  - output/listing_<item_slug>_de.md # 德语上架文案
  - output/ad_<item_slug>.yaml       # kleinanzeigen-bot 可用的 YAML

依赖：
  - bl CLI (bailian-cli) 已安装并登录
  - Python 3.8+
"""

import subprocess
import json
import os
import sys
import glob as glob_mod
import re
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
PROJECT_ROOT = Path(r"C:\AI\cc\2ndhand")
INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"
DATA_DIR = PROJECT_ROOT / "data"
CODE_DIR = PROJECT_ROOT / "code"

# 德国时区 (CEST=UTC+2, CET=UTC+1 — 用 astimezone 自动处理)
TZ_DE = datetime.now().astimezone().tzinfo

# eBay 私人卖家声明（德语）
DISCLAIMER_DE = (
    "Es handelt sich um einen Privatverkauf. "
    "Ich übernehme keine Garantie und Rücknahme!!! "
    "Viel Spass beim Bieten!!!"
)

# ── 分类映射 (Kleinanzeigen Kategorie-Hierarchie) ─────
CATEGORY_GUESS = {
    "kopfhörer": "Elektronik & Nähmaschinen > Kopfhörer & Headsets",
    "earbuds": "Elektronik & Nähmaschinen > Kopfhörer & Headsets",
    "headphone": "Elektronik & Nähmaschinen > Kopfhörer & Headsets",
    "saugroboter": "Haushalt & Wohnen > Reinigung & Staubsauger > Saugroboter",
    "roomba": "Haushalt & Wohnen > Reinigung & Staubsauger > Saugroboter",
    "staubsauger": "Haushalt & Wohnen > Reinigung & Staubsauger > Staubsauger",
}

# ── 售价参考 (成色 → 折扣区间) ─────────────────────────
CONDITION_DISCOUNT = {
    "9": (0.55, 0.70),   # 9成新 → 原价55%-70%
    "8": (0.40, 0.55),
    "7": (0.30, 0.45),
    "6": (0.20, 0.35),
}


# ── 工具函数 ────────────────────────────────────────────
def run_bl(args: list, timeout: int = 120) -> dict:
    """运行 bl CLI 并返回 JSON 结果。"""
    cmd = ["bl"] + args + ["--output", "json", "--non-interactive"]
    print(f"  [CMD] bl {' '.join(args[:6])}{'...' if len(args) > 6 else ''}")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, encoding="utf-8")
        if r.returncode != 0:
            print(f"  [ERR] bl exit={r.returncode}: {r.stderr[:500]}")
            return {}
        # 有时输出可能包含多行 JSON，取最后一个有效 JSON 块
        out = r.stdout.strip()
        try:
            return json.loads(out)
        except json.JSONDecodeError:
            # 尝试提取 JSON 行
            for line in reversed(out.splitlines()):
                line = line.strip()
                if line.startswith("{"):
                    try:
                        return json.loads(line)
                    except json.JSONDecodeError:
                        continue
            print(f"  [WARN] Could not parse JSON, raw: {out[:300]}")
            return {"raw": out}
    except subprocess.TimeoutExpired:
        print(f"  [ERR] bl timeout after {timeout}s")
        return {}


def now_de() -> str:
    """德国本地时间 ISO 字符串。"""
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def slugify(text: str) -> str:
    """文本 → 文件安全名。"""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "_", text)
    return text[:50]


def guess_category(name_en: str, name_de: str) -> str:
    """根据物品名称猜测 Kleinanzeigen 分类。"""
    combined = f"{name_en} {name_de}".lower()
    for kw, cat in CATEGORY_GUESS.items():
        if kw in combined:
            return cat
    return "Sonstiges"


# ── 步骤 1: 照片分析 ──────────────────────────────────
def analyze_photos(image_paths: list) -> dict:
    """
    用 qwen-vl-max 分析照片，返回物品清单。
    """
    print("\n" + "="*60)
    print("📸 步骤1: 视觉分析照片")
    print("="*60)

    images = [str(p) for p in image_paths]
    if not images:
        print("❌ input/ 中没有照片！")
        return {}

    print(f"  共 {len(images)} 张照片:")
    for img in images:
        sz = os.path.getsize(img)
        print(f"    - {Path(img).name} ({sz/1024:.0f} KB)")

    # 构建 image 参数列表
    image_args = []
    for img in images:
        image_args += ["--image", img]

    prompt = (
        "你是一个二手物品鉴定专家。上面这些照片来自同一批要卖的东西。"
        "请仔细分析，完成以下任务：\n\n"
        "1. **物品识别与去重**：列出所有不同物品。不同角度的同一件物品算同一个。统计一共有几样。\n\n"
        "2. **每样物品的信息**：\n"
        "   - 英文名称/型号名（用于文件命名，如 lg_hbs_fn7）\n"
        "   - 简短中文描述、成色（几成新，0-10打分作为数字）\n"
        "   - 关键规格/性能要点（尽可能准确）\n"
        "   - 估计原价（新机时欧元价格）\n\n"
        "3. **建议售价**（欧元参，考德国eBay Kleinanzeigen行情）：合理售价区间。\n\n"
        "请用以下 JSON 格式回复（只输出 JSON，不要其他文字）：\n"
        "{\n"
        '  "item_count": 2,\n'
        '  "items": [\n'
        '    {\n'
        '      "name_zh": "物品中文名",\n'
        '      "name_en": "item_name_for_slug",\n'
        '      "condition": 8.5,\n'
        '      "condition_desc": "几成新及说明",\n'
        '      "specs": ["规格1", "规格2"],\n'
        '      "flaws": ["缺陷1（无则为空数组）"],\n'
        '      "highlights": ["卖点1", "卖点2"],\n'
        '      "includes": ["配件1", "配件2"],\n'
        '      "new_price_eur": 130,\n'
        '      "price_min_eur": 65,\n'
        '      "price_max_eur": 85\n'
        '    }\n'
        '  ]\n'
        "}\n"
    )

    result = run_bl(
        ["omni", "--text-only", "--model", "qwen3.5-omni-plus"]
        + image_args
        + ["--message", prompt],
        timeout=180
    )

    # 解析 JSON
    if "content" in result:
        raw = result["content"]
    elif "raw" in result:
        raw = result["raw"]
    else:
        print(f"  [ERR] Unexpected response: {json.dumps(result, ensure_ascii=False)[:500]}")
        return {}

    # 尝试提取 JSON
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # 提取 ```json ... ``` 块
        m = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw)
        if m:
            try:
                data = json.loads(m.group(1))
            except json.JSONDecodeError:
                print(f"  [ERR] JSON block parse failed")
                print(f"  [RAW] {raw[:800]}")
                return {}
        else:
            # 尝试找第一个 { 到最后一个 }
            m2 = re.search(r"\{[\s\S]*\}", raw)
            if m2:
                try:
                    data = json.loads(m2.group(0))
                except json.JSONDecodeError:
                    print(f"  [ERR] JSON extraction failed")
                    print(f"  [RAW] {raw[:800]}")
                    return {}
            else:
                print(f"  [ERR] No JSON found in response")
                print(f"  [RAW] {raw[:800]}")
                return {}

    print(f"\n  ✅ 识别出 {data.get('item_count', 0)} 样物品")
    for item in data.get("items", []):
        print(f"    - {item.get('name_zh', '?')} ({item.get('condition', '?')}/10)")
    return data


# ── 步骤 2: 生成德语上架文案 ───────────────────────────
def generate_german_listing(item: dict) -> str:
    """
    用 qwen-max 生成德语 Kleinanzeigen 文案。
    """
    print(f"\n  📝 生成德语文案: {item.get('name_zh', '?')}")
    name = item.get("name_zh", "")
    condition = item.get("condition", 8)
    condition_desc = item.get("condition_desc", "")
    highlights = item.get("highlights", [])
    flaws = item.get("flaws", [])
    includes = item.get("includes", [])
    specs = item.get("specs", [])
    price = item.get("price_min_eur", 0)
    new_price = item.get("new_price_eur", 0)

    hl_text = "\n".join(f"- {h}" for h in highlights) if highlights else "- 功能正常"
    fl_text = "\n".join(f"- {f}" for f in flaws) if flaws else "- 无明显缺陷"
    inc_text = "\n".join(f"- {i}" for i in includes) if includes else "- 主机本体"
    spec_text = "\n".join(f"- {s}" for s in specs) if specs else ""

    prompt = (
        f"你是经验丰富的德国 eBay Kleinanzeigen 卖家。为以下二手物品撰写德语上架文案。\n\n"
        f"**物品**：{name}\n"
        f"**成色**：{condition}/10 — {condition_desc}\n"
        f"**新机价**：约 €{new_price}\n\n"
        f"**卖点**：\n{hl_text}\n\n"
        f"**规格/性能**：\n{spec_text}\n\n"
        f"**缺陷（如有）**：\n{fl_text}\n\n"
        f"**包含配件**：\n{inc_text}\n\n"
        f"**定价**：€{price} VB\n\n"
        "**要求**：\n"
        "1. 标题格式：<品牌> <型号> <核心卖点关键词> | <亮点1> | <亮点2>\n"
        "2. 正文：友好问候 + 成色说明 + 功能卖点 + 包含配件 + 价格 + 物流说明\n"
        "3. 如物品有缺陷，诚实写明，但用积极语气（如建议换配件后如新）\n"
        "4. 文末必须一字不改加上这段声明：\n"
        f'"{DISCLAIMER_DE}"\n'
        "5. 德语地道、自然、友好，使用适当 Emoji\n"
        "6. 最终输出为完整文案（可直接复制粘贴到 Kleinanzeigen）"
    )

    result = run_bl(
        ["text", "chat", "--model", "qwen3.7-max", "--message", prompt],
        timeout=90
    )

    text = ""
    if "choices" in result:
        text = result["choices"][0]["message"].get("content", "")
    elif "content" in result:
        text = result["content"]
    elif "raw" in result:
        text = result["raw"]

    if not text:
        print(f"  [WARN] 德语文案生成失败，使用备用模板")
        text = f"**{name}**\n\n{condition_desc}\n\n{DISCLAIMER_DE}"

    # 确保声明存在
    if DISCLAIMER_DE not in text:
        text += f"\n\n{DISCLAIMER_DE}"

    return text.strip()


# ── 步骤 3: 生成 YAML ──────────────────────────────────
def generate_yaml(item: dict, listing_text: str, image_paths: list) -> dict:
    """
    根据物品信息 + 德语文案生成 kleinanzeigen-bot 兼容的 YAML 配置。
    返回 dict（后续用 yaml.dump 写出）。
    """
    name_en = item.get("name_en", "item")
    slug = slugify(name_en)
    name_de = item.get("name_zh", "")

    category = guess_category(name_en, name_de)

    # 提取标题（文案第一行或前 80 字符）
    title_line = listing_text.split("\n")[0].strip().strip("*").strip()
    if len(title_line) < 10:
        # 找 **Titel:** 后的行
        for i, line in enumerate(listing_text.split("\n")):
            if "titel" in line.lower() and ":" in line:
                title_line = listing_text.split("\n")[i + 1].strip().strip("*").strip()
                break
    if len(title_line) < 5:
        title_line = name_de

    # 成色映射
    cond = item.get("condition", 8)
    if cond >= 9:
        condition_s = "like_new"
    elif cond >= 7:
        condition_s = "ok"
    elif cond >= 5:
        condition_s = "alright"
    else:
        condition_s = "defect"

    # 图片 glob
    img_patterns = []
    for img in image_paths:
        img_name = Path(img).name
        # 拷贝图片到 output/images/ 下
        dest_dir = OUTPUT_DIR / "images"
        dest_dir.mkdir(exist_ok=True)
        dest = dest_dir / img_name
        if not dest.exists():
            shutil.copy2(img, dest)
        img_patterns.append(f"images/{img_name}")

    yaml_data = {
        "active": True,
        "type": "OFFER",
        "title": title_line[:80],  # 限制长度
        "description": listing_text,
        "category": category,
        "price": int(item.get("price_min_eur", 10)),
        "price_type": "NEGOTIABLE",
        "shipping_type": "SHIPPING",
        "shipping_costs": 4.99,
        "special_attributes": {
            "condition_s": condition_s,
        },
        "images": img_patterns,
        "republication_interval": 7,
    }

    return yaml_data


# ── 步骤 4: 生成中文报告 ───────────────────────────────
def generate_report(analysis: dict, listings: dict, yamls: dict) -> str:
    """生成完整的中文鉴定报告 (Markdown)。"""
    lines = [
        "# 二手物品鉴定报告",
        "",
        f"**分析日期**：{now_de()}",
        f"**来源照片**：{analysis.get('photo_count', 0)}张",
        f"**分析模型**：qwen3.5-omni-plus / qwen3.7-max",
        "",
        "---",
        "",
        f"## 物品清单（共{analysis.get('item_count', 0)}样）",
        "",
    ]

    for i, item in enumerate(analysis.get("items", []), 1):
        name = item.get("name_zh", f"物品{i}")
        name_en = item.get("name_en", f"item_{i}")
        cond = item.get("condition", "?")
        cond_desc = item.get("condition_desc", "")
        specs = item.get("specs", [])
        flaws = item.get("flaws", [])
        highlights = item.get("highlights", [])
        includes = item.get("includes", [])
        new_price = item.get("new_price_eur", "?")
        pmin = item.get("price_min_eur", "?")
        pmax = item.get("price_max_eur", "?")

        lines.append(f"### 物品{i}：{name}")
        lines.append("")
        lines.append(f"- **英文名/型号**：{name_en}")
        lines.append(f"- **成色**：{cond}/10 — {cond_desc}")
        lines.append(f"- **新机参考价**：€{new_price}")
        lines.append("")
        lines.append("**规格/性能要点**：")
        for s in specs:
            lines.append(f"  - {s}")
        lines.append("")
        lines.append("**卖点**：")
        for h in highlights:
            lines.append(f"  - {h}")
        if flaws:
            lines.append("")
            lines.append("**缺陷**：")
            for f in flaws:
                lines.append(f"  - {f}")
        lines.append("")
        lines.append("**包含配件**：")
        for inc in includes:
            lines.append(f"  - {inc}")
        lines.append("")
        lines.append(f"- **建议售价**：€{pmin} – €{pmax}")
        lines.append(f"- **上架定价**：€{pmin} VB")
        lines.append("")
        lines.append("---")
        lines.append("")

    # 输出文件索引
    lines.append("## 输出文件")
    lines.append("")
    lines.append("| 文件 | 说明 |")
    lines.append("|------|------|")
    lines.append(f"| `items_report.md` | 本报告 |")
    for slug in listings:
        lines.append(f"| `listing_{slug}_de.md` | 德语上架文案 |")
    for slug in yamls:
        lines.append(f"| `ad_{slug}.yaml` | kleinanzeigen-bot YAML |")
    lines.append("")
    lines.append("## 免责声明")
    lines.append("")
    lines.append(f"> {DISCLAIMER_DE}")

    return "\n".join(lines)


# ── 主流程 ────────────────────────────────────────────
def main():
    print("="*60)
    print("🔄 2ndhand Auto-Pipeline 启动")
    print(f"   时间: {now_de()}")
    print("="*60)

    # 确保目录存在
    for d in [INPUT_DIR, OUTPUT_DIR, DATA_DIR, CODE_DIR]:
        d.mkdir(exist_ok=True)

    # 收集照片
    img_exts = ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.bmp")
    image_paths = []
    for ext in img_exts:
        image_paths.extend(glob_mod.glob(str(INPUT_DIR / ext)))
        image_paths.extend(glob_mod.glob(str(INPUT_DIR / ext.upper())))
    # 去重排序
    image_paths = sorted(set(str(p) for p in image_paths))

    if not image_paths:
        print("❌ input/ 中没有照片。请放入照片后重试。")
        print(f"   支持的格式: {', '.join(img_exts)}")
        return 1

    # ── 步骤1: 视觉分析 ──
    analysis = analyze_photos(image_paths)
    if not analysis or not analysis.get("items"):
        print("❌ 未能从照片中识别出物品。")
        return 1

    analysis["photo_count"] = len(image_paths)

    # ── 步骤2+3: 并行处理每样物品 ──
    listings = {}
    yamls = {}

    for i, item in enumerate(analysis.get("items", [])):
        print(f"\n{'─'*60}")
        print(f"📦 处理物品 {i+1}/{analysis['item_count']}: {item.get('name_zh', '?')}")
        print(f"{'─'*60}")

        slug = slugify(item.get("name_en", f"item_{i+1}"))

        # 2a: 德语文案
        listing_text = generate_german_listing(item)

        listing_md = f"# {item.get('name_zh', '物品')} — eBay Kleinanzeigen 德语上架文案\n\n"
        listing_md += f"---\n\n{listing_text}\n"

        listing_path = OUTPUT_DIR / f"listing_{slug}_de.md"
        listing_path.write_text(listing_md, encoding="utf-8")
        print(f"  💾 文案已保存: {listing_path.name}")
        listings[slug] = True

        # 2b: YAML
        yaml_data = generate_yaml(item, listing_text, image_paths)
        yaml_path = OUTPUT_DIR / f"ad_{slug}.yaml"
        yaml_text = yaml_dump_pretty(yaml_data)
        yaml_path.write_text(yaml_text, encoding="utf-8")
        print(f"  💾 YAML 已保存: {yaml_path.name}")
        yamls[slug] = yaml_data

    # ── 步骤4: 生成报告 ──
    print(f"\n{'─'*60}")
    print("📋 生成中文鉴定报告")
    report = generate_report(analysis, listings, yamls)
    report_path = OUTPUT_DIR / "items_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"  💾 报告已保存: {report_path.name}")

    # ── 打印摘要 ──
    print("\n" + "="*60)
    print("✅ 全部完成！")
    print("="*60)
    print(f"\n📁 输出目录: {OUTPUT_DIR}")
    print(f"\n📊 识别物品: {analysis['item_count']} 样")
    for i, item in enumerate(analysis.get("items", []), 1):
        slug = slugify(item.get("name_en", f"item_{i}"))
        print(f"  {i}. {item.get('name_zh', '?')}")
        print(f"     文案: output/listing_{slug}_de.md")
        print(f"     YAML: output/ad_{slug}.yaml")
        print(f"     售价: €{item.get('price_min_eur', '?')} – €{item.get('price_max_eur', '?')}")

    print(f"\n📋 下一步: 用 kleinanzeigen-bot 上架")
    print(f"   kleinanzeigen-bot publish --ads=output/ad_*.yaml")
    print()

    return 0


def yaml_dump_pretty(data: dict) -> str:
    """Pretty-print YAML without external dependency."""
    lines = []
    for key, value in data.items():
        lines.append(f"{key}: {yaml_value(value, 0)}")
    return "\n".join(lines) + "\n"


def yaml_value(val, indent: int) -> str:
    """递归格式化 YAML 值。"""
    pad = "  " * indent
    if isinstance(val, bool):
        return "true" if val else "false"
    elif isinstance(val, (int, float)):
        if isinstance(val, float) and val == int(val):
            return str(int(val))
        return str(val)
    elif isinstance(val, str):
        # 多行文本用 | 块
        if "\n" in val:
            lines = val.strip().split("\n")
            result = "|\n"
            for line in lines:
                result += f"{pad}  {line}\n"
            return result.rstrip("\n")
        # 包含特殊字符引号
        if any(c in val for c in [":", "#", "{", "}", "[", "]", ",", "&", "*", "?", "|", "-", "<", ">", "=", "!", "%", "@", "`", "'", '"']):
            return f"'{val}'"
        return val
    elif isinstance(val, list):
        if not val:
            return "[]"
        # 检查元素是否有复杂类型
        if any(isinstance(v, (dict, list)) for v in val):
            result = "\n"
            for v in val:
                result += f"{pad}  - {yaml_value(v, indent + 1).lstrip()}\n"
            return result.rstrip("\n")
        else:
            result = "\n"
            for v in val:
                result += f"{pad}  - {yaml_value(v, indent + 1)}\n"
            return result.rstrip("\n")
    elif isinstance(val, dict):
        if not val:
            return "{}"
        result = "\n"
        for k, v in val.items():
            vstr = yaml_value(v, indent + 1)
            if vstr.startswith("\n"):
                result += f"{pad}  {k}:{vstr}\n"
            else:
                result += f"{pad}  {k}: {vstr}\n"
        return result.rstrip("\n")
    else:
        return str(val)


if __name__ == "__main__":
    sys.exit(main())
