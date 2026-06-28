import sqlite3
from pathlib import Path

DATABASE = Path("guardian/database/guardian.db")


def get_connection():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS automation_rules(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        trigger TEXT NOT NULL,
        target TEXT NOT NULL,
        action TEXT NOT NULL,
        cooldown INTEGER DEFAULT 300,
        retries INTEGER DEFAULT 3,
        timeout INTEGER DEFAULT 60,
        priority INTEGER DEFAULT 5,
        enabled INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS automation_jobs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_id INTEGER,
        service TEXT,
        status TEXT,
        progress INTEGER DEFAULT 0,
        started_at TEXT,
        finished_at TEXT,
        duration REAL DEFAULT 0,
        exit_code INTEGER,
        FOREIGN KEY(rule_id) REFERENCES automation_rules(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS automation_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        level TEXT,
        message TEXT,
        FOREIGN KEY(job_id) REFERENCES automation_jobs(id)
    )
    """)

    conn.commit()
    conn.close()


init_database()
