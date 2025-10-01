import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from src.ai.analyzer import CryptoAnalyzer
from src.chat_store.store import (
    generate_chat_name,
    save_chat_session,
    update_chat_session,
    get_user_sessions,
    load_chat_session,
    delete_chat_session,
)


def _ensure_chat_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "analyzer" not in st.session_state:
        with st.spinner("🔄 Loading cryptocurrency intelligence engine..."):
            st.session_state.analyzer = CryptoAnalyzer()

    if "related_questions" not in st.session_state:
        st.session_state.related_questions = []

    if "current_session_id" not in st.session_state:
        st.session_state.current_session_id = None
