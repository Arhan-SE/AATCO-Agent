import os
import sqlite3
import asyncio
import json

from mcp import ClientSession
from mcp.client.sse import sse_client

# --- Database functions (from email_saver.py) ---

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

# --- Email trigger logic (from trigger.py) ---

async def check_emails(session):
    try:
        # Use specific Gmail query format
        query = {
            "query": {
                "query": "is:unread"
            },
            "tool": {
                "name": "gmail_find_email",
                "description": "Finds an email message."
            }
        }
        print("\nChecking unread emails...")
        result = await session.call_tool("gmail_find_email", arguments=query)
        
        if result.content:
            # Get the first email's text
            email_text = result.content[0].text
            
            def extract_field(field_name):
                start = email_text.find(f'"{field_name}": "') + len(f'"{field_name}": "')
                end = email_text.find('"', start)
                return email_text[start:end] if start > len(f'"{field_name}": "') else ""
            
            def extract_array(field_name):
                start = email_text.find(f'"{field_name}": [') + len(f'"{field_name}": [')
                end = email_text.find(']', start)
                if start > len(f'"{field_name}": ['):
                    array_text = email_text[start:end]
                    return [item.strip('"') for item in array_text.split(',')]
                return []
            
            # Extract all useful fields
            email_data = {
                "id": extract_field("id"),
                "subject": extract_field("subject"),
                "snippet": extract_field("raw__snippet"),
                "date": extract_field("date"),
                "from_name": extract_field("from__name"),
                "from_email": extract_field("from__email"),
                "to_names": extract_array("to__names"),
                "to_emails": extract_array("to__emails"),
                "body_plain": extract_field("body_plain"),
                "message_id": extract_field("message_id"),
                "thread_id": extract_field("thread_id"),
                "message_url": extract_field("message_url"),
                "labels": extract_array("labels"),
                "attachment_count": extract_field("attachment_count")
            }
            
            print("\nEmail Details:")
            print(f"ID: {email_data['id']}")
            print(f"Subject: {email_data['subject']}")
            print(f"Snippet: {email_data['snippet']}")
            print(f"Date: {email_data['date']}")
            print(f"From: {email_data['from_name']} <{email_data['from_email']}>")
            print(f"To: {', '.join(email_data['to_names'])} <{', '.join(email_data['to_emails'])}>")
            print(f"Message ID: {email_data['message_id']}")
            print(f"Thread ID: {email_data['thread_id']}")
            print(f"Labels: {', '.join(email_data['labels'])}")
            print(f"Attachments: {email_data['attachment_count']}")
            print(f"Message URL: {email_data['message_url']}")
            print(f"Body (Plain): {email_data['body_plain']}")

            # Save email to local database
            save_email(
                message_id=email_data["message_id"],
                subject=email_data["subject"],
                snippet=email_data["snippet"],
                date=email_data["date"],
                from_email=email_data["from_email"],
                attachment_url=None,
                email_url=email_data["message_url"]
            )
        else:
            print("No unread emails found.")
            
    except Exception as e:
        print(f"Error checking emails: {e}")

async def run_email_trigger():
    print("Initializing email trigger.......")
    
    # Connect to the Zapier MCP server using SSE
    async with sse_client("https://actions.zapier.com/mcp/sk-ak-arSsp59aQJioIwJAn60HiMQDLw/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            await check_emails(session)

if __name__ == "__main__":
    asyncio.run(run_email_trigger())