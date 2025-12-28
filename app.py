import os
import requests
import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask_jarvis', methods=['POST'])
def ask_jarvis():
    try:
        data = request.get_json()
        msg = data.get('msg', '')
        user = data.get('userName', 'Ansh Kesharwani')
        lang = data.get('lang', 'en')

        url = "https://api.perplexity.ai/chat/completions"
        api_key = os.getenv('PPLX_API_KEY')
        headers = {"Authorization": f"Bearer {api_key}"}

        system_content = (
            f"You are J.A.R.V.I.S, female AI. Creator: Ansh Kesharwani. "
            f"RULES: Be very brief. Direct answers only."
        )

        payload = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": msg}
            ],
            "max_tokens": 150
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        if resp.status_code == 200:
            reply = resp.json()['choices'][0]['message']['content']
            clean_reply = re.sub(r'[^\w\s,.!?]', '', reply)
            return jsonify({"reply": clean_reply})
        
        return jsonify({"reply": "API Busy. Try again."})
    except Exception as e:
        return jsonify({"reply": "Connection Slow."})

if __name__ == '__main__':
    # Render ke liye port process.env se lena zaroori ho sakta hai
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

