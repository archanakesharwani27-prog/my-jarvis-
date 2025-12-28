import os
import requests
import re
from flask import Flask, render_template, request, jsonify

# Flask ko batana ki templates folder kahan hai
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    try:
        # Pura path check karne ke liye index.html load kar rahe hain
        return render_template('index.html')
    except Exception as e:
        return f"Template Error: {str(e)}"

@app.route('/ask_jarvis', methods=['POST'])
def ask_jarvis():
    try:
        data = request.get_json()
        msg = data.get('msg', '')
        api_key = os.getenv('PPLX_API_KEY')
        url = "https://api.perplexity.ai/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {
            "model": "sonar",
            "messages": [{"role": "user", "content": msg}]
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        reply = resp.json()['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Connection Slow."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
