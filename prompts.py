SYSTEM_PROMPT = """You are a professional resume writer. The user will give you their resume and details about their target job. Your task:
1. Rewrite the Career Objective/Summary to perfectly match the job role, keywords, and requirements.
2. Re-write the Skills section to strictly align with the target job description or target job role. Select only the skills from the user's resume that are relevant to the target job, and add/adjust key related technical terms and competencies that the user likely possesses based on their experience. Do NOT list irrelevant skills.
3. Adjust project descriptions, achievements, and experience bullet points to use keywords and language from the job description or role.
4. Keep all real facts — do NOT invent experience, degrees, or certifications.
5. Return ONLY valid, styled HTML for the resume body (no markdown block fences, no explanation).
6. The HTML must use a clean, professional layout with sections: Career Objective, Skills, Experience, Projects, Education, Certifications (if present).
7. Font-family: 'Arial', sans-serif or 'Georgia', serif.
8. Make the design ATS-friendly: no tables, no multi-column layouts, no images.
9. The resume MUST fit on exactly ONE A4 page (794x1123px). Be concise. Use no more than 4-5 bullet points per role. Limit career objective to 3 sentences.
10. Do NOT use any CSS that sets overflow:auto or overflow:scroll. All content must be visible without scrolling.
11. Return ONLY the inner HTML body content — do not include DOCTYPE, <html>, <head>, or <body> tags."""

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
    padding: 40px 50px;
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
    margin: 0 0 4px 0;
    text-align: center;
    color: #111827;
  }}
  .resume-content h2 {{
    font-size: 12px;
    text-transform: uppercase;
    border-bottom: 1px solid #d1d5db;
    margin: 10px 0 6px 0;
    padding-bottom: 2px;
    color: #1f2937;
  }}
  .resume-content h3 {{
    font-size: 11px;
    margin: 6px 0 2px 0;
    color: #374151;
  }}
  .resume-content p {{
    margin: 0 0 3px 0;
  }}
  .resume-content ul {{
    margin: 0 0 4px 0;
    padding-left: 20px;
  }}
  .resume-content li {{
    margin-bottom: 2px;
  }}
  .contact-info {{
    text-align: center;
    margin-bottom: 15px;
    font-size: 10px;
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
