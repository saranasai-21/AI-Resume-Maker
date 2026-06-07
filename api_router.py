import os
import requests
import streamlit as st
import time
import logging
from prompts import SYSTEM_PROMPT, get_optimization_prompt, get_company_research_prompt

# Configure logging for Hugging Face Spaces stderr visibility
logging.basicConfig(level=logging.INFO)

def get_key(name: str) -> str:
    """
    Get API key from Streamlit secrets (for Hugging Face Spaces) or environment variables.
    """
    # Try streamlit secrets first
    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass
    
    # Try environment variables
    return os.environ.get(name, "")

def get_providers():
    """
    Retrieve configured providers based on available keys.
    Returns a list of dicts: [{'type': 'gemini', 'key': '...'}, ...]
    """
    providers = []
    
    # 1. Gemini keys (supports up to 6 agents)
    for i in range(1, 7):
        key = get_key(f"GEMINI_KEY_{i}")
        if key:
            providers.append({"type": "gemini", "key": key, "name": f"Gemini Agent {i}"})
            
    # 2. Groq key
    groq_key = get_key("GROQ_KEY")
    if groq_key:
        providers.append({"type": "groq", "key": groq_key, "name": "Groq Agent"})
        
    # 3. OpenRouter key
    or_key = get_key("OPENROUTER_KEY")
    if or_key:
        providers.append({"type": "openrouter", "key": or_key, "name": "OpenRouter Agent"})
        
    return providers

def call_gemini(key: str, sys_prompt: str, prompt: str, image_b64: str) -> str:
    """
    Call Gemini API using the newer stable gemini-2.5-flash model.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
    
    parts = [{"text": prompt}]
    
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
            raise Exception(f"Failed to parse image data: {e}")
            
    payload = {
        "contents": [{"parts": parts}],
        "systemInstruction": {"parts": [{"text": sys_prompt}]},
        "generationConfig": {
            "temperature": 0.2
        }
    }
    
    response = requests.post(url, json=payload, timeout=30)
    if response.status_code != 200:
        raise Exception(f"Gemini API returned status {response.status_code}: {response.text}")
        
    data = response.json()
    
    # Safety Block Check (HF Space deployment checks, point 3)
    if 'promptFeedback' in data and data['promptFeedback'].get('blockReason'):
        raise Exception(f"Gemini safety block: {data['promptFeedback']['blockReason']}")
        
    try:
        text = data['candidates'][0]['content']['parts'][0]['text']
        return text
    except KeyError:
        raise Exception(f"Unexpected response structure: {data}")

def call_openai_compatible(url: str, key: str, model: str, sys_prompt: str, prompt: str, image_b64: str, provider_name: str) -> str:
    """
    Call OpenAI-compatible APIs (Groq, OpenRouter).
    """
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
            raise Exception("Groq standard models do not support vision in this setup. Skipping Groq.")
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
        
    response = requests.post(url, headers=headers, json=payload, timeout=35)
    if response.status_code != 200:
        raise Exception(f"{provider_name} API returned status {response.status_code}: {response.text}")
        
    data = response.json()
    try:
        return data['choices'][0]['message']['content']
    except KeyError:
        raise Exception(f"Unexpected OpenAI-compatible response structure: {data}")

def run_resume_optimization(resume_text: str, job_desc_text: str, job_role: str, job_image_base64: str, company_name: str) -> dict:
    """
    Runs the multi-provider fallback resume optimization routing.
    Returns a dict: {"success": bool, "content": str, "provider": str, "errors": list}
    """
    providers = get_providers()
    
    # Pre-build prompts
    sys_prompt = SYSTEM_PROMPT + get_company_research_prompt(company_name)
    prompt = get_optimization_prompt(resume_text, job_desc_text, job_role)
    
    if not providers:
        return {
            "success": False,
            "content": "<h2>Error: No API keys configured.</h2><p>Please check your Hugging Face Space secrets or local environment variables.</p>",
            "provider": "None",
            "errors": ["No active API keys found."]
        }
        
    errors = []
    for p in providers:
        try:
            if p["type"] == "gemini":
                try:
                    result = call_gemini(p["key"], sys_prompt, prompt, job_image_base64)
                except Exception as e:
                    # Retry once on 429 (BUG 4 & HF check 2)
                    if "429" in str(e):
                        print(f"[ResumeAI] {p['name']} hit 429. Retrying in 3 seconds...", flush=True)
                        logging.warning(f"{p['name']} hit 429. Retrying in 3 seconds...")
                        time.sleep(3)
                        result = call_gemini(p["key"], sys_prompt, prompt, job_image_base64)
                    else:
                        raise e
                return {"success": True, "content": result, "provider": p["name"], "errors": errors}
                
            elif p["type"] == "groq":
                if job_image_base64:
                    errors.append("Groq skipped: Vision input not supported by Groq agent.")
                    continue
                result = call_openai_compatible(
                    url="https://api.groq.com/openai/v1/chat/completions",
                    key=p["key"],
                    model="llama-3.3-70b-versatile",
                    sys_prompt=sys_prompt,
                    prompt=prompt,
                    image_b64=None,
                    provider_name="groq"
                )
                return {"success": True, "content": result, "provider": p["name"], "errors": errors}
                
            elif p["type"] == "openrouter":
                # Using google/gemini-flash-1.5 as free tier fallback
                result = call_openai_compatible(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    key=p["key"],
                    model="google/gemini-flash-1.5",
                    sys_prompt=sys_prompt,
                    prompt=prompt,
                    image_b64=job_image_base64,
                    provider_name="openrouter"
                )
                return {"success": True, "content": result, "provider": p["name"], "errors": errors}
                
        except Exception as e:
            # Print and log errors (BUG 3 fix)
            print(f"[ResumeAI] ERROR: {p['name']} failed: {e}", flush=True)
            logging.error(f"{p['name']} failed: {e}")
            errors.append(f"{p['name']} failed: {str(e)}")
            
            # Delay between provider attempts (BUG 4 delay fix)
            if p != providers[-1]:
                time.sleep(1.5)
            continue
            
    # If all agents failed
    error_msg = (
        f"<div style='color:#ef4444; font-weight:bold; margin-bottom:10px;'>All AI agents failed or rate limited:</div>"
        f"<ul style='color:#ef4444; font-size:12px;'>" + "".join(f"<li>{e}</li>" for e in errors) + "</ul>"
    )
    return {"success": False, "content": error_msg, "provider": "Fallback failure", "errors": errors}
