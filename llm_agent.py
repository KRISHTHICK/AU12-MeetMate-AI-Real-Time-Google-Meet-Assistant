# llm_agent.py
import os
try:
    import openai
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False

def summarize_with_openai(merged_text, openai_api_key, model="gpt-3.5-turbo"):
    if not OPENAI_AVAILABLE:
        raise RuntimeError("openai package not installed")
    openai.api_key = openai_api_key
    prompt = f"""
Read the meeting merged transcript and screen notes below. Provide:
1) Short summary in 6 bullets.
2) Action items (task, owner if mentioned, due date if mentioned).
3) Top 3 topics discussed.
4) Who spoke the most (approx) based on timestamps.
5) A suggested flowchart description (steps) if applicable.

Content:
{merged_text[:4000]}
"""
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[{"role":"user","content":prompt}],
        temperature=0.2,
        max_tokens=800
    )
    return resp['choices'][0]['message']['content']
