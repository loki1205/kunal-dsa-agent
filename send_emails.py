import os
import re
import sqlite3
import smtplib
import ssl
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_env():
    """Local .env file parser fallback."""
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    parts = line.strip().split("=", 1)
                    if len(parts) == 2:
                        os.environ[parts[0].strip()] = parts[1].strip()

def get_db_connection():
    db_path = os.getenv("DB_PATH", "problems.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            status TEXT CHECK(status IN ('new','inprogress','done')) DEFAULT 'new',
            skip_until DATETIME NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    return conn

def evaluate_schedule():
    schedule_mode = os.getenv("SCHEDULE_MODE", "daily").lower()
    if schedule_mode == "weekly":
        current_day = datetime.utcnow().strftime("%a").upper()
        target_day = os.getenv("WEEKLY_DAY", "MON").upper()
        if current_day != target_day:
            print(f"Skipping: Today is {current_day}, weekly execution set for {target_day}.")
            return None
        return int(os.getenv("WEEKLY_COUNT", "20"))
    return int(os.getenv("DAILY_COUNT", "5"))

def fetch_problems(conn, limit):
    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    query = """
        SELECT id, name, url, status FROM problems
        WHERE status != 'done'
        AND (skip_until IS NULL OR skip_until <= ?)
        ORDER BY 
            CASE status WHEN 'inprogress' THEN 1 WHEN 'new' THEN 2 END ASC,
            id ASC
        LIMIT ?
    """
    return conn.execute(query, (now_str, limit)).fetchall()

def generate_email_content(problems):
    """Generates both text fallback and modern dark-theme HTML blocks."""
    # 1. Plain Text Fallback
    text_lines = ["Problem List:\n"]
    if not problems:
        text_lines.append("No items available for today.")
    else:
        for p in problems:
            text_lines.append(f"- (id: {p['id']}) {p['name']} - {p['url']}")
    text_body = "\n".join(text_lines)

    # 2. Modern Dark Theme HTML Layout
    html_items = ""
    if not problems:
        html_items = """
        <div style="background-color: #1e1e24; border: 1px dashed #3f3f46; border-radius: 8px; padding: 24px; text-align: center; color: #a1a1aa;">
            Inbox Zero! No pending problems matching current target criteria.
        </div>"""
    else:
        for p in problems:
            badge_color = "#3b82f6" if p['status'] == "new" else "#10b981"
            html_items += f"""
            <div style="background-color: #1e1e24; border: 1px solid #27272a; border-radius: 8px; padding: 18px; margin-bottom: 14px;">
                <table width="100%" cellspacing="0" cellpadding="0">
                    <tr>
                        <td>
                            <span style="background-color: {badge_color}; color: #ffffff; font-size: 11px; font-weight: bold; text-transform: uppercase; padding: 3px 8px; border-radius: 4px; display: inline-block; margin-bottom: 8px;">
                                {p['status']}
                            </span>
                            <span style="background-color: #3f3f46; color: #e4e4e7; font-size: 11px; font-weight: bold; padding: 3px 8px; border-radius: 4px; display: inline-block; margin-left: 6px; margin-bottom: 8px;">
                                ID: {p['id']}
                            </span>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <h3 style="margin: 4px 0 10px 0; font-size: 18px; font-weight: 600;">
                                <a href="{p['url']}" target="_blank" style="color: #f4f4f5; text-decoration: none;">{p['name']} &rarr;</a>
                            </h3>
                        </td>
                    </tr>
                </table>
            </div>
            """

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 20px 0; background-color: #09090b; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #f4f4f5;">
        <table width="100%" cellspacing="0" cellpadding="0" style="background-color: #09090b;">
            <tr>
                <td align="center">
                    <table width="100%" id="email-container" style="max-width: 600px; background-color: #121214; border: 1px solid #1c1c1f; border-radius: 12px; padding: 32px; text-align: left; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.4);">
                        <tr>
                            <td>
                                <h2 style="margin: 0 0 6px 0; color: #ffffff; font-size: 22px; font-weight: 700; letter-spacing: -0.5px;">💻 DSA Daily Digest</h2>
                                <p style="margin: 0 0 24px 0; color: #71717a; font-size: 14px;">Your deterministic automated data structures & algorithms queue.</p>
                                <hr style="border: 0; border-top: 1px solid #27272a; margin-bottom: 24px;" />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                {html_items}
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <div style="margin-top: 28px; background-color: #18181b; border-radius: 6px; padding: 16px; border: 1px solid #27272a;">
                                    <p style="margin: 0 0 8px 0; font-size: 13px; font-weight: bold; color: #a1a1aa; text-transform: uppercase; letter-spacing: 0.5px;">⚡ Quick Actions</p>
                                    <p style="margin: 0 0 12px 0; font-size: 13px; color: #71717a;">Reply directly to this email using either execution format rule line:</p>
                                    <code style="display: block; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; background-color: #09090b; color: #34d399; padding: 8px; border-radius: 4px; font-size: 13px; margin-bottom: 6px; border: 1px solid #1c1c1f;">[id] - done</code>
                                    <code style="display: block; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; background-color: #09090b; color: #60a5fa; padding: 8px; border-radius: 4px; font-size: 13px; border: 1px solid #1c1c1f;">[id] - skip - [days]</code>
                                </div>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    return text_body, html_body

def main():
    load_env()
    dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
    
    limit = evaluate_schedule()
    if limit is None:
        return

    conn = get_db_connection()
    problems = fetch_problems(conn, limit)
    
    text_content, html_content = generate_email_content(problems)

    if dry_run:
        output_filename = "dry_run_preview.html"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print("--- 🧪 LOCAL DRY RUN ACTIVATED ---")
        print(f"-> Generated structural HTML preview: ./{output_filename}")
        print("-> Database pipeline transactions bypassed. No emails dispatched.")
        conn.close()
        return

    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    email_to = os.getenv("EMAIL_TO")
    subject_prefix = os.getenv("EMAIL_SUBJECT_PREFIX", "DSA Problem")
    
    # 1. Fetch your custom display attributes
    from_name = os.getenv("EMAIL_FROM_NAME", "DSA Daily Digest")
    from_address = os.getenv("EMAIL_FROM_ADDRESS", smtp_user) # Fallback to user if not specified

    msg = MIMEMultipart("alternative")
    
    # 2. Bind the custom alias address string instead of the login username
    msg["From"] = f'"{from_name}" <{from_address}>'
    msg["To"] = email_to
    msg["Subject"] = f"{subject_prefix} of the Day"

    msg.attach(MIMEText(text_content, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, email_to, msg.as_string())

    print(f"Production Email successfully sent with {len(problems)} items.")

    if problems:
        target_ids = [p["id"] for p in problems if p["status"] == "new"]
        if target_ids:
            conn.execute(
                f"UPDATE problems SET status = 'inprogress' WHERE id IN ({','.join(['?']*len(target_ids))})",
                target_ids
            )
            conn.commit()
    
    conn.close()

if __name__ == "__main__":
    main()