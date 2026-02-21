import streamlit as st
import os


def get_current_user() -> dict | None:
    """
    Get the currently logged-in user.

    On HF Spaces (with hf_oauth: true): reads user info from st.experimental_user.
    Locally: uses a dev user so the app is testable without OAuth.

    Returns dict with 'id' and 'name', or None if not authenticated.
    """
    # Check if running on HF Spaces
    is_hf_space = os.environ.get("SPACE_ID") is not None

    if is_hf_space:
        user_info = st.experimental_user
        if user_info and user_info.get("is_logged_in"):
            return {
                "id": user_info.get("sub", user_info.get("name", "unknown")),
                "name": user_info.get("name", "User"),
            }
        return None
    else:
        # Local development — use a mock user
        return {
            "id": "dev_user",
            "name": "Dev User (local)",
        }


def require_auth() -> dict:
    """
    Gate the app behind authentication.
    Returns user dict if authenticated, otherwise shows login prompt and stops.
    """
    user = get_current_user()

    if user is None:
        st.title("NotebookLM Clone")
        st.info("Please log in with your Hugging Face account to continue.")
        st.stop()

    return user
