import streamlit as st

from src.auth.authentication import create_user, verify_user, get_user_id


def render_auth_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            '<h1 class="main-header">🚀 Crypto AI Analyst</h1>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="sub-header">Intelligent cryptocurrency market analysis powered by AI</p>',
            unsafe_allow_html=True,
        )

        tab1, tab2 = st.tabs(["🔐 **Login**", "📝 **Sign Up**"])

        # -------- LOGIN --------
        with tab1:
            st.markdown("### Welcome Back")
            with st.form("login_form"):
                login_username = st.text_input(
                    "👤 Username", placeholder="Enter your username"
                )
                login_password = st.text_input(
                    "🔒 Password",
                    type="password",
                    placeholder="Enter your password",
                )
                login_btn = st.form_submit_button(
                    "🚀 Login to Dashboard", use_container_width=True
                )

                if login_btn:
                    if verify_user(login_username, login_password):
                        st.session_state.authenticated = True
                        st.session_state.username = login_username
                        st.session_state.user_id = get_user_id(login_username)
                        st.success("🎉 Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")

        # -------- SIGN UP --------
        with tab2:
            st.markdown("### Create Account")
            with st.form("signup_form"):
                signup_username = st.text_input(
                    "👤 Choose Username", placeholder="Enter username"
                )
                signup_email = st.text_input(
                    "📧 Email (optional)", placeholder="your.email@example.com"
                )
                signup_password = st.text_input(
                    "🔒 Choose Password",
                    type="password",
                    placeholder="Minimum 6 characters",
                )
                confirm_password = st.text_input(
                    "✅ Confirm Password",
                    type="password",
                    placeholder="Re-enter your password",
                )
                signup_btn = st.form_submit_button(
                    "✨ Create Account", use_container_width=True
                )

                if signup_btn:
                    if signup_password != confirm_password:
                        st.error("❌ Passwords do not match")
                    elif len(signup_password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    elif create_user(
                        signup_username, signup_password, signup_email
                    ):
                        st.success("✅ Account created successfully! Please login.")
                    else:
                        st.error("❌ Username already exists")
