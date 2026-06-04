# -*- coding: utf-8 -*-
"""Find and delete all Temu-related emails across all Gmail folders."""
import imaplib
import email
from email.header import decode_header
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

EMAIL = "jaojingomatic27@googlemail.com"
PASSWORD = "bcsh vyll idmy csny"
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

SKIP_FOLDERS = [
    "Trash", "Junk",
    "[Gmail]/&YkBnCZCuTvY-",    # All Mail (duplicates)
    "[Gmail]/&XfJSIJZkkK5O9g-",  # Trash
    "[Gmail]/&V4NXPpCuTvY-",     # Spam
]


def decode_mime(val):
    if val is None:
        return ""
    parts = decode_header(val)
    res = []
    for data, charset in parts:
        if isinstance(data, bytes):
            try:
                res.append(data.decode(charset or "utf-8", errors="replace"))
            except Exception:
                res.append(data.decode("utf-8", errors="replace"))
        else:
            res.append(str(data))
    return "".join(res)


def is_temu(subject, sender_name, sender_addr, sender_domain):
    """Check if email is Temu-related."""
    text = f"{subject} {sender_name} {sender_addr} {sender_domain}".lower()
    # Check for temu keyword
    if "temu" in text:
        return True
    # Check temu domains
    if "temu.com" in sender_domain or sender_domain.endswith(".temu"):
        return True
    return False


def main():
    print("=" * 60)
    print("Temu Email Finder & Deleter")
    print("=" * 60)

    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)
    print("Connected.\n")

    # List folders
    status, folder_list = mail.list()
    folders = []
    for f in folder_list:
        raw = f.decode(errors="replace").split('"/" ')[-1].strip('"')
        if raw not in SKIP_FOLDERS and raw.strip():
            folders.append(raw)

    all_to_delete = {}
    all_info = []

    for folder in folders:
        try:
            status, _ = mail.select(folder)
            if status != "OK":
                continue
        except Exception:
            continue

        status, data = mail.uid("SEARCH", None, "ALL")
        if status != "OK" or not data[0]:
            continue

        all_uids = data[0].split()
        total = len(all_uids)
        print(f"Scanning {folder} ({total} msgs)...")

        folder_uids = []
        chunk_size = 200
        for start in range(0, len(all_uids), chunk_size):
            chunk = all_uids[start:start+chunk_size]
            uids_str = ",".join(uid.decode() for uid in chunk)
            try:
                status, data = mail.uid("FETCH", uids_str, "(RFC822.HEADER)")
                if status != "OK":
                    continue
                for i in range(0, len(data), 2):
                    if i >= len(data):
                        break
                    resp = data[i]
                    if not isinstance(resp, tuple):
                        continue
                    resp_text = resp[0].decode(errors="replace")
                    m = re.search(r'UID\s+(\d+)', resp_text)
                    if not m:
                        continue
                    uid = m.group(1)
                    try:
                        msg = email.message_from_bytes(resp[1])
                    except Exception:
                        continue
                    subject = decode_mime(msg.get("Subject", ""))
                    sender = decode_mime(msg.get("From", ""))
                    name, addr = "", ""
                    if "<" in sender:
                        name = sender.split("<")[0].strip().strip('"')
                        addr = sender.split("<")[1].split(">")[0].strip()
                    else:
                        addr = sender.strip()
                        name = ""
                    domain = addr.split("@")[1].lower() if "@" in addr else ""
                    if is_temu(subject, name, addr, domain):
                        folder_uids.append(uid)
                        all_info.append((folder, domain, name or addr, subject[:100]))
            except Exception:
                pass
            if total > 200:
                print(f"  progress: {min(start+chunk_size, total)}/{total}")

        if folder_uids:
            all_to_delete[folder] = folder_uids
            print(f"  Found {len(folder_uids)} Temu emails")

    # Summary
    total = sum(len(uids) for uids in all_to_delete.values())
    print(f"\n{'='*60}")
    print(f"Temu emails found: {total}")
    print(f"{'='*60}")

    if total == 0:
        print("No Temu emails found.")
        mail.logout()
        return

    for folder, domain, sender, subj in all_info:
        print(f"  [{folder}] {sender} | {subj}")

    # Delete
    print(f"\nDeleting {total} Temu emails...")
    deleted = 0
    for folder, uids in all_to_delete.items():
        mail.select(folder)
        for start in range(0, len(uids), 100):
            batch = uids[start:start+100]
            uids_str = ",".join(uid for uid in batch)
            try:
                mail.uid("STORE", uids_str, "+FLAGS", "\\Deleted")
                deleted += len(batch)
            except Exception:
                for uid in batch:
                    try:
                        mail.uid("STORE", uid, "+FLAGS", "\\Deleted")
                        deleted += 1
                    except Exception:
                        pass
        try:
            mail.expunge()
        except Exception:
            pass
        print(f"  {folder}: {len(uids)} deleted")

    mail.logout()
    print(f"\n[DONE] {deleted} Temu emails moved to Trash.")


if __name__ == "__main__":
    main()
