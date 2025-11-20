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
        with st.spinner("Loading analysis engine..."):
            st.session_state.analyzer = CryptoAnalyzer()

    if "related_questions" not in st.session_state:
        st.session_state.related_questions = []

    if "current_session_id" not in st.session_state:
        st.session_state.current_session_id = None


def _render_sidebar():
    with st.sidebar:
        st.header("Sessions")
        st.caption(f"Signed in as {st.session_state.username}")

        # Save / update current chat manually (simpler than auto-saving every rerun)
        if st.session_state.messages:
            if st.session_state.current_session_id:
                if st.button("Save current chat"):
                    ok = update_chat_session(
                        st.session_state.current_session_id,
                        st.session_state.messages,
                    )
                    if ok:
                        st.success("Chat updated.")
                    else:
                        st.error("Could not update chat.")
            else:
                if st.button("Save current chat"):
                    chat_name = generate_chat_name(
                        st.session_state.messages,
                        st.session_state.analyzer,
                    )
                    session_id = save_chat_session(
                        st.session_state.user_id,
                        chat_name,
                        st.session_state.messages,
                    )
                    st.session_state.current_session_id = session_id
                    st.success(f"Saved: {chat_name}")

        st.divider()

        sessions = get_user_sessions(st.session_state.user_id)

        if sessions:
            st.subheader("Saved chats")
            for session in sessions:
                session_id, session_name, created_at = session
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(session_name, key=f"load_{session_id}"):
                        loaded_name, messages = load_chat_session(session_id)
                        if loaded_name:
                            st.session_state.messages = messages
                            st.session_state.current_session_id = session_id
                            st.session_state.related_questions = []
                            st.success(f"Loaded: {loaded_name}")
                            st.rerun()
                        else:
                            st.error("Could not load this chat.")
                with col2:
                    if st.button("X", key=f"delete_{session_id}"):
                        if delete_chat_session(session_id):
                            if st.session_state.current_session_id == session_id:
                                st.session_state.current_session_id = None
                                st.session_state.messages = []
                            st.success("Chat deleted.")
                            st.rerun()
                        else:
                            st.error("Could not delete this chat.")
        else:
            st.info("No saved chats yet.")

        st.divider()

        st.subheader("Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("New chat"):
                st.session_state.messages = []
                st.session_state.related_questions = []
                st.session_state.current_session_id = None
                st.rerun()
        with col2:
            if st.button("Clear"):
                st.session_state.messages = []
                st.session_state.related_questions = []
                st.rerun()

        if st.button("Log out"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.user_id = None
            st.session_state.messages = []
            st.session_state.current_session_id = None
            st.rerun()

        st.divider()

        # Related questions / suggestions
        if st.session_state.related_questions:
            st.subheader("Suggested follow-ups")
            for q in st.session_state.related_questions:
                if st.button(q, key=f"suggest_{q}"):
                    st.session_state.messages.append({"role": "user", "content": q})
                    st.rerun()
        else:
            st.subheader("Quick start")
            defaults = [
                "Bitcoin price and news analysis",
                "Ethereum market update with recent news",
                "NEAR protocol price and developments",
                "Current crypto market overview",
            ]
            for q in defaults:
                if st.button(q, key=f"default_{q}"):
                    st.session_state.messages.append({"role": "user", "content": q})
                    st.rerun()


def _render_messages():
    col1, col2, col3 = st.columns([1, 98, 1])
    with col2:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                text = st.session_state.analyzer.clean_text(message["content"])
                st.markdown(text)

                if message["role"] == "assistant":
                    # Prices expander
                    if message.get("prices"):
                        with st.expander("Market prices", expanded=False):
                            for coin in message["prices"]:
                                name = f"{coin['name']} ({coin['symbol']})"
                                price = f"{coin['price']:,.2f}"
                                change = f"{coin['change']:+.2f}%"
                                st.markdown(f"**{name}**")
                                st.markdown(f"Price: {price}  |  Change: {change}")
                                st.divider()

                    # News expander
                    if message.get("news"):
                        with st.expander("News used in analysis", expanded=False):
                            for i, item in enumerate(message["news"][:6]):
                                clean_title = st.session_state.analyzer.clean_text(
                                    item["title"]
                                )
                                st.markdown(f"- {clean_title}")
                                st.caption(
                                    f"{item['source']}  |  Sentiment score: {item['sentiment']:+d}"
                                )
                                if item["url"] and item["url"] != "#":
                                    st.markdown(f"[Open article]({item['url']})")
                                if i < len(message["news"][:6]) - 1:
                                    st.divider()

        # Process last user message if needed
        if st.session_state.messages:
            last = st.session_state.messages[-1]
            if last["role"] == "user" and "processed" not in last:
                st.session_state.messages[-1]["processed"] = True

                with st.chat_message("assistant"):
                    history = []
                    for msg in st.session_state.messages[:-1]:
                        if msg["role"] == "user":
                            history.append(HumanMessage(content=msg["content"]))
                        elif msg["role"] == "assistant":
                            history.append(AIMessage(content=msg["content"]))

                    with st.spinner("Analyzing market data and news..."):
                        response, prices, news, related_questions = (
                            st.session_state.analyzer.analyze(
                                last["content"], history
                            )
                        )

                    st.markdown(response)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                        "prices": prices,
                        "news": news,
                    }
                )
                st.session_state.related_questions = related_questions
                st.rerun()


def _render_input():
    prompt = st.chat_input(
        "Ask about any cryptocurrency (for example: Bitcoin price analysis)"
    )
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()


def _render_footer():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
        **Data sources**
        - CoinGecko
        - CryptoPanic
        - Google Gemini
        """
        )
    with col2:
        st.markdown(
            """
        **What you can do**
        - Check current prices
        - See recent news
        - Ask for short-term outlook
        """
        )
    with col3:
        st.markdown(
            """
        **Tips**
        - Be specific in your questions
        - Ask about multiple coins
        - Ask to connect news and price moves
        """
        )


def render_chat_page():
    st.markdown("## Crypto AI Analyst")
    st.markdown(
        "Ask about cryptocurrencies and get a combined view of prices and recent news."
    )

    _ensure_chat_state()
    _render_sidebar()
    _render_messages()
    _render_input()
    _render_footer()
