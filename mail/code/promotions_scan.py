# -*- coding: utf-8 -*-
"""Clean up all Gmail Promotions category emails."""
import imaplib, email, sys, io, re
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone, timedelta
from collections import defaultdict

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
mail.select("INBOX")

# Try X-GM-RAW with non-UID SEARCH
print("Searching for category:promotions...")
try:
    status, data = mail.search(None, "X-GM-RAW", "category:promotions")
    if status == "OK":
        promo_ids = data[0].split()
        print(f"Found {len(promo_ids)} promotions emails via X-GM-RAW")
    else:
        print("X-GM-RAW search failed")
        promo_ids = []
except Exception as e:
    print(f"X-GM-RAW error: {e}")
    promo_ids = []

if not promo_ids:
    print("\nTrying alternative: scanning ALL INBOX with Gmail category headers...")
    # Fallback: fetch all and check X-GM-LABELS for \\Promotions
    status, data = mail.uid("SEARCH", None, "ALL")
    all_uids = data[0].split()
    print(f"Total INBOX: {len(all_uids)}, scanning with X-GM-LABELS...")

    promo_uids = []
    for start in range(0, len(all_uids), 300):
        chunk = all_uids[start:start+300]
        uids_str = ",".join(uid.decode() for uid in chunk)
        try:
            status, data = mail.uid("FETCH", uids_str, "(RFC822.HEADER X-GM-LABELS)")
            if status != "OK": continue
            for i in range(0, len(data), 2):
                if i >= len(data): break
                resp = data[i]
                if not isinstance(resp, tuple): continue
                resp_text = resp[0].decode(errors="replace")
                m = re.search(r'UID\s+(\d+)', resp_text)
                if not m: continue
                uid = m.group(1)
                # Check for Promotions category in X-GM-LABELS
                has_promo = False
                for line in resp_text.split("\r\n"):
                    if "X-GM-LABELS" in line:
                        labels = line.lower()
                        if "promotion" in labels or "\\\\promotions" in labels.replace("\\\\","\\"):
                            has_promo = True
                        break
                if has_promo:
                    promo_uids.append(uid)
        except: pass
        if (start // 300) % 5 == 0:
            print(f"  progress: {min(start+300, len(all_uids))}/{len(all_uids)}, found {len(promo_uids)}")

    print(f"Found {len(promo_uids)} promotions via X-GM-LABELS")
    promo_ids = [uid.encode() for uid in promo_uids]

if not promo_ids:
    print("\nNo promotions emails found. Your account may not have category tabs enabled.")
    print("Falling back to full ad-style scan on remaining inbox...")

    # Full scan approach
    AD_KW = ["unsubscribe", "discount", "sale", "deal", "promo", "coupon",
             "save", "shop now", "newsletter", "weekly", "flash sale",
             "free shipping", "don't miss", "act now", "last chance",
             "rewards", "cashback", "subscribe"]
    AD_SENDER_KW = ["noreply", "no-reply", "newsletter", "marketing", "mailer",
                    "info@", "hello@", "team@"]
    TRUSTED = ["github.com", "google.com", "googlemail.com", "gmail.com",
               "microsoft.com", "apple.com"]

    mail.select("INBOX")
    status, data = mail.uid("SEARCH", None, "ALL")
    all_uids = data[0].split()
    print(f"INBOX: {len(all_uids)} total")

    promo_uids = []
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
                subject = decode_mime(msg.get("Subject", "")).lower()
                sender = decode_mime(msg.get("From", "")).lower()
                if "<" in sender:
                    addr = sender.split("<")[1].split(">")[0]
                else:
                    addr = sender.strip()
                domain = addr.split("@")[1] if "@" in addr else ""

                # Skip trusted
                if any(t in domain for t in TRUSTED): continue

                score = 0
                if any(kw in subject for kw in AD_KW): score += 2
                if any(kw in sender for kw in AD_SENDER_KW): score += 1
                if any(kw in domain for kw in AD_SENDER_KW): score += 1
                if score >= 2:
                    promo_uids.append(uid)
        except: pass
        if (start // 300) % 5 == 0:
            print(f"  progress: {min(start+300, len(all_uids))}/{len(all_uids)}, found {len(promo_uids)}")

    promo_ids = [uid.encode() for uid in promo_uids]
    print(f"Found {len(promo_ids)} ad/promotion emails via heuristic scan")

# Show summary by sender
print(f"\nTotal: {len(promo_ids)} promotions emails")
print("\nDeleting...")

if promo_ids:
    mail.select("INBOX")
    deleted = 0
    for start in range(0, len(promo_ids), 100):
        batch = promo_ids[start:start+100]
        ids_str = ",".join(mid.decode() if isinstance(mid, bytes) else mid for mid in batch)
        try:
            status, _ = mail.store(ids_str, "+FLAGS", "\\Deleted")
            if status == "OK": deleted += len(batch)
            else:
                for mid in batch:
                    try:
                        s, _ = mail.store(mid, "+FLAGS", "\\Deleted")
                        if s == "OK": deleted += 1
                    except: pass
        except:
            for mid in batch:
                try:
                    mail.store(mid, "+FLAGS", "\\Deleted")
                    deleted += 1
                except: pass
    mail.expunge()

mail.logout()
print(f"[DONE] {deleted} promotions emails deleted.")
if not promo_ids:
    print("No promotions emails found.")
