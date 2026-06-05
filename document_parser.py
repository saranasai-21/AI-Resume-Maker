import io
import streamlit as st

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None

def extract_text_from_file(uploaded_file) -> str:
    """
    Extract text content from an uploaded PDF, DOCX, or text file.
    """
    if not uploaded_file:
        return ""
        
    filename = uploaded_file.name.lower()
    
    if filename.endswith(".pdf"):
        if PdfReader is None:
            st.error("pypdf library is not installed. Cannot parse PDF.")
            return ""
        try:
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            return ""
            
    elif filename.endswith(".docx"):
        if Document is None:
            st.error("python-docx library is not installed. Cannot parse DOCX.")
            return ""
        try:
            doc = Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text.strip()
        except Exception as e:
            st.error(f"Error reading DOCX: {e}")
            return ""
            
    else:
        # Default to reading as plain text UTF-8
        try:
            return uploaded_file.getvalue().decode("utf-8").strip()
        except Exception as e:
            try:
                # Try latin-1 encoding if UTF-8 fails
                return uploaded_file.getvalue().decode("latin-1").strip()
            except Exception as e2:
                st.error(f"Failed to read file as text: {e2}")
                return ""
