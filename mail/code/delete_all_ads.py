# -*- coding: utf-8 -*-
"""
Delete ALL advertising emails across all Gmail folders.
Re-scans, then deletes using UID-based operations.
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
    "microsoft.com", "apple.com",
]
TRUSTED_SENDERS = ["github", "google", "notifications@"]

SKIP_FOLDERS = [
    "Trash", "Junk",
    "[Gmail]/&YkBnCZCuTvY-",   # All Mail (duplicates INBOX)
    "[Gmail]/&XfJSIJZkkK5O9g-", # Trash
    "[Gmail]/&V4NXPpCuTvY-",    # Spam
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
    print("Gmail Bulk Ad Deleter")
    print(f"Account: {EMAIL}")
    print("=" * 60)

    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)
    print("Connected.\n")

    # List folders
    status, folder_list = mail.list()
    folders = []
    for f in folder_list:
        raw = f.decode(errors="replace").split('"/" ')[-1].strip('"')
        if raw not in SKIP_FOLDERS and raw.strip():
            folders.append(raw)

    print(f"Will scan: {[f for f in folders]}\n")

    # Phase 1: Find all ad UIDs per folder
    all_to_delete = {}  # folder -> [uid1, uid2, ...]
    all_info = []       # (folder, domain, sender, subject)

    for folder in folders:
        try:
            status, _ = mail.select(folder)
            if status != "OK":
                print(f"  SKIP {folder}: cannot select")
                continue
        except Exception:
            print(f"  SKIP {folder}: cannot select")
            continue

        status, data = mail.uid("SEARCH", None, "ALL")
        if status != "OK" or not data[0]:
            print(f"  {folder}: empty")
            continue

        all_uids = data[0].split()
        total = len(all_uids)
        print(f"  Scanning {folder}: {total} msgs...")

        folder_uids = []
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
                    resp_text = resp[0].decode(errors="replace")
                    m = re.search(r'UID\s+(\d+)', resp_text)
                    if not m:
                        continue
                    uid = m.group(1)
                    try:
                        msg = email.message_from_bytes(resp[1])
                    except Exception:
                        continue
                    subject = decode_mime(msg.get("Subject", ""))
                    name, addr, domain = parse_sender(msg)
                    if is_ad(subject, name, addr, domain):
                        folder_uids.append(uid)
                        all_info.append((folder, domain, name or addr, subject[:80]))
            except Exception as e:
                pass
            if total > 200:
                print(f"    progress: {min(start+chunk_size, total)}/{total}")

        print(f"  {folder}: found {len(folder_uids)} ads")
        if folder_uids:
            all_to_delete[folder] = folder_uids

    # Phase 2: Summary
    total_ads = sum(len(uids) for uids in all_to_delete.values())
    print(f"\n{'='*60}")
    print(f"TOTAL ADS TO DELETE: {total_ads}")
    print(f"Across {len(all_to_delete)} folders")
    print(f"{'='*60}")

    by_domain = defaultdict(int)
    for folder, domain, sender, subj in all_info:
        by_domain[domain] += 1
    for domain in sorted(by_domain.keys(), key=lambda d: by_domain[d], reverse=True):
        print(f"  {domain}: {by_domain[domain]}")

    if total_ads == 0:
        print("\nNothing to delete.")
        mail.logout()
        return

    # Phase 3: Delete
    print(f"\nDeleting {total_ads} emails...")
    total_deleted = 0

    for folder, uids in all_to_delete.items():
        try:
            mail.select(folder)
        except Exception:
            print(f"  Cannot select {folder}, skipping...")
            continue

        # Delete in batches of 100
        for start in range(0, len(uids), 100):
            batch = uids[start:start+100]
            uids_str = ",".join(uid for uid in batch)
            try:
                status, _ = mail.uid("STORE", uids_str, "+FLAGS", "\\Deleted")
                if status == "OK":
                    total_deleted += len(batch)
                else:
                    # One-by-one fallback
                    for uid in batch:
                        try:
                            s, _ = mail.uid("STORE", uid, "+FLAGS", "\\Deleted")
                            if s == "OK":
                                total_deleted += 1
                        except Exception:
                            pass
            except Exception:
                for uid in batch:
                    try:
                        mail.uid("STORE", uid, "+FLAGS", "\\Deleted")
                        total_deleted += 1
                    except Exception:
                        pass
        # Expunge this folder
        try:
            mail.expunge()
        except Exception:
            pass
        print(f"  {folder}: {len(uids)} deleted")

    mail.logout()
    print(f"\n[DONE] {total_deleted} advertising emails moved to Trash.")
    print("They will be permanently deleted after 30 days.")


if __name__ == "__main__":
    main()
