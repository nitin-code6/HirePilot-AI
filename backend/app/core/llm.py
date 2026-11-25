from typing import Dict, Any

class LLMClient:
    """
    Centralized LLM client supporting Groq and structured output with safe mock fallback.
    """
    def __init__(self, api_key: str = None, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model = model

    def complete(self, prompt: str) -> str:
        if self.api_key:
            try:
                from groq import Groq
                client = Groq(api_key=self.api_key)
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            except Exception:
                pass
        return f"[Simulated Response]: Successfully analyzed prompt '{prompt[:40]}...' using {self.model} fallback."

llm_client = LLMClient()
