# app/modules/crop_chatbot/service.py
import os
import uuid
import asyncio
import edge_tts
from langdetect import detect
from deep_translator import GoogleTranslator
from groq import Groq
from app.modules.chatbot.rag_retriever import get_top_answers

# ---------------- LANGUAGE HELPERS ----------------
def contains_telugu(text: str) -> bool:
    return any('\u0C00' <= ch <= '\u0C7F' for ch in text)

def detect_language(text: str) -> str:
    try:
        return "te" if contains_telugu(text) else detect(text)
    except:
        return "en"

def translate_text(text: str, src: str, dest: str) -> str:
    try:
        return GoogleTranslator(source=src, target=dest).translate(text)
    except:
        return text

# ---------------- EDGE TTS ----------------
async def edge_tts_speak(text: str, lang: str = "te") -> str:
    filename = f"static/audio/{uuid.uuid4()}.mp3"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    voice = "te-IN-ShrutiNeural" if lang == "te" else "en-US-AriaNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)
    return filename

def text_to_speech(text: str, lang: str = "te") -> str:
    return asyncio.run(edge_tts_speak(text, lang))

# ---------------- CHATBOT LOGIC ----------------
def chatbot(query: str) -> str:
    if query.lower() in ["hi", "hello", "hai", "hii"]:
        return "👋 నమస్కారం రైతు గారూ! Hello Farmer! How can I help you today?"
    
    if get_top_answers is None:
        return "Chatbot is currently unavailable. Please check server configuration."
    
    context = get_top_answers(query)
    # Call Groq API
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an agriculture assistant for Indian farmers. "
                    "Give ONLY practical cultivation advice. "
                    "Answer in maximum 5 short bullet points. "
                    "No introduction, no conclusion, no theory."
                )
            },
            {
                "role": "user",
                "content": f"Farmer question:\n{query}\n\nReference info:\n{chr(10).join(context)}"
            }
        ],
        temperature=0.2,
        max_tokens=150
    )
    return completion.choices[0].message.content.strip()

# ---------------- PROCESS CHAT ----------------
def process_chat(message: str, mode: str = "text") -> dict:
    if mode == "text":
        return {"response": chatbot(message), "audio": None}

    # Voice mode
    lang = detect_language(message)
    text_en = translate_text(message, "te", "en") if lang == "te" else message
    bot_en = chatbot(text_en)
    bot_te = translate_text(bot_en, "en", "te") if lang == "te" else bot_en
    audio_file = text_to_speech(bot_te, "te") if lang == "te" else None
    return {"response": bot_te, "audio": audio_file}