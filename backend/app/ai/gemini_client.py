import os
from openai import OpenAI


def _ask_groq(prompt: str) -> str | None:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        return None
    try:
        client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key,
        )
        model = os.getenv("GROQ_MODEL", "llama3-8b-8192")
        res = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.7,
        )
        return res.choices[0].message.content
    except Exception:
        return None


def _ask_ollama(prompt: str) -> str | None:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    try:
        client = OpenAI(base_url=base_url, api_key="ollama")
        model = os.getenv("OLLAMA_MODEL", "llama3")
        res = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.7,
        )
        return res.choices[0].message.content
    except Exception:
        return None


def ask(prompt: str, fallback: str = "AI insights unavailable at this time.") -> str:
    result = _ask_groq(prompt)
    if result:
        return result

    result = _ask_ollama(prompt)
    if result:
        return result

    return fallback
