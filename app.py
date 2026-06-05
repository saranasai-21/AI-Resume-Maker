import os
import streamlit as st
import requests
import base64
import io

try:
    from pypdf import PdfReader
except ImportError:
    pass

try:
    from docx import Document
except ImportError:
    pass

# --- API Configuration and Fallback Logic ---

def get_providers():
    providers = []
    for i in range(1, 7):
        key = os.getenv(f"GEMINI_KEY_{i}")
        if key:
            providers.append({"type": "gemini", "key": key})
            
    groq_key = os.getenv("GROQ_KEY")
    if groq_key:
        providers.append({"type": "groq", "key": groq_key})
        
    or_key = os.getenv("OPENROUTER_KEY")
    if or_key:
        providers.append({"type": "openrouter", "key": or_key})
        
    return providers

SYSTEM_PROMPT = """You are a professional resume writer. The user will give you their resume and a job description. Your task:
1. Rewrite the Career Objective to perfectly match the job role and keywords
2. Update the Skills section to highlight skills most relevant to the job
3. Adjust project descriptions, achievements, and experience bullet points to use keywords and language from the JD
4. Keep all real facts — do NOT invent experience or education
5. Return ONLY valid HTML for the resume body (no markdown, no explanation), using inline styles, structured for an A4 page
6. The HTML must use a clean, professional single-column layout with sections: Career Objective, Skills, Experience, Projects, Education, Certifications (only if present)
7. Use font-family: 'Georgia', serif for headings and 'Arial', sans-serif for body
8. Make the design ATS-friendly: no tables, no columns, no images."""

def call_gemini(key, sys_prompt, prompt, image_b64):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={key}"
    parts = [{"text": f"SYSTEM: {sys_prompt}\n\nUSER: {prompt}"}]
    
    if image_b64 and "," in image_b64:
        try:
            mime_type = image_b64.split(";")[0].split(":")[1]
            base64_data = image_b64.split(",")[1]
            parts.append({
                "inline_data": {
                    "mime_type": mime_type,
                    "data": base64_data
                }
            })
        except Exception as e:
            st.error(f"Failed to parse image for Gemini: {e}")
            
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {"temperature": 0.2}
    }
    
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Gemini error: {response.text}")
        
    data = response.json()
    try:
        text = data['candidates'][0]['content']['parts'][0]['text']
        return text
    except KeyError:
        raise Exception(f"Unexpected Gemini response structure: {data}")

def call_openai_compatible(url, key, model, sys_prompt, prompt, image_b64, provider_name):
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    messages = [{"role": "system", "content": sys_prompt}]
    content = [{"type": "text", "text": prompt}]
    
    if image_b64:
        if provider_name == "groq":
            raise Exception("Groq standard models do not support vision. Skipping.")
        content.append({
            "type": "image_url",
            "image_url": {"url": image_b64}
        })
        
    messages.append({"role": "user", "content": content})
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.2
    }
    
    if provider_name == "openrouter":
        headers["HTTP-Referer"] = "https://huggingface.co/spaces/"
        headers["X-Title"] = "ResumeAI"
        
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"{provider_name} error: {response.text}")
        
    data = response.json()
    return data['choices'][0]['message']['content']

def optimize_resume(resume_text, job_description_text, job_image_base64, company_name):
    providers = get_providers()
    if not providers:
        st.warning("Running in local mode without API keys? Output might fail unless keys are injected via environment.")
        
    sys_prompt = SYSTEM_PROMPT
    if company_name:
        sys_prompt += f"\n\nIMPORTANT ADVANCED DIRECTIVE: You must act as an expert recruiter for {company_name}. Research and use your knowledge of {company_name}'s past recruitment preferences, company culture, and successful resume patterns for this specific role. Tailor the resume strongly to appeal directly to what {company_name} looks for in candidates."

    prompt = f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{job_description_text}\n\nReturn ONLY the HTML."
    
    errors = []
    for p in providers:
        try:
            if p["type"] == "gemini":
                result = call_gemini(p["key"], sys_prompt, prompt, job_image_base64)
                return result
            elif p["type"] == "groq":
                if job_image_base64:
                    continue # Skip Groq if image is present
                result = call_openai_compatible("https://api.groq.com/openai/v1/chat/completions", p["key"], "llama-3.3-70b-versatile", sys_prompt, prompt, None, "groq")
                return result
            elif p["type"] == "openrouter":
                result = call_openai_compatible("https://openrouter.ai/api/v1/chat/completions", p["key"], "anthropic/claude-3.5-sonnet", sys_prompt, prompt, job_image_base64, "openrouter")
                return result
        except Exception as e:
            errors.append(f"{p['type']} failed: {str(e)}")
            continue
            
    if not providers:
        return "<h2 style='color:red;'>Error: No API keys configured in environment variables.</h2>"
    
    return f"<h2 style='color:red;'>All API providers failed or rate limited.</h2><p>{str(errors)}</p>"

def extract_text_from_file(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        try:
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            return ""
    elif uploaded_file.name.endswith(".docx"):
        try:
            doc = Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            st.error(f"Error reading DOCX: {e}")
            return ""
    else:
        try:
            return uploaded_file.getvalue().decode("utf-8")
        except:
            return ""

# --- UI Layout ---

st.set_page_config(page_title="ResumeAI Optimizer", page_icon="🚀", layout="wide")

st.markdown("""
<style>
/* CSS optimizations for mobile & clean design */
.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
}
h1 {
    background: -webkit-linear-gradient(45deg, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px;
    font-size: 2.5rem;
}
@media (max-width: 768px) {
    h1 { font-size: 2rem; }
    .subtitle { font-size: 1rem; }
}
.subtitle {
    color: #6b7280;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}
.a4-container {
    width: 100%;
    max-width: 800px;
    background: white;
    padding: 40px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.06);
    border-radius: 12px;
    margin: 0 auto;
    border: 1px solid #e5e7eb;
}
@media (max-width: 768px) {
    .a4-container {
        padding: 15px; /* smaller padding on mobile */
    }
}
/* Input boxes styling */
.stTextArea textarea {
    border-radius: 8px;
    border: 1px solid #e5e7eb;
}
.stTextArea textarea:focus {
    border-color: #8b5cf6;
    box-shadow: 0 0 0 1px #8b5cf6;
}
.css-1n76uvr {
    gap: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

st.title("ResumeAI 🚀")
st.markdown("<div class='subtitle'>Smart Resume Optimizer — Clean & Mobile Optimized</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.header("Inputs")
    
    st.markdown("**(1) Upload Your Existing Resume**")
    uploaded_resume = st.file_uploader("Upload PDF or DOCX file", type=["pdf", "docx"], label_visibility="collapsed")
    
    st.markdown("**(2) Target Job Description**")
    job_desc_text = st.text_area("Paste the target job description text...", height=150, label_visibility="collapsed")
    
    st.markdown("**(Optional) Upload JD as Image**")
    uploaded_image = st.file_uploader("If the JD is an image, upload it here", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    
    img_b64 = ""
    if uploaded_image is not None:
        file_bytes = uploaded_image.getvalue()
        mime_type = uploaded_image.type
        encoded = base64.b64encode(file_bytes).decode()
        img_b64 = f"data:{mime_type};base64,{encoded}"
        st.success("Image attached successfully.")

    st.markdown("---")
    st.subheader("Advanced Settings")
    enable_advanced = st.checkbox("Enable Company Research")
    company_name = ""
    if enable_advanced:
        company_name = st.text_input("Target Company Name", placeholder="e.g., Google, CyberNext...")

    st.markdown("<br>", unsafe_allow_html=True)
    optimize_btn = st.button("✨ Optimize Resume", use_container_width=True, type="primary")

with col2:
    st.header("Tailored A4 Preview")
    
    if 'optimized_html' not in st.session_state:
        st.session_state['optimized_html'] = ""
        
    if optimize_btn:
        if uploaded_resume is None:
            st.error("Please upload your existing resume (.pdf or .docx).")
        elif not job_desc_text.strip() and not img_b64:
            st.error("Please provide a job description (text or image).")
        elif enable_advanced and not company_name.strip():
            st.error("Please enter the target company name or disable Company Research.")
        else:
            with st.spinner("Extracting text and tailoring resume with AI..."):
                extracted_resume_text = extract_text_from_file(uploaded_resume)
                
                if not extracted_resume_text.strip():
                    st.error("Could not extract any text from the uploaded file. Please ensure it's a valid PDF or DOCX.")
                else:
                    raw_html = optimize_resume(extracted_resume_text, job_desc_text, img_b64, company_name)
                    
                    clean_html = raw_html.strip()
                    if clean_html.startswith('```html'):
                        clean_html = clean_html[7:]
                    elif clean_html.startswith('```'):
                        clean_html = clean_html[3:]
                    if clean_html.endswith('```'):
                        clean_html = clean_html[:-3]
                    clean_html = clean_html.strip()
                    
                    st.session_state['optimized_html'] = clean_html
                    st.success("Optimization Complete!")

    if st.session_state['optimized_html']:
        html_content = st.session_state['optimized_html']
        
        # Download HTML Button
        st.download_button(
            label="📄 Download Resume (Open in browser and Print to PDF)",
            data=html_content,
            file_name="tailored_resume.html",
            mime="text/html",
            use_container_width=True
        )
        
        # Render HTML preview safely
        st.components.v1.html(
            f"<div class='a4-container'>{html_content}</div>",
            height=800,
            scrolling=True
        )
    else:
        st.info("Upload your resume, provide a job description, and click **Optimize Resume** to generate your tailored single-page resume.")
