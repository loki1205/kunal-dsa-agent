# 💻 DSA Email Scheduler System

A completely self-hosted, **zero-cost**, zero-dependency GitHub-based system that automatically emails you Data Structures & Algorithms problems on a schedule, tracks their progress, and handles interactive email replies to update states.

---

## 🛠️ System Architecture

No backend infrastructure, no dedicated instances, and no paid platforms. The system uses:

* **GitHub Actions**: Triggers daily automated execution loops and processes inbound webhook requests.
* **SQLite (`problems.db`)**: The version-controlled, single source of truth for problem states.
* **Gmail (SMTP)**: Secure outbound delivery system.
* **Google Apps Script**: Listens for inbound email responses and triggers the repository workflow via GitHub's API.

---

## 📊 State Engine & Logic Rules

### Core Database Schema
| Column | Type | Constraints / Default | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique reference identifier |
| `name` | TEXT | NOT NULL | Name of the DSA challenge |
| `url` | TEXT | NOT NULL | Direct link to the problem page |
| `status` | TEXT | CHECK('new', 'inprogress', 'done') DEFAULT 'new' | Internal milestone pointer |
| `skip_until` | DATETIME | NULL | Expiry timestamp for hidden entries |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Table entry creation mark |

### Execution Logic
1.  **Visibility**: A problem is fetched *only* if `status != 'done'` AND (`skip_until` is passed or `NULL`).
2.  **Priority**: Active items are prioritized in strict logical order: `inprogress` first, followed by `new` entries.
3.  **State Upgrades**: As soon as a `new` problem is emailed, its state transitions to `inprogress`. It will cycle through your lists repeatedly until marked as `done`.

---

## ⚡ Quick Actions (Email Replies)

Update problem statuses directly from your mail client. Simply reply to any dispatch email with commands on their own lines:

> **`[id] - done`**
> Marks the entry permanently as `done`. It will never be emailed again.

> **`[id] - skip - [days]`**
> Postpones visibility. Temporarily hides the problem without resetting its core milestone priority.
> *Example: `42 - skip - 7` suppresses problem ID 42 for exactly 7 days.*

---

## 🚀 Setup & Installation

### 1. Initialize Database
Clone this repository to your machine, set up your variables inside a `.env` file, and seed your problem database tracker:
```bash
python seed_db.py