import os
import psycopg2
import psycopg2.extras
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    if "db" in st.secrets:
        db_conf = st.secrets["db"]
        return psycopg2.connect(
            host=db_conf["DB_HOST"],
            database=db_conf["DB_NAME"],
            user=db_conf["DB_USER"],
            password=db_conf["DB_PASSWORD"],
            port=db_conf.get("DB_PORT", "5432"),
            sslmode=db_conf.get("DB_SSLMODE", "require"),
        )

    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "crypto_ai"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        port=os.getenv("DB_PORT", "5432"),
    )


def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        conn.commit()
    except Exception as e:
        st.error(f"DB init failed: {e!r}")
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass
