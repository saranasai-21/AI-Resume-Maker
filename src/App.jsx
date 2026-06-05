import React, { useState, useEffect, useRef, useLayoutEffect } from 'react';
import './App.css';

// SVG Icons
const SparklesIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
);

const FileTextIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>
);

const BriefcaseIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
);

const DownloadIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
);

const SunIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M20 12h2"/><path d="M2 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
);

const MoonIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
);

const AlertCircleIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>
);

const ImageIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
);

const BuildingIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="16" height="20" x="4" y="2" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/></svg>
);


// Prepopulated sample data
const SAMPLE_RESUME = `JOHN DOE
john.doe@email.com | (123) 456-7890 | Seattle, WA | linkedin.com/in/johndoe

CAREER OBJECTIVE
Resourceful and detail-oriented Software Engineer with 5+ years of experience specializing in building scalable web applications, optimizing backend architectures, and driving frontend performance. Proven track record of leading development initiatives and delivering high-impact technical solutions.

SKILLS
- Languages: JavaScript (ES6+), TypeScript, HTML5, CSS3, SQL
- Frameworks & Libraries: React, Node.js, Express, Next.js, Redux, TailwindCSS
- Tools & Databases: Git, Docker, Webpack, PostgreSQL, MongoDB, AWS (S3, EC2)

PROFESSIONAL EXPERIENCE
Senior Software Engineer | TechSphere Solutions (2022 - Present)
- Led a team of 4 developers to redesign the core e-commerce frontend in React, improving page load speeds by 35% and increasing user conversion by 12%.
- Designed and built a microservices-based API using Node.js and Express, facilitating 10M+ daily transactions with 99.9% uptime.
- Mentored junior engineers, established code review standards, and introduced CI/CD pipelines using GitHub Actions.

Software Engineer | Innovate Corp (2020 - 2022)
- Developed responsive web interfaces for SaaS analytics platform using React and Tailwind CSS, improving user retention by 8%.
- Integrated third-party APIs (Stripe, SendGrid) and reduced database query response times by 40% through index optimization.

PROJECTS
Fintech Dashboard
- Architected a real-time financial tracking application using React and Chart.js, rendering dynamic analytics for over 50,000 active monthly users.
- Secured application endpoints utilizing OAuth 2.0 and JWT.

EDUCATION
B.S. in Computer Science | University of Washington (Graduated 2020)`;

const SAMPLE_JD = `Frontend Engineer (React)
At CyberNext, we are building the next generation of cybersecurity dashboards. We are looking for a Senior Frontend Engineer with expert-level React skills.

Requirements:
- Strong experience in React, TypeScript, and state management (Redux or Context API)
- Deep understanding of web performance optimization, code-splitting, and lazy loading
- Experience with modern UI design systems, Tailwind CSS, and styling components
- Familiarity with build tools like Vite or Webpack
- Passion for clean code, mentoring others, and collaborating with cross-functional teams
- Nice to have: Node.js experience and experience with micro-frontends`;

const MOCK_TAILORED_HTML = `<div style="font-family: Arial, sans-serif; padding: 10px; color: #1f2937;">
  <h1 style="font-family: Georgia, serif; text-align: center; font-size: 26px; margin: 0 0 4px 0; font-weight: bold; color: #111827;">JOHN DOE</h1>
  <p style="text-align: center; margin: 0 0 16px 0; font-size: 11px; color: #4b5563; font-weight: 500;">
    john.doe@email.com &nbsp;|&nbsp; (123) 456-7890 &nbsp;|&nbsp; Seattle, WA &nbsp;|&nbsp; linkedin.com/in/johndoe
  </p>
  
  <h2 style="font-family: Georgia, serif; border-bottom: 1.5px solid #111827; font-size: 14px; margin: 16px 0 6px 0; padding-bottom: 2px; text-transform: uppercase; font-weight: bold; color: #111827; letter-spacing: 0.5px;">Career Objective</h2>
  <p style="line-height: 1.5; margin: 0 0 12px 0; font-size: 11px; color: #374151;">
    Performance-driven Senior Frontend Engineer with 5+ years of experience specializing in building responsive React applications, optimization of web performance, and state management. Proven track record of leading developer teams to redesign e-commerce platforms using React, improving load times by 35%. Eager to apply expert React skills, TypeScript proficiency, and passion for clean, maintainable code to drive cybersecurity dashboard initiatives at CyberNext.
  </p>
  
  <h2 style="font-family: Georgia, serif; border-bottom: 1.5px solid #111827; font-size: 14px; margin: 16px 0 6px 0; padding-bottom: 2px; text-transform: uppercase; font-weight: bold; color: #111827; letter-spacing: 0.5px;">Skills</h2>
  <p style="line-height: 1.5; margin: 0 0 12px 0; font-size: 11px; color: #374151;">
    <strong>React Ecosystem:</strong> React, TypeScript, Redux, Context API, Next.js, micro-frontends<br/>
    <strong>Web Styling & Dev:</strong> Tailwind CSS, CSS3, HTML5, styling components, Webpack, Vite<br/>
    <strong>Backend & Systems:</strong> Node.js, Express, REST APIs, PostgreSQL, MongoDB, Git, Docker, CI/CD (GitHub Actions), AWS
  </p>
  
  <h2 style="font-family: Georgia, serif; border-bottom: 1.5px solid #111827; font-size: 14px; margin: 16px 0 6px 0; padding-bottom: 2px; text-transform: uppercase; font-weight: bold; color: #111827; letter-spacing: 0.5px;">Experience</h2>
  <div style="margin-bottom: 12px;">
    <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 12px; color: #111827; margin-bottom: 2px;">
      <span>Senior Software Engineer (Frontend Lead)</span>
      <span>2022 - Present</span>
    </div>
    <div style="display: flex; justify-content: space-between; font-style: italic; font-size: 10.5px; color: #4b5563; margin-bottom: 6px;">
      <span>TechSphere Solutions</span>
      <span>Seattle, WA</span>
    </div>
    <ul style="margin: 0; padding-left: 20px; font-size: 11px; color: #374151;">
      <li style="margin-bottom: 4px;">Led a team of 4 developers to redesign the core e-commerce frontend in React and TypeScript, optimizing page load speeds by 35% through code-splitting and lazy loading, yielding a 12% conversion increase.</li>
      <li style="margin-bottom: 4px;">Implemented centralized state management utilizing Redux, standardizing data architecture and improving responsiveness.</li>
      <li style="margin-bottom: 4px;">Mentored junior frontend developers, established code review standards, and introduced Vite-based build configurations to accelerate development.</li>
      <li style="margin-bottom: 4px;">Collaborated on a microservices-based API using Node.js and Express, ensuring 99.9% uptime for high-frequency operations.</li>
    </ul>
  </div>
  
  <div style="margin-bottom: 12px;">
    <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 12px; color: #111827; margin-bottom: 2px;">
      <span>Software Engineer</span>
      <span>2020 - 2022</span>
    </div>
    <div style="display: flex; justify-content: space-between; font-style: italic; font-size: 10.5px; color: #4b5563; margin-bottom: 6px;">
      <span>Innovate Corp</span>
      <span>Seattle, WA</span>
    </div>
    <ul style="margin: 0; padding-left: 20px; font-size: 11px; color: #374151;">
      <li style="margin-bottom: 4px;">Developed responsive web interfaces for SaaS analytics platforms using React and Tailwind CSS, resulting in an 8% user retention improvement.</li>
      <li style="margin-bottom: 4px;">Integrated third-party APIs (Stripe, SendGrid) and reduced database query response times by 40% through index optimization.</li>
    </ul>
  </div>
  
  <h2 style="font-family: Georgia, serif; border-bottom: 1.5px solid #111827; font-size: 14px; margin: 16px 0 6px 0; padding-bottom: 2px; text-transform: uppercase; font-weight: bold; color: #111827; letter-spacing: 0.5px;">Projects</h2>
  <div style="margin-bottom: 12px;">
    <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 11.5px; color: #111827; margin-bottom: 2px;">
      <span>Fintech Analytics Dashboard</span>
      <span>React, Chart.js, Tailwind CSS</span>
    </div>
    <ul style="margin: 0; padding-left: 20px; font-size: 11px; color: #374151;">
      <li style="margin-bottom: 4px;">Architected a real-time financial tracking application in React with Chart.js, rendering dynamic analytics for 50,000+ active monthly users while securing endpoints via JWT/OAuth 2.0.</li>
    </ul>
  </div>
  
  <h2 style="font-family: Georgia, serif; border-bottom: 1.5px solid #111827; font-size: 14px; margin: 16px 0 6px 0; padding-bottom: 2px; text-transform: uppercase; font-weight: bold; color: #111827; letter-spacing: 0.5px;">Education</h2>
  <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 11px; color: #111827;">
    <span>B.S. in Computer Science</span>
    <span>Graduated 2020</span>
  </div>
  <div style="display: flex; justify-content: space-between; font-style: italic; font-size: 10.5px; color: #4b5563;">
    <span>University of Washington</span>
    <span>Seattle, WA</span>
  </div>
</div>`;

function App() {
  const [resumeText, setResumeText] = useState(SAMPLE_RESUME);
  const [jobDescription, setJobDescription] = useState(SAMPLE_JD);
  const [jobImageBase64, setJobImageBase64] = useState('');
  const [advancedEnabled, setAdvancedEnabled] = useState(false);
  const [companyName, setCompanyName] = useState('');
  
  const [optimizedHtml, setOptimizedHtml] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [theme, setTheme] = useState('dark');
  const [previewScale, setPreviewScale] = useState(1);
  const [fontSize, setFontSize] = useState(11);

  const previewWrapperRef = useRef(null);
  const previewContainerRef = useRef(null);
  const previewContentRef = useRef(null);

  // Set initial theme
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  // Handle preview container scaling to fit responsiveness
  useEffect(() => {
    if (!previewWrapperRef.current) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (let entry of entries) {
        const width = entry.contentRect.width;
        // Baseline width is 794px for A4. Scale factor is width / 794.
        const newScale = Math.min((width - 8) / 794, 1.0);
        setPreviewScale(newScale);
      }
    });

    resizeObserver.observe(previewWrapperRef.current);
    return () => resizeObserver.disconnect();
  }, [optimizedHtml, isLoading]);

  // Auto-fit loop when optimized HTML renders
  useLayoutEffect(() => {
    if (!optimizedHtml || isLoading) return;

    const container = previewContentRef.current;
    if (!container) return;

    // Reset base font size to 11px
    let size = 11;
    container.style.fontSize = `${size}px`;
    container.style.setProperty('--base-font-size', `${size}px`);

    while (container.scrollHeight > 1123 && size > 8) {
      size -= 0.5;
      container.style.fontSize = `${size}px`;
      container.style.setProperty('--base-font-size', `${size}px`);
    }

    setFontSize(size);
  }, [optimizedHtml, isLoading]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  const loadDemo = () => {
    setIsLoading(true);
    setErrorMessage('');
    
    // Simulate a brief AI loading delay for beautiful UI effect
    setTimeout(() => {
      setOptimizedHtml(MOCK_TAILORED_HTML);
      setIsLoading(false);
    }, 1200);
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setJobImageBase64(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const removeImage = () => {
    setJobImageBase64('');
  };

  const handleOptimize = async () => {
    if (!resumeText.trim() || (!jobDescription.trim() && !jobImageBase64)) {
      setErrorMessage('Please provide both an existing resume and a job description (text or image).');
      return;
    }
    if (advancedEnabled && !companyName.trim()) {
      setErrorMessage('Please enter the target company name or disable Advanced Company Research.');
      return;
    }

    setIsLoading(true);
    setErrorMessage('');
    setOptimizedHtml('');

    try {
      // Point to local FastAPI proxy backend
      const response = await fetch('/api/optimize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          resume_text: resumeText,
          job_description_text: jobDescription,
          job_image_base64: jobImageBase64,
          company_name: advancedEnabled ? companyName : ''
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data?.detail || `API error: ${response.status} ${response.statusText}`);
      }

      const content = data.html;

      // Clean up markdown block fences if included by the LLM
      let cleanHtml = content.trim();
      if (cleanHtml.startsWith('```html')) {
        cleanHtml = cleanHtml.substring(7);
      } else if (cleanHtml.startsWith('```')) {
        cleanHtml = cleanHtml.substring(3);
      }
      if (cleanHtml.endsWith('```')) {
        cleanHtml = cleanHtml.substring(0, cleanHtml.length - 3);
      }
      cleanHtml = cleanHtml.trim();

      setOptimizedHtml(cleanHtml);
    } catch (err) {
      console.error(err);
      setErrorMessage(err.message || 'An unexpected error occurred while communicating with the backend.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadPdf = () => {
    if (!optimizedHtml) return;

    const opt = {
      margin: 0,
      filename: 'resume.pdf',
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };

    const element = previewContentRef.current;
    if (window.html2pdf && element) {
      window.html2pdf().from(element).set(opt).save();
    } else {
      setErrorMessage('PDF generator library (html2pdf) is not loaded.');
    }
  };

  const handleDownloadDocx = async () => {
    if (!optimizedHtml) return;

    if (!window.docx) {
      setErrorMessage('DOCX generator library (docx.js) is not loaded.');
      return;
    }

    try {
      const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } = window.docx;

      const parser = new DOMParser();
      const docEl = parser.parseFromString(optimizedHtml, 'text/html');
      const body = docEl.body;

      const docxChildren = [];

      // Helper to parse formatting inside elements
      const parseTextContainer = (element) => {
        const runs = [];
        element.childNodes.forEach((node) => {
          if (node.nodeType === Node.TEXT_NODE) {
            if (node.textContent) {
              runs.push(new TextRun({ text: node.textContent }));
            }
          } else if (node.nodeType === Node.ELEMENT_NODE) {
            const tagName = node.tagName.toUpperCase();
            if (tagName === 'STRONG' || tagName === 'B') {
              runs.push(new TextRun({ text: node.textContent, bold: true }));
            } else if (tagName === 'EM' || tagName === 'I') {
              runs.push(new TextRun({ text: node.textContent, italic: true }));
            } else if (tagName === 'BR') {
              runs.push(new TextRun({ text: '', break: 1 }));
            } else if (tagName === 'SPAN') {
              const isBold = node.style.fontWeight === 'bold' || node.style.fontWeight === '700';
              const isItalic = node.style.fontStyle === 'italic';
              runs.push(new TextRun({ text: node.textContent, bold: isBold, italic: isItalic }));
            } else {
              runs.push(new TextRun({ text: node.textContent }));
            }
          }
        });
        return runs;
      };

      // Traverse children of parsed HTML body
      const traverse = (nodes) => {
        nodes.forEach((node) => {
          if (node.nodeType !== Node.ELEMENT_NODE) return;
          const tagName = node.tagName.toUpperCase();

          if (tagName === 'H1') {
            docxChildren.push(new Paragraph({
              children: [new TextRun({ text: node.textContent, bold: true, size: 28, font: 'Georgia' })],
              heading: HeadingLevel.HEADING_1,
              alignment: AlignmentType.CENTER,
              spacing: { before: 200, after: 120 },
            }));
          } else if (tagName === 'H2') {
            docxChildren.push(new Paragraph({
              children: [new TextRun({ text: node.textContent, bold: true, size: 22, font: 'Georgia' })],
              heading: HeadingLevel.HEADING_2,
              spacing: { before: 180, after: 80 },
            }));
          } else if (tagName === 'H3') {
            docxChildren.push(new Paragraph({
              children: [new TextRun({ text: node.textContent, bold: true, size: 18, font: 'Georgia' })],
              heading: HeadingLevel.HEADING_3,
              spacing: { before: 120, after: 60 },
            }));
          } else if (tagName === 'P') {
            const isCenter = node.style.textAlign === 'center' || node.className === 'resume-header-info';
            docxChildren.push(new Paragraph({
              children: parseTextContainer(node),
              alignment: isCenter ? AlignmentType.CENTER : AlignmentType.LEFT,
              spacing: { after: 100 },
            }));
          } else if (tagName === 'UL') {
            node.querySelectorAll('li').forEach((li) => {
              docxChildren.push(new Paragraph({
                children: parseTextContainer(li),
                bullet: { level: 0 },
                spacing: { after: 60 },
              }));
            });
          } else if (tagName === 'OL') {
            node.querySelectorAll('li').forEach((li) => {
              docxChildren.push(new Paragraph({
                children: parseTextContainer(li),
                bullet: { level: 0 },
                spacing: { after: 60 },
              }));
            });
          } else if (tagName === 'DIV') {
            const hasBlocks = Array.from(node.children).some(child => 
              ['DIV', 'P', 'UL', 'OL', 'H1', 'H2', 'H3', 'H4'].includes(child.tagName.toUpperCase())
            );
            if (hasBlocks) {
              traverse(node.childNodes);
            } else {
              const isCenter = node.style.textAlign === 'center' || node.className === 'resume-header-info';
              docxChildren.push(new Paragraph({
                children: parseTextContainer(node),
                alignment: isCenter ? AlignmentType.CENTER : AlignmentType.LEFT,
                spacing: { after: 100 },
              }));
            }
          } else if (['SPAN', 'STRONG', 'B', 'EM', 'I'].includes(tagName)) {
            docxChildren.push(new Paragraph({
              children: parseTextContainer(node),
              spacing: { after: 100 },
            }));
          }
        });
      };

      traverse(body.childNodes);

      if (docxChildren.length === 0) {
        docxChildren.push(new Paragraph({
          children: [new TextRun({ text: body.textContent || "Tailored Resume" })],
        }));
      }

      const docFile = new Document({
        sections: [{
          properties: {
            page: {
              margin: {
                top: 1440,
                bottom: 1440,
                left: 1440,
                right: 1440,
              }
            }
          },
          children: docxChildren,
        }],
      });

      const blob = await Packer.toBlob(docFile);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'resume.docx';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

    } catch (err) {
      console.error(err);
      setErrorMessage(`Failed to export DOCX: ${err.message}`);
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="logo-container">
          <div className="logo-icon">
            <SparklesIcon />
          </div>
          <span className="logo-text">ResumeAI</span>
          <span className="logo-badge">PRO</span>
        </div>
        <div className="header-actions">
          <button 
            className="theme-toggle-btn" 
            onClick={toggleTheme} 
            title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
            aria-label="Toggle Theme"
          >
            {theme === 'dark' ? <SunIcon /> : <MoonIcon />}
          </button>
        </div>
      </header>

      {/* Main Workspace */}
      <main className="main-content">
        {/* Left Inputs Panel */}
        <section className="left-panel">
          {errorMessage && (
            <div className="error-banner">
              <AlertCircleIcon />
              <div style={{ flex: 1 }}>
                <span>{errorMessage}</span>
                {errorMessage.includes("API error") && (
                  <div style={{ marginTop: '8px' }}>
                    <button 
                      onClick={loadDemo}
                      className="logo-badge"
                      style={{ 
                        background: 'var(--accent-gradient)', 
                        border: 'none', 
                        color: 'white', 
                        cursor: 'pointer',
                        padding: '4px 10px',
                        borderRadius: '6px',
                        fontWeight: '700',
                        fontSize: '0.8rem',
                        boxShadow: '0 2px 8px var(--accent-glow)'
                      }}
                    >
                      Load Demo Resume (Skip API)
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          <div className="input-card">
            <h2 className="card-title">
              <FileTextIcon /> Existing Resume
            </h2>
            <p className="card-subtitle">Paste your current resume content here</p>
            <textarea
              className="resume-textarea"
              placeholder="Paste your existing resume here (work history, skills, education, etc.)..."
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
            />
          </div>

          <div className="input-card">
            <h2 className="card-title">
              <BriefcaseIcon /> Job Description
            </h2>
            <p className="card-subtitle">Paste the job description or upload an image</p>
            <textarea
              className="resume-textarea"
              placeholder="Paste the target job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              style={{ height: '140px' }}
            />
            
            <div className="image-upload-container">
              <label className="image-upload-btn">
                <ImageIcon />
                <span>Upload JD Image</span>
                <input type="file" accept="image/*" onChange={handleImageUpload} style={{ display: 'none' }} />
              </label>
              {jobImageBase64 && (
                <div className="image-preview-badge">
                  <span>Image Attached</span>
                  <button onClick={removeImage} className="remove-img-btn" title="Remove image">&times;</button>
                </div>
              )}
            </div>
          </div>

          <div className="input-card">
            <div className="advanced-toggle-header">
              <div>
                <h2 className="card-title" style={{ fontSize: '1.05rem' }}>
                  <BuildingIcon /> Advanced Company Research
                </h2>
                <p className="card-subtitle" style={{ marginTop: '4px', fontSize: '0.8rem' }}>
                  Tailor to the company's culture and recruitment patterns
                </p>
              </div>
              <label className="toggle-switch">
                <input 
                  type="checkbox" 
                  checked={advancedEnabled} 
                  onChange={(e) => setAdvancedEnabled(e.target.checked)} 
                />
                <span className="slider round"></span>
              </label>
            </div>
            
            {advancedEnabled && (
              <div className="advanced-input-container">
                <input 
                  type="text" 
                  className="company-input" 
                  placeholder="Enter target company name (e.g. CyberNext)..."
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                />
              </div>
            )}
          </div>

          <button
            className="optimize-btn"
            onClick={handleOptimize}
            disabled={isLoading || !resumeText.trim() || (!jobDescription.trim() && !jobImageBase64)}
          >
            {isLoading ? (
              <>
                <div className="spinner" />
                <span>Optimizing Resume...</span>
              </>
            ) : (
              <>
                <SparklesIcon />
                <span>Optimize Resume</span>
              </>
            )}
          </button>
        </section>

        {/* Right Output Panel */}
        <section className="right-panel">
          <div className="output-header">
            <h2 className="output-title">Tailored A4 Preview</h2>
            {optimizedHtml && (
              <span className="logo-badge" style={{ background: '#10b981' }}>
                Auto-fit font: {fontSize}px
              </span>
            )}
          </div>

          {/* Scaled Preview Frame */}
          <div className="preview-wrapper" ref={previewWrapperRef}>
            <div className="preview-scroll-container">
              <div 
                className="preview-container"
                ref={previewContainerRef}
                style={{ '--preview-scale': previewScale }}
              >
                {isLoading ? (
                  <div className="loading-preview">
                    <div className="spinner" style={{ width: '40px', height: '40px', borderTopColor: 'var(--accent-color)' }} />
                    <span className="loading-text">Tailoring your resume with AI...</span>
                  </div>
                ) : optimizedHtml ? (
                  <div 
                    className="preview-content resume-body" 
                    ref={previewContentRef}
                    style={{ fontSize: `${fontSize}px` }}
                    dangerouslySetInnerHTML={{ __html: optimizedHtml }}
                  />
                ) : (
                  <div className="empty-preview">
                    <svg className="empty-preview-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <h3 className="empty-preview-title">No Resume Generated</h3>
                    <p className="empty-preview-text">
                      Fill out the inputs on the left and click <strong>Optimize Resume</strong> to generate your tailored single-page resume.
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Download Action Buttons */}
          {optimizedHtml && !isLoading && (
            <div className="action-buttons">
              <button className="download-btn pdf-btn" onClick={handleDownloadPdf}>
                <DownloadIcon /> Download PDF
              </button>
              <button className="download-btn docx-btn" onClick={handleDownloadDocx}>
                <DownloadIcon /> Download DOCX
              </button>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
