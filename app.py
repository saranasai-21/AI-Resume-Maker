import base64
import streamlit as st
import streamlit.components.v1 as components
import document_parser
import prompts
import api_router

# --- Premium Layout & Page Configuration ---
st.set_page_config(
    page_title="ResumeAI - Advanced Resume Optimizer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Theme & Custom CSS Styles ---
st.markdown("""
<style>
/* Curator gradient and premium spacing */
.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Glassmorphism Title Card */
.hero-card {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.05) 0%, rgba(124, 58, 237, 0.05) 100%);
    border: 1px solid rgba(229, 231, 235, 0.5);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
}
.hero-title {
    font-size: 3.2rem;
    font-weight: 850;
    margin: 0 0 5px 0;
    background: -webkit-linear-gradient(45deg, #2563eb, #7c3aed, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-subtitle {
    color: #4b5563;
    font-size: 1.15rem;
    margin-bottom: 0px;
    font-weight: 400;
}

/* Custom CSS Card Styling */
.custom-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02), 0 2px 4px -1px rgba(0,0,0,0.02);
    margin-bottom: 20px;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Tab Overrides */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background-color: #f3f4f6;
    padding: 6px;
    border-radius: 10px;
}
.stTabs [data-baseweb="tab"] {
    height: 38px;
    border-radius: 8px;
    background-color: transparent;
    color: #4b5563;
    font-weight: 600;
    border: none;
    transition: all 0.2s ease;
}
.stTabs [aria-selected="true"] {
    background-color: white !important;
    color: #2563eb !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

/* Beautiful custom button hover action */
div.stButton > button {
    background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.2) !important;
    transition: all 0.3s ease !important;
    height: 50px;
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #1d4ed8, #6d28d9) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(124, 58, 237, 0.3) !important;
}

/* Download option panel */
.download-card {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
}
.download-title {
    color: #15803d;
    font-weight: 700;
    font-size: 1.15rem;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Skeleton preview */
.skeleton-box {
    border: 2px dashed #e5e7eb;
    border-radius: 12px;
    background-color: #fafafa;
    padding: 60px 40px;
    text-align: center;
    color: #6b7280;
}
</style>
""", unsafe_allow_html=True)

# --- Sidebar Configuration (Settings Hub) ---
with st.sidebar:
    st.image("https://img.icons8.com/gradient/96/resume.png", width=64)
    st.markdown("### **ResumeAI Engine**")
    st.caption("AI-powered single page ATS optimization router")
    st.markdown("---")
    
    st.subheader("💡 Advanced Directives")
    enable_advanced = st.checkbox("Enable Company Research Mode", value=False)
    company_name = ""
    if enable_advanced:
        company_name = st.text_input(
            "Target Company Name", 
            placeholder="e.g. Google, CyberNext, Stripe...",
            help="Directs the fallback agent to tailor tone and alignment specifically to the company's culture and guidelines."
        )
        
    st.markdown("---")
    st.markdown("#### **Active Key Fallback Chain**")
    providers = api_router.get_providers()
    if providers:
        st.success(f"Configured Agents: {len(providers)}")
        for i, p in enumerate(providers):
            st.markdown(f"**{i+1}.** `{p['name']}` ({p['type']})")
    else:
        st.warning("⚠️ No environment API keys found! Fallback will fail unless keys are injected.")
        
    st.markdown("---")
    st.caption("Created for Sarana Sai Bagadi • v2.1")

# --- Hero Title Section ---
st.markdown("""
<div class="hero-card">
    <h1 class="hero-title">ResumeAI</h1>
    <div class="hero-subtitle">Optimize & Tailor your resume to any job or role on exactly one A4 page.</div>
</div>
""", unsafe_allow_html=True)

# --- Layout Grid: Inputs (Left) and Outputs (Right) ---
col1, col2 = st.columns([1, 1.2], gap="large")

# Initialize Session State
if 'optimized_html' not in st.session_state:
    st.session_state['optimized_html'] = ""
if 'active_provider' not in st.session_state:
    st.session_state['active_provider'] = ""

with col1:
    st.subheader("📂 Optimization Inputs")
    
    # Card 1: Resume Upload
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📝 Upload Your Resume</div>', unsafe_allow_html=True)
    uploaded_resume = st.file_uploader(
        "Upload Resume (PDF or DOCX)",
        type=["pdf", "docx"],
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Card 2: Target Job Requirements
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🎯 Target Job Details</div>', unsafe_allow_html=True)
    st.caption("Select one of the tabs below to provide details about the job:")
    
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
            height=160,
            placeholder="Paste target job requirements, skills, and qualifications text here...",
            label_visibility="collapsed"
        )
        
    with tab_role:
        job_role = st.text_input(
            "Enter target job role...",
            placeholder="e.g. Senior Python Backend Developer, Data Scientist...",
            label_visibility="collapsed"
        )
        st.info("💡 Useful when a full job description is unavailable. The engine optimizes your resume based on standard industry skills for this role.")
        
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
            st.success("Image uploaded successfully!")
            st.image(file_bytes, caption="Uploaded JD Image", use_column_width=True)
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action Trigger Button
    st.markdown("<br>", unsafe_allow_html=True)
    optimize_btn = st.button("✨ Optimize & Tailor Resume", use_container_width=True)

with col2:
    st.subheader("🖥️ Tailored Resume Workspace")
    
    # Trigger processing on button click
    if optimize_btn:
        if uploaded_resume is None:
            st.error("⚠️ Please upload your existing resume (.pdf or .docx).")
        elif not job_desc_text.strip() and not job_role.strip() and not img_b64:
            st.error("⚠️ Please specify at least one job input method (JD Text, Job Role, or JD Image).")
        elif enable_advanced and not company_name.strip():
            st.error("⚠️ Please enter the company name in the sidebar or disable Company Research Mode.")
        else:
            with st.spinner("🚀 Extracting text and tailoring resume with AI agents..."):
                extracted_resume_text = document_parser.extract_text_from_file(uploaded_resume)
                
                if not extracted_resume_text.strip():
                    st.error("⚠️ Could not extract text from the file. Please ensure it contains readable text.")
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
                        st.success(f"Tailored successfully using {result['provider']}!")
                    else:
                        st.session_state['optimized_html'] = ""
                        st.session_state['active_provider'] = ""
                        st.markdown(result["content"], unsafe_allow_html=True)

    # Output Rendering Block
    if st.session_state['optimized_html']:
        html_content = st.session_state['optimized_html']
        plain_text_resume = document_parser.convert_html_to_text(html_content)
        
        # 1. Download Options Card
        st.markdown(f"""
        <div class="download-card">
            <div class="download-title">✅ Resume Tailored Successfully!</div>
            <div style="font-size: 13px; color: #1e293b; margin-bottom: 15px;">
                Your resume was optimized using <strong>{st.session_state['active_provider']}</strong> and fits perfectly on a single A4 page. Download the file below.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Download Buttons Column
        dcol1, dcol2 = st.columns(2)
        with dcol1:
            st.download_button(
                label="📄 Download HTML Resume",
                data=html_content,
                file_name="tailored_resume.html",
                mime="text/html",
                use_container_width=True
            )
        with dcol2:
            st.download_button(
                label="📝 Download Plain Text (MD)",
                data=plain_text_resume,
                file_name="tailored_resume.md",
                mime="text/markdown",
                use_container_width=True
            )
            
        st.markdown("""
        <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 12px; margin-top: 10px; font-size: 12px; color: #1e3a8a;">
            💡 <strong>How to Print to A4 PDF:</strong> Open the downloaded HTML file in Google Chrome (or any browser), press <code>Ctrl + P</code> (or <code>Cmd + P</code>), set Margins to <strong>'None'</strong>, enable <strong>Background Graphics</strong>, and save as PDF.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 2. Preview Panel Tabs (A4 Preview and Plain Text Output)
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
            
    else:
        # Default placeholder when state is empty
        st.markdown("""
        <div class="skeleton-box">
            <div style="font-size: 64px; margin-bottom: 20px;">📄</div>
            <h3 style="margin: 0 0 10px 0; color: #374151; font-weight: 700;">Resume Preview Workspace</h3>
            <p style="margin: 0 auto 25px auto; font-size: 14px; max-width: 400px; color: #6b7280;">
                Provide your existing resume and job details on the left, then click <strong>Optimize & Tailor Resume</strong> to generate your single-page tailored output.
            </p>
            <div style="max-width: 250px; margin: 0 auto; display: flex; flex-direction: column; gap: 8px;">
                <div style="height: 10px; background-color: #f3f4f6; border-radius: 4px; border: 1px solid #e5e7eb;"></div>
                <div style="height: 10px; background-color: #f3f4f6; border-radius: 4px; border: 1px solid #e5e7eb; width: 80%; margin: 0 auto;"></div>
                <div style="height: 10px; background-color: #f3f4f6; border-radius: 4px; border: 1px solid #e5e7eb; width: 90%; margin: 0 auto;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
