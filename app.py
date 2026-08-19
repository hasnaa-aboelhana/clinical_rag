import streamlit as st

from rag_engine import retrieve


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Cliniq RAG",
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
       GLOBAL
       ====================================================== */

    .stApp {
        background-color: #0B0F14;
        color: #E8EDF3;
    }

    .main .block-container {
        max-width: 1180px;
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
        background-color: #0F141A;
        border-right: 1px solid #202832;
    }

    section[data-testid="stSidebar"] .block-container {
        padding: 30px 20px;
    }

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        text-align: left;
        background-color: transparent;
        border: none;
        color: #AAB4BF;
        padding: 10px 12px;
        border-radius: 8px;
        font-size: 13px;
        margin-bottom: 4px;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #17211F;
        color: #69DDB7;
        border: none;
    }


    /* ======================================================
       TYPOGRAPHY
       ====================================================== */

    h1 {
        color: #F4F7FA !important;
        font-size: 32px !important;
        letter-spacing: -1px;
    }

    h2 {
        color: #E8EDF3 !important;
    }

    h3 {
        color: #E8EDF3 !important;
    }

    p {
        color: #AAB4BF;
    }


    /* ======================================================
       HEADER
       ====================================================== */

    .eyebrow {
        color: #62D9B2;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .subtitle {
        color: #788592;
        font-size: 14px;
        margin-top: -8px;
        margin-bottom: 25px;
    }


    /* ======================================================
       QUESTION INPUT
       ====================================================== */

    label {
        color: #C4CDD6 !important;
    }

    div[data-testid="stTextArea"] textarea {
        background-color: #11171E !important;
        color: #E8EDF3 !important;
        border: 1px solid #29333E !important;
        border-radius: 10px !important;
        font-size: 14px !important;
        padding: 14px !important;
    }

    div[data-testid="stTextArea"] textarea:focus {
        border-color: #55C8A4 !important;
        box-shadow: 0 0 0 1px #55C8A4 !important;
    }


    /* ======================================================
       MAIN BUTTON
       ====================================================== */

    .stButton > button {
        background-color: #62D9B2;
        color: #07100D;
        border: none;
        border-radius: 8px;
        font-weight: 700;
        font-size: 13px;
        min-height: 42px;
    }

    .stButton > button:hover {
        background-color: #79E5C3;
        color: #07100D;
        border: none;
    }


    /* ======================================================
       METRIC CARDS
       ====================================================== */

    div[data-testid="metric-container"] {
        background-color: #11171E;
        border: 1px solid #202A34;
        border-radius: 10px;
        padding: 16px;
    }

    div[data-testid="stMetricLabel"] {
        color: #71808D !important;
        font-size: 10px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    div[data-testid="stMetricValue"] {
        color: #F0F4F7 !important;
        font-size: 25px !important;
    }


    /* ======================================================
       EVIDENCE CARDS
       ====================================================== */

    .evidence-box {
        background-color: #11171E;
        border: 1px solid #202A34;
        border-radius: 11px;
        padding: 18px;
        margin-bottom: 14px;
    }

    .evidence-label {
        color: #62D9B2;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.2px;
        text-transform: uppercase;
    }

    .similarity-badge {
        color: #69DDB7;
        background-color: #14251F;
        border: 1px solid #24483C;
        border-radius: 6px;
        padding: 5px 9px;
        font-size: 11px;
        font-weight: 700;
    }

    .source-info {
        color: #8A96A3;
        font-size: 12px;
        margin-top: 8px;
        margin-bottom: 14px;
    }

    .source-info strong {
        color: #D1D8DE;
    }

    .evidence-text {
        color: #C4CDD6;
        font-size: 13px;
        line-height: 1.7;
        background-color: #0D1217;
        border-left: 3px solid #315448;
        border-radius: 4px;
        padding: 13px 15px;
    }


    /* ======================================================
       ANSWER BOX
       ====================================================== */

    .answer-box {
        background-color: #101C18;
        border: 1px solid #24483C;
        border-radius: 11px;
        padding: 20px;
        margin-bottom: 20px;
        color: #DCE6E2;
        font-size: 15px;
        line-height: 1.8;
    }

    .answer-label {
        color: #62D9B2;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }


    /* ======================================================
       STATUS BOX
       ====================================================== */

    .ready-box {
        background-color: #101C18;
        border: 1px solid #24483C;
        border-radius: 20px;
        padding: 7px 13px;
        color: #69DDB7;
        font-size: 11px;
        font-weight: 700;
        text-align: center;
    }


    /* ======================================================
       DIVIDERS
       ====================================================== */

    hr {
        border-color: #202832 !important;
    }


    /* ======================================================
       EXPANDERS
       ====================================================== */

    div[data-testid="stExpander"] {
        background-color: #11171E;
        border: 1px solid #202A34;
        border-radius: 10px;
    }


    /* ======================================================
       INFO / WARNING
       ====================================================== */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .footer-text {
        text-align: center;
        color: #4F5A65;
        font-size: 10px;
        margin-top: 50px;
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
        "## Cliniq<span style='color:#62D9B2;'>RAG</span>",
        unsafe_allow_html=True
    )

    st.caption(
        "Evidence-grounded clinical intelligence"
    )

    st.divider()

    st.markdown(
        "**WORKSPACE**"
    )

    st.button(
        "✦  Ask a question",
        use_container_width=True
    )

    st.button(
        "◷  Query history",
        use_container_width=True
    )

    st.button(
        "◈  Evidence library",
        use_container_width=True
    )

    st.divider()

    st.markdown(
        "**RETRIEVAL ENGINE**"
    )

    st.caption(
        "SentenceTransformer embeddings"
    )

    st.caption(
        "Chroma vector database"
    )

    st.caption(
        "Cosine similarity retrieval"
    )

    st.divider()

    st.markdown(
        "**DOCUMENT**"
    )

    st.caption(
        "NICE Mental Health Guideline"
    )

    st.divider()

    st.caption(
        "Clinical RAG prototype"
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
        '<div class="subtitle">'
        'Search the indexed clinical guideline and inspect the '
        'evidence supporting each answer.'
        '</div>',
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

st.subheader(
    "Clinical question"
)

st.caption(
    "Ask a question about the information contained in the indexed guideline."
)

question = st.text_area(
    "Clinical question",
    placeholder=(
        "Example: How should healthcare professionals "
        "manage extreme fear of childbirth?"
    ),
    height=110,
    label_visibility="collapsed"
)


button_col, empty_col = st.columns(
    [1.5, 6]
)

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

            # ------------------------------------------------
            # CLINICAL ANSWER
            # ------------------------------------------------

            st.divider()

            st.subheader(
                "Clinical answer"
            )

            st.markdown(
                f'<div class="answer-box">'
                f'<div class="answer-label">GROUNDED RESPONSE</div>'
                f'{response["answer"]}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.caption(
                "Answer generated only from the retrieved guideline evidence."
            )


            # ------------------------------------------------
            # RESULTS HEADER
            # ------------------------------------------------

            st.divider()

            result_title, result_info = st.columns(
                [4, 2],
                vertical_alignment="center"
            )

            with result_title:

                st.subheader(
                    "Retrieval results"
                )

            with result_info:

                st.caption(
                    "Ranked by semantic similarity"
                )


            # ------------------------------------------------
            # METRICS
            # ------------------------------------------------

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


            # ------------------------------------------------
            # SUPPORTING EVIDENCE
            # ------------------------------------------------

            st.subheader(
                "Supporting evidence"
            )

            st.caption(
                "The passages below were retrieved from the indexed guideline."
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


                # --------------------------------------------
                # CARD
                # --------------------------------------------

                with st.container(
                    border=True
                ):

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


                    # ----------------------------------------
                    # SOURCE INFORMATION
                    # ----------------------------------------

                    source_name = source or "NICE Mental Health Guideline"

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


                    # ----------------------------------------
                    # EVIDENCE TEXT
                    # ----------------------------------------

                    st.markdown(
                        "##### Evidence excerpt"
                    )

                    st.markdown(
                        f'<div class="evidence-text">'
                        f'{text}'
                        f'</div>',
                        unsafe_allow_html=True
                    )


                    # ----------------------------------------
                    # DETAILS
                    # ----------------------------------------

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
    "<div class='footer-text'>"
    "Cliniq RAG · Retrieval-Augmented Clinical Decision Support"
    "<br>"
    "Answers are generated from retrieved evidence and should be "
    "verified against the original guideline."
    "</div>",
    unsafe_allow_html=True
)