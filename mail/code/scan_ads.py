# -*- coding: utf-8 -*-
"""
Scan Gmail for advertising emails. Classify by sender.
Read-only — no deletion without user confirmation.
"""
import imaplib
import email
from email.header import decode_header
from collections import defaultdict
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EMAIL = "jaojingomatic27@googlemail.com"
PASSWORD = "bcsh vyll idmy csny"
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

# Heuristic keywords for advertising emails (case-insensitive)
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

TRUSTED_SENDERS = [
    "github", "google", "notifications@",
]


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


def score_ad(subject, sender_name, sender_addr, sender_domain):
    """Return (is_likely_ad: bool, confidence: int, reason: str)"""
    confidence = 0
    reasons = []

    subj_lower = subject.lower()
    name_lower = sender_name.lower()
    domain_lower = sender_domain.lower()
    addr_lower = sender_addr.lower()

    # Check trusted senders first
    for trusted in TRUSTED_DOMAINS:
        if trusted in domain_lower:
            return False, 0, "trusted domain"
    for trusted in TRUSTED_SENDERS:
        if trusted in addr_lower:
            return False, 0, "trusted sender"

    # Subject keywords
    for kw in AD_SUBJECT_KW:
        if kw in subj_lower:
            confidence += 2
            reasons.append(f"subject:'{kw}'")
            break  # one match is enough

    # Sender name patterns
    if any(kw in name_lower for kw in AD_SENDER_KW):
        confidence += 1
        reasons.append("sender:noreply/info")

    # Domain patterns
    if any(kw in domain_lower for kw in AD_SENDER_KW):
        confidence += 1
        reasons.append("domain:marketing")

    # Check for unsubscribe link pattern in subject
    if re.search(r'(un)?subscribe|opt[-\s]?out', subj_lower):
        confidence += 3
        reasons.append("unsubscribe")

    # Very short subjects from commercial domains often = ads
    if len(subject) < 5 and domain_lower not in TRUSTED_DOMAINS:
        confidence += 1
        reasons.append("short_subject")

    is_ad = confidence >= 2
    return is_ad, confidence, "+".join(reasons) if reasons else "none"


def fetch_all_headers(mail, folder):
    """Fetch all email headers from a folder. Returns list of (uid, msg)."""
    results = []
    try:
        status, _ = mail.select(folder)
        if status != "OK":
            print(f"  Cannot select {folder}")
            return results
    except Exception:
        print(f"  Cannot select {folder}")
        return results

    status, data = mail.search(None, "ALL")
    if status != "OK":
        print(f"  Search failed for {folder}")
        return results

    msg_ids = data[0].split()
    total = len(msg_ids)
    print(f"  {total} messages in {folder}")

    if total == 0:
        return results

    # Limit to 600 most recent
    if total > 600:
        msg_ids = msg_ids[-600:]
        print(f"  Scanning most recent 600...")

    # Fetch in chunks of 200 for speed
    chunk_size = 200
    for start in range(0, len(msg_ids), chunk_size):
        chunk = msg_ids[start:start+chunk_size]
        # Build fetch command: msg_id1,msg_id2,...
        ids_str = ",".join(mid.decode() for mid in chunk)
        try:
            status, data = mail.fetch(ids_str, "(RFC822.HEADER UID)")
            if status != "OK":
                continue

            # Parse multi-message response
            for item in data:
                if not isinstance(item, tuple):
                    continue
                header_text = item[0].decode(errors="replace")
                body = item[1]
                uid = None
                for line in header_text.split("\r\n"):
                    # line format: "... (UID 12345)"
                    m = re.search(r'UID\s+(\d+)', line)
                    if m:
                        uid = m.group(1)
                        break
                try:
                    msg = email.message_from_bytes(body)
                except Exception:
                    continue
                results.append((uid, msg))
        except Exception as e:
            print(f"  Batch fetch error: {e}")
        print(f"  Progress: {min(start+chunk_size, len(msg_ids))}/{len(msg_ids)}")

    return results


def main():
    print("=" * 70)
    print("Gmail Advertising Email Scanner")
    print(f"Account: {EMAIL}")
    print("=" * 70)

    # Connect
    print("\n[1/4] Connecting...")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)
    print("  Connected.")

    # Scan folders
    print("\n[2/4] Scanning folders...")
    all_ads = []

    # Always scan INBOX
    print("\n  --- INBOX ---")
    headers = fetch_all_headers(mail, "INBOX")
    print(f"  Parsing {len(headers)} headers...")

    for uid, msg in headers:
        subject = decode_mime(msg.get("Subject", ""))
        name, addr, domain = parse_sender(msg)
        date = msg.get("Date", "")
        is_ad, confidence, reason = score_ad(subject, name, addr, domain)
        if is_ad:
            all_ads.append({
                "uid": uid,
                "folder": "INBOX",
                "sender_name": name or addr,
                "sender_addr": addr,
                "sender_domain": domain,
                "subject": subject,
                "date": date,
                "confidence": confidence,
                "reason": reason,
            })

    mail.logout()

    # Group and display
    print("\n[3/4] Classifying...")

    # Group by sender domain
    by_domain = defaultdict(list)
    for ad in all_ads:
        by_domain[ad["sender_domain"]].append(ad)

    print("\n" + "=" * 70)
    print(f"ADVERTISING EMAILS FOUND: {len(all_ads)}")
    print(f"From {len(by_domain)} different domains")
    print("=" * 70)

    # Category groups for easier decision-making
    categories = defaultdict(list)
    for ad in all_ads:
        domain = ad["sender_domain"]
        name = ad["sender_name"]
        # Classify into categories
        d = domain.lower()
        n = name.lower()

        if any(kw in d for kw in ["amazon", "ebay", "aliexpress", "wish", "shopify", "etsy"]):
            cat = "Shopping Platforms"
        elif any(kw in d for kw in ["nike", "adidas", "zara", "hm", "uniqlo", "gap", "levi", "fashion", "clothing"]):
            cat = "Fashion/Clothing"
        elif any(kw in d for kw in ["apple", "samsung", "dell", "hp", "lenovo", "bestbuy", "newegg", "tech", "gadget"]):
            cat = "Electronics/Tech"
        elif any(kw in d for kw in ["uber", "lyft", "doordash", "grubhub", "food", "delivery", "restaurant", "pizza", "mcdonald", "starbucks"]):
            cat = "Food/Delivery"
        elif any(kw in d for kw in ["airline", "hotel", "booking", "expedia", "trip", "travel", "flight"]):
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
        elif "noreply" in d or "no-reply" in d:
            cat = "Automated/No-reply"
        elif any(kw in d for kw in ["social", "linkedin", "facebook", "twitter", "instagram", "tiktok"]):
            cat = "Social Media"
        else:
            cat = "Other"
        categories[cat].append(ad)

    # Print by category
    cat_order = [
        "Shopping Platforms", "Fashion/Clothing", "Electronics/Tech",
        "Food/Delivery", "Travel", "Finance", "Newsletters/Blogs",
        "Gaming", "Education", "Health/Fitness", "Social Media",
        "Automated/No-reply", "Other"
    ]

    print("\n--- By Category ---\n")
    total_shown = 0
    for cat in cat_order:
        if cat not in categories:
            continue
        ads = categories[cat]
        total_shown += len(ads)
        # Sub-group by domain
        doms = defaultdict(list)
        for a in ads:
            doms[a["sender_domain"]].append(a)
        print(f"[{cat}]  {len(ads)} emails from {len(doms)} domains")
        for domain in sorted(doms.keys(), key=lambda d: len(doms[d]), reverse=True):
            dads = doms[domain]
            # Sub-group by sender name
            names = defaultdict(list)
            for a in dads:
                names[a["sender_name"]].append(a)
            for sname in sorted(names.keys(), key=lambda n: len(names[n]), reverse=True):
                nads = names[sname]
                print(f"  {len(nads):4d} | {domain:40s} | {sname[:50]}")
                for a in nads[:3]:
                    print(f"         {a['subject'][:90]}")
                if len(nads) > 3:
                    print(f"         ... +{len(nads)-3} more")
        print()

    # Summary
    print("=" * 70)
    print(f"[4/4] SUMMARY")
    print("=" * 70)
    print(f"  Total advertising emails found: {len(all_ads)}")
    print(f"  From unique domains:           {len(by_domain)}")
    print(f"  Categories:                    {len(categories)}")
    print()
    print("NO emails have been deleted.")
    print("Review the categories above and tell me which to delete.")
    print("Examples: 'delete Shopping Platforms and Newsletters'")
    print("          'delete all'")
    print("          'delete everything except Finance'")


if __name__ == "__main__":
    main()
