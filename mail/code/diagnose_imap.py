# -*- coding: utf-8 -*-
"""Diagnose Gmail IMAP connection issues."""
import imaplib
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
PASSWORD_RAW = "bcsh vyll idmy csny"

# Try different email and password formats
tests = [
    ("jaojingomatic27@googlemail.com", PASSWORD_RAW),
    ("jaojingomatic27@googlemail.com", PASSWORD_RAW.replace(" ", "")),
    ("jaojingomatic27@gmail.com", PASSWORD_RAW),
    ("jaojingomatic27@gmail.com", PASSWORD_RAW.replace(" ", "")),
]

print("Gmail IMAP Diagnostic")
print("=" * 60)
print("Testing different credential formats...\n")

for email_addr, password in tests:
    print(f"Test: {email_addr} / password_len={len(password)}")
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(email_addr, password)
        print(f"  [SUCCESS] Login OK!")
        # List folders to confirm
        status, data = mail.list()
        if status == "OK":
            folders = [f.decode(errors="replace").split('"/" ')[-1].strip('"') for f in data]
            print(f"  Folders: {len(folders)} found")
            for f in folders[:20]:
                print(f"    - {f}")
            if len(folders) > 20:
                print(f"    ... and {len(folders)-20} more")
        mail.logout()
        break
    except imaplib.IMAP4.error as e:
        err = str(e)
        print(f"  [FAIL] {err[:120]}")
        # Check common issues
        if "Application-specific password" in err:
            print("  -> Hint: App password may be wrong or IMAP not enabled")
        elif "Invalid credentials" in err:
            print("  -> Hint: Wrong email or password")
        elif "Less secure" in err or "security" in err.lower():
            print("  -> Hint: Need to enable 'Allow less secure apps' or use App Password")
    except Exception as e:
        print(f"  [ERROR] {type(e).__name__}: {e}")
    print()

print("\nDone. If all fail, please check:")
print("1. IMAP is enabled: Gmail Settings -> See all settings -> Forwarding and POP/IMAP -> Enable IMAP")
print("2. App Password is correct (16 chars, generated for 'Mail' app)")
print("3. Try generating a NEW App Password (delete old one first)")
