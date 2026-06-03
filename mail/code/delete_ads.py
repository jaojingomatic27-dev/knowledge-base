# -*- coding: utf-8 -*-
"""
Delete advertising emails from Gmail INBOX.
Re-scans then deletes. Uses UID-based operations for reliability.
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


def main():
    print("=" * 60)
    print("Gmail Ad Deleter")
    print(f"Account: {EMAIL}")
    print("=" * 60)

    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)
    print("Connected.\n")

    # Step 1: Scan INBOX using UID SEARCH
    mail.select("INBOX")
    status, data = mail.uid("SEARCH", None, "ALL")
    if status != "OK":
        print("Search failed.")
        mail.logout()
        return

    all_uids = data[0].split()
    total = len(all_uids)
    print(f"Total INBOX messages: {total}")

    # Limit to recent 600 for performance
    if total > 600:
        all_uids = all_uids[-600:]
        print(f"Scanning most recent 600...")

    # Step 2: Fetch headers and identify ads (using UID fetch)
    to_delete_uids = []
    to_delete_info = []
    chunk_size = 200

    for start in range(0, len(all_uids), chunk_size):
        chunk = all_uids[start:start+chunk_size]
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
                body = resp[1]  # body is second element of tuple
                # Extract UID from response
                resp_text = resp[0].decode(errors="replace")
                m = re.search(r'UID\s+(\d+)', resp_text)
                if not m:
                    continue
                uid = m.group(1)
                try:
                    msg = email.message_from_bytes(body)
                except Exception:
                    continue
                subject = decode_mime(msg.get("Subject", ""))
                name, addr, domain = parse_sender(msg)
                if is_ad(subject, name, addr, domain):
                    to_delete_uids.append(uid)
                    to_delete_info.append((domain, name or addr, subject[:80]))
        except Exception as e:
            print(f"  Fetch error in chunk: {e}")
        print(f"  Scanned {min(start+chunk_size, len(all_uids))}/{len(all_uids)}")

    print(f"\nFound {len(to_delete_uids)} advertising emails.\n")

    if not to_delete_uids:
        print("Nothing to delete.")
        mail.logout()
        return

    # Show summary
    by_domain = defaultdict(list)
    for uid, (domain, name, subj) in zip(to_delete_uids, to_delete_info):
        by_domain[domain].append((name, subj))

    print("--- To Delete ---")
    for domain in sorted(by_domain.keys()):
        items = by_domain[domain]
        print(f"  {domain}: {len(items)} emails")
        for name, subj in items[:3]:
            print(f"    [{name}] {subj}")
        if len(items) > 3:
            print(f"    ... +{len(items)-3} more")
    print()

    # Step 3: Delete using UID STORE
    print(f"Deleting {len(to_delete_uids)} emails...")

    deleted = 0
    for start in range(0, len(to_delete_uids), 100):
        batch = to_delete_uids[start:start+100]
        uids_str = ",".join(uid for uid in batch)
        try:
            status, _ = mail.uid("STORE", uids_str, "+FLAGS", "\\Deleted")
            if status == "OK":
                deleted += len(batch)
            else:
                # Try one-by-one
                for uid in batch:
                    try:
                        s, _ = mail.uid("STORE", uid, "+FLAGS", "\\Deleted")
                        if s == "OK":
                            deleted += 1
                    except Exception:
                        pass
        except Exception as e:
            print(f"  Batch delete error: {e}")
        print(f"  Progress: {min(start+100, len(to_delete_uids))}/{len(to_delete_uids)}")

    # Expunge
    print("Expunging...")
    mail.expunge()
    mail.logout()

    print(f"\n[DONE] {deleted} advertising emails moved to Trash.")
    print("They'll be permanently deleted after 30 days.")


if __name__ == "__main__":
    main()
