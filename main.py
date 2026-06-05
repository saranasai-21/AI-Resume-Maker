import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

# Mount static files for React
if os.path.exists("dist"):
    app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")

class OptimizeRequest(BaseModel):
    resume_text: str
    job_description_text: str
    job_image_base64: str = ""
    company_name: str = ""

def get_providers():
    providers = []
    # Collect all Gemini keys (1 through 6)
    for i in range(1, 7):
        key = os.getenv(f"GEMINI_KEY_{i}")
        if key:
            providers.append({"type": "gemini", "key": key})
            
    # Collect Groq Key
    groq_key = os.getenv("GROQ_KEY")
    if groq_key:
        providers.append({"type": "groq", "key": groq_key})
        
    # Collect OpenRouter Key
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
        # Format: data:image/jpeg;base64,...
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
            print(f"Failed to parse image for Gemini: {e}")
            
    payload = {
        "contents": [{
            "parts": parts
        }],
        "generationConfig": {
            "temperature": 0.2
        }
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
    
    messages = [
        {"role": "system", "content": sys_prompt}
    ]
    
    content = [{"type": "text", "text": prompt}]
    
    if image_b64:
        if provider_name == "groq":
            raise Exception("Groq standard models do not support vision. Skipping.")
            
        content.append({
            "type": "image_url",
            "image_url": {
                "url": image_b64
            }
        })
        
    messages.append({"role": "user", "content": content})
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.2
    }
    
    if provider_name == "openrouter":
        headers["HTTP-Referer"] = "https://resumeai-optimizer.hf.space"
        headers["X-Title"] = "ResumeAI"
        
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"{provider_name} error: {response.text}")
        
    data = response.json()
    return data['choices'][0]['message']['content']


@app.post("/api/optimize")
def optimize_resume(req: OptimizeRequest):
    providers = get_providers()
    if not providers:
        raise HTTPException(status_code=500, detail="No API Keys configured in the environment.")
        
    sys_prompt = SYSTEM_PROMPT
    if req.company_name:
        sys_prompt += f"\n\nIMPORTANT ADVANCED DIRECTIVE: You must act as an expert recruiter for {req.company_name}. Research and use your knowledge of {req.company_name}'s past recruitment preferences, company culture, and successful resume patterns for this specific role. Tailor the resume strongly to appeal directly to what {req.company_name} looks for in candidates."

    prompt = f"RESUME:\n{req.resume_text}\n\nJOB DESCRIPTION:\n{req.job_description_text}\n\nReturn ONLY the HTML."
    
    errors = []
    
    for p in providers:
        try:
            print(f"Attempting provider: {p['type']}")
            if p["type"] == "gemini":
                result = call_gemini(p["key"], sys_prompt, prompt, req.job_image_base64)
                return {"html": result}
            elif p["type"] == "groq":
                if req.job_image_base64:
                    print("Skipping Groq due to image presence.")
                    continue 
                result = call_openai_compatible("https://api.groq.com/openai/v1/chat/completions", p["key"], "llama-3.3-70b-versatile", sys_prompt, prompt, None, "groq")
                return {"html": result}
            elif p["type"] == "openrouter":
                result = call_openai_compatible("https://openrouter.ai/api/v1/chat/completions", p["key"], "anthropic/claude-3.5-sonnet", sys_prompt, prompt, req.job_image_base64, "openrouter")
                return {"html": result}
        except Exception as e:
            print(f"Provider {p['type']} failed: {e}")
            errors.append(f"{p['type']} failed: {str(e)}")
            continue
            
    # If we exhaust all providers
    raise HTTPException(status_code=500, detail=f"All API providers failed or rate limited. Errors: {errors}")

@app.get("/{full_path:path}")
def serve_react(full_path: str):
    if os.path.exists("dist/index.html") and full_path == "":
        return FileResponse("dist/index.html")
    # Handle Vite fallback routing for SPA
    file_path = os.path.join("dist", full_path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    elif os.path.exists("dist/index.html"):
        return FileResponse("dist/index.html")
    return {"message": "API is running. Build React app first to serve frontend."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
