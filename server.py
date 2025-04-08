import os
import anthropic
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Anthropic API key
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("❌ ERROR: ANTHROPIC_API_KEY is not set! Check your environment variables.")

# Initialize Claude client
client = anthropic.Anthropic(api_key=api_key)

# Initialize Flask app
app = Flask(__name__)

def get_claude_response(user_prompt):
    """Function to get response from Claude API"""
    try:
        print("⚡ Sending request to Claude...")
        print(f"📨 Prompt: {user_prompt}")
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",  # or "claude-3-opus" if available to you
            max_tokens=1000,
            temperature=0.7,
            messages=[{"role": "user", "content": user_prompt}]
        )
        print("✅ Received response from Claude")
        return response.content[0].text
    except Exception as e:
        print(f"❌ Error while calling Claude: {str(e)}")
        return f"Error: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    """API Endpoint to handle chat requests"""
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    response = get_claude_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
