import speech_recognition as sr
from openai import OpenAI
import os
import sys

# ==========================================
# 👑 AG Labs 安定版 (ElevenLabsを排除！)
# ==========================================
OPENAI_API_KEY = "client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY')"
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def listen_and_transcribe():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("\n🎤 Listening... (日本語でどうぞ！)")
        audio = r.listen(source)
    try:
        # 耳はGoogle（無料）
        return r.recognize_google(audio, language="ja-JP")
    except:
        return None
code ag_setup.py
def translate_and_speak(japanese_text):
    if not japanese_text: return
    try:
        # ① 翻訳 (OpenAI)
        res = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Translate to natural English."},
                      {"role": "user", "content": japanese_text}]
        )
        english_text = res.choices[0].message.content
        print(f"🧠 AI: {english_text}")

        # ② 【ここが重要！】ElevenLabsを使わず、Windows標準の「SAPI」で喋る
        # これならAPIキーも、課金も、エラーも一切関係ありません！
        import win32com.client
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(english_text)

    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    print("--- AG Platforms Emergency System Online ---")
    while True:
        text = listen_and_transcribe()
        if text:
            translate_and_speak(text)