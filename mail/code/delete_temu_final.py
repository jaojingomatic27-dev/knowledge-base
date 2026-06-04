# -*- coding: utf-8 -*-
"""Directly delete remaining Temu emails from All Mail."""
import imaplib, email, sys, io, re
from email.header import decode_header

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EMAIL = "jaojingomatic27@googlemail.com"
PASSWORD = "bcsh vyll idmy csny"

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

# Target: All Mail
folder = "[Gmail]/&YkBnCZCuTvY-"
mail.select(folder)
print(f"Selected: All Mail")

status, data = mail.uid("SEARCH", None, "ALL")
all_uids = data[0].split()
print(f"Total: {len(all_uids)} messages")

# Find all Temu UIDs
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
            uid = m.group(1)
            try: msg = email.message_from_bytes(resp[1])
            except: continue
            text = f"{decode_mime(msg.get('Subject',''))} {decode_mime(msg.get('From',''))}".lower()
            if "temu" in text:
                temu_uids.append(uid)
    except: pass
    if len(all_uids) > 300:
        print(f"  Scanning: {min(start+300, len(all_uids))}/{len(all_uids)}")

print(f"\nTemu in All Mail: {len(temu_uids)}")

if not temu_uids:
    print("None found. All clear!")
    mail.logout()
    exit()

# Show a few
for uid in temu_uids[:5]:
    print(f"  UID {uid}")

# Delete from All Mail
print(f"\nDeleting {len(temu_uids)} from All Mail...")
deleted = 0
for start in range(0, len(temu_uids), 100):
    batch = temu_uids[start:start+100]
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
print(f"\n[DONE] {deleted} Temu emails permanently removed from All Mail.")
