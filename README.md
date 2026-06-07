---
title: ResumeAI Optimizer
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.35.0
app_file: app.py
pinned: false
---

# 📄 ResumeAI Optimizer

ResumeAI Optimizer is a premium, AI-powered Streamlit web application designed to tailor your resume to a specific job description, job role, or job description image, ensuring it is optimized for Applicant Tracking Systems (ATS) and formatted to fit perfectly on exactly **one A4 page**.

Using a multi-agent system with automatic failovers and rate-limit retries, ResumeAI Optimizer ensures high reliability and quality by routing requests across Gemini, Groq, and OpenRouter APIs.

---

## ✨ Key Features

- **🎯 ATS-Optimized Tailoring**: Rewrites career summaries, structures and highlights relevant skills, and enhances experience bullet points using high-impact action verbs.
- **📄 Single-Page A4 Constraint**: Features a dynamic client-side scaling and font-reduction engine that automatically scales the resume HTML to fit perfectly on a single A4 page without overflowing or scrolling.
- **💼 Flexible Input Methods**:
  - **Job Description (JD) Text**: Paste direct text requirements.
  - **Target Job Role**: When full descriptions aren't available, the AI researches the industry standard requirements for the role.
  - **JD Image Upload**: Supports scanning job description images using LLM vision capabilities.
- **🏢 Company-Specific Alignment**: Option to align the tone, terminology, and engineering/business culture specifically with top target employers (e.g., Google, Stripe, CyberNext).
- **🤖 Robust Multi-Agent Routing & Failover**:
  - Automatically queries available API keys sequentially.
  - Configurable with up to **6 Gemini Keys** (Gemini Agents 1-6) using the newer `gemini-2.5-flash` model.
  - Falls back to **Groq Agent** (`llama-3.3-70b-versatile`) or **OpenRouter Agent** (`google/gemini-flash-1.5`) if primary agents hit rate limits or fail.
  - Implements automatic retry on 429 rate limit errors with exponential backoffs.
- **📥 Premium Document Formats**:
  - **Live Single-Page A4 Preview**: Dynamic iframe previewing of HTML resume rendering.
  - **Download PDF**: Server-side PDF rendering via WeasyPrint (or instructions for printing via browser for exact scaling).
  - **Download DOCX**: Auto-generated Word documents via `python-docx` and `BeautifulSoup4` featuring customized margins, typography, and section styling.
  - **Extracted Plain Text**: View and copy the markdown plain-text equivalent of the tailored resume.

---

## 🛠️ Technology Stack

- **Frontend/App Framework**: [Streamlit](https://streamlit.io/)
- **Document Processing**: `pypdf`, `python-docx`, `beautifulsoup4`, `lxml`
- **PDF Generation**: `weasyprint`
- **AI Integration**: Custom HTTP requests interacting with Gemini (`generativelanguage.googleapis.com`), Groq, and OpenRouter APIs.

---

## 🚀 Getting Started

### 📋 Prerequisites

Ensure you have Python 3.9+ installed on your machine.

### 🔧 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/saranasai-21/AI-Resume-Maker.git
   cd AI-Resume-Maker
   ```

2. **Install System Dependencies** (Required for PDF Generation via WeasyPrint):
   - **Windows**: Install GTK+ or MSYS2 packages for `pango` and `cairo`.
   - **Linux**: Install package requirements via `apt`:
     ```bash
     sudo apt-get install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 libffi-dev shared-mime-info
     ```

3. **Install Python Packages**:
   ```bash
   pip install -r requirements.txt
   ```

### 🔑 Configuration (API Keys)

The application pulls API keys from either Streamlit Secrets (for cloud deployment like Hugging Face Spaces) or local environment variables.

Create a `.env` file or export the variables in your shell:
```env
# Gemini API keys (configure up to 6 for multi-agent fallback)
GEMINI_KEY_1=your_gemini_key_here
GEMINI_KEY_2=your_second_gemini_key_here

# Groq API key (optional fallback)
GROQ_KEY=your_groq_key_here

# OpenRouter API key (optional fallback)
OPENROUTER_KEY=your_openrouter_key_here
```

### 💻 Running Locally

Launch the Streamlit web application:
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📁 Repository Structure

- [app.py](file:///c:/Users/Sarana%20Sai%20Bagadi/Downloads/AI-Resume-Maker/app.py): The main entry point of the Streamlit application setting up the premium theme, customized styling cards, tabs, inputs, and download structures.
- [api_router.py](file:///c:/Users/Sarana%20Sai%20Bagadi/Downloads/AI-Resume-Maker/api_router.py): Houses routing logic, multi-agent fallback sequences, rate limit retries, API request payloads, and safety checks.
- [document_parser.py](file:///c:/Users/Sarana%20Sai%20Bagadi/Downloads/AI-Resume-Maker/document_parser.py): Contains utilities to extract text from PDF/DOCX files, parse generated HTML back to structured markdown, and compile HTML content into downloadable PDF/DOCX bytes.
- [prompts.py](file:///c:/Users/Sarana%20Sai%20Bagadi/Downloads/AI-Resume-Maker/prompts.py): System instructions, tailoring guidelines (single-page constraint, ATS layout, no hallucination rules), and the core HTML preview template.
- [requirements.txt](file:///c:/Users/Sarana%20Sai%20Bagadi/Downloads/AI-Resume-Maker/requirements.txt): Python dependencies list.
- [packages.txt](file:///c:/Users/Sarana%20Sai%20Bagadi/Downloads/AI-Resume-Maker/packages.txt): Linux package dependencies for PDF rendering.
