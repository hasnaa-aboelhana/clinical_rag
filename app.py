import streamlit as st

from rag_engine import retrieve


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="404: Hallucination Not Found",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       COLOR PALETTE
       ====================================================== */

    :root {
        --green: #3D6B5C;
        --blue-gray: #5C747D;
        --cream: #F4F1EA;
        --dark: #26352F;
        --muted: #687873;
        --white: #FFFFFF;
        --border: #D9DDD7;
        --soft-green: #E7EEE9;
        --soft-blue: #E8EEF0;
    }


    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {
        background-color: var(--cream);
        color: var(--dark);
    }

    .main .block-container {
        max-width: 1150px;
        padding-top: 35px;
        padding-bottom: 60px;
    }

    [data-testid="stDecoration"] {
        display: none;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background-color: var(--green);
        border-right: none;
    }

    section[data-testid="stSidebar"] .block-container {
        padding: 30px 22px;
    }

    section[data-testid="stSidebar"] p {
        color: #DCE6E1 !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.18) !important;
    }

    .sidebar-logo {
        color: #FFFFFF;
        font-size: 22px;
        font-weight: 800;
        line-height: 1.2;
        letter-spacing: -0.6px;
        margin-bottom: 7px;
    }

    .sidebar-logo span {
        color: #C9DDD5;
    }

    .sidebar-description {
        color: #D5E2DD;
        font-size: 12px;
        line-height: 1.5;
        margin-bottom: 25px;
    }

    .sidebar-heading {
        color: #BFD3CB;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    .sidebar-item {
        color: #E8F0EC;
        font-size: 12px;
        margin: 9px 0;
    }

    .sidebar-dot {
        color: #BBD4CA;
        margin-right: 7px;
    }

    .sidebar-footer {
        position: fixed;
        bottom: 20px;
        color: #BFD3CB;
        font-size: 10px;
        line-height: 1.5;
    }


    /* ======================================================
       TYPOGRAPHY
       ====================================================== */

    h1 {
        color: var(--dark) !important;
        font-size: 38px !important;
        font-weight: 800 !important;
        letter-spacing: -1.5px !important;
        margin-bottom: 5px !important;
    }

    h2 {
        color: var(--dark) !important;
        font-size: 24px !important;
        font-weight: 750 !important;
    }

    h3 {
        color: var(--dark) !important;
    }

    p {
        color: var(--muted);
    }

    label {
        color: var(--dark) !important;
    }


    /* ======================================================
       HEADER
       ====================================================== */

    .eyebrow {
        color: var(--green);
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        margin-bottom: 7px;
    }

    .subtitle {
        color: var(--muted);
        font-size: 14px;
        line-height: 1.6;
        max-width: 650px;
        margin-bottom: 20px;
    }

    .project-tag {
        display: inline-block;
        background-color: var(--soft-green);
        color: var(--green);
        border: 1px solid #CBDAD3;
        border-radius: 20px;
        padding: 7px 12px;
        font-size: 11px;
        font-weight: 700;
    }


    /* ======================================================
       QUESTION AREA
       ====================================================== */

    .question-label {
        color: var(--dark);
        font-size: 15px;
        font-weight: 750;
        margin-bottom: 4px;
    }

    .question-help {
        color: var(--muted);
        font-size: 12px;
        margin-bottom: 10px;
    }

    div[data-testid="stTextArea"] textarea {
        background-color: #FFFFFF !important;
        color: var(--dark) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
        padding: 15px !important;
        box-shadow: 0 2px 8px rgba(38,53,47,0.04) !important;
    }

    div[data-testid="stTextArea"] textarea:focus {
        border-color: var(--green) !important;
        box-shadow: 0 0 0 1px var(--green) !important;
    }


    /* ======================================================
       BUTTON
       ====================================================== */

    .stButton > button {
        background-color: var(--green);
        color: #FFFFFF;
        border: none;
        border-radius: 9px;
        font-weight: 700;
        font-size: 13px;
        min-height: 43px;
        padding: 0 20px;
        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        background-color: #31594C;
        color: #FFFFFF;
        border: none;
        transform: translateY(-1px);
    }


    /* ======================================================
       STATUS
       ====================================================== */

    .ready-box {
        background-color: var(--soft-green);
        border: 1px solid #CBDAD3;
        border-radius: 20px;
        padding: 8px 13px;
        color: var(--green);
        font-size: 10px;
        font-weight: 800;
        text-align: center;
        letter-spacing: 0.5px;
    }


    /* ======================================================
       ANSWER CARD
       ====================================================== */

    .answer-card {
        background-color: #FFFFFF;
        border: 1px solid var(--border);
        border-left: 4px solid var(--green);
        border-radius: 13px;
        padding: 23px 25px;
        margin-top: 10px;
        margin-bottom: 25px;
        box-shadow: 0 3px 12px rgba(38,53,47,0.05);
    }

    .answer-label {
        color: var(--green);
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .answer-text {
        color: var(--dark);
        font-size: 15px;
        line-height: 1.75;
    }

    .answer-note {
        color: var(--muted);
        font-size: 11px;
        margin-top: 15px;
        padding-top: 12px;
        border-top: 1px solid #E5E7E3;
    }


    /* ======================================================
       METRIC CARDS
       ====================================================== */

    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 11px;
        padding: 15px;
        box-shadow: 0 2px 7px rgba(38,53,47,0.03);
    }

    div[data-testid="stMetricLabel"] {
        color: var(--muted) !important;
        font-size: 9px !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    div[data-testid="stMetricValue"] {
        color: var(--dark) !important;
        font-size: 24px !important;
        font-weight: 750 !important;
    }


    /* ======================================================
       EVIDENCE CARDS
       ====================================================== */

    .evidence-header {
        color: var(--dark);
        font-size: 22px;
        font-weight: 750;
        margin-top: 10px;
    }

    .evidence-description {
        color: var(--muted);
        font-size: 12px;
        margin-bottom: 15px;
    }

    .evidence-label {
        color: var(--green);
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.2px;
        text-transform: uppercase;
    }

    .similarity-badge {
        color: var(--blue-gray);
        background-color: var(--soft-blue);
        border: 1px solid #CEDADD;
        border-radius: 7px;
        padding: 5px 9px;
        font-size: 11px;
        font-weight: 800;
        text-align: center;
    }

    .source-info {
        color: var(--muted);
        font-size: 12px;
        margin-top: 9px;
        margin-bottom: 13px;
    }

    .source-info strong {
        color: var(--dark);
    }

    .evidence-text {
        color: #43514C;
        font-size: 13px;
        line-height: 1.75;
        background-color: #F8F8F5;
        border: 1px solid #E4E6E1;
        border-left: 3px solid var(--blue-gray);
        border-radius: 7px;
        padding: 14px 16px;
    }


    /* ======================================================
       EXPANDERS
       ====================================================== */

    div[data-testid="stExpander"] {
        background-color: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 9px;
    }


    /* ======================================================
       DIVIDERS
       ====================================================== */

    hr {
        border-color: #D9DDD7 !important;
    }


    /* ======================================================
       ALERTS
       ====================================================== */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .footer-text {
        text-align: center;
        color: #87938E;
        font-size: 10px;
        line-height: 1.6;
        margin-top: 55px;
        padding-top: 20px;
        border-top: 1px solid #D9DDD7;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-logo">
            404<span>: Hallucination Not Found</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-description">
            Evidence-grounded clinical intelligence.
            Ask questions and trace every answer back
            to the retrieved guideline evidence.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-heading">RETRIEVAL ENGINE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-item">
            <span class="sidebar-dot">●</span>
            SentenceTransformer embeddings
        </div>

        <div class="sidebar-item">
            <span class="sidebar-dot">●</span>
            Chroma vector database
        </div>

        <div class="sidebar-item">
            <span class="sidebar-dot">●</span>
            Cosine similarity retrieval
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-heading">DOCUMENT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-item">
            <span class="sidebar-dot">●</span>
            NICE Mental Health Guideline
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-footer">
            404: Hallucination Not Found<br>
            Evidence should always be verified<br>
            against the original guideline.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns(
    [5, 1],
    vertical_alignment="center"
)

with header_left:

    st.markdown(
        '<div class="eyebrow">CLINICAL DECISION SUPPORT</div>',
        unsafe_allow_html=True
    )

    st.title(
        "Ask the evidence."
    )

    st.markdown(
        """
        <div class="subtitle">
            Search the indexed clinical guideline and inspect the
            evidence supporting each answer.
        </div>
        """,
        unsafe_allow_html=True
    )

with header_right:

    st.markdown(
        '<div class="ready-box">● SYSTEM READY</div>',
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# QUESTION AREA
# ============================================================

st.markdown(
    '<div class="question-label">Clinical question</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="question-help">
        Ask a question about the information contained in the indexed guideline.
    </div>
    """,
    unsafe_allow_html=True
)

question = st.text_area(
    "Clinical question",
    placeholder=(
        "Example: How should healthcare professionals manage "
        "tokophobia or extreme fear of childbirth?"
    ),
    height=110,
    label_visibility="collapsed"
)


button_col, empty_col = st.columns([1.4, 6])

with button_col:

    search_clicked = st.button(
        "Search evidence  →",
        use_container_width=True
    )


# ============================================================
# SEARCH
# ============================================================

if search_clicked:

    if not question.strip():

        st.warning(
            "Please enter a clinical question first."
        )

    else:

        with st.spinner(
            "Searching the clinical evidence..."
        ):

            response = retrieve(question)


        # ====================================================
        # REFUSAL
        # ====================================================

        if response["refused"]:

            st.divider()

            st.subheader(
                "Insufficient evidence"
            )

            st.error(
                response["refusal"]["reason"]
            )

            st.markdown(
                "**Suggested next steps:**"
            )

            for step in response["refusal"]["next_steps"]:

                st.markdown(
                    f"• {step}"
                )


        # ====================================================
        # SUCCESS
        # ====================================================

        else:

            results = response["results"]
            answer = response["answer"]

            st.divider()


            # =================================================
            # CLINICAL ANSWER
            # =================================================

            st.markdown(
                '<div class="evidence-header">Clinical answer</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="answer-card">
                    <div class="answer-label">
                        GROUNDED RESPONSE
                    </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="answer-text">{answer}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                """
                    <div class="answer-note">
                        Answer generated only from the retrieved
                        guideline evidence.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


            # =================================================
            # RESULTS HEADER
            # =================================================

            result_title, result_info = st.columns(
                [4, 2],
                vertical_alignment="center"
            )

            with result_title:

                st.markdown(
                    '<div class="evidence-header">'
                    'Retrieval results'
                    '</div>',
                    unsafe_allow_html=True
                )

            with result_info:

                st.caption(
                    "Ranked by semantic similarity"
                )


            # =================================================
            # METRICS
            # =================================================

            metric1, metric2, metric3 = st.columns(3)

            best_score = max(
                result["similarity"]
                for result in results
            )

            with metric1:

                st.metric(
                    "Evidence found",
                    len(results)
                )

            with metric2:

                st.metric(
                    "Best similarity",
                    f"{best_score:.2f}"
                )

            with metric3:

                st.metric(
                    "Threshold",
                    "0.70"
                )


            st.write("")


            # =================================================
            # SUPPORTING EVIDENCE
            # =================================================

            st.markdown(
                '<div class="evidence-header">'
                'Supporting evidence'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="evidence-description">
                    The passages below were retrieved from the
                    indexed clinical guideline.
                </div>
                """,
                unsafe_allow_html=True
            )


            # =================================================
            # EACH EVIDENCE RESULT
            # =================================================

            for result in results:

                rank = result["rank"]
                similarity = result["similarity"]
                page = result["page"]
                source = result["source"]
                section_number = result["section_number"]
                section_title = result["section_title"]
                text = result["text"]


                with st.container(border=True):

                    top_left, top_right = st.columns(
                        [5, 1],
                        vertical_alignment="center"
                    )

                    with top_left:

                        st.markdown(
                            f'<div class="evidence-label">'
                            f'SOURCE {rank:02d}'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                    with top_right:

                        st.markdown(
                            f'<div class="similarity-badge">'
                            f'{similarity:.2f}'
                            f'</div>',
                            unsafe_allow_html=True
                        )


                    # -----------------------------------------
                    # SOURCE INFORMATION
                    # -----------------------------------------

                    source_name = (
                        "NICE Mental Health Guideline"
                        if source
                        else "Clinical guideline"
                    )

                    metadata_parts = [
                        f"**{source_name}**"
                    ]

                    if page is not None:

                        metadata_parts.append(
                            f"Page {page}"
                        )

                    section_info = ""

                    if section_number:

                        section_info += str(
                            section_number
                        )

                    if section_title:

                        if section_info:

                            section_info += " · "

                        section_info += str(
                            section_title
                        )

                    if section_info:

                        metadata_parts.append(
                            section_info
                        )

                    st.markdown(
                        "  ·  ".join(metadata_parts)
                    )


                    # -----------------------------------------
                    # EVIDENCE
                    # -----------------------------------------

                    st.markdown(
                        "##### Evidence excerpt"
                    )

                    st.markdown(
                        f'<div class="evidence-text">'
                        f'{text}'
                        f'</div>',
                        unsafe_allow_html=True
                    )


                    # -----------------------------------------
                    # DETAILS
                    # -----------------------------------------

                    with st.expander(
                        "View retrieval details"
                    ):

                        st.write(
                            f"**Chunk ID:** "
                            f"{result['chunk_id']}"
                        )

                        st.write(
                            f"**Similarity score:** "
                            f"{similarity:.4f}"
                        )

                        st.write(
                            f"**Page:** "
                            f"{page}"
                        )

                        if section_number:

                            st.write(
                                f"**Section:** "
                                f"{section_number}"
                            )

                        if section_title:

                            st.write(
                                f"**Section title:** "
                                f"{section_title}"
                            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-text">
        404: Hallucination Not Found · Retrieval-Augmented Clinical Decision Support
        <br>
        Answers are generated from retrieved evidence and should be verified
        against the original guideline.
    </div>
    """,
    unsafe_allow_html=True
)