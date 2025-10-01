import re
from datetime import datetime

import psycopg2
import psycopg2.extras
from langchain_core.messages import HumanMessage

from src.database.connection import get_db_connection


def generate_chat_name(messages, analyzer) -> str:
    """Generate a meaningful chat name using AI based on conversation content"""
    if not messages or len(messages) < 2:
        return f"Chat_{datetime.now().strftime('%Y-%m-%d %H:%M')}"

    first_user_message = ""
    for msg in messages:
        if msg["role"] == "user":
            first_user_message = msg["content"]
            break

    if not first_user_message:
        return f"Chat_{datetime.now().strftime('%Y-%m-%d %H:%M')}"

    prompt = f"""Based on this cryptocurrency question: "{first_user_message}"

Generate a short, descriptive chat session name (max 4-5 words) that captures the main topic.
Examples:
- "Bitcoin price analysis" -> "Bitcoin Market Analysis"
- "Ethereum news and price" -> "Ethereum News Update" 
- "NEAR protocol developments" -> "NEAR Protocol Review"
- "General crypto market" -> "Market Overview"

Return only the session name, no quotes or explanations:"""

    try:
        response = analyzer.ai.invoke([HumanMessage(content=prompt)])
        name = response.content.strip()
        name = re.sub(r'["\']', "", name)
        if len(name) > 50:
            name = name[:47] + "..."
        return name if name else f"Chat_{datetime.now().strftime('%Y-%m-%d %H:%M')}"
    except Exception:
        return f"Chat_{datetime.now().strftime('%Y-%m-%d %H:%M')}"


def save_chat_session(user_id, session_name, messages):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO chat_sessions (user_id, session_name) VALUES (%s, %s) RETURNING id",
            (user_id, session_name),
        )
        session_id = cur.fetchone()[0]

        for msg in messages:
            prices_str = str(msg.get("prices", [])) if "prices" in msg else None
            news_str = str(msg.get("news", [])) if "news" in msg else None

            cur.execute(
                """
                INSERT INTO messages (session_id, role, content, prices, news)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (session_id, msg["role"], msg["content"], prices_str, news_str),
            )

        conn.commit()
        return session_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def update_chat_session(session_id, messages) -> bool:
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM messages WHERE session_id = %s", (session_id,))

        for msg in messages:
            prices_str = str(msg.get("prices", [])) if "prices" in msg else None
            news_str = str(msg.get("news", [])) if "news" in msg else None

            cur.execute(
                """
                INSERT INTO messages (session_id, role, content, prices, news)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (session_id, msg["role"], msg["content"], prices_str, news_str),
            )

        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()


def get_user_sessions(user_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT id, session_name, created_at
        FROM chat_sessions
        WHERE user_id = %s
        ORDER BY created_at DESC
        """,
        (user_id,),
    )
    sessions = cur.fetchall()
    cur.close()
    conn.close()
    return sessions


def load_chat_session(session_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute("SELECT session_name FROM chat_sessions WHERE id = %s", (session_id,))
        session_result = cur.fetchone()
        if not session_result:
            return None, []

        session_name = session_result["session_name"]

        cur.execute(
            """
            SELECT role, content, prices, news
            FROM messages
            WHERE session_id = %s
            ORDER BY created_at ASC
            """,
            (session_id,),
        )

        messages = []
        for row in cur.fetchall():
            message = {
                "role": row["role"],
                "content": row["content"],
            }

            if row["prices"]:
                try:
                    message["prices"] = eval(row["prices"])
                except Exception:
                    message["prices"] = []

            if row["news"]:
                try:
                    message["news"] = eval(row["news"])
                except Exception:
                    message["news"] = []

            messages.append(message)

        return session_name, messages
    finally:
        cur.close()
        conn.close()


def delete_chat_session(session_id) -> bool:
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM chat_sessions WHERE id = %s", (session_id,))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()
