# ResumeAI Optimizer
An advanced AI-powered resume tailoring and optimization system developed using Streamlit, Python, and multi-agent LLM routing. This project optimizes and tailors resumes to target job descriptions, roles, or job description images to ensure they are ATS-compliant and fit exactly onto a single A4 page.

📌 Project Overview
A professional resume is critical for:
- Passing Applicant Tracking Systems (ATS)
- Tailoring key skills to specific job requirements
- Highlighting relevant work experience using strong action verbs
- Fitting high-impact career details on a single A4 page
- Standing out to hiring managers and recruiters

This project uses a multi-agent routing system across different LLM providers (Gemini, Groq, and OpenRouter) to rewrite, format, and align your resume to a target job description or role. The system features a modern Streamlit interface with a live single-page A4 preview and multi-format (PDF/DOCX) download options.

Deep Learning & LLM Architecture
The resume optimizer uses:
- **Multi-Agent & Multi-Provider Routing**: Connects to Gemini, Groq, and OpenRouter APIs.
- **Sequential Fallback Mechanism**: Sequentially queries up to 6 configured Gemini keys first, falling back to Groq, and then OpenRouter if previous attempts fail or get rate-limited.
- **Vision Integration**: Utilizes Gemini 2.5 Flash for analyzing uploaded Job Description (JD) images.
- **Custom System Prompt & Guidelines**: Enforces ATS compliance, single-page format constraints, and zero-hallucination rules.
- **Automated Rate Limit Handling**: Automatic detection of HTTP 429 errors with built-in delay and retry logic.

📊 Feature & Alignment Options
The system is built to process:
- **Resume Uploads**: Parses text from PDF and DOCX files (including paragraph and table data).
- **Target Job Description Text**: Direct input text parser for specific job requirements.
- **Target Job Role**: AI-powered role researching (looks up standard industry expectations for a role when a full JD is not available).
- **JD Image Scan**: Base64 image-to-text decoding using LLM vision capabilities.
- **Target Company Alignment**: Tone and style alignment specific to a company's hiring standards and work culture (e.g. Google, Stripe).

📈 System Features & Quality
| Feature | Implementation Details |
| --- | --- |
| **A4 Single-Page Fit** | Auto-font-scaling loop using client-side JavaScript to reduce font size dynamically (from 11px down to 7.5px) if content exceeds page bounds. |
| **ATS Formatting** | Plain Arial/Georgia typography, clean hierarchy (H1, H2, H3, list bullets), no layout tables, and no multi-column formats. |
| **Downloadable DOCX** | Server-side conversion using BeautifulSoup4 and `python-docx` to format margins (0.5"), headings, bullet points, and contact details. |
| **Downloadable PDF** | Server-side HTML-to-PDF rendering using WeasyPrint with styling, with fallback print-to-pdf instructions. |

Technologies Used
- Python
- Streamlit
- WeasyPrint
- PyPDF
- python-docx
- BeautifulSoup4
- Requests / API integration

🚀 Streamlit Application
The Streamlit dashboard allows users to:
- Upload existing resumes in PDF or DOCX format.
- Input target job details via text description, job role, or image upload.
- Choose optional target company styling.
- Preview the tailored resume in real-time in a single-page A4 mockup.
- Download the optimized resume in PDF or DOCX format, or copy the markdown plain-text translation.

Run the Project
Install System Dependencies (For PDF rendering via WeasyPrint)
- **Windows**: Install GTK+ or MSYS2 packages for `pango` and `cairo`.
- **Linux (Debian/Ubuntu)**:
  `sudo apt-get install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 libffi-dev shared-mime-info`

Install Python Requirements
- `pip install -r requirements.txt`

Run Streamlit App
- `streamlit run app.py`

📂 Project Structure
ResumeAI Optimizer
│
├── app.py
├── api_router.py
├── document_parser.py
├── prompts.py
├── requirements.txt
├── packages.txt
└── README.md

Developed as an advanced AI career tool using multi-agent architectures for professional resume customization.

🌐 Live Demo
Streamlit App / HF Space: https://huggingface.co/spaces/fournew/ResumeAI-Optimizer
