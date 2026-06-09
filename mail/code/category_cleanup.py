# -*- coding: utf-8 -*-
"""
Delete Gmail dynamic category emails older than 2 weeks.
Categories: promotions, social, updates, forums
One-time move to Spam for stuck emails. No permanent filters created.
"""
import imaplib, email, sys, io, re
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone, timedelta
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EMAIL = "jaojingomatic27@googlemail.com"
PASSWORD = "bcsh vyll idmy csny"
CUTOFF = datetime.now(timezone.utc) - timedelta(days=14)
SPAM = "[Gmail]/&V4NXPpCuTvY-"
ALL_MAIL = "[Gmail]/&YkBnCZCuTvY-"

CATEGORIES = {
    "promotions": "category:promotions",
    "social": "category:social",
    "updates": "category:updates",
    "forums": "category:forums",
}

def decode_mime(val):
    if val is None: return ""
    parts = decode_header(val)
    res = []
    for data, charset in parts:
        if isinstance(data, bytes):
            try: res.append(data.decode(charset or "utf-8", errors="replace"))
            except: res.append(data.decode("utf-8", errors="replace"))
        else: res.append(str(data))
    return "".join(res)

def parse_date(msg):
    try: return parsedate_to_datetime(msg.get("Date", ""))
    except: return None

mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
mail.login(EMAIL, PASSWORD)

print(f"Cutoff: {CUTOFF.strftime('%Y-%m-%d')} (older than 2 weeks)")
print(f"Categories: {list(CATEGORIES.keys())}\n")

# Phase 1: Find old emails per category using UID search
all_old_uids = defaultdict(list)  # folder -> [(uid, subject, sender, date, cat)]
all_recent_info = []

for cat_name, query in CATEGORIES.items():
    print(f"--- {cat_name} ---")
    mail.select("INBOX")

    try:
        status, data = mail.search(None, "X-GM-RAW", query)
    except:
        print(f"  X-GM-RAW failed, skipping")
        continue

    if status != "OK" or not data[0]:
        print(f"  No emails")
        continue

    seq_ids = data[0].split()  # These are sequence numbers, need UIDs
    total = len(seq_ids)
    print(f"  {total} emails, filtering by date...")

    old_count = 0
    recent_count = 0

    for start in range(0, len(seq_ids), 300):
        chunk = seq_ids[start:start+300]
        ids_str = ",".join(mid.decode() for mid in chunk)
        try:
            status, data = mail.fetch(ids_str, "(UID RFC822.HEADER)")
            if status != "OK": continue
        except: continue

        for i in range(0, len(data), 2):
            if i >= len(data): break
            resp = data[i]
            if not isinstance(resp, tuple): continue
            resp_text = resp[0].decode(errors="replace")

            # Extract UID
            uid = None
            m = re.search(r'UID\s+(\d+)', resp_text)
            if m: uid = m.group(1)
            if not uid: continue

            try: msg = email.message_from_bytes(resp[1])
            except: continue

            subject = decode_mime(msg.get("Subject", ""))
            sender = decode_mime(msg.get("From", ""))
            date = parse_date(msg)

            if date and date < CUTOFF:
                all_old_uids["INBOX"].append((uid, subject[:80], sender[:60],
                                              date.strftime("%Y-%m-%d"), cat_name))
                old_count += 1
            else:
                recent_count += 1

        if total > 300:
            print(f"    progress: {min(start+300, total)}/{total}")

    print(f"  Old: {old_count}, Recent: {recent_count}")

# Summary
total_old = sum(len(v) for v in all_old_uids.values())
print(f"\n{'='*60}")
print(f"TOTAL old category emails: {total_old}")
print(f"{'='*60}")

if total_old == 0:
    print("Nothing to do!")
    mail.logout()
    exit()

# Breakdown
by_cat = defaultdict(list)
for folder, items in all_old_uids.items():
    for uid, subj, sender, date, cat in items:
        by_cat[cat].append((uid, subj, sender, date))

for cat in CATEGORIES:
    if cat in by_cat:
        items = by_cat[cat]
        doms = defaultdict(int)
        for uid, subj, sender, date in items:
            if "<" in sender:
                dom = sender.split("<")[1].split(">")[0].split("@")[-1]
            else:
                dom = sender.strip().split("@")[-1]
            doms[dom] += 1
        print(f"\n{cat}: {len(items)} old emails")
        for dom, n in sorted(doms.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"    {dom}: {n}")
        for uid, subj, sender, date in items[:3]:
            print(f"    [{date}] {sender[:40]}")

# Phase 2: Delete from INBOX
print(f"\n{'='*60}")
print(f"Deleting {total_old} old category emails from INBOX...")
mail.select("INBOX")
deleted = 0
failed_uids = []

for folder, items in all_old_uids.items():
    mail.select(folder)
    for start in range(0, len(items), 100):
        batch = items[start:start+100]
        uids_str = ",".join(uid for uid, _, _, _, _ in batch)
        try:
            status, _ = mail.uid("STORE", uids_str, "+FLAGS", "\\Deleted")
            if status == "OK":
                deleted += len(batch)
            else:
                for uid, _, _, _, _ in batch:
                    try:
                        s, _ = mail.uid("STORE", uid, "+FLAGS", "\\Deleted")
                        if s == "OK": deleted += 1
                        else: failed_uids.append((uid, batch[batch.index((uid,))]))
                    except: failed_uids.append((uid, [x for x in batch if x[0]==uid][0] if any(x[0]==uid for x in batch) else (uid,"","","","")))
        except Exception as e:
            for uid, subj, sender, date, cat in batch:
                try:
                    mail.uid("STORE", uid, "+FLAGS", "\\Deleted")
                    deleted += 1
                except:
                    failed_uids.append((uid, subj, sender, date, cat))
    mail.expunge()
    print(f"  {folder}: {len(items)} processed")

print(f"Deleted: {deleted}, Failed: {len(failed_uids)}")

# Phase 3: Move failed emails to Spam (one-time, no filter rule)
if failed_uids:
    print(f"\n{'='*60}")
    print(f"Moving {len(failed_uids)} stuck emails to Spam (one-time only)...")
    mail.select("INBOX")
    spam_moved = 0

    for start in range(0, len(failed_uids), 100):
        batch = failed_uids[start:start+100]
        uids_str = ",".join(uid for uid, _, _, _, _ in batch)
        try:
            status, _ = mail.uid("MOVE", uids_str, SPAM)
            if status == "OK":
                spam_moved += len(batch)
            else:
                for uid, _, _, _, _ in batch:
                    try:
                        s, _ = mail.uid("MOVE", uid, SPAM)
                        if s == "OK": spam_moved += 1
                    except:
                        # Last resort: COPY + delete
                        try:
                            mail.uid("COPY", uid, SPAM)
                            mail.uid("STORE", uid, "+FLAGS", "\\Deleted")
                            spam_moved += 1
                        except: pass
        except:
            for uid, _, _, _, _ in batch:
                try:
                    mail.uid("MOVE", uid, SPAM)
                    spam_moved += 1
                except:
                    try:
                        mail.uid("COPY", uid, SPAM)
                        mail.uid("STORE", uid, "+FLAGS", "\\Deleted")
                        spam_moved += 1
                    except: pass

    mail.expunge()
    print(f"Moved to Spam: {spam_moved}")

mail.logout()

print(f"\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
print(f"  Deleted:       {deleted}")
print(f"  Moved to Spam: {len(failed_uids)} (one-time)")
print(f"  Total cleaned: {deleted + len(failed_uids)}")
print(f"\nThis is a ONE-TIME cleanup. No permanent filters created.")
print(f"New emails will arrive normally and NOT be auto-spammed.")
