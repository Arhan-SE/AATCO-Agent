import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "emails.db")

def init_db():
    """
    Initialize the SQLite database and create the emails table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            message_id TEXT PRIMARY KEY,
            subject TEXT,
            snippet TEXT,
            date TEXT,
            from_email TEXT,
            attachment_url TEXT,
            email_url TEXT
        )
    """)
    conn.commit()
    conn.close()

def email_exists(message_id):
    """
    Check if an email with the given message_id already exists in the local database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM emails WHERE message_id = ?", (message_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def save_email(
    message_id,
    subject,
    snippet,
    date,
    from_email,
    attachment_url=None,
    email_url=None
):
    """
    Save email data to the local SQLite database if the message_id does not already exist.
    """
    init_db()
    if email_exists(message_id):
        print(f"Email with Message id {message_id} already exists. Skipping save.")
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO emails (message_id, subject, snippet, date, from_email, attachment_url, email_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            message_id,
            subject,
            snippet,
            date,
            from_email,
            attachment_url if attachment_url else "",
            email_url if email_url else ""
        )
    )
    conn.commit()
    conn.close()
    print(f"Email with Message id {message_id} saved successfully.")
    return True
