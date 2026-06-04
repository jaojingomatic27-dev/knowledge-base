# -*- coding: utf-8 -*-
"""Check if remaining Temu emails are in Trash."""
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

# Check Trash folder (UTF-7 encoded)
trash_names = ["[Gmail]/&XfJSIJZkkK5O9g-", "[Gmail]/Trash", "Trash"]
for name in trash_names:
    try:
        mail.select(name)
        status, data = mail.uid("SEARCH", None, "ALL")
        if status == "OK" and data[0]:
            uids = data[0].split()
            print(f"{name} (Trash): {len(uids)} total")

            temu_count = 0
            for start in range(0, len(uids), 300):
                chunk = uids[start:start+300]
                uids_str = ",".join(uid.decode() for uid in chunk)
                try:
                    status, data2 = mail.uid("FETCH", uids_str, "(RFC822.HEADER)")
                    if status != "OK": continue
                    for i in range(0, len(data2), 2):
                        if i >= len(data2): break
                        resp = data2[i]
                        if not isinstance(resp, tuple): continue
                        try: msg = email.message_from_bytes(resp[1])
                        except: continue
                        text = f"{decode_mime(msg.get('Subject',''))} {decode_mime(msg.get('From',''))}".lower()
                        if "temu" in text: temu_count += 1
                except: pass
            print(f"  -> {temu_count} Temu emails in Trash")
            break
    except Exception as e:
        print(f"{name}: {e}")

mail.logout()
