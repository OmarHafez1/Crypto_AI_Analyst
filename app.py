import streamlit as st
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage
from src.ai.analyzer import CryptoAnalyzer

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
    st.write("Ask anything about crypto prices and news.")

    # Display history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle new user input
    if prompt := st.chat_input("Ask about any cryptocurrency..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            history = []
            for m in st.session_state.messages[:-1]:
                if m["role"] == "user":
                    history.append(HumanMessage(content=m["content"]))
                else:
                    history.append(AIMessage(content=m["content"]))

            response, _, _, _ = st.session_state.analyzer.analyze(prompt, history)
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "analyzer" not in st.session_state:
        st.session_state.analyzer = CryptoAnalyzer()

if __name__ == "__main__":
    main()
