import streamlit as st


def apply_theme():
    st.markdown(
        """
    <style>
    /* Main theme colors */
    :root {
        --primary: #6366F1;
        --primary-dark: #4F46E5;
        --secondary: #10B981;
        --accent: #F59E0B;
        --background: #0F172A;
        --surface: #1E293B;
        --text-primary: #F1F5F9;
        --text-secondary: #94A3B8;
        --border: #334155;
    }

    /* Main container */
    .main {
        background: linear-gradient(135deg, var(--background) 0%, #1E1B4B 100%);
        color: var(--text-primary);
    }

    /* Headers */
    .main-header {
        font-size: 3rem;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 2rem 0;
        font-weight: 800;
        letter-spacing: -0.02em;
    }

    .sub-header {
        text-align: center;
        color: var(--text-secondary);
        margin-bottom: 3rem;
        font-size: 1.3rem;
        font-weight: 300;
    }

    /* Sidebar styling */
    .css-1d391kg, .css-1lcbmhc {
        background: var(--surface) !important;
        border-right: 1px solid var(--border);
    }

    /* Chat messages with beautiful bubbles */
    .stChatMessage {
        padding: 1rem 0;
    }

    [data-testid="stChatMessage"] {
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        border: 1px solid var(--border);
    }

    /* User message bubble */
    [data-testid="stChatMessage"][data-message-author="user"] {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
        margin-left: 2rem;
        border-bottom-right-radius: 5px;
    }

    /* Assistant message bubble */
    [data-testid="stChatMessage"][data-message-author="assistant"] {
        background: var(--surface);
        color: var(--text-primary);
        margin-right: 2rem;
        border-bottom-left-radius: 5px;
    }

    /* Chat input */
    .stChatInput {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .stChatInput input {
        background: transparent !important;
        color: var(--text-primary) !important;
        font-size: 1.1rem;
        border: none !important;
        box-shadow: none !important;
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }

    /* Sidebar buttons */
    .sidebar-button {
        width: 100%;
        margin: 0.3rem 0;
        text-align: left;
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-primary) !important;
    }

    .sidebar-button:hover {
        background: var(--primary) !important;
        color: white !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: var(--surface) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px;
        font-weight: 600;
    }

    .streamlit-expanderContent {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px;
    }

    /* Cards for prices and news */
    .price-card {
        background: var(--surface);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid var(--border);
        margin: 0.5rem 0;
    }

    .news-card {
        background: var(--surface);
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid var(--border);
        margin: 0.8rem 0;
        transition: all 0.3s ease;
    }

    .news-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }

    /* Success messages */
    .stSuccess {
        background: linear-gradient(135deg, var(--secondary) 0%, #059669 100%);
        color: white;
        border-radius: 12px;
        border: none;
    }

    /* Session list items */
    .session-item {
        background: var(--surface);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid var(--border);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .session-item:hover {
        background: var(--primary);
        color: white;
    }

    /* Progress and loading */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--surface);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-dark);
    }

    /* Text sizes */
    .stChatMessage {
        font-size: 1.1rem;
        line-height: 1.6;
    }

    .stExpander {
        font-size: 0.95rem;
    }

    .stButton button {
        font-size: 0.95rem;
    }

    .stTextInput input {
        font-size: 1rem;
    }

    .stSidebar {
        font-size: 0.9rem;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
