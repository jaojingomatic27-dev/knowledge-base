# -*- coding: utf-8 -*-
"""Move stuck Temu emails to Spam folder via IMAP MOVE."""
import imaplib, email, sys, io, re
from email.header import decode_header

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EMAIL = "jaojingomatic27@googlemail.com"
PASSWORD = "bcsh vyll idmy csny"
ALL_MAIL = "[Gmail]/&YkBnCZCuTvY-"
SPAM = "[Gmail]/&V4NXPpCuTvY-"  # 垃圾邮件

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

mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
mail.login(EMAIL, PASSWORD)

# Find Temu in All Mail
print("[1] Finding Temu in All Mail...")
mail.select(ALL_MAIL)
status, data = mail.uid("SEARCH", None, "ALL")
all_uids = data[0].split()
print(f"All Mail: {len(all_uids)} total")

temu_uids = []
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
            try: msg = email.message_from_bytes(resp[1])
            except: continue
            text = f"{decode_mime(msg.get('Subject',''))} {decode_mime(msg.get('From',''))}".lower()
            if "temu" in text:
                temu_uids.append(m.group(1))
    except: pass

print(f"Temu found: {len(temu_uids)}")

if not temu_uids:
    print("None found!")
    mail.logout()
    exit()

# Move to Spam
print(f"\n[2] Moving {len(temu_uids)} to Spam ({SPAM})...")
mail.select(ALL_MAIL)
moved = 0
for start in range(0, len(temu_uids), 100):
    batch = temu_uids[start:start+100]
    uids_str = ",".join(uid for uid in batch)
    try:
        status, _ = mail.uid("MOVE", uids_str, SPAM)
        if status == "OK":
            moved += len(batch)
        else:
            # Fallback: COPY then STORE +FLAGS \Deleted
            status2, _ = mail.uid("COPY", uids_str, SPAM)
            if status2 == "OK":
                mail.uid("STORE", uids_str, "+FLAGS", "\\Deleted")
                moved += len(batch)
    except Exception as e:
        # Try one-by-one fallback
        for uid in batch:
            try:
                s, _ = mail.uid("MOVE", uid, SPAM)
                if s == "OK": moved += 1
            except:
                try:
                    mail.uid("COPY", uid, SPAM)
                    mail.uid("STORE", uid, "+FLAGS", "\\Deleted")
                    moved += 1
                except: pass
    print(f"  Progress: {min(start+100, len(temu_uids))}/{len(temu_uids)}")

mail.expunge()
print(f"Moved {moved} to Spam")

# Verify
print(f"\n[3] Verifying...")
mail.select(ALL_MAIL)
status, data = mail.uid("SEARCH", None, "ALL")
all_uids = data[0].split()
remaining = 0
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
            try: msg = email.message_from_bytes(resp[1])
            except: continue
            text = f"{decode_mime(msg.get('Subject',''))} {decode_mime(msg.get('From',''))}".lower()
            if "temu" in text: remaining += 1
    except: pass

# Also check Spam count
mail.select(SPAM)
status, data = mail.search(None, "ALL")
spam_count = len(data[0].split()) if data[0] else 0

mail.logout()
print(f"Temu in All Mail: {remaining}")
print(f"Total in Spam: {spam_count}")
if remaining == 0:
    print("\n[SUCCESS] All Temu moved to Spam!")
    print("Gmail will learn to auto-filter Temu as spam from now on.")
else:
    print(f"\n{remaining} still stuck - manual cleanup needed")
