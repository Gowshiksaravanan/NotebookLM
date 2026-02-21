import streamlit as st
import uuid
from datetime import datetime
import random
import time


# ── Mock responses ───────────────────────────────────────────────────────────
MOCK_RESPONSES = [
    {
        "content": (
            "Based on the uploaded sources, the key concept revolves around "
            "the relationship between the variables discussed in Chapter 3. "
            "The author emphasizes that understanding this foundation is critical "
            "before moving to advanced topics."
        ),
        "citations": [
            {"source": "lecture_notes.pdf", "page": 3, "text": "the relationship between variables..."},
            {"source": "textbook_ch3.pdf", "page": 42, "text": "understanding this foundation..."},
        ],
    },
    {
        "content": (
            "The sources indicate three main approaches to this problem:\n\n"
            "1. **Direct method** — Apply the formula from Section 2.1\n"
            "2. **Iterative approach** — Build up from base cases\n"
            "3. **Approximation** — Use the simplified model when precision isn't critical\n\n"
            "The textbook recommends starting with the direct method for beginners."
        ),
        "citations": [
            {"source": "textbook_ch2.pdf", "page": 15, "text": "direct method... apply the formula"},
        ],
    },
    {
        "content": (
            "I couldn't find specific information about that topic in your "
            "uploaded sources. Try uploading additional materials that cover this "
            "subject, or rephrase your question to relate more closely to the "
            "content in your current sources."
        ),
        "citations": [],
    },
    {
        "content": (
            "Great question! According to the lecture slides, this concept "
            "was introduced in Week 5. The key takeaway is that the process involves "
            "three stages: **initialization**, **processing**, and **validation**. "
            "Each stage has specific requirements that must be met before proceeding."
        ),
        "citations": [
            {"source": "week5_slides.pptx", "page": 8, "text": "three stages: initialization..."},
            {"source": "week5_slides.pptx", "page": 12, "text": "specific requirements..."},
        ],
    },
]


def get_mock_response(query: str) -> dict:
    """Simulate a RAG response. Will be replaced with actual RAG pipeline."""
    time.sleep(1.2)
    return random.choice(MOCK_RESPONSES)


def render_chat(notebook: dict):
    """Render the chat interface."""

    source_count = len(notebook["sources"])

    # ── No sources warning ──
    if source_count == 0:
        st.markdown(
            """
            <div style="
                padding: 14px 20px;
                background: rgba(234,179,8,0.08);
                border: 1px solid rgba(234,179,8,0.2);
                border-radius: 12px;
                color: #d4a017;
                font-size: 0.9rem;
                margin-bottom: 16px;
            ">
                Upload sources in the <strong>Sources</strong> tab to start chatting with your documents.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Chat history ──
    chat_container = st.container(height=480)

    with chat_container:
        if not notebook["messages"]:
            st.markdown(
                """
                <div class="empty-state" style="padding: 80px 20px;">
                    <div style="font-size: 3rem; margin-bottom: 16px;">💬</div>
                    <h3>Start a conversation</h3>
                    <p>Ask questions about your uploaded sources.<br>
                    The AI will answer using only your documents<br>
                    and provide citations for every claim.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for msg in notebook["messages"]:
                avatar = "🧑" if msg["role"] == "user" else "🤖"
                with st.chat_message(msg["role"], avatar=avatar):
                    st.markdown(msg["content"])

                    # Citations
                    if msg["role"] == "assistant" and msg.get("citations"):
                        citations_html = ""
                        for cite in msg["citations"]:
                            citations_html += (
                                f'<span class="citation-chip">'
                                f'📄 {cite["source"]} &middot; p.{cite["page"]}'
                                f'</span>'
                            )
                        st.markdown(
                            f'<div style="margin-top: 10px;">{citations_html}</div>',
                            unsafe_allow_html=True,
                        )
                        # Expandable full citation text
                        with st.expander("View cited passages"):
                            for cite in msg["citations"]:
                                st.markdown(
                                    f'> *"{cite["text"]}"*\n>\n'
                                    f'> — **{cite["source"]}**, page {cite["page"]}'
                                )

    # ── Chat input ──
    if prompt := st.chat_input(
        "Ask a question about your sources...",
        key=f"chat_input_{notebook['id']}",
    ):
        user_msg = {
            "id": str(uuid.uuid4()),
            "role": "user",
            "content": prompt,
            "citations": [],
            "created_at": datetime.now().isoformat(),
        }
        notebook["messages"].append(user_msg)

        with st.spinner("Thinking..."):
            response = get_mock_response(prompt)

        assistant_msg = {
            "id": str(uuid.uuid4()),
            "role": "assistant",
            "content": response["content"],
            "citations": response["citations"],
            "created_at": datetime.now().isoformat(),
        }
        notebook["messages"].append(assistant_msg)
        st.rerun()

    # ── Controls ──
    if notebook["messages"]:
        cols = st.columns([5, 1])
        with cols[1]:
            if st.button("Clear chat", use_container_width=True):
                notebook["messages"] = []
                st.rerun()
