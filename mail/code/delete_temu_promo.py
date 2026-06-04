# -*- coding: utf-8 -*-
"""
Delete Temu emails in Gmail's Promotions category using X-GM-RAW search.
Targets: category:promotions + temu
"""
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


def fetch_temu_in_folder(mail, folder, search_query):
    """Search and fetch Temu emails in a folder using X-GM-RAW."""
    results = []
    try:
        mail.select(folder)
    except Exception:
        print(f"  SKIP: cannot select {folder}")
        return results

    # Use X-GM-RAW for Gmail native search
    try:
        status, data = mail.uid("SEARCH", None, "X-GM-RAW", search_query)
    except Exception as e:
        print(f"  X-GM-RAW failed for {folder}: {e}, falling back to ALL")
        status, data = mail.uid("SEARCH", None, "ALL")

    if status != "OK" or not data[0]:
        print(f"  No matches in {folder}")
        return results

    uids = data[0].split()
    print(f"  {folder}: {len(uids)} matches for '{search_query}'")

    # Fetch headers
    for start in range(0, len(uids), 200):
        chunk = uids[start:start+200]
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
                # Check if Temu-related
                full_text = f"{subject} {sender}".lower()
                if "temu" in full_text:
                    results.append((uid, subject[:100], sender[:80]))
        except Exception:
            pass
        if len(uids) > 200:
            print(f"    progress: {min(start+200, len(uids))}/{len(uids)}")

    return results


def main():
    print("=" * 60)
    print("Temu Promotions Deleter")
    print(f"Account: {EMAIL}")
    print("=" * 60)

    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)
    print("Connected.\n")

    # Search queries - Gmail native syntax
    queries = [
        "category:promotions Temu",
        "category:promotions temu",
    ]

    all_found = []

    # Search INBOX
    print("--- INBOX ---")
    for q in queries:
        found = fetch_temu_in_folder(mail, "INBOX", q)
        all_found.extend(found)
        if found:
            break  # case-insensitive match should find all

    # Also search All Mail for any that might be only in Promotions
    print("\n--- [Gmail]/All Mail ---")
    try:
        # All Mail folder
        all_mail_names = ["[Gmail]/&YkBnCZCuTvY-", "[Gmail]/All Mail"]
        for name in all_mail_names:
            found = fetch_temu_in_folder(mail, name, "category:promotions temu")
            if found:
                all_found.extend(found)
                break
    except Exception:
        pass

    # Deduplicate by UID
    seen_uids = set()
    unique = []
    for uid, subj, sender in all_found:
        if uid not in seen_uids:
            seen_uids.add(uid)
            unique.append((uid, subj, sender))

    print(f"\n{'='*60}")
    print(f"TOTAL Temu in Promotions: {len(unique)}")
    print(f"{'='*60}")

    if not unique:
        print("None found (likely all already deleted in previous cleanup).")
        mail.logout()
        return

    for uid, subj, sender in unique[:30]:
        print(f"  {sender[:60]} | {subj}")
    if len(unique) > 30:
        print(f"  ... and {len(unique)-30} more")

    # Delete
    print(f"\nDeleting {len(unique)} emails...")

    # Delete from INBOX (where they live)
    mail.select("INBOX")
    uids_only = [u for u, _, _ in unique]
    deleted = 0
    for start in range(0, len(uids_only), 100):
        batch = uids_only[start:start+100]
        uids_str = ",".join(uid for uid in batch)
        try:
            status, _ = mail.uid("STORE", uids_str, "+FLAGS", "\\Deleted")
            if status == "OK":
                deleted += len(batch)
            else:
                for uid in batch:
                    try:
                        mail.uid("STORE", uid, "+FLAGS", "\\Deleted")
                        deleted += 1
                    except Exception:
                        pass
        except Exception:
            for uid in batch:
                try:
                    mail.uid("STORE", uid, "+FLAGS", "\\Deleted")
                    deleted += 1
                except Exception:
                    pass

    mail.expunge()
    mail.logout()
    print(f"\n[DONE] {deleted} Temu Promotions emails deleted.")


if __name__ == "__main__":
    main()
