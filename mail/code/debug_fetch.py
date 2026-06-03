# -*- coding: utf-8 -*-
"""Debug: test UID FETCH response format."""
import imaplib
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EMAIL = "jaojingomatic27@googlemail.com"
PASSWORD = "bcsh vyll idmy csny"

mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
mail.login(EMAIL, PASSWORD)
mail.select("INBOX")

# Get all UIDs
status, data = mail.uid("SEARCH", None, "ALL")
all_uids = data[0].split()[-600:]
print(f"Total UIDs (recent 600): {len(all_uids)}")

# Fetch first 5 UIDs
test_uids = all_uids[:5]
uids_str = ",".join(uid.decode() for uid in test_uids)
print(f"Fetching UIDs: {uids_str}")

status, data = mail.uid("FETCH", uids_str, "(RFC822.HEADER)")
print(f"Status: {status}")
print(f"Data type: {type(data)}")
print(f"Data length: {len(data)}")

for i, item in enumerate(data):
    print(f"\n--- Item {i} ---")
    print(f"  Type: {type(item)}")
    if isinstance(item, tuple):
        print(f"  item[0] (first 200 chars): {item[0][:200]}")
        print(f"  item[1] length: {len(item[1])}")
        # Parse first few headers from item[1]
        try:
            from email import message_from_bytes
            msg = message_from_bytes(item[1])
            print(f"  Subject: {msg.get('Subject', 'N/A')[:80]}")
            print(f"  From: {msg.get('From', 'N/A')[:80]}")
        except Exception as e:
            print(f"  Parse error: {e}")
    elif isinstance(item, bytes):
        print(f"  bytes (first 200): {item[:200]}")
    else:
        print(f"  value: {str(item)[:200]}")

mail.logout()
