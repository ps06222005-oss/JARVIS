# memory.py

import sqlite3
from datetime import datetime

# =========================
# CONNECT DATABASE
# =========================

conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

# =========================
# CREATE TABLES
# =========================

# User Information
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

# Preferences
cursor.execute("""
CREATE TABLE IF NOT EXISTS preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT,
    value TEXT
)
""")

# Chat History
cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT,
    ai_response TEXT,
    time TEXT
)
""")

# Tasks
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    status TEXT
)
""")

conn.commit()

# =========================
# USER NAME
# =========================

def save_user_name(name):

    cursor.execute("DELETE FROM user_info")

    cursor.execute(
        "INSERT INTO user_info(name) VALUES(?)",
        (name,)
    )

    conn.commit()


def get_user_name():

    cursor.execute("SELECT name FROM user_info LIMIT 1")

    data = cursor.fetchone()

    if data:
        return data[0]

    return None


# =========================
# PREFERENCES
# =========================

def save_preference(key, value):

    cursor.execute(
        "INSERT INTO preferences(key, value) VALUES(?, ?)",
        (key, value)
    )

    conn.commit()


def get_preferences():

    cursor.execute("SELECT key, value FROM preferences")

    return cursor.fetchall()


# =========================
# CHAT MEMORY
# =========================

def save_chat(user_message, ai_response):

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO chats(user_message, ai_response, time)
    VALUES (?, ?, ?)
    """, (user_message, ai_response, current_time))

    conn.commit()


def get_chat_history(limit=10):

    cursor.execute("""
    SELECT user_message, ai_response, time
    FROM chats
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    return cursor.fetchall()


# =========================
# TASKS
# =========================

def add_task(task):

    cursor.execute("""
    INSERT INTO tasks(task, status)
    VALUES (?, ?)
    """, (task, "pending"))

    conn.commit()


def complete_task(task_id):

    cursor.execute("""
    UPDATE tasks
    SET status='completed'
    WHERE id=?
    """, (task_id,))

    conn.commit()


def get_tasks():

    cursor.execute("""
    SELECT id, task, status
    FROM tasks
    """)

    return cursor.fetchall()


# =========================
# CLOSE DATABASE
# =========================

def close_db():
    conn.close()


# =========================
# TESTING
# =========================

if __name__ == "__main__":

    save_user_name("Prince")

    save_preference("voice", "male")
    save_preference("theme", "dark")

    save_chat(
        "Hello Jarvis",
        "Hello Prince, how can I help you?"
    )

    add_task("Open YouTube")

    print("\nUser:")
    print(get_user_name("prince"))

    print("\nPreferences:")
    print(get_preferences())

    print("\nChats:")
    print(get_chat_history())

    print("\nTasks:")
    print(get_tasks())

    close_db()