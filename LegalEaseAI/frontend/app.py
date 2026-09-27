import base64
import html
import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv(
    "FRONTEND_BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #0e1117;
        color: white;
    }

    /* Main content width */
    .block-container {
        max-width: 850px;
        padding-top: 45px;
        padding-bottom: 50px;
    }

    /* Logo */
    .logo {
        text-align: center;
        font-size: 48px;
        margin-bottom: 0px;
    }

    /* Main title */
    .main-title {
        text-align: center;
        font-size: 28px;
        font-weight: 700;
        margin-top: 5px;
        margin-bottom: 8px;
        color: #f1f1f1;
    }

    .subtitle {
        text-align: center;
        color: #aeb4c0;
        font-size: 14px;
        margin-bottom: 35px;
    }

    /* Labels */
    label {
        color: #e8e8e8 !important;
        font-weight: 500 !important;
    }

    /* Text inputs */
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        background-color: #262934 !important;
        border: 1px solid #343743 !important;
        border-radius: 6px !important;
    }

    input,
    textarea {
        color: white !important;
    }

    textarea {
        min-height: 90px !important;
    }

    /* Generate button */
    .stButton > button {
        background-color: #1f2937;
        color: white;
        border: 1px solid #4b5563;
        border-radius: 6px;
        font-weight: 600;
        padding: 8px 18px;
    }

    .stButton > button:hover {
        border-color: #7c8cff;
        color: white;
    }

    /* Download buttons */
    .stDownloadButton > button {
        width: 100%;
        border-radius: 6px;
    }

    /* Generated document */
    .document-box {
        background-color: #181b22;
        border: 1px solid #343743;
        border-radius: 8px;
        padding: 25px;
        margin-top: 20px;
        color: #eeeeee;
        white-space: pre-wrap;
        line-height: 1.6;
    }

    .section-title {
        color: #ffffff;
        font-size: 20px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 10px;
    }

    /* Info box */
    .info-box {
        background-color: #12304b;
        border-radius: 5px;
        padding: 12px;
        color: #dbeafe;
        margin-top: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""

if "terms" not in st.session_state:
    st.session_state.terms = []

if "document_type" not in st.session_state:
    st.session_state.document_type = ""


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="logo">⚖️</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-title">LegalEase</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">AI Legal Document Generator</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# INPUTS
# ---------------------------------------------------------

document_type = st.text_input(
    "Document Type (Ex: Agreement, Contract, NDA)",
    placeholder="Enter document type",
)

parties = st.text_area(
    "Parties Involved",
    placeholder="Example: Landlord: Arun Kumar\nTenant: Swetha",
    height=90,
)

terms = st.text_area(
    "Terms & Conditions (Use semicolons for bullet points)",
    placeholder=(
        "Example: Monthly rent is Rs. 15000;\n"
        "Security deposit is Rs. 30000;\n"
        "Rent must be paid before the 5th of every month"
    ),
    height=100,
)

effective_date = st.text_input(
    "Effective Date",
    placeholder="Example: 01-10-2026",
)


# ---------------------------------------------------------
# GENERATE BUTTON
# ---------------------------------------------------------

generate = st.button(
    "Generate Document",
    type="secondary",
)


if not st.session_state.generated_text:
    st.markdown(
        """
        <div class="info-box">
        ℹ️ Click 'Generate Document' to start.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# GENERATE DOCUMENT
# ---------------------------------------------------------

if generate:

    if not document_type.strip():
        st.error("Please enter the document type.")

    elif not parties.strip():
        st.error("Please enter the parties involved.")

    elif not terms.strip():
        st.error("Please enter the terms and conditions.")

    elif not effective_date.strip():
        st.error("Please enter the effective date.")

    else:

        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": effective_date,
        }

        try:

            with st.spinner("Generating your legal document..."):

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120,
                )

            if response.status_code == 200:

                result = response.json()

                st.session_state.generated_text = result.get(
                    "text",
                    ""
                )

                st.session_state.terms = result.get(
                    "terms",
                    []
                )

                st.session_state.document_type = document_type

                st.rerun()

            else:

                try:
                    error_detail = response.json().get(
                        "detail",
                        response.text
                    )
                except Exception:
                    error_detail = response.text

                st.error(
                    f"Backend error ({response.status_code}): "
                    f"{error_detail}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to the LegalEase backend. "
                "Make sure the FastAPI server is running on "
                "http://127.0.0.1:8000."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The request took too long. "
                "Please try again."
            )

        except Exception as exc:

            st.error(
                f"Unexpected error: {exc}"
            )


# ---------------------------------------------------------
# GENERATED DOCUMENT
# ---------------------------------------------------------

if st.session_state.generated_text:

    st.markdown(
        '<div class="section-title">Generated Document</div>',
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(
        ["Preview", "Edit"]
    )

    # -----------------------------------------------------
    # PREVIEW
    # -----------------------------------------------------

    with tab1:

        safe_text = html.escape(
            st.session_state.generated_text
        )

        st.markdown(
            f"""
            <div class="document-box">
            {safe_text.replace(chr(10), "<br>")}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------
    # EDIT
    # -----------------------------------------------------

    with tab2:

        edited_text = st.text_area(
            "Edit your document",
            value=st.session_state.generated_text,
            height=500,
        )

        if st.button("Save Changes"):

            st.session_state.generated_text = edited_text

            st.success(
                "Changes saved successfully."
            )

            st.rerun()


    # -----------------------------------------------------
    # DOWNLOAD
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">Download Document</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    export_payload_base = {
        "document_type": st.session_state.document_type,
        "text": st.session_state.generated_text,
        "terms": st.session_state.terms,
    }

    # TXT
    with col1:

        try:

            txt_response = requests.post(
                f"{BACKEND_URL}/export",
                json={
                    **export_payload_base,
                    "format": "txt",
                },
                timeout=60,
            )

            if txt_response.status_code == 200:

                st.download_button(
                    "Download TXT",
                    data=txt_response.content,
                    file_name="LegalEase_Document.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

        except Exception:
            st.warning("TXT export unavailable.")


    # DOCX
    with col2:

        try:

            docx_response = requests.post(
                f"{BACKEND_URL}/export",
                json={
                    **export_payload_base,
                    "format": "docx",
                },
                timeout=60,
            )

            if docx_response.status_code == 200:

                st.download_button(
                    "Download DOCX",
                    data=docx_response.content,
                    file_name="LegalEase_Document.docx",
                    mime=(
                        "application/"
                        "vnd.openxmlformats-officedocument."
                        "wordprocessingml.document"
                    ),
                    use_container_width=True,
                )

        except Exception:
            st.warning("DOCX export unavailable.")


    # PDF
    with col3:

        try:

            pdf_response = requests.post(
                f"{BACKEND_URL}/export",
                json={
                    **export_payload_base,
                    "format": "pdf",
                },
                timeout=60,
            )

            if pdf_response.status_code == 200:

                st.download_button(
                    "Download PDF",
                    data=pdf_response.content,
                    file_name="LegalEase_Document.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

        except Exception:
            st.warning("PDF export unavailable.")


    # -----------------------------------------------------
    # NOTICE
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="info-box">
        ⚠️ LegalEase generates draft documents for review.
        It does not replace advice from a qualified legal professional.
        </div>
        """,
        unsafe_allow_html=True,
    )