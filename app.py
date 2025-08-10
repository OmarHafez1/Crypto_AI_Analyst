import streamlit as st
from dotenv import load_dotenv

from src.database.connection import init_db
from src.ui.theme import apply_theme

load_dotenv()


def main():
    init_db()

    st.set_page_config(
        page_title="Crypto AI Analyst",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    apply_theme()

    st.title("🚀 Crypto AI Analyst")
    st.write("First skeleton version – chat and AI will be added later.")


if __name__ == "__main__":
    main()
