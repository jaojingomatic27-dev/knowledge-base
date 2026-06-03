# -*- coding: utf-8 -*-
"""
Deep scan all Gmail messages beyond the first 600.
Uses Gmail's X-GM-RAW search for category:promotions
and scans ALL folders including encoded labels.
"""
import imaplib
import email
from email.header import decode_header
from collections import defaultdict
import sys
import io
import re
import binascii

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EMAIL = "jaojingomatic27@googlemail.com"
PASSWORD = "bcsh vyll idmy csny"
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

AD_SUBJECT_KW = [
    "unsubscribe", "opt-out", "offer", "discount", "sale", "deal",
    "promo", "coupon", "voucher", r"%\s*off", "save", "shop now",
    "buy now", "limited time", "exclusive", "newsletter", "weekly",
    "monthly deal", "flash sale", "clearance", "final sale",
    "free shipping", "new arrivals", "just landed", "trending",
    "don't miss", "act now", "ending soon", "last chance",
    "member", "rewards", "cashback", "earn", "bonus",
    "subscribe", "subscription", "trial",
]

AD_SENDER_KW = [
    "noreply", "no-reply", "newsletter", "marketing", "mailer",
    "info@", "hello@", "team@", "support@", "contact@",
    "notifications", "alerts", "updates",
]

TRUSTED_DOMAINS = [
    "github.com", "google.com", "googlemail.com", "gmail.com",
    "microsoft.com", "apple.com", "amazon.com",
]
TRUSTED_SENDERS = ["github", "google", "notifications@"]


def decode_mime(val):
    if val is None:
        return ""
    parts = decode_header(val)
    res = []
    for data, charset in parts:
        if isinstance(data, bytes):
            try:
                res.append(data.decode(charset or "utf-8", errors="replace"))
            except Exception:
                res.append(data.decode("utf-8", errors="replace"))
        else:
            res.append(str(data))
    return "".join(res)


def decode_utf7(text):
    """Decode Gmail's modified UTF-7 folder names."""
    if not text:
        return text
    # Only decode if it contains &
    if '&' not in text:
        return text
    result = []
    i = 0
    while i < len(text):
        if text[i] == '&':
            end = text.find('-', i)
            if end == -1:
                result.append(text[i])
                i += 1
            else:
                b64 = text[i+1:end]
                if not b64:
                    result.append('&')
                else:
                    try:
                        # Modified UTF-7 uses + instead of / for base64
                        b64_std = b64.replace(',', '/')
                        # Add padding
                        padding = 4 - len(b64_std) % 4
                        if padding != 4:
                            b64_std += '=' * padding
                        decoded = binascii.a2b_base64(b64_std)
                        result.append(decoded.decode('utf-16-be', errors='replace'))
                    except Exception:
                        result.append(f'[{b64}]')
                i = end + 1
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)


def parse_sender(msg):
    sender = decode_mime(msg.get("From", ""))
    name, addr = "", ""
    if "<" in sender:
        name = sender.split("<")[0].strip().strip('"').strip("'")
        addr = sender.split("<")[1].split(">")[0].strip()
    else:
        addr = sender.strip()
        name = addr
    domain = addr.split("@")[1].lower() if "@" in addr else "unknown"
    return name, addr, domain


def is_ad(subject, sender_name, sender_addr, sender_domain):
    subj_lower = subject.lower()
    name_lower = sender_name.lower()
    domain_lower = sender_domain.lower()
    addr_lower = sender_addr.lower()
    for t in TRUSTED_DOMAINS:
        if t in domain_lower:
            return False
    for t in TRUSTED_SENDERS:
        if t in addr_lower:
            return False
    score = 0
    for kw in AD_SUBJECT_KW:
        if kw in subj_lower:
            score += 2
            break
    if any(kw in name_lower for kw in AD_SENDER_KW):
        score += 1
    if any(kw in domain_lower for kw in AD_SENDER_KW):
        score += 1
    if re.search(r'(un)?subscribe|opt[-\s]?out', subj_lower):
        score += 3
    return score >= 2


def fetch_headers_uid(mail, uids, label=""):
    """Fetch RFC822.HEADER for a list of UIDs. Returns [(uid, msg), ...]."""
    results = []
    chunk_size = 200
    for start in range(0, len(uids), chunk_size):
        chunk = uids[start:start+chunk_size]
        uids_str = ",".join(uid.decode() for uid in chunk)
        try:
            status, data = mail.uid("FETCH", uids_str, "(RFC822.HEADER)")
            if status != "OK":
                continue
            for i in range(0, len(data), 2):
                if i >= len(data):
                    break
                resp = data[i]
                if not isinstance(resp, tuple):
                    continue
                resp_text = resp[0].decode(errors="replace")
                m = re.search(r'UID\s+(\d+)', resp_text)
                if not m:
                    continue
                uid = m.group(1)
                try:
                    msg = email.message_from_bytes(resp[1])
                except Exception:
                    continue
                results.append((uid, msg))
        except Exception as e:
            print(f"    Fetch error: {e}")
        if len(uids) > 200:
            print(f"    {label} progress: {min(start+chunk_size, len(uids))}/{len(uids)}")
    return results


def scan_folder(mail, folder_name, search_criteria="ALL"):
    """Scan a folder and return ad emails."""
    all_ads = []
    try:
        status, _ = mail.select(folder_name)
        if status != "OK":
            print(f"  [SKIP] Cannot select: {folder_name}")
            return all_ads
    except Exception as e:
        print(f"  [SKIP] Cannot select {folder_name}: {e}")
        return all_ads

    # Search
    try:
        if search_criteria == "ALL":
            status, data = mail.uid("SEARCH", None, "ALL")
        else:
            status, data = mail.uid("SEARCH", None, "X-GM-RAW", search_criteria)
    except Exception:
        # Fall back to ALL if X-GM-RAW fails
        status, data = mail.uid("SEARCH", None, "ALL")

    if status != "OK":
        print(f"  [SKIP] Search failed for {folder_name}")
        return all_ads

    all_uids = data[0].split()
    total = len(all_uids)
    decoded = decode_utf7(folder_name)
    print(f"  {decoded}: {total} messages")

    if total == 0:
        return all_ads

    headers = fetch_headers_uid(mail, all_uids, label=decoded)
    print(f"  {decoded}: parsed {len(headers)} headers, classifying...")

    for uid, msg in headers:
        subject = decode_mime(msg.get("Subject", ""))
        name, addr, domain = parse_sender(msg)
        date = msg.get("Date", "")
        if is_ad(subject, name, addr, domain):
            all_ads.append({
                "uid": uid,
                "folder": folder_name,
                "sender_name": name or addr,
                "sender_addr": addr,
                "sender_domain": domain,
                "subject": subject,
                "date": date,
            })

    print(f"  {decoded}: found {len(all_ads)} ads")
    return all_ads


def main():
    print("=" * 70)
    print("Gmail Deep Ad Scanner — All Folders")
    print(f"Account: {EMAIL}")
    print("=" * 70)

    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)
    print("Connected.\n")

    # List all folders with decoded names
    print("[0] Folder map (UTF-7 decoded):")
    status, folder_list = mail.list()
    folders_raw = []
    for f in folder_list:
        raw = f.decode(errors="replace").split('"/" ')[-1].strip('"')
        decoded = decode_utf7(raw)
        folders_raw.append(raw)
        print(f"    {raw}")
        print(f"    -> {decoded}")
    print()

    # Determine which folders to scan
    # Focus on: INBOX, [Gmail]/All Mail, and custom labels
    to_scan = []
    skip = ["Trash", "Junk", "[Gmail]/&YkBnCZCuTvY-",  # Trash
            "[Gmail]/&XfJSIJZkkK5O9g-"]  # Spam

    for raw in folders_raw:
        if raw in skip:
            continue
        # Skip empty or separator
        if not raw.strip():
            continue
        to_scan.append(raw)

    print(f"\n[1] Will scan {len(to_scan)} folders: {[decode_utf7(f) for f in to_scan]}")
    print()

    all_ads = []
    for folder in to_scan:
        decoded = decode_utf7(folder)
        if decoded == "INBOX":
            print(f"\n--- {decoded} (scanning ALL, not just recent 600) ---")
        else:
            print(f"\n--- {decoded} ---")
        ads = scan_folder(mail, folder)
        all_ads.extend(ads)

    mail.logout()

    # Deduplicate by subject+sender combo
    seen = set()
    unique_ads = []
    for ad in all_ads:
        key = (ad["subject"].lower().strip(), ad["sender_addr"].lower())
        if key not in seen:
            seen.add(key)
            unique_ads.append(ad)
    dupes = len(all_ads) - len(unique_ads)
    if dupes > 0:
        print(f"\n[DEDUP] Removed {dupes} duplicates (same subject+sender across folders)")

    # Group by domain
    by_domain = defaultdict(list)
    for ad in unique_ads:
        by_domain[ad["sender_domain"]].append(ad)

    print("\n" + "=" * 70)
    print(f"TOTAL ADVERTISING EMAILS FOUND: {len(unique_ads)}")
    print(f"From {len(by_domain)} unique domains")
    print("=" * 70)

    # Categorize
    categories = defaultdict(list)
    for ad in unique_ads:
        d = ad["sender_domain"].lower()
        n = ad["sender_name"].lower()
        if any(kw in d for kw in ["amazon", "ebay", "aliexpress", "wish", "shopify", "etsy"]):
            cat = "Shopping Platforms"
        elif any(kw in d for kw in ["nike", "adidas", "zara", "hm", "uniqlo", "gap", "levi", "fashion", "clothing"]):
            cat = "Fashion/Clothing"
        elif any(kw in d for kw in ["apple", "samsung", "dell", "hp", "lenovo", "bestbuy", "newegg", "tech", "gadget"]):
            cat = "Electronics/Tech"
        elif any(kw in d for kw in ["uber", "lyft", "doordash", "grubhub", "food", "delivery", "restaurant", "pizza", "burger", "mcdonald", "starbucks"]):
            cat = "Food/Delivery"
        elif any(kw in d for kw in ["hotel", "booking", "expedia", "trip", "travel", "flight"]):
            cat = "Travel"
        elif any(kw in d for kw in ["bank", "credit", "insurance", "finance", "paypal", "venmo", "coinbase", "robinhood"]):
            cat = "Finance"
        elif any(kw in d or kw in n for kw in ["newsletter", "digest", "weekly", "daily", "blog", "medium", "substack"]):
            cat = "Newsletters/Blogs"
        elif any(kw in d for kw in ["game", "gaming", "steam", "epic", "nintendo", "playstation", "xbox"]):
            cat = "Gaming"
        elif any(kw in d for kw in ["course", "learn", "education", "udemy", "coursera", "skillshare"]):
            cat = "Education"
        elif any(kw in d for kw in ["health", "fitness", "gym", "vitamin", "supplement", "pharma"]):
            cat = "Health/Fitness"
        elif "noreply" in d or "no-reply" in d or "mailer" in d or "marketing" in d or "mailing" in d:
            cat = "Marketing/No-reply"
        elif any(kw in d for kw in ["social", "linkedin", "facebook", "twitter", "instagram", "tiktok"]):
            cat = "Social Media"
        elif any(kw in d for kw in ["reward", "bonus", "payback", "coupon", "point", "loyalty"]):
            cat = "Rewards/Loyalty"
        elif any(kw in d for kw in ["job", "stepstone", "indeed", "career", "recruit"]):
            cat = "Job/Recruitment"
        else:
            cat = "Other"
        categories[cat].append(ad)

    cat_order = [
        "Shopping Platforms", "Fashion/Clothing", "Electronics/Tech",
        "Food/Delivery", "Travel", "Finance", "Rewards/Loyalty",
        "Job/Recruitment", "Newsletters/Blogs", "Gaming", "Education",
        "Health/Fitness", "Social Media", "Marketing/No-reply", "Other"
    ]

    print("\n--- By Category ---\n")
    total_shown = 0
    for cat in cat_order:
        if cat not in categories:
            continue
        ads = categories[cat]
        total_shown += len(ads)
        doms = defaultdict(list)
        for a in ads:
            doms[a["sender_domain"]].append(a)
        print(f"\n[{cat}] {len(ads)} emails, {len(doms)} domains")
        for domain in sorted(doms.keys(), key=lambda d: len(doms[d]), reverse=True):
            dads = doms[domain]
            names = defaultdict(list)
            for a in dads:
                names[a["sender_name"]].append(a)
            for sname in sorted(names.keys(), key=lambda n: len(names[n]), reverse=True):
                nads = names[sname]
                print(f"  {len(nads):4d} {domain:45s} {sname[:55]}")
                for a in nads[:2]:
                    print(f"         {a['subject'][:85]}")
                if len(nads) > 2:
                    print(f"         ... +{len(nads)-2} more")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total ads found:    {len(unique_ads)}")
    print(f"  Unique domains:     {len(by_domain)}")
    print(f"  Categories:         {len(categories)}")
    print(f"  (Duplicates across folders removed: {dupes})")
    print("\nNo emails deleted. Review and confirm categories to delete.")


if __name__ == "__main__":
    main()
