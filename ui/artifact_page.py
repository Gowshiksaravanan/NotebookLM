import streamlit as st
import uuid
from datetime import datetime
import time


# ── Mock Content ─────────────────────────────────────────────────────────────

MOCK_CONVERSATION_SUMMARY = {
    "brief": """## Conversation Summary (Brief)

**Topics Discussed:**
- Relationship between core variables from Chapter 3
- Three problem-solving methodologies and when to use each
- The three-stage process (initialization → processing → validation)

**Key Questions Asked:**
- What are the main approaches to the problem? → Three methods identified
- How do the lecture notes differ from the textbook? → Application vs. theory

**Unresolved:** No questions remain open from the conversation.
""",
    "detailed": """## Conversation Summary (Detailed)

### Discussion Flow
The conversation covered 4 main exchanges exploring the source material.

### Topics Explored
1. **Core Concepts (Q1-Q2):** User asked about the foundational relationship between variables. The AI identified Chapter 3 as the primary source and highlighted it as a prerequisite for advanced topics.

2. **Methodology Comparison (Q3):** User inquired about different problem-solving approaches. Three methods were identified — direct, iterative, and approximation — with trade-offs explained for each.

3. **Process Stages (Q4):** Discussion about the three-stage process introduced in Week 5 lectures: initialization, processing, and validation.

### Key Insights from Chat
- The direct method is recommended as the starting point for beginners
- Lecture notes and textbook provide complementary perspectives
- Each stage has specific requirements that must be met before proceeding

### Citations Used
| Source | Times Referenced |
|--------|----------------|
| textbook_ch3.pdf | 3 |
| lecture_notes.pdf | 2 |
| week5_slides.pptx | 2 |
| textbook_ch2.pdf | 1 |
""",
}

MOCK_DOCUMENT_SUMMARY = {
    "brief": """## Document Summary (Brief)

**Core Theme:** The sources examine the relationship between key variables and present multiple problem-solving methodologies.

**Key Takeaways:**
- Three approaches exist: direct method, iterative approach, and approximation
- The direct method provides exact results but requires complete data
- A three-stage process (initialization → processing → validation) underpins the framework
- Lecture materials focus on application; textbook provides theoretical depth

**Bottom Line:** Master the direct method first, then explore alternatives as complexity increases.
""",
    "detailed": """## Document Summary (Detailed)

### 1. Foundational Framework
The sources establish a foundational framework centered on the relationship between core variables discussed primarily in Chapter 3. The author emphasizes that a thorough understanding of this relationship is a prerequisite before advancing to more complex topics. The framework operates through a three-stage process:

- **Initialization** — Setting up parameters and base conditions
- **Processing** — Executing the core computational logic
- **Validation** — Verifying outputs meet confidence thresholds

### 2. Methodological Approaches
Three distinct methodological approaches are presented across the sources:

| Method | Best For | Trade-off |
|--------|----------|-----------|
| **Direct** | Complete datasets, exact results needed | Requires full data availability |
| **Iterative** | Incomplete data, convergent solutions | Multiple passes, slower |
| **Approximation** | Quick estimates, non-critical precision | Sacrifices accuracy for speed |

The textbook (Section 2.1) recommends beginners start with the direct method, as it builds intuition for how the formula maps inputs to outputs.

### 3. Cross-Source Analysis
The lecture notes (Week 5) and textbook chapters approach the same material from complementary angles:
- **Lectures** — Emphasize practical application with worked examples
- **Textbook** — Provides theoretical depth, proofs, and edge cases
- **Slides** — Offer visual summaries and quick-reference diagrams

### 4. Key Definitions
- **Confidence threshold** — The minimum acceptable level of certainty for a result
- **Convergence** — The point at which iterative refinements produce negligible improvement
- **Base case** — The simplest instance of a problem used as a starting point

### 5. Conclusion
Mastering these fundamentals is essential before proceeding to advanced modules. The recommended learning path is: direct method → iterative approach → approximation, building complexity gradually.
""",
}

MOCK_PODCAST_SCRIPT = """## Podcast: Deep Dive Study Session

**Alex:** Hey everyone, welcome back to another deep dive study session! I'm Alex, and I'm here with Sam. Today we've got some really meaty material to break down. Sam, I read through the summary and honestly, there's a lot going on. Where do we even start?

**Sam:** Right, so let's zoom out first. The big picture here is about problem-solving methodology — specifically, the idea that there isn't just one way to solve a problem. The sources lay out three distinct approaches, and understanding when to use which one is really the meta-skill they're teaching.

**Alex:** Okay, three approaches. Let's go through them one by one?

**Sam:** Absolutely. So the first one is called the **direct method**. Think of it like having a recipe where you know all the ingredients and all the steps. You plug your values into the formula, follow the steps, and you get your exact answer. Clean, precise, done.

**Alex:** That sounds like the dream scenario. Why doesn't everyone just use that all the time?

**Sam:** Great question — and this is where it gets interesting. The direct method has a strict requirement: you need *complete* data. Every single input has to be known. In academic exercises, sure, they give you everything. But in the real world? You're often working with gaps, estimates, or noisy data.

**Alex:** Ah, so that's where the second approach comes in?

**Sam:** Exactly — the **iterative approach**. Instead of solving it in one shot, you start with your best guess and then keep refining. Each pass gets you closer to the real answer. It's like sculptors — you start with a rough block and keep chipping away until it looks right.

**Alex:** I love that analogy. So how do you know when to stop iterating?

**Sam:** That's actually one of the key concepts — **convergence**. You stop when the difference between iterations becomes so small that it's negligible. The sources define a confidence threshold, and once you're within that threshold, you're done.

**Alex:** Makes sense. And the third method?

**Sam:** **Approximation**. This one is all about pragmatism. Sometimes you don't need five decimal places of precision. You just need a ballpark. Is this going to cost us $100 or $10,000? The approximation method gives you that answer fast, at the cost of some accuracy.

**Alex:** So it's really about matching your tool to the job.

**Sam:** Exactly right. And that's actually what the sources are trying to teach. It's not just "here are three formulas." It's "here's how to think about which tool fits which situation." That metacognitive skill is what separates a good problem-solver from someone who just memorizes formulas.

**Alex:** One thing I noticed in the summary was this three-stage process — initialization, processing, validation. How does that fit in?

**Sam:** Good catch. That process applies to *all three* methods. Regardless of which approach you choose, you always: set up your initial conditions, run the computation, and then validate your results. It's like a universal wrapper around any problem-solving method.

**Alex:** That's a really clean mental model. I wish my professors had explained it that way.

**Sam:** Ha! Well, that's what the lecture notes try to do — they focus on practical application. The textbook goes deeper into the theory and proofs, but the lectures are where you get the worked examples and intuition.

**Alex:** Alright, I think that's a solid overview. Any final advice for students studying this material?

**Sam:** Start with the direct method. Get really comfortable with it. Once you feel solid, move to iterative, then approximation. Don't try to learn all three at once — build up gradually. And always check your work with that validation step.

**Alex:** Brilliant advice. Thanks Sam, and thanks everyone for listening. Until next time — keep studying smart, not just hard!
"""

MOCK_QUIZ = {
    5: """## Practice Quiz (5 Questions)

### Question 1
What is the primary advantage of the direct method?

- A) It works with incomplete data
- B) It provides exact results in a single pass
- C) It is the fastest method
- D) It requires no validation

**Answer: B**
**Explanation:** The direct method applies the formula once to produce exact results, unlike iterative methods that require multiple passes.

---

### Question 2
Which stage comes immediately after initialization in the three-stage process?

- A) Validation
- B) Optimization
- C) Processing
- D) Calibration

**Answer: C**
**Explanation:** The three stages are: initialization → processing → validation.

---

### Question 3
When should the approximation method be preferred?

- A) When working with critical systems
- B) When precision is not the primary concern
- C) When the dataset is very small
- D) When the direct method fails

**Answer: B**
**Explanation:** Approximation trades precision for speed, ideal when exact results aren't required.

---

### Question 4
What does "convergence" refer to in the iterative approach?

- A) The point where the algorithm starts
- B) When iterations produce negligible differences
- C) The final validation step
- D) Combining multiple methods together

**Answer: B**
**Explanation:** Convergence is reached when successive iterations produce results so close together that further refinement is unnecessary.

---

### Question 5
What is the recommended learning order for the three methods?

- A) Approximation → Iterative → Direct
- B) Iterative → Direct → Approximation
- C) Direct → Iterative → Approximation
- D) Any order is equally effective

**Answer: C**
**Explanation:** The textbook recommends starting with the direct method to build intuition, then progressing to iterative and approximation.
""",
    10: """## Practice Quiz (10 Questions)

### Question 1
What is the primary advantage of the direct method?

- A) It works with incomplete data
- B) It provides exact results in a single pass
- C) It is the fastest method
- D) It requires no validation

**Answer: B**

---

### Question 2
Which stage comes immediately after initialization?

- A) Validation
- B) Optimization
- C) Processing
- D) Calibration

**Answer: C**

---

### Question 3
When should the approximation method be preferred?

- A) When working with critical systems
- B) When precision is not the primary concern
- C) When the dataset is very small
- D) When the direct method fails

**Answer: B**

---

### Question 4
What does "convergence" mean in the iterative approach?

- A) The point where the algorithm starts
- B) When iterations produce negligible differences
- C) The final validation step
- D) Combining multiple methods

**Answer: B**

---

### Question 5
What is the recommended learning order?

- A) Approximation → Iterative → Direct
- B) Iterative → Direct → Approximation
- C) Direct → Iterative → Approximation
- D) Any order is fine

**Answer: C**

---

### Question 6
What does the direct method require?

- A) Multiple iterations
- B) Complete data
- C) A confidence threshold
- D) An initial estimate

**Answer: B**

---

### Question 7
What is a "confidence threshold"?

- A) How sure you are about your method choice
- B) The minimum acceptable certainty for a result
- C) The maximum number of iterations
- D) The accuracy of the approximation method

**Answer: B**

---

### Question 8
How do lecture notes differ from the textbook?

- A) Lectures focus on theory, textbook on application
- B) Lectures focus on application, textbook on theory
- C) They cover different topics entirely
- D) There is no significant difference

**Answer: B**

---

### Question 9
What is a "base case" in this context?

- A) The most complex problem instance
- B) The simplest problem instance used as a starting point
- C) The final validated result
- D) A failed iteration

**Answer: B**

---

### Question 10
The three-stage process applies to which methods?

- A) Only the direct method
- B) Only the iterative method
- C) Direct and iterative only
- D) All three methods

**Answer: D**
""",
}


def get_latest_artifact(notebook: dict, artifact_type: str) -> dict | None:
    """Get the most recent artifact of a given type."""
    for artifact in reversed(notebook["artifacts"]):
        if artifact["type"] == artifact_type:
            return artifact
    return None


def get_all_artifacts(notebook: dict, artifact_type: str) -> list[dict]:
    """Get all artifacts of a given type, newest first."""
    return [a for a in reversed(notebook["artifacts"]) if a["type"] == artifact_type]


def generate_mock_artifact(artifact_type: str, **kwargs) -> dict:
    """Simulate artifact generation."""
    time.sleep(1.5)

    if artifact_type == "conversation_summary":
        style = kwargs.get("style", "detailed")
        content = MOCK_CONVERSATION_SUMMARY.get(style, MOCK_CONVERSATION_SUMMARY["detailed"])
        title = f"Conversation Summary ({'Brief' if style == 'brief' else 'Detailed'})"
    elif artifact_type == "document_summary":
        style = kwargs.get("style", "detailed")
        content = MOCK_DOCUMENT_SUMMARY.get(style, MOCK_DOCUMENT_SUMMARY["detailed"])
        title = f"Document Summary ({'Brief' if style == 'brief' else 'Detailed'})"
    elif artifact_type == "podcast":
        content = MOCK_PODCAST_SCRIPT
        title = "Podcast Episode"
    elif artifact_type == "quiz":
        num_q = kwargs.get("num_questions", 5)
        content = MOCK_QUIZ.get(num_q, MOCK_QUIZ[5])
        title = f"Practice Quiz ({num_q}Q)"
    else:
        content = ""
        title = artifact_type

    return {
        "id": str(uuid.uuid4()),
        "type": artifact_type,
        "title": title,
        "content": content,
        "audio_path": None,
        "created_at": datetime.now().isoformat(),
    }


def _render_artifact_card(artifact: dict, index: int, notebook: dict):
    """Render a single artifact with actions."""
    try:
        dt = datetime.fromisoformat(artifact["created_at"])
        time_str = dt.strftime("%b %d at %H:%M")
    except (ValueError, KeyError):
        time_str = ""

    st.markdown(
        f"""
        <div style="
            padding: 4px 0 8px 0;
            font-size: 0.8rem;
            color: #707088;
        ">Generated {time_str}</div>
        """,
        unsafe_allow_html=True,
    )

    # Content
    with st.container(height=400, border=True):
        st.markdown(artifact["content"])

    # Audio player for podcast
    if artifact["type"] == "podcast":
        if artifact.get("audio_path"):
            st.audio(artifact["audio_path"])
        else:
            st.markdown(
                """
                <div style="
                    display: flex; align-items: center; gap: 10px;
                    padding: 12px 16px;
                    background: rgba(102,126,234,0.06);
                    border: 1px solid rgba(102,126,234,0.15);
                    border-radius: 10px;
                    margin-top: 8px;
                ">
                    <span style="font-size: 1.3rem;">🔇</span>
                    <span style="font-size: 0.85rem; color: #8888aa;">
                        Audio player will appear here when TTS is connected.
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Actions
    st.markdown('<div style="margin-top: 8px;"></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 3])
    with c1:
        st.download_button(
            "Download .md",
            data=artifact["content"],
            file_name=f"{artifact['title'].lower().replace(' ', '_')}.md",
            mime="text/markdown",
            key=f"dl_{artifact['id']}",
            use_container_width=True,
        )
    with c2:
        if st.button("Delete", key=f"del_{artifact['id']}", use_container_width=True):
            notebook["artifacts"].remove(artifact)
            st.rerun()


def _render_history(artifacts: list[dict], label: str):
    """Show older artifacts in a collapsed section."""
    if len(artifacts) > 1:
        with st.expander(f"Previous {label} ({len(artifacts) - 1})"):
            for a in artifacts[1:]:
                try:
                    dt = datetime.fromisoformat(a["created_at"])
                    time_str = dt.strftime("%b %d at %H:%M")
                except (ValueError, KeyError):
                    time_str = ""
                st.markdown(f"**{a['title']}** — {time_str}")
                with st.container(height=200, border=True):
                    st.markdown(a["content"])
                c1, c2, c3 = st.columns([1, 1, 4])
                with c1:
                    st.download_button(
                        "Download",
                        data=a["content"],
                        file_name=f"{a['title'].lower().replace(' ', '_')}.md",
                        mime="text/markdown",
                        key=f"dl_hist_{a['id']}",
                        use_container_width=True,
                    )
                with c2:
                    # No delete in history to keep things simple
                    pass


# ── Main Render ──────────────────────────────────────────────────────────────

def render_artifacts(notebook: dict):
    """Render artifact generation with sub-tabs: Summary | Podcast | Quiz."""

    if not notebook["sources"]:
        st.markdown(
            """
            <div class="empty-state">
                <div style="font-size: 3rem; margin-bottom: 16px;">🎯</div>
                <h3>Add sources first</h3>
                <p>Upload documents in the <strong>Sources</strong> tab to unlock<br>
                summary, quiz, and podcast generation.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    tab_summary, tab_podcast, tab_quiz = st.tabs(
        ["  Summary  ", "  Podcast  ", "  Quiz  "]
    )

    # ── SUMMARY TAB ──────────────────────────────────────────────────────────
    with tab_summary:

        # ── Section 1: Conversation Summary ──
        st.markdown(
            """
            <div style="
                display: flex; align-items: center; gap: 10px;
                margin-bottom: 12px;
            ">
                <div style="
                    width: 36px; height: 36px; border-radius: 10px;
                    background: rgba(102,126,234,0.12);
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1.1rem;
                ">💬</div>
                <div>
                    <span style="font-weight:600; font-size:1rem; color:#e0e0f0;">
                        Conversation Summary
                    </span>
                    <p style="font-size:0.82rem; color:#808098; margin:2px 0 0 0;">
                        Summarize your chat history — topics discussed, key insights, and citations used.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        has_messages = len(notebook["messages"]) > 0

        if not has_messages:
            st.markdown(
                """
                <div style="
                    text-align: center; padding: 30px 20px;
                    color: #606078;
                    border: 1px dashed rgba(255,255,255,0.08);
                    border-radius: 14px;
                ">
                    <p style="margin:0;">No conversation yet. Start chatting in the <strong>Chat</strong> tab first.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            col_cs1, col_cs2, col_cs3 = st.columns([2, 2, 2])
            with col_cs1:
                conv_style = st.radio(
                    "Style",
                    ["brief", "detailed"],
                    format_func=lambda x: "Brief" if x == "brief" else "Detailed",
                    horizontal=True,
                    key=f"conv_sum_style_{notebook['id']}",
                )
            with col_cs3:
                st.markdown('<div style="margin-top: 24px;"></div>', unsafe_allow_html=True)
                gen_conv_sum = st.button(
                    "Generate Conversation Summary",
                    type="primary",
                    use_container_width=True,
                    key=f"gen_conv_sum_{notebook['id']}",
                )

            if gen_conv_sum:
                with st.spinner("Summarizing conversation..."):
                    artifact = generate_mock_artifact("conversation_summary", style=conv_style)
                notebook["artifacts"].append(artifact)
                st.rerun()

            conv_summaries = get_all_artifacts(notebook, "conversation_summary")
            if conv_summaries:
                _render_artifact_card(conv_summaries[0], 0, notebook)
                _render_history(conv_summaries, "conversation summaries")

        # ── Divider between sections ──
        st.markdown(
            '<div style="margin: 30px 0; border-top: 1px solid rgba(255,255,255,0.06);"></div>',
            unsafe_allow_html=True,
        )

        # ── Section 2: Document Summary ──
        st.markdown(
            """
            <div style="
                display: flex; align-items: center; gap: 10px;
                margin-bottom: 12px;
            ">
                <div style="
                    width: 36px; height: 36px; border-radius: 10px;
                    background: rgba(34,197,94,0.12);
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1.1rem;
                ">📄</div>
                <div>
                    <span style="font-weight:600; font-size:1rem; color:#e0e0f0;">
                        Document Summary
                    </span>
                    <p style="font-size:0.82rem; color:#808098; margin:2px 0 0 0;">
                        Summarize content from your uploaded sources — key concepts, themes, and connections.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_ds1, col_ds2, col_ds3 = st.columns([2, 2, 2])
        with col_ds1:
            doc_style = st.radio(
                "Style",
                ["brief", "detailed"],
                format_func=lambda x: "Brief (1 page)" if x == "brief" else "Detailed (full analysis)",
                horizontal=True,
                key=f"doc_sum_style_{notebook['id']}",
            )
        with col_ds3:
            st.markdown('<div style="margin-top: 24px;"></div>', unsafe_allow_html=True)
            gen_doc_sum = st.button(
                "Generate Document Summary",
                type="primary",
                use_container_width=True,
                key=f"gen_doc_sum_{notebook['id']}",
            )

        if gen_doc_sum:
            with st.spinner("Analyzing sources and generating summary..."):
                artifact = generate_mock_artifact("document_summary", style=doc_style)
            notebook["artifacts"].append(artifact)
            st.rerun()

        doc_summaries = get_all_artifacts(notebook, "document_summary")
        if doc_summaries:
            _render_artifact_card(doc_summaries[0], 0, notebook)
            _render_history(doc_summaries, "document summaries")

    # ── PODCAST TAB ──────────────────────────────────────────────────────────
    with tab_podcast:
        # Podcast depends on having any summary (conversation or document)
        latest_doc_summary = get_latest_artifact(notebook, "document_summary")
        latest_conv_summary = get_latest_artifact(notebook, "conversation_summary")
        latest_summary = latest_doc_summary or latest_conv_summary
        has_summary = latest_summary is not None

        st.markdown(
            """
            <div style="margin-bottom: 20px;">
                <span style="font-weight:600; font-size:1rem; color:#e0e0f0;">
                    Generate Podcast
                </span>
                <p style="font-size:0.85rem; color:#808098; margin-top:4px;">
                    Create a conversational podcast episode from your summary.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not has_summary:
            # Locked state
            st.markdown(
                """
                <div style="
                    text-align: center;
                    padding: 50px 30px;
                    background: rgba(255,255,255,0.02);
                    border: 1px solid rgba(255,255,255,0.06);
                    border-radius: 16px;
                ">
                    <div style="font-size: 2.5rem; margin-bottom: 16px;">🔒</div>
                    <h3 style="color: #a0a0b8; font-weight: 600; margin-bottom: 8px;">
                        Summary Required
                    </h3>
                    <p style="color: #707088; font-size: 0.9rem; line-height: 1.6;">
                        Generate a summary first in the <strong>Summary</strong> tab.<br>
                        The podcast is created from your summary to ensure accuracy.
                    </p>
                    <div style="
                        margin-top: 20px;
                        display: inline-flex; align-items: center; gap: 8px;
                        padding: 8px 18px;
                        background: rgba(102,126,234,0.08);
                        border: 1px solid rgba(102,126,234,0.15);
                        border-radius: 20px;
                        font-size: 0.82rem;
                        color: #8090d0;
                    ">
                        📝 Summary &nbsp;→&nbsp; 🎙️ Podcast
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # Show which summary will be used
            sum_title = latest_summary["title"]
            try:
                dt = datetime.fromisoformat(latest_summary["created_at"])
                sum_time = dt.strftime("%b %d at %H:%M")
            except (ValueError, KeyError):
                sum_time = ""

            st.markdown(
                f"""
                <div style="
                    display: flex; align-items: center; gap: 12px;
                    padding: 12px 18px;
                    background: rgba(34,197,94,0.06);
                    border: 1px solid rgba(34,197,94,0.15);
                    border-radius: 12px;
                    margin-bottom: 16px;
                ">
                    <span style="font-size: 1.2rem;">📝</span>
                    <div>
                        <span style="font-size: 0.85rem; color: #a0b8a0;">
                            Based on:
                        </span>
                        <strong style="color: #c0e0c0;">{sum_title}</strong>
                        <span style="color: #708070; font-size: 0.8rem;">
                            &nbsp;({sum_time})
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns([3, 1])
            with col2:
                gen_podcast = st.button(
                    "Generate Podcast",
                    type="primary",
                    use_container_width=True,
                    key=f"gen_pod_{notebook['id']}",
                )

            if gen_podcast:
                with st.spinner("Creating podcast script and audio..."):
                    artifact = generate_mock_artifact("podcast")
                notebook["artifacts"].append(artifact)
                st.rerun()

            # Display latest podcast
            podcasts = get_all_artifacts(notebook, "podcast")
            if podcasts:
                st.divider()
                st.markdown(
                    f'<span style="font-weight:600; font-size:0.9rem; color:#b0b0c8;">'
                    f'Latest Podcast</span>',
                    unsafe_allow_html=True,
                )
                _render_artifact_card(podcasts[0], 0, notebook)
                _render_history(podcasts, "podcasts")
            else:
                st.markdown(
                    """
                    <div style="
                        text-align: center; padding: 40px 20px;
                        color: #606078; margin-top: 16px;
                        border: 1px dashed rgba(255,255,255,0.08);
                        border-radius: 14px;
                    ">
                        <div style="font-size: 2rem; margin-bottom: 10px;">🎙️</div>
                        <p>No podcast generated yet.<br>
                        Click <strong>Generate Podcast</strong> to create one from your summary.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ── QUIZ TAB ─────────────────────────────────────────────────────────────
    with tab_quiz:
        st.markdown(
            """
            <div style="margin-bottom: 20px;">
                <span style="font-weight:600; font-size:1rem; color:#e0e0f0;">
                    Generate Quiz
                </span>
                <p style="font-size:0.85rem; color:#808098; margin-top:4px;">
                    Create multiple-choice questions from your sources to test your understanding.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_q1, col_q2, col_q3 = st.columns([2, 2, 2])
        with col_q1:
            num_questions = st.select_slider(
                "Number of questions",
                options=[5, 10],
                value=5,
                key=f"quiz_num_{notebook['id']}",
            )
        with col_q3:
            st.markdown('<div style="margin-top: 24px;"></div>', unsafe_allow_html=True)
            gen_quiz = st.button(
                "Generate Quiz",
                type="primary",
                use_container_width=True,
                key=f"gen_quiz_{notebook['id']}",
            )

        if gen_quiz:
            with st.spinner(f"Generating {num_questions} questions..."):
                artifact = generate_mock_artifact("quiz", num_questions=num_questions)
            notebook["artifacts"].append(artifact)
            st.rerun()

        # Display latest quiz
        quizzes = get_all_artifacts(notebook, "quiz")
        if quizzes:
            st.divider()
            st.markdown(
                f'<span style="font-weight:600; font-size:0.9rem; color:#b0b0c8;">'
                f'Latest Quiz</span>',
                unsafe_allow_html=True,
            )
            _render_artifact_card(quizzes[0], 0, notebook)
            _render_history(quizzes, "quizzes")
        else:
            st.markdown(
                """
                <div style="
                    text-align: center; padding: 40px 20px;
                    color: #606078; margin-top: 16px;
                    border: 1px dashed rgba(255,255,255,0.08);
                    border-radius: 14px;
                ">
                    <div style="font-size: 2rem; margin-bottom: 10px;">❓</div>
                    <p>No quiz generated yet.<br>
                    Choose the number of questions and click <strong>Generate Quiz</strong>.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
