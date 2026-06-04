# -*- coding: utf-8 -*-
"""
Fix stuck Temu emails: remove \Deleted flag (restore to INBOX),
then properly delete from INBOX with expunge.
"""
import imaplib, email, sys, io, re
from email.header import decode_header

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EMAIL = "jaojingomatic27@googlemail.com"
PASSWORD = "bcsh vyll idmy csny"
ALL_MAIL = "[Gmail]/&YkBnCZCuTvY-"

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

# Step 1: Find Temu UIDs in All Mail
print("[1] Finding Temu UIDs in All Mail...")
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

# Step 2: Remove \Deleted flag to restore them
print(f"\n[2] Removing \\Deleted flag (restoring {len(temu_uids)} emails)...")
mail.select(ALL_MAIL)
restored = 0
for start in range(0, len(temu_uids), 100):
    batch = temu_uids[start:start+100]
    uids_str = ",".join(uid for uid in batch)
    try:
        status, _ = mail.uid("STORE", uids_str, "-FLAGS", "\\Deleted")
        if status == "OK": restored += len(batch)
        else:
            for uid in batch:
                try:
                    s, _ = mail.uid("STORE", uid, "-FLAGS", "\\Deleted")
                    if s == "OK": restored += 1
                except: pass
    except:
        for uid in batch:
            try:
                mail.uid("STORE", uid, "-FLAGS", "\\Deleted")
                restored += 1
            except: pass
print(f"  Restored {restored}, waiting for Gmail to sync...")

# Give Gmail a moment to sync labels
import time
time.sleep(3)

# Step 3: Now delete from INBOX properly
print(f"\n[3] Deleting from INBOX...")
mail.select("INBOX")
status, data = mail.uid("SEARCH", None, "ALL")
inbox_uids = data[0].split()
print(f"INBOX: {len(inbox_uids)} total")

# Find Temu in INBOX now
temu_inbox = []
for start in range(0, len(inbox_uids), 300):
    chunk = inbox_uids[start:start+300]
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
                temu_inbox.append(m.group(1))
    except: pass

print(f"Temu in INBOX: {len(temu_inbox)}")

if temu_inbox:
    deleted = 0
    for start in range(0, len(temu_inbox), 100):
        batch = temu_inbox[start:start+100]
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
    print(f"  Marked {deleted} as deleted")
    mail.expunge()
    print("  Expunged INBOX")

# Step 4: Verify
print(f"\n[4] Final verification...")
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

print(f"Temu remaining in All Mail: {remaining}")

mail.logout()
if remaining == 0:
    print("[SUCCESS] All Temu emails permanently deleted!")
else:
    print(f"[NOTE] {remaining} still in All Mail (likely in Trash now)")
    print("Check https://mail.google.com and empty Trash manually if needed.")
