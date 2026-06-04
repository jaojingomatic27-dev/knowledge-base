# -*- coding: utf-8 -*-
"""Delete eBay emails older than 2 weeks from INBOX."""
import imaplib, email, sys, io, re
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EMAIL = "jaojingomatic27@googlemail.com"
PASSWORD = "bcsh vyll idmy csny"
CUTOFF = datetime.now(timezone.utc) - timedelta(days=14)

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
    date_str = msg.get("Date", "")
    try:
        return parsedate_to_datetime(date_str)
    except:
        return None

def is_ebay(msg):
    sender = decode_mime(msg.get("From", "")).lower()
    if "<" in sender:
        addr = sender.split("<")[1].split(">")[0]
    else:
        addr = sender.strip()
    return "ebay" in addr.lower() or "ebay" in sender

mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
mail.login(EMAIL, PASSWORD)

print(f"Cutoff date: {CUTOFF.strftime('%Y-%m-%d')} (older than 2 weeks)")
print(f"Scanning INBOX for old eBay emails...\n")

mail.select("INBOX")
status, data = mail.uid("SEARCH", None, "ALL")
all_uids = data[0].split()
print(f"INBOX: {len(all_uids)} total")

old_ebay = []
recent_ebay = []

for start in range(0, len(all_uids), 300):
    chunk = all_uids[start:start+300]
    uids_str = ",".join(uid.decode() for uid in chunk)
    try:
        status, data = mail.uid("FETCH", uids_str, "(RFC822.HEADER)")
        if status != "OK": continue
        for i in range(0, len(data), 2):
            if i >= len(data): break
            resp = data[i]
            if not isinstance(resp, tuple): continue
            resp_text = resp[0].decode(errors="replace")
            m = re.search(r'UID\s+(\d+)', resp_text)
            if not m: continue
            uid = m.group(1)
            try: msg = email.message_from_bytes(resp[1])
            except: continue
            if not is_ebay(msg): continue

            subject = decode_mime(msg.get("Subject", ""))
            date = parse_date(msg)
            if date is None:
                # If can't parse date, treat as old
                old_ebay.append((uid, subject, "unknown date"))
            elif date < CUTOFF:
                old_ebay.append((uid, subject, date.strftime("%Y-%m-%d")))
            else:
                recent_ebay.append((uid, subject, date.strftime("%Y-%m-%d")))
    except: pass

print(f"eBay emails found:")
print(f"  Old (>2 weeks):  {len(old_ebay)}")
print(f"  Recent (<2 wks): {len(recent_ebay)}")

if not old_ebay:
    print("\nNo old eBay emails to delete.")
    mail.logout()
    exit()

# Show sample
print(f"\nOld eBay emails (kept recent {len(recent_ebay)}):")
for uid, subj, date in old_ebay[:10]:
    print(f"  [{date}] {subj[:90]}")
if len(old_ebay) > 10:
    print(f"  ... and {len(old_ebay)-10} more")

# Delete
print(f"\nDeleting {len(old_ebay)} old eBay emails...")
deleted = 0
uids = [u for u, _, _ in old_ebay]
for start in range(0, len(uids), 100):
    batch = uids[start:start+100]
    uids_str = ",".join(uid for uid in batch)
    try:
        status, _ = mail.uid("STORE", uids_str, "+FLAGS", "\\Deleted")
        if status == "OK": deleted += len(batch)
        else:
            for uid in batch:
                try:
                    s, _ = mail.uid("STORE", uid, "+FLAGS", "\\Deleted")
                    if s == "OK": deleted += 1
                except: pass
    except:
        for uid in batch:
            try:
                mail.uid("STORE", uid, "+FLAGS", "\\Deleted")
                deleted += 1
            except: pass

mail.expunge()
mail.logout()

print(f"[DONE] {deleted} old eBay emails deleted.")
print(f"Kept {len(recent_ebay)} recent eBay emails (within 2 weeks).")
