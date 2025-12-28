import os, requests, re
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
        user = data.get('userName', 'User')
        lang = data.get('lang', 'en')
        
        url = "https://api.perplexity.ai/chat/completions"
	headers = {"Authorization": f"Bearer {os.getenv('PPLX_API_KEY')}"}
        system_content = (
            f"You are J.A.R.V.I.S, female AI. Creator: Ansh Kesharwani. Respond in {lang}. "
            f"RULES: Be very brief. Direct answers only. No stars. User: {user}."
        )
        
        payload = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": msg}
            ],
            "max_tokens": 150 # Tokens kam kiye taaki fast reply aaye
        }

        # Timeout 15 seconds kiya taaki lambi waiting na ho
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        if resp.status_code == 200:
            reply = resp.json()['choices'][0]['message']['content']
            clean_reply = re.sub(r'[^\w\s,.!?]', '', reply).strip()
            return jsonify({"reply": clean_reply})
        return jsonify({"reply": "API Busy. Try again."})
    except Exception as e:
        return jsonify({"reply": "Connection Slow."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

