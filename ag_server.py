from flask import Flask, request, send_file
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

# .env ファイルからOPENAI_API_KEYなどを読み込む
load_dotenv()

app = Flask(__name__)
CORS(app) # ブラウザからのアクセスを許可！

# 🔑 APIキーはバックエンド側で隠し持つ！
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

@app.route('/speak', methods=['POST'])
def speak():
    text = request.json.get('text', 'こんにちは、社長。')
    # OpenAIに発注（米津風？Echoボイス）
    response = client.audio.speech.create(model='tts-1', voice='echo', input=text)
    
    file_path = 'output.mp3'
    response.stream_to_file(file_path)
    return send_file(file_path, mimetype='audio/mpeg')

if __name__ == '__main__':
    print('🚀 AG Labs セキュリティ門番、起動しました！ (Port 5000)')
    app.run(port=5000)
