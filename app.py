import streamlit as st
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage
from src.ai.analyzer import CryptoAnalyzer

from src.database.connection import init_db
from src.ui.theme import apply_theme
from src.ui.chat_page import render_chat_page

from src.auth.authentication import create_user, verify_user, get_user_id

load_dotenv()

def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = None

def main():
    init_db()

    st.set_page_config(
        page_title="Crypto AI Analyst",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded",
    )


    apply_theme()
    init_session_state()

    if not st.session_state.authenticated:
        render_auth_page()
    else:
        render_chat_page()

if __name__ == "__main__":
    main()
