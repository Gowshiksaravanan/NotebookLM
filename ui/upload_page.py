import streamlit as st
import uuid
from datetime import datetime


ALLOWED_TYPES = ["pdf", "pptx", "txt"]
MAX_FILE_SIZE_MB = 15
MAX_SOURCES_PER_NOTEBOOK = 20

FILE_TYPE_CONFIG = {
    "pdf": {"icon": "📕", "color": "239,68,68", "label": "PDF"},
    "pptx": {"icon": "📊", "color": "249,115,22", "label": "PPTX"},
    "txt": {"icon": "📝", "color": "59,130,246", "label": "TXT"},
    "url": {"icon": "🌐", "color": "34,197,94", "label": "URL"},
    "youtube": {"icon": "🎬", "color": "239,68,68", "label": "YouTube"},
}


def render_sources(notebook: dict):
    """Render source upload and management."""

    total = len(notebook["sources"])
    remaining = MAX_SOURCES_PER_NOTEBOOK - total

    # ── Header with count ──
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:20px;">
            <div>
                <span style="font-size:1.1rem; font-weight:600; color:#e0e0f0;">Sources</span>
                <span style="
                    margin-left: 10px;
                    padding: 3px 10px;
                    background: rgba(102,126,234,0.15);
                    color: #8090d0;
                    border-radius: 12px;
                    font-size: 0.8rem;
                    font-weight: 600;
                ">{total} / {MAX_SOURCES_PER_NOTEBOOK}</span>
            </div>
            <span style="font-size:0.8rem; color:#606078;">{remaining} slots remaining</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Upload section ──
    col_upload, col_url = st.columns([1, 1], gap="large")

    with col_upload:
        st.markdown(
            '<p style="font-weight:600; font-size:0.9rem; color:#b0b0c8; margin-bottom:8px;">'
            "Upload Files</p>",
            unsafe_allow_html=True,
        )
        uploaded_files = st.file_uploader(
            "Drop files here",
            type=ALLOWED_TYPES,
            accept_multiple_files=True,
            help=f"PDF, PPTX, TXT — max {MAX_FILE_SIZE_MB}MB each",
            key=f"uploader_{notebook['id']}",
            label_visibility="collapsed",
        )

        if uploaded_files:
            for f in uploaded_files:
                existing_names = [s["filename"] for s in notebook["sources"]]
                if f.name in existing_names:
                    continue
                if len(notebook["sources"]) >= MAX_SOURCES_PER_NOTEBOOK:
                    st.error(f"Limit of {MAX_SOURCES_PER_NOTEBOOK} sources reached.")
                    break

                file_size_mb = f.size / (1024 * 1024)
                if file_size_mb > MAX_FILE_SIZE_MB:
                    st.error(f"**{f.name}** is too large ({file_size_mb:.1f}MB).")
                    continue

                source = {
                    "id": str(uuid.uuid4()),
                    "filename": f.name,
                    "file_type": f.name.rsplit(".", 1)[-1].lower(),
                    "size_mb": round(file_size_mb, 2),
                    "chunk_count": 0,
                    "status": "ready",
                    "error_message": None,
                    "created_at": datetime.now().isoformat(),
                }
                notebook["sources"].append(source)
                st.toast(f"Added {f.name}", icon="✅")

    with col_url:
        st.markdown(
            '<p style="font-weight:600; font-size:0.9rem; color:#b0b0c8; margin-bottom:8px;">'
            "Add Web Source</p>",
            unsafe_allow_html=True,
        )
        url_input = st.text_input(
            "URL",
            placeholder="https://example.com  or  YouTube link",
            label_visibility="collapsed",
            key=f"url_input_{notebook['id']}",
        )
        if st.button("Add URL", use_container_width=True, type="primary"):
            if not url_input.strip():
                st.warning("Enter a URL.")
            elif len(notebook["sources"]) >= MAX_SOURCES_PER_NOTEBOOK:
                st.error(f"Limit of {MAX_SOURCES_PER_NOTEBOOK} sources reached.")
            else:
                url = url_input.strip()
                existing_urls = [s.get("source_url") for s in notebook["sources"]]
                if url in existing_urls:
                    st.warning("Already added.")
                else:
                    is_youtube = "youtube.com" in url or "youtu.be" in url
                    file_type = "youtube" if is_youtube else "url"
                    display_name = url[:55] + "..." if len(url) > 55 else url

                    source = {
                        "id": str(uuid.uuid4()),
                        "filename": display_name,
                        "file_type": file_type,
                        "size_mb": None,
                        "source_url": url,
                        "chunk_count": 0,
                        "status": "ready",
                        "error_message": None,
                        "created_at": datetime.now().isoformat(),
                    }
                    notebook["sources"].append(source)
                    st.toast(f"Added {file_type} source", icon="✅")
                    st.rerun()

    # ── Source list ──
    st.divider()

    if not notebook["sources"]:
        st.markdown(
            """
            <div style="
                text-align: center; padding: 50px 20px;
                color: #606078;
            ">
                <div style="font-size: 3rem; margin-bottom: 16px;">📄</div>
                <h3 style="color: #a0a0b8; font-weight: 600;">No sources yet</h3>
                <p style="font-size: 0.9rem;">Upload documents or add web links above.<br>
                Your sources power the AI chat and artifact generation.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f'<p style="font-weight:600; font-size:0.9rem; color:#a0a0b8; margin-bottom:12px;">'
        f'Your Sources ({len(notebook["sources"])})</p>',
        unsafe_allow_html=True,
    )

    for i, source in enumerate(notebook["sources"]):
        ft = source["file_type"]
        cfg = FILE_TYPE_CONFIG.get(ft, {"icon": "📄", "color": "150,150,170", "label": ft.upper()})

        meta_parts = [cfg["label"]]
        if source.get("size_mb"):
            meta_parts.append(f"{source['size_mb']} MB")
        if source["chunk_count"] > 0:
            meta_parts.append(f"{source['chunk_count']} chunks")
        meta_str = " · ".join(meta_parts)

        status = source["status"]

        with st.container(border=True):
            col_icon, col_info, col_status, col_del = st.columns([0.5, 4, 1.2, 0.8])

            with col_icon:
                st.markdown(
                    f'<div style="font-size:1.8rem; text-align:center; padding-top:4px;">'
                    f'{cfg["icon"]}</div>',
                    unsafe_allow_html=True,
                )

            with col_info:
                st.markdown(f"**{source['filename']}**")
                st.caption(meta_str)

            with col_status:
                if status == "ready":
                    st.success("Ready")
                elif status == "processing":
                    st.warning("Processing")
                elif status == "failed":
                    st.error("Failed")

            with col_del:
                st.markdown('<div style="padding-top:8px;"></div>', unsafe_allow_html=True)
                if st.button("X", key=f"rm_{source['id']}", help="Remove source"):
                    notebook["sources"].pop(i)
                    st.rerun()
