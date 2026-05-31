import os
import re
import sqlite3
from datetime import datetime, timedelta

def load_env():
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, val = line.strip().split("=", 1)
                    os.environ[key.strip()] = val.strip()

def process_payload(body_text):
    db_path = os.getenv("DB_PATH", "problems.db")
    conn = sqlite3.connect(db_path)
    
    # Regex pattern matrices matching input criteria specs
    done_pattern = re.compile(r"^\s*(\d+)\s*-\s*done\s*$", re.IGNORECASE)
    skip_pattern = re.compile(r"^\s*(\d+)\s*-\s*skip\s*-\s*(\d+)\s*$", re.IGNORECASE)

    lines = body_text.splitlines()
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue

        # Parse match candidates safely without breaking core application cycle
        try:
            done_match = done_pattern.match(line_clean)
            if done_match:
                item_id = int(done_match.group(1))
                conn.execute("UPDATE problems SET status = 'done' WHERE id = ?", (item_id,))
                print(f"Processed: Item {item_id} changed status to done.")
                continue

            skip_match = skip_pattern.match(line_clean)
            if skip_match:
                item_id = int(skip_match.group(1))
                days_count = int(skip_match.group(2))
                
                skip_date = (datetime.utcnow() + timedelta(days=days_count)).strftime("%Y-%m-%d %H:%M:%S")
                conn.execute("UPDATE problems SET skip_until = ? WHERE id = ?", (skip_date, item_id))
                print(f"Processed: Item {item_id} suppressed until {skip_date}.")
                continue

        except Exception as e:
            print(f"Skipping malformed evaluation sequence structural line processing error: {e}")
            continue

    conn.commit()
    conn.close()

if __name__ == "__main__":
    load_env()
    # Extracts input via Environment variable parameter injection safely
    raw_payload = os.getenv("EMAIL_BODY_PAYLOAD", "")
    if raw_payload:
        process_payload(raw_payload)
    else:
        print("No input parameter body content detected.")