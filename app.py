import base64
import streamlit as st
import streamlit.components.v1 as components
import document_parser
import prompts
import api_router

# --- Premium Layout & Page Configuration ---
st.set_page_config(
    page_title="ResumeAI",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Premium Theme & Custom CSS Styles (BUG 1 Fix) ---
st.html("""
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=DM+Serif+Display:ital@0;1&display=swap" rel="stylesheet">
<style>
/* Main backgrounds and styles */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #0c0c14 !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Adjust top padding to prevent header cutoff (UI fix) */
[data-testid="stAppViewBlockContainer"] {
    padding-top: 3.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 800px !important;
    margin: 0 auto !important;
}

/* Hero Section */
.hero-bar {
    background-color: #13131f;
    border-bottom: 1px solid #2a2a3d;
    padding: 24px 40px;
    text-align: center;
    margin-bottom: 30px;
    border-radius: 12px;
    width: 100%;
    box-sizing: border-box;
}
.hero-logo {
    font-family: 'DM Serif Display', serif;
    font-size: 36px;
    color: #e2e8f0;
    margin-bottom: 8px;
    font-weight: normal;
}
.hero-logo span {
    color: #6ee7b7;
}
.hero-tagline {
    font-size: 15px;
    color: #64748b;
    margin-bottom: 16px;
}
.hero-steps {
    display: inline-flex;
    align-items: center;
    gap: 12px;
}
.step-pill {
    background-color: #0c0c14;
    border: 1px solid #2a2a3d;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    color: #e2e8f0;
    transition: all 0.3s ease;
    animation: pulse-border 3s infinite;
}
.step-pill:nth-child(1) { animation-delay: 0s; }
.step-pill:nth-child(3) { animation-delay: 1s; }
.step-pill:nth-child(5) { animation-delay: 2s; }
.step-pill:hover {
    border-color: #6ee7b7;
    color: #6ee7b7;
    transform: translateY(-1px);
}
.step-arrow {
    color: #64748b;
    font-size: 14px;
}
@keyframes pulse-border {
    0% { border-color: #2a2a3d; }
    50% { border-color: #134e4a; }
    100% { border-color: #2a2a3d; }
}

/* Responsive iframe adjustments for A4 Preview */
iframe[title="streamlit_components.v1.html"] {
    width: 100% !important;
    height: 1200px !important;
    border: none !important;
}
@media (max-width: 899px) {
    iframe[title="streamlit_components.v1.html"] {
        height: 145vw !important;
        max-height: 1200px !important;
    }
}

/* Custom cards */
.custom-card {
    background-color: #13131f;
    border: 1px solid #2a2a3d;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
}
.card-title {
    font-family: 'DM Serif Display', serif;
    font-size: 20px;
    color: #e2e8f0;
    margin-bottom: 16px;
    border-bottom: 1px solid #2a2a3d;
    padding-bottom: 8px;
}

/* Textareas and text inputs */
div[data-baseweb="input"], div[data-baseweb="textarea"] {
    background-color: #0c0c14 !important;
    border: 1px solid #2a2a3d !important;
    border-radius: 8px !important;
}
div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {
    background-color: #0c0c14 !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within {
    border-color: #6ee7b7 !important;
}

/* Tabs */
div[data-testid="stTabs"] {
    background-color: transparent !important;
}
div[data-testid="stTabs"] button {
    background-color: transparent !important;
    color: #64748b !important;
    border: 1px solid #2a2a3d !important;
    border-radius: 20px !important;
    padding: 6px 16px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stTabs"] button:hover {
    color: #e2e8f0 !important;
    border-color: #64748b !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    background-color: #134e4a !important;
    color: #6ee7b7 !important;
    border-color: #6ee7b7 !important;
}
div[data-testid="stTabs"] div[data-baseweb="tab-highlight"] {
    background-color: transparent !important;
}

/* CTA Buttons */
div[data-testid="stButton"] button {
    background-color: #6ee7b7 !important;
    color: #0c0c14 !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    border: none !important;
    width: 100% !important;
    padding: 12px 24px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stButton"] button:hover {
    background-color: #a7f3d0 !important;
    color: #0c0c14 !important;
}

/* Download buttons */
div[data-testid="stDownloadButton"] button {
    background-color: transparent !important;
    color: #6ee7b7 !important;
    border: 1px solid #6ee7b7 !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    width: 100% !important;
    padding: 10px 16px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stDownloadButton"] button:hover {
    background-color: #134e4a !important;
    color: #6ee7b7 !important;
    border-color: #6ee7b7 !important;
}

/* Skeleton preview */
.skeleton-box {
    background-color: #13131f;
    border: 1px dashed #2a2a3d;
    border-radius: 12px;
    padding: 40px 24px;
    text-align: center;
    color: #64748b;
    margin-top: 20px;
}
.skeleton-box h3 {
    font-family: 'DM Serif Display', serif;
    color: #e2e8f0 !important;
}
.skeleton-line {
    height: 10px;
    background-color: #0c0c14;
    border-radius: 4px;
    border: 1px solid #2a2a3d;
    margin: 8px auto;
}

/* Custom Status messages */
.status-success {
    background-color: #134e4a;
    border: 1px solid #6ee7b7;
    color: #6ee7b7;
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 14px;
    margin-bottom: 16px;
    font-family: 'DM Sans', sans-serif;
}
.status-error {
    background-color: #1f0a0a;
    border: 1px solid #f87171;
    color: #f87171;
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 14px;
    margin-bottom: 16px;
    font-family: 'DM Sans', sans-serif;
}
.status-info {
    background-color: #0f1a2e;
    border: 1px solid #1e40af;
    color: #93c5fd;
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 14px;
    margin-bottom: 16px;
    font-family: 'DM Sans', sans-serif;
}

/* Hide standard Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""")

# Helper functions for status notifications to match requested designs
def show_success(message: str):
    st.markdown(f'<div class="status-success">✓ {message}</div>', unsafe_allow_html=True)

def show_error(message: str):
    st.markdown(f'<div class="status-error">⚠️ {message}</div>', unsafe_allow_html=True)

def show_info(message: str):
    st.markdown(f'<div class="status-info">💡 {message}</div>', unsafe_allow_html=True)

# --- Hero Title Section ---
st.markdown("""
<div class="hero-bar">
    <div class="hero-logo">Resume<span>AI</span></div>
    <div class="hero-tagline">Tailor your resume to any job. One page. Always.</div>
    <div class="hero-steps">
        <span class="step-pill">① Upload</span>
        <span class="step-arrow">→</span>
        <span class="step-pill">② Describe</span>
        <span class="step-arrow">→</span>
        <span class="step-pill">③ Download</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize Session State
if 'optimized_html' not in st.session_state:
    st.session_state['optimized_html'] = ""
if 'active_provider' not in st.session_state:
    st.session_state['active_provider'] = ""

# --- WORKSPACE CONTAINER (Centered Stack Layout) ---

# Card 1: Configuration & Upload
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">📁 1. Upload Resume</div>', unsafe_allow_html=True)

st.markdown("<div style='font-size:14px; margin-bottom:8px; font-weight:600;'>Upload Your Existing Resume</div>", unsafe_allow_html=True)
uploaded_resume = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"],
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# Card 2: Job Details
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">💼 2. Target Job Details</div>', unsafe_allow_html=True)

st.caption("Provide details about the job using any tab below:")

tab_desc, tab_role, tab_img = st.tabs([
    "📄 Job Description Text",
    "💼 Target Job Role",
    "🖼️ Upload JD Image"
])

job_desc_text = ""
job_role = ""
img_b64 = ""

with tab_desc:
    job_desc_text = st.text_area(
        "Paste target job description text...",
        height=180,
        placeholder="Paste target job requirements, skills, and qualifications text here...",
        label_visibility="collapsed"
    )
    
with tab_role:
    job_role = st.text_input(
        "Enter target job role...",
        placeholder="e.g. Senior Python Backend Developer, Data Scientist, Frontend Developer...",
        label_visibility="collapsed"
    )
    st.markdown('<div style="font-size: 12px; color: #64748b; margin-top: 8px;">💡 If a full job description is unavailable, the AI will research and tailor the resume based on standard industry expectations for this role.</div>', unsafe_allow_html=True)
    
with tab_img:
    uploaded_image = st.file_uploader(
        "Upload JD Image",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )
    if uploaded_image is not None:
        file_bytes = uploaded_image.getvalue()
        mime_type = uploaded_image.type
        encoded = base64.b64encode(file_bytes).decode()
        img_b64 = f"data:{mime_type};base64,{encoded}"
        show_success("Image uploaded successfully!")
        st.image(file_bytes, caption="Uploaded JD Image", use_column_width=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<div style='font-size:14px; margin-bottom:8px; font-weight:600;'>Company Specific Wording (Optional)</div>", unsafe_allow_html=True)
enable_advanced = st.checkbox("Enable Target Company Alignment", value=False)
company_name = ""
if enable_advanced:
    company_name = st.text_input(
        "Target Company Name", 
        placeholder="e.g. Google, CyberNext, Stripe...",
        help="Directs the fallback agent to tailor wording and culture fit to this company's hiring guidelines."
    )

st.markdown('</div>', unsafe_allow_html=True)

# Action Trigger Button
optimize_btn = st.button("✨ Optimize & Tailor Resume", use_container_width=True)

st.markdown("---")

# Trigger processing on button click
if optimize_btn:
    if uploaded_resume is None:
        show_error("Please upload your existing resume (.pdf or .docx).")
    elif not job_desc_text.strip() and not job_role.strip() and not img_b64:
        show_error("Please specify at least one job input method (JD Text, Job Role, or JD Image).")
    elif enable_advanced and not company_name.strip():
        show_error("Please enter the company name or disable Target Company Alignment.")
    else:
        with st.spinner("🚀 Extracting text and tailoring resume with AI agents..."):
            extracted_resume_text = document_parser.extract_text_from_file(uploaded_resume)
            
            if not extracted_resume_text.strip():
                show_error("Could not extract text from the file. Please ensure it contains readable text.")
            else:
                # Execute multi-agent optimization routing
                result = api_router.run_resume_optimization(
                    resume_text=extracted_resume_text,
                    job_desc_text=job_desc_text,
                    job_role=job_role,
                    job_image_base64=img_b64,
                    company_name=company_name
                )
                
                if result["success"]:
                    raw_html = result["content"]
                    
                    # Clean LLM code block tags
                    clean_html = raw_html.strip()
                    if clean_html.startswith('```html'):
                        clean_html = clean_html[7:]
                    elif clean_html.startswith('```'):
                        clean_html = clean_html[3:]
                    if clean_html.endswith('```'):
                        clean_html = clean_html[:-3]
                    clean_html = clean_html.strip()
                    
                    st.session_state['optimized_html'] = clean_html
                    st.session_state['active_provider'] = result["provider"]
                else:
                    st.session_state['optimized_html'] = ""
                    st.session_state['active_provider'] = ""
                    st.markdown(result["content"], unsafe_allow_html=True)

# Output Rendering Block (BUG 6 fix & Redesign)
if st.session_state['optimized_html']:
    html_content = st.session_state['optimized_html']
    plain_text_resume = document_parser.convert_html_to_text(html_content)
    
    # Pre-generate DOCX bytes and PDF bytes
    docx_bytes = document_parser.generate_docx_bytes(html_content)
    pdf_bytes = document_parser.generate_pdf_bytes(html_content)
    
    show_success(f"Tailored successfully using {st.session_state['active_provider']} and auto-fit to one page!")
    
    # 1. Preview Panel Tabs (A4 Preview and Plain Text Output)
    preview_tab, text_tab = st.tabs([
        "👁️ Live Single-Page A4 Preview",
        "📝 Extracted Plain Text Resume"
    ])
    
    with preview_tab:
        # Embed HTML content in the responsive A4 wrapper
        full_preview_html = prompts.HTML_PREVIEW_TEMPLATE.format(html_content=html_content)
        # Render using correct components module
        components.html(
            full_preview_html,
            height=1200,
            scrolling=True
        )
        
    with text_tab:
        st.caption("Copy or inspect the plain text markdown output generated from the tailored resume:")
        st.text_area(
            "Plain Text Output",
            plain_text_resume,
            height=800,
            label_visibility="collapsed"
        )
        
    # Download Bar (HTML added back as fallback)
    st.markdown("<br><div style='font-size:14px; margin-bottom:8px; font-weight:600;'>Download Tailored Formats</div>", unsafe_allow_html=True)
    dcol1, dcol2, dcol3 = st.columns(3)
    with dcol1:
        if pdf_bytes:
            st.download_button(
                label="📄 Download PDF",
                data=pdf_bytes,
                file_name="tailored_resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.button("📄 PDF (Unavailable)", disabled=True, use_container_width=True)
    with dcol2:
        st.download_button(
            label="📝 Download DOCX",
            data=docx_bytes,
            file_name="tailored_resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
    with dcol3:
        st.download_button(
            label="🌐 Download HTML",
            data=html_content,
            file_name="tailored_resume.html",
            mime="text/html",
            use_container_width=True
        )
        
    # Browser saving note (styled as custom info)
    if not pdf_bytes:
        show_info("<strong>PDF generation fallback:</strong> Pango/WeasyPrint is not fully configured on this server. Please download the HTML version, open it in Chrome/Edge, and use <strong>Print to PDF</strong> (Margins: None, Background Graphics: Enabled).")
        
else:
    # Default placeholder when state is empty
    st.markdown("""
    <div class="skeleton-box">
        <div style="font-size: 64px; margin-bottom: 20px;">📄</div>
        <h3>Resume Preview Workspace</h3>
        <p style="margin: 0 auto 25px auto; font-size: 14px; max-width: 450px; color: #64748b; line-height: 1.5;">
            Provide your existing resume and job details above, then click <strong>Optimize & Tailor Resume</strong> to generate your single-page tailored output.
        </p>
        <div style="max-width: 250px; margin: 0 auto; display: flex; flex-direction: column; gap: 8px;">
            <div class="skeleton-line" style="width: 100%;"></div>
            <div class="skeleton-line" style="width: 80%;"></div>
            <div class="skeleton-line" style="width: 90%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
