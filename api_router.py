import os
import requests
import streamlit as st
import time
import logging
from prompts import (
    SYSTEM_PROMPT, get_optimization_prompt, get_company_research_prompt,
    STAGE1_SYSTEM_PROMPT, STAGE2_SYSTEM_PROMPT, get_stage1_prompt, get_stage2_prompt
)

# Configure logging for Hugging Face Spaces stderr visibility
logging.basicConfig(level=logging.INFO)

def secrets_file_exists() -> bool:
    """
    Check if a streamlit secrets.toml file exists in standard directories
    to avoid triggering Streamlit's automatic FileNotFoundError warning in the UI.
    """
    paths = [
        os.path.join(".streamlit", "secrets.toml"),
        os.path.join("/app", ".streamlit", "secrets.toml"),
        os.path.join("/root", ".streamlit", "secrets.toml"),
    ]
    try:
        home = os.path.expanduser("~")
        paths.append(os.path.join(home, ".streamlit", "secrets.toml"))
    except Exception:
        pass
        
    for p in paths:
        if os.path.exists(p):
            return True
    return False

def get_key(name: str) -> str:
    """
    Get API key from environment variables or Streamlit secrets.
    Checks environment variables first, then streamlit secrets to avoid UI warnings.
    """
    # 1. Try environment variables first
    val = os.environ.get(name, "")
    if val:
        return val
        
    # 2. Try streamlit secrets only if secrets file is present
    if secrets_file_exists():
        try:
            if name in st.secrets:
                return st.secrets[name]
        except Exception:
            pass
            
    return ""

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
    Runs the multi-provider fallback resume optimization routing in two stages:
    Stage 1: Content tailoring using the first available provider.
    Stage 2: HTML layout formatting using the next available provider.
    """
    providers = get_providers()
    if not providers:
        return {
            "success": False,
            "content": "<h2>Error: No API keys configured.</h2><p>Please check your Hugging Face Space secrets or local environment variables.</p>",
            "provider": "None",
            "errors": ["No active API keys found."]
        }
        
    errors = []
    
    # ------------------ STAGE 1: CONTENT TAILORING ------------------
    stage1_prompt = get_stage1_prompt(resume_text, job_desc_text, job_role)
    stage1_sys = STAGE1_SYSTEM_PROMPT + get_company_research_prompt(company_name)
    
    stage1_text = ""
    stage1_provider_idx = -1
    stage1_provider_name = ""
    
    for idx, p in enumerate(providers):
        try:
            if p["type"] == "gemini":
                try:
                    res = call_gemini(p["key"], stage1_sys, stage1_prompt, job_image_base64)
                except Exception as e:
                    # Retry once on 429
                    if "429" in str(e):
                        print(f"[ResumeAI] Stage 1: {p['name']} hit 429. Retrying in 3 seconds...", flush=True)
                        time.sleep(3)
                        res = call_gemini(p["key"], stage1_sys, stage1_prompt, job_image_base64)
                    else:
                        raise e
                stage1_text = res
                
            elif p["type"] == "groq":
                if job_image_base64:
                    errors.append("Groq skipped: Vision input not supported by Groq agent.")
                    continue
                res = call_openai_compatible(
                    url="https://api.groq.com/openai/v1/chat/completions",
                    key=p["key"],
                    model="llama-3.3-70b-versatile",
                    sys_prompt=stage1_sys,
                    prompt=stage1_prompt,
                    image_b64=None,
                    provider_name="groq"
                )
                stage1_text = res
                
            elif p["type"] == "openrouter":
                res = call_openai_compatible(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    key=p["key"],
                    model="google/gemini-flash-1.5",
                    sys_prompt=stage1_sys,
                    prompt=stage1_prompt,
                    image_b64=job_image_base64,
                    provider_name="openrouter"
                )
                stage1_text = res
                
            if stage1_text and stage1_text.strip():
                stage1_provider_idx = idx
                stage1_provider_name = p["name"]
                break
        except Exception as e:
            print(f"[ResumeAI] Stage 1 ERROR: {p['name']} failed: {e}", flush=True)
            errors.append(f"Stage 1 {p['name']} failed: {str(e)}")
            if p != providers[-1]:
                time.sleep(1.5)
            continue
            
    if not stage1_text or not stage1_text.strip():
        error_msg = (
            f"<div style='color:#ef4444; font-weight:bold; margin-bottom:10px;'>Stage 1: Content tailoring failed on all providers:</div>"
            f"<ul style='color:#ef4444; font-size:12px;'>" + "".join(f"<li>{e}</li>" for e in errors) + "</ul>"
        )
        return {"success": False, "content": error_msg, "provider": "Fallback failure", "errors": errors}
        
    # ------------------ STAGE 2: FORMATTING & LAYOUT ------------------
    # Prefer the next provider in the list to avoid rate limits
    stage2_providers = []
    if len(providers) > 1:
        stage2_providers = providers[stage1_provider_idx + 1:] + providers[:stage1_provider_idx + 1]
    else:
        stage2_providers = providers
        
    stage2_prompt = get_stage2_prompt(stage1_text)
    stage2_sys = STAGE2_SYSTEM_PROMPT
    
    final_html = ""
    stage2_provider_name = ""
    
    for p in stage2_providers:
        try:
            # We don't pass the image to Stage 2 since it's formatting text only
            if p["type"] == "gemini":
                try:
                    res = call_gemini(p["key"], stage2_sys, stage2_prompt, None)
                except Exception as e:
                    if "429" in str(e):
                        print(f"[ResumeAI] Stage 2: {p['name']} hit 429. Retrying in 3 seconds...", flush=True)
                        time.sleep(3)
                        res = call_gemini(p["key"], stage2_sys, stage2_prompt, None)
                    else:
                        raise e
                final_html = res
                
            elif p["type"] == "groq":
                res = call_openai_compatible(
                    url="https://api.groq.com/openai/v1/chat/completions",
                    key=p["key"],
                    model="llama-3.3-70b-versatile",
                    sys_prompt=stage2_sys,
                    prompt=stage2_prompt,
                    image_b64=None,
                    provider_name="groq"
                )
                final_html = res
                
            elif p["type"] == "openrouter":
                res = call_openai_compatible(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    key=p["key"],
                    model="google/gemini-flash-1.5",
                    sys_prompt=stage2_sys,
                    prompt=stage2_prompt,
                    image_b64=None,
                    provider_name="openrouter"
                )
                final_html = res
                
            if final_html and final_html.strip():
                stage2_provider_name = p["name"]
                break
        except Exception as e:
            print(f"[ResumeAI] Stage 2 ERROR: {p['name']} failed: {e}", flush=True)
            errors.append(f"Stage 2 {p['name']} failed: {str(e)}")
            if p != stage2_providers[-1]:
                time.sleep(1.5)
            continue
            
    if not final_html or not final_html.strip():
        error_msg = (
            f"<div style='color:#ef4444; font-weight:bold; margin-bottom:10px;'>Stage 2: Formatting failed on all providers:</div>"
            f"<ul style='color:#ef4444; font-size:12px;'>" + "".join(f"<li>{e}</li>" for e in errors) + "</ul>"
        )
        return {"success": False, "content": error_msg, "provider": "Fallback failure", "errors": errors}
        
    combined_provider = f"{stage1_provider_name} (Content) → {stage2_provider_name} (Format)"
    return {"success": True, "content": final_html, "provider": combined_provider, "errors": errors}

def run_stage2_only(tailored_text: str) -> dict:
    """
    Runs Stage 2 (formatting) only, using the available providers.
    """
    providers = get_providers()
    if not providers:
        return {
            "success": False,
            "content": "<h2>Error: No API keys configured.</h2>",
            "provider": "None",
            "errors": ["No active API keys found."]
        }
    
    errors = []
    stage2_prompt = get_stage2_prompt(tailored_text)
    stage2_sys = STAGE2_SYSTEM_PROMPT
    
    final_html = ""
    stage2_provider_name = ""
    
    for p in providers:
        try:
            if p["type"] == "gemini":
                try:
                    res = call_gemini(p["key"], stage2_sys, stage2_prompt, None)
                except Exception as e:
                    if "429" in str(e):
                        print(f"[ResumeAI] Stage 2 Only: {p['name']} hit 429. Retrying in 3 seconds...", flush=True)
                        time.sleep(3)
                        res = call_gemini(p["key"], stage2_sys, stage2_prompt, None)
                    else:
                        raise e
                final_html = res
                
            elif p["type"] == "groq":
                res = call_openai_compatible(
                    url="https://api.groq.com/openai/v1/chat/completions",
                    key=p["key"],
                    model="llama-3.3-70b-versatile",
                    sys_prompt=stage2_sys,
                    prompt=stage2_prompt,
                    image_b64=None,
                    provider_name="groq"
                )
                final_html = res
                
            elif p["type"] == "openrouter":
                res = call_openai_compatible(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    key=p["key"],
                    model="google/gemini-flash-1.5",
                    sys_prompt=stage2_sys,
                    prompt=stage2_prompt,
                    image_b64=None,
                    provider_name="openrouter"
                )
                final_html = res
                
            if final_html and final_html.strip():
                stage2_provider_name = p["name"]
                break
        except Exception as e:
            print(f"[ResumeAI] Stage 2 Only ERROR: {p['name']} failed: {e}", flush=True)
            errors.append(f"Stage 2 {p['name']} failed: {str(e)}")
            if p != providers[-1]:
                time.sleep(1.5)
            continue
            
    if not final_html or not final_html.strip():
        error_msg = "Formatting failed on all providers: " + ", ".join(errors)
        return {"success": False, "content": error_msg, "provider": "Fallback failure", "errors": errors}
        
    return {"success": True, "content": final_html.strip(), "provider": stage2_provider_name, "errors": errors}
