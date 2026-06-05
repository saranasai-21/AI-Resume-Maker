import base64
import streamlit as st
import document_parser
import prompts
import api_router

# Page configuration for a spacious, professional feel
st.set_page_config(
    page_title="ResumeAI - Smart Resume Optimizer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium stylesheet injection
st.markdown("""
<style>
/* Modern styling with curated harmonious color palette */
.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
}
h1 {
    background: -webkit-linear-gradient(45deg, #2563eb, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px;
    font-size: 2.8rem;
    font-weight: 800;
}
.subtitle {
    color: #4b5563;
    font-size: 1.15rem;
    margin-bottom: 2rem;
    font-weight: 400;
}
.input-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: #1f2937;
    margin-top: 10px;
    margin-bottom: 5px;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    height: 40px;
    white-space: pre-wrap;
    background-color: #f3f4f6;
    border-radius: 6px;
    padding: 10px 16px;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background-color: #2563eb !important;
    color: white !important;
}
/* Input boxes styling */
.stTextArea textarea, .stTextInput input {
    border-radius: 8px;
    border: 1px solid #d1d5db;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 1px #2563eb;
}
hr {
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# Application Header
st.title("ResumeAI 🚀")
st.markdown("<div class='subtitle'>Smart Resume Optimizer — Clean, Professional & Mobile Optimized</div>", unsafe_allow_html=True)

# Create two columns for the workspace
col1, col2 = st.columns([1, 1.2], gap="large")

# Initialize session state for the optimized HTML resume
if 'optimized_html' not in st.session_state:
    st.session_state['optimized_html'] = ""
if 'active_provider' not in st.session_state:
    st.session_state['active_provider'] = ""

with col1:
    st.header("1. Upload & Target")
    
    st.markdown("<div class='input-header'>Upload Your Existing Resume</div>", unsafe_allow_html=True)
    uploaded_resume = st.file_uploader(
        "Upload PDF or DOCX file",
        type=["pdf", "docx"],
        label_visibility="collapsed"
    )
    
    st.markdown("<div class='input-header'>Target Job Requirements</div>", unsafe_allow_html=True)
    st.caption("Provide details about the target job. Select any method below:")
    
    # Elegant tabbed interface for Job Details
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
            placeholder="Paste the full job description text here (skills, qualifications, details)...",
            label_visibility="collapsed"
        )
        
    with tab_role:
        job_role = st.text_input(
            "Enter target job role...",
            placeholder="e.g. Senior Frontend Developer, Data Scientist, Product Manager...",
            label_visibility="collapsed"
        )
        st.info("💡 If you don't have a full job description, we will research and tailor your resume based on standard industry requirements for this role.")
        
    with tab_img:
        uploaded_image = st.file_uploader(
            "Upload Job Description Image",
            type=["png", "jpg", "jpeg"],
            label_visibility="collapsed"
        )
        if uploaded_image is not None:
            file_bytes = uploaded_image.getvalue()
            mime_type = uploaded_image.type
            encoded = base64.b64encode(file_bytes).decode()
            img_b64 = f"data:{mime_type};base64,{encoded}"
            st.success("Image attached successfully!")
            st.image(file_bytes, caption="JD Image Preview", use_column_width=True)

    st.markdown("---")
    st.subheader("Advanced Settings")
    enable_advanced = st.checkbox("Enable Company Research Mode")
    company_name = ""
    if enable_advanced:
        company_name = st.text_input(
            "Target Company Name", 
            placeholder="e.g. Google, CyberNext, Stripe...",
            help="Tailors wording, culture fit, and values specific to this company's hiring history."
        )

    st.markdown("<br>", unsafe_allow_html=True)
    optimize_btn = st.button("✨ Optimize Resume", use_container_width=True, type="primary")

with col2:
    st.header("2. Tailored A4 Preview")
    
    if optimize_btn:
        # Input Validation
        if uploaded_resume is None:
            st.error("⚠️ Please upload your existing resume (.pdf or .docx).")
        elif not job_desc_text.strip() and not job_role.strip() and not img_b64:
            st.error("⚠️ Please provide at least one job input (Job Description Text, Job Role, or JD Image).")
        elif enable_advanced and not company_name.strip():
            st.error("⚠️ Please enter the target company name or disable Company Research Mode.")
        else:
            with st.spinner("Extracting text and tailoring resume with AI..."):
                extracted_resume_text = document_parser.extract_text_from_file(uploaded_resume)
                
                if not extracted_resume_text.strip():
                    st.error("⚠️ Could not extract any text from the uploaded file. Please ensure it is a valid, readable PDF or DOCX.")
                else:
                    # Run API optimization fallback routing
                    result = api_router.run_resume_optimization(
                        resume_text=extracted_resume_text,
                        job_desc_text=job_desc_text,
                        job_role=job_role,
                        job_image_base64=img_b64,
                        company_name=company_name
                    )
                    
                    if result["success"]:
                        raw_html = result["content"]
                        
                        # Clean up markdown code blocks if the LLM outputted them
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
                        # Display error logs from fallback sequence
                        st.markdown(result["content"], unsafe_allow_html=True)

    # Output rendering panel
    if st.session_state['optimized_html']:
        html_content = st.session_state['optimized_html']
        
        # Download and Provider info
        st.markdown(f"**Agent Provider:** `{st.session_state['active_provider']}`")
        
        st.download_button(
            label="📄 Download Single-Page HTML Resume",
            data=html_content,
            file_name="tailored_resume.html",
            mime="text/html",
            use_container_width=True
        )
        
        # Embed in the responsive A4 wrapper template
        preview_page = prompts.HTML_PREVIEW_TEMPLATE.format(html_content=html_content)
        
        # Render the custom scaling A4 page inside the iframe component
        st.components.v1.html(
            preview_page,
            height=1200,
            scrolling=True
        )
    else:
        st.info("Upload your resume, specify the target job/role on the left, and click **Optimize Resume** to generate your tailored single-page resume.")
