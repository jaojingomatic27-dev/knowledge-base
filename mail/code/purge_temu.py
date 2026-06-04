# -*- coding: utf-8 -*-
"""Permanently delete ALL Temu emails — two-pass approach:
1. Move to Trash (delete from All Mail)
2. Permanently expunge from Trash
"""
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

# Step 1: Find all Temu in All Mail
ALL_MAIL = "[Gmail]/&YkBnCZCuTvY-"
TRASH_1 = "[Gmail]/&XfJSIJZkkK5O9g-"
TRASH_2 = "Trash"

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
    if (start // 300) % 10 == 0:
        print(f"  Scanning: {min(start+300, len(all_uids))}/{len(all_uids)}, found {len(temu_uids)}")

print(f"Temu found: {len(temu_uids)}")

if not temu_uids:
    print("None found. All clear!")
    mail.logout()
    exit()

# Step 2: Move to Trash (delete from All Mail, do NOT expunge)
print(f"\n[2] Moving {len(temu_uids)} to Trash...")
mail.select(ALL_MAIL)
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
print(f"  Marked {deleted} as Deleted")

# Expunge All Mail (should move them to Trash)
print("  Expunging All Mail...")
mail.expunge()

# Step 3: Find and permanently delete from Trash
print(f"\n[3] Purging from Trash...")
for trash_name in [TRASH_1, TRASH_2]:
    try:
        mail.select(trash_name)
        status, data = mail.search(None, "ALL")
        if status == "OK":
            count = len(data[0].split()) if data[0] else 0
            print(f"  {trash_name}: {count} messages")

            # Search for Temu in Trash
            temu_in_trash = []
            if count > 0:
                mail.select(trash_name)
                status2, data2 = mail.uid("SEARCH", None, "ALL")
                if status2 == "OK" and data2[0]:
                    trash_uids = data2[0].split()
                    for start in range(0, len(trash_uids), 300):
                        chunk = trash_uids[start:start+300]
                        uids_str = ",".join(uid.decode() for uid in chunk)
                        try:
                            status3, data3 = mail.uid("FETCH", uids_str, "(RFC822.HEADER)")
                            if status3 != "OK": continue
                            for i in range(0, len(data3), 2):
                                if i >= len(data3): break
                                resp = data3[i]
                                if not isinstance(resp, tuple): continue
                                try: msg = email.message_from_bytes(resp[1])
                                except: continue
                                text = f"{decode_mime(msg.get('Subject',''))} {decode_mime(msg.get('From',''))}".lower()
                                if "temu" in text:
                                    m = re.search(r'UID\s+(\d+)', resp[0].decode(errors="replace"))
                                    if m: temu_in_trash.append(m.group(1))
                        except: pass

            print(f"  Temu in {trash_name}: {len(temu_in_trash)}")

            if temu_in_trash:
                # Permanently delete from Trash
                perm_deleted = 0
                for start in range(0, len(temu_in_trash), 100):
                    batch = temu_in_trash[start:start+100]
                    uids_str = ",".join(uid for uid in batch)
                    try:
                        status, _ = mail.uid("STORE", uids_str, "+FLAGS", "\\Deleted")
                        if status == "OK": perm_deleted += len(batch)
                    except: pass
                mail.expunge()
                print(f"  Permanently deleted {perm_deleted} from {trash_name}")
            break
    except Exception as e:
        print(f"  Error with {trash_name}: {e}")

# Step 4: Final verification
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
    if (start // 300) % 10 == 0:
        print(f"  Verifying: {min(start+300, len(all_uids))}/{len(all_uids)}")

mail.logout()
print(f"\nTemu remaining: {remaining}")
if remaining == 0:
    print("[SUCCESS] All Temu emails permanently deleted!")
else:
    print(f"[WARNING] {remaining} still present - may need manual cleanup via Gmail web")
