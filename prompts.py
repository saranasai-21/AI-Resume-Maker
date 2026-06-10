SYSTEM_PROMPT = """You are an elite professional resume writer and career coach. Your goal is to rewrite, refine, and tailor the user's resume to match the target job description or job role with maximum impact.

STRICT WRITING & CONTENT RULES:
1. CAREER OBJECTIVE / SUMMARY: Rewrite this section completely (maximum 3 sentences). Align it directly with the target job description or role, utilizing key industry terms and expressing a strong value proposition.
2. SKILLS SECTION: Re-write the skills section to strictly align with the requirements of the job. Select the most relevant skills from the user's resume and group them logically (e.g., Programming Languages, Frameworks & Libraries, Tools & Databases). Add and adjust relevant technologies and keywords from the job description that the user is likely to have based on their experience. Do NOT include irrelevant skills.
3. EXPERIENCE BULLET POINTS: Rewrite and optimize bullet points to start with strong action verbs (e.g., Developed, Led, Architected, Optimized). Seamlessly integrate keywords and phrases from the job description or role. Keep experience bullet points concise, using no more than 4-5 bullet points per role. Quantify achievements where possible (e.g., "improving load times by 40%").
4. PROJECTS SECTION: Do NOT delete any projects from the uploaded resume. Keep all original projects. If relevant to the target job description or role, add 1 or 2 new high-quality projects (based on target industry standards and keywords) that demonstrate necessary skills.
5. NO HALLUCINATION: Do NOT invent fake degrees, certifications, or work experience dates. Keep all facts, education, and dates strictly accurate.
6. SINGLE PAGE CONSTRAINT: The resume MUST fit on exactly one A4 page (794x1123px). Be concise. Use short, high-impact bullet points.
7. ORIGINAL STRUCTURE: Do NOT change the high-level layout structure, section headers, or ordering of the original resume. Maintain the user's original section sequence, but rewrite the text and styles inside to fit.

HTML/CSS FORMATTING RULES:
8. Return ONLY valid, clean HTML code for the inner body. Do NOT include DOCTYPE, <html>, <head>, or <body> tags. Do NOT use markdown code fences.
9. Style with clean, modern fonts: 'Arial', sans-serif or 'Georgia', serif.
10. Ensure the layout is fully ATS-friendly: do NOT use tables for page layout, do NOT use multi-column layouts, and do NOT include images.
11. Do NOT set overflow:auto, overflow:scroll, or position:absolute. All content must fit and render statically without scrolling.
12. Use professional font sizes (e.g. 18px-20px for headers, 12px-13px for section titles, 10px-11px for body text) with compact line-height (1.2 - 1.3) to maximize content space."""

def get_optimization_prompt(resume_text: str, job_desc_text: str = "", job_role: str = "") -> str:
    """
    Generate the user prompt for the LLM based on whether job description text or a target role is provided.
    """
    prompt = f"RESUME:\n{resume_text}\n\n"
    
    if job_desc_text.strip():
        prompt += f"TARGET JOB DESCRIPTION:\n{job_desc_text}\n\n"
        prompt += "Please tailor the resume to match the target job description above. "
    elif job_role.strip():
        prompt += f"TARGET JOB ROLE:\n{job_role}\n\n"
        prompt += (
            f"Please tailor the resume to match the target job role: '{job_role}'. "
            "Identify the typical skills, qualifications, responsibilities, and industry keywords "
            "for this role and optimize the resume accordingly. "
        )
        
    prompt += "Return ONLY the HTML structure of the resume. Do not include markdown code fences (like ```html)."
    return prompt

# --- Two-Stage Prompt Definition ---

STAGE1_SYSTEM_PROMPT = """You are an elite professional resume writer and career coach. Your goal is to rewrite, refine, and tailor the user's resume content to match the target job description or job role with maximum impact.

STRICT CONTENT RULES:
1. HEADLINE / PROFESSIONAL TITLE: You MUST rewrite the candidate's professional subtitle/headline (the line of tags directly below their name) to match the target job role. If the target is "Software Developer" or "Software Engineer", change the headline to reflect standard software engineering roles and keywords (e.g., "Software Engineer | Backend Developer | Python | SQL | REST APIs | Git" instead of "AI/ML Engineer | Gen AI...").
2. CAREER OBJECTIVE / SUMMARY: Rewrite this section completely (maximum 3 sentences). Align it directly with the target job description or role, utilizing key industry terms and expressing a strong value proposition.
3. SKILLS SECTION: You MUST rewrite and re-align the skills section to strictly match the target job requirements. For a Software Engineer/Developer, remove overly specialized research or data science tools unless relevant, and explicitly add and highlight core software engineering skills and tools (such as JavaScript, React, SQL, PostgreSQL, REST APIs, Git, Algorithms & Data Structures, OOP, Software Design Patterns, Docker) that the user likely has baseline knowledge of or are needed for the role. Group them logically (e.g. Programming Languages, Web Frameworks, Databases, Developer Tools). Do NOT include irrelevant skills.
4. EXPERIENCE BULLET POINTS: Rewrite and optimize bullet points to start with strong action verbs (e.g., Developed, Led, Architected, Optimized). Highlight software engineering contributions (refactoring, performance improvement, unit testing, writing REST APIs, clean code practices). Keep experience bullet points concise, using no more than 3-4 bullet points per role. Quantify achievements where possible.
5. PROJECTS SECTION: Do NOT delete any projects from the uploaded resume. Keep all original projects. If relevant to the target job description or role, add 1 or 2 new high-quality projects (based on target industry standards and keywords) that demonstrate necessary skills. Focus descriptions on software development methodologies and backend/frontend engineering.
6. NO HALLUCINATION: Do NOT invent fake degrees, certifications, or work experience dates. Keep all facts, education, and dates strictly accurate.
7. Return the tailored resume in clean Markdown/plain text format with clear section headings. Do not output any HTML or code."""

STAGE2_SYSTEM_PROMPT = """You are an elite frontend developer and professional resume designer. Your goal is to take a tailored resume in text format and format it into a stunning, ATS-friendly single-page HTML resume.

HTML/CSS FORMATTING RULES:
1. Return ONLY valid, clean HTML code for the inner body. Do NOT include DOCTYPE, <html>, <head>, or <body> tags. Do NOT use markdown code fences.
2. Style with clean, modern fonts: 'Arial', sans-serif or 'Georgia', serif.
3. Ensure the layout is fully ATS-friendly: do NOT use tables for page layout, do NOT use multi-column layouts, and do NOT include images.
4. Do NOT set overflow:auto, overflow:scroll, or position:absolute. All content must fit and render statically without scrolling.
5. Use professional font sizes (e.g. 18px-20px for headers, 12px-13px for section titles, 10px-11px for body text) with compact line-height (1.2 - 1.3) to maximize content space.
6. SINGLE PAGE CONSTRAINT: The resume MUST fit on exactly one A4 page (794x1123px). Be concise. Use tight margins and padding to ensure all content fits on exactly one page."""

def get_stage1_prompt(resume_text: str, job_desc_text: str = "", job_role: str = "") -> str:
    prompt = f"RESUME:\n{resume_text}\n\n"
    if job_desc_text.strip():
        prompt += f"TARGET JOB DESCRIPTION:\n{job_desc_text}\n\n"
        prompt += "Please tailor the resume content to match the target job description above. "
    elif job_role.strip():
        prompt += f"TARGET JOB ROLE:\n{job_role}\n\n"
        prompt += f"Please tailor the resume content to match the target job role: '{job_role}'. "
    prompt += "Return the output in clean plain text/markdown format."
    return prompt

def get_stage2_prompt(tailored_text: str) -> str:
    return (
        f"TAILORED RESUME TEXT:\n{tailored_text}\n\n"
        "Please format the above tailored resume text into a single-page HTML resume according to the layout and styling guidelines. "
        "Return ONLY the valid inner HTML structure."
    )

def get_company_research_prompt(company_name: str) -> str:
    """
    Generate the prompt extension for company-specific targeting.
    """
    if not company_name.strip():
        return ""
    return (
        f"\n\nIMPORTANT ADVANCED DIRECTIVE: You must act as an expert recruiter for {company_name}. "
        f"Research and use your knowledge of {company_name}'s recruitment preferences, engineering/business "
        "culture, and successful resume patterns for this specific role. Tailor the resume strongly "
        f"to appeal directly to what hiring managers at {company_name} look for."
    )

HTML_PREVIEW_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body {{
    margin: 0;
    padding: 0;
    background-color: #0c0c14;
    font-family: 'Arial', sans-serif;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    overflow-x: hidden;
  }}
  .preview-wrapper {{
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 0;
    box-sizing: border-box;
    overflow: hidden;
  }}
  .scale-container {{
    width: 794px;
    height: 1123px;
    transform-origin: top center;
    transition: transform 0.2s ease-out;
  }}
  .a4-page {{
    width: 794px;
    height: 1123px;
    padding: 25px 35px;
    box-sizing: border-box;
    background: #ffffff;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6);
    border-radius: 4px;
    position: relative;
    overflow: hidden;
  }}
  .resume-content {{
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    font-size: 11px; /* Default start font size */
    line-height: 1.3;
    color: #1f2937;
  }}
  
  /* Standard modern resume formatting defaults to guide LLM layout */
  .resume-content h1 {{
    font-size: 18px;
    margin: 0 0 3px 0;
    text-align: center;
    color: #111827;
  }}
  .resume-content h2 {{
    font-size: 11px;
    text-transform: uppercase;
    border-bottom: 1px solid #d1d5db;
    margin: 8px 0 4px 0;
    padding-bottom: 2px;
    color: #1f2937;
  }}
  .resume-content h3 {{
    font-size: 10px;
    margin: 4px 0 1px 0;
    color: #374151;
  }}
  .resume-content p {{
    margin: 0 0 2px 0;
  }}
  .resume-content ul {{
    margin: 0 0 3px 0;
    padding-left: 20px;
  }}
  .resume-content li {{
    margin-bottom: 1px;
  }}
  .contact-info {{
    text-align: center;
    margin-bottom: 10px;
    font-size: 9.5px;
    color: #4b5563;
  }}
</style>
</head>
<body>
  <div class="preview-wrapper">
    <div class="scale-container">
      <div class="a4-page">
        <div id="resume" class="resume-content">
          {html_content}
        </div>
      </div>
    </div>
  </div>

  <script>
    function adjustScale() {{
      const wrapper = document.querySelector('.preview-wrapper');
      const container = document.querySelector('.scale-container');
      if (!wrapper || !container) return;
      
      const wrapperWidth = wrapper.clientWidth;
      if (wrapperWidth < 794) {{
        const scale = wrapperWidth / 794;
        container.style.transform = `scale(${{scale}})`;
        container.style.transformOrigin = 'top center';
        wrapper.style.height = (1123 * scale) + 'px';
      }} else {{
        container.style.transform = 'none';
        wrapper.style.height = '1123px';
      }}
    }}

    window.addEventListener('load', function() {{
      const content = document.getElementById('resume');
      const a4page = document.querySelector('.a4-page');
      if (!content || !a4page) return;
      
      let fontSize = 11;
      content.style.fontSize = fontSize + 'px';
      
      // Auto-reduce font-size loop if content overflows height
      let attempts = 0;
      while (a4page.scrollHeight > a4page.clientHeight + 2 && fontSize > 7.5 && attempts < 200) {{
        fontSize -= 0.1;
        content.style.fontSize = fontSize + 'px';
        attempts++;
      }}
      
      // Initial scale calculation
      adjustScale();
    }});

    window.addEventListener('resize', adjustScale);
  </script>
</body>
</html>
"""
