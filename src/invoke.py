from langchain.chat_models import ChatOpenAI
import google.generativeai as genai
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Leer las API keys desde variables de entorno (cargadas por Docker)
openai_api_key = os.getenv("OPENROUTER_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

if not all([openai_api_key, google_api_key, deepseek_api_key]):
    raise ValueError("Faltan una o más API Keys en las variables de entorno.")

# ---------- GPT-4o via OpenRouter ----------
def init_chatgpt_openrouter():
    return ChatOpenAI(
        openai_api_key=openai_api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        model_name="openai/chatgpt-4o-latest"
    )

#----------- Claude via OpenRouter ----------
def init_claude_openrouter(model_name="anthropic/claude-3-sonnet"):
    return ChatOpenAI(
        openai_api_key=openai_api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        model_name=model_name
    )

# ---------- DeepSeek ----------
def init_deepseek():
    client = OpenAI(
        api_key=deepseek_api_key,
        base_url="https://api.deepseek.com"
    )
    return client

# ---------- Gemini ----------
def init_gemini(model_name="gemini-1.5-flash"):
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel(model_name)
    return model

def get_all_models():
    return {
        "GPT-4o":init_chatgpt_openrouter(),
        "Claude 3 Sonnet": init_claude_openrouter(),
        "Deepseek": init_deepseek(),
        "Gemini": init_gemini()
    }