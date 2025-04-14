import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get DeepSeek API key
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("❌ ERROR: DEEPSEEK_API_KEY is not set! Check your environment variables.")

# Initialize Flask app
app = Flask(__name__)

def get_deepseek_response(user_prompt):
    """Function to get response from DeepSeek API"""
    try:
        print("⚡ Sending request to DeepSeek...")
        print(f"📨 Prompt: {user_prompt}")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": user_prompt}],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        response.raise_for_status()
        result = response.json()
        print("✅ Received response from DeepSeek")
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ Error while calling DeepSeek: {str(e)}")
        return f"Error: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    """API Endpoint to handle chat requests"""
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    response = get_deepseek_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
