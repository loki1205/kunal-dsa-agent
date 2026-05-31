# seed_db.py
import sqlite3

conn = sqlite3.connect("problems.db")
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

# Seed test array data entries
sample_problems = [
    ("Two Sum", "https://leetcode.com/problems/two-sum/"),
    ("Valid Parentheses", "https://leetcode.com/problems/valid-parentheses/"),
    ("Merge Two Sorted Lists", "https://leetcode.com/problems/merge-two-sorted-lists/")
]

conn.executemany("INSERT INTO problems (name, url) VALUES (?, ?)", sample_problems)
conn.commit()
conn.close()
print("Database initialized and populated with basic sample dataset.")