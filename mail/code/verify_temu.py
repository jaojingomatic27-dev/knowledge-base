# -*- coding: utf-8 -*-
"""Quick verification: are there any remaining Temu emails?"""
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

folders = ["INBOX", "[Gmail]/&YkBnCZCuTvY-"]  # INBOX, All Mail
total = 0

for folder in folders:
    try:
        mail.select(folder)
    except:
        continue
    status, data = mail.uid("SEARCH", None, "ALL")
    if status != "OK" or not data[0]:
        print(f"{folder}: empty")
        continue
    uids = data[0].split()
    print(f"{folder}: {len(uids)} total, scanning for temu...")

    found = 0
    for start in range(0, len(uids), 300):
        chunk = uids[start:start+300]
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
                    found += 1
        except: pass
    print(f"  -> {found} Temu emails remaining")
    total += found

print(f"\nTotal Temu remaining: {total}")
print("All clear!" if total == 0 else f"{total} still present - may need another pass")

mail.logout()
