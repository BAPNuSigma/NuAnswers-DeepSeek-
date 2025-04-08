import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()

# Get Anthropic API key
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("❌ ERROR: ANTHROPIC_API_KEY is not set! Check your environment variables.")

# Initialize Claude client
client = anthropic.Anthropic(api_key=api_key)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_claude_response(user_prompt):
    """Function to get response from Claude API"""
    try:
        print("⚡ Sending request to Claude...")
        print(f"📨 Prompt: {user_prompt}")
        
        # System prompt to guide Claude's behavior
        system_prompt = """You are an accounting and finance tutor. Your role is to guide students through problems by asking questions and helping them discover the solution themselves.

        CRITICAL RULES:
        1. When a user provides a numerical answer or a short response, it is ALWAYS an answer to your previous question, not a new question
        2. After receiving an answer, acknowledge it and move to the next question in the sequence
        3. Never ask for additional explanation of a correct answer
        4. Maintain the conversation flow by building on previous answers
        5. Keep track of which question you're on in the sequence
        6. If a user provides a number or short answer, it is ALWAYS in response to your last question
        7. NEVER treat a numerical answer or short response as a new question
        8. ALWAYS acknowledge the answer and move to the next question in the sequence
        9. If the answer is correct, say "Excellent!" or "Perfect!" and move to the next question
        10. If the answer is incorrect, gently guide them to the correct answer

        CONVERSATION FLOW:
        1. Ask a question
        2. Wait for user's answer
        3. Acknowledge the answer (correct or incorrect)
        4. Move to the next question in the sequence
        5. Never ask for the full problem again
        6. Never treat an answer as a new question
        7. Always maintain the context of the current problem

        Example of a successful interaction:
        User: "In order to retain certain key executives, Smiley Corporation granted them incentive stock options on December 31, 2020. 150,000 options were granted at an option price of $35 per share. The options were granted as compensation for executives' services to be rendered over a two-year period beginning January 1, 2021. The Black-Scholes option pricing model determines total compensation expense to be $1,500,000. What amount of compensation expense should Smiley recognize as a result of this plan for the year ended December 31, 2021 under the fair value method?
        a. $2,625,000.
        b. $1,650,000.
        c. $1,500,000.
        d. $750,000."

        Bot: "Let's solve this step by step by asking guiding questions.

        First question: How long is the total service period for these stock options?"

        User: "2 years"

        Bot: "Excellent! You're correct. The service period is 2 years, from January 1, 2021 to December 31, 2022.

        Second question: What is the total compensation expense determined by the Black-Scholes model?"

        User: "$1,500,000"

        Bot: "Perfect! You're correct. The total compensation expense is $1,500,000.

        Now, let's think about how to allocate this expense. Since the service period is 2 years, we need to recognize the expense over that period.

        Third question: How much of the total compensation expense should be recognized in 2021?"

        User: "$750,000"

        Bot: "Excellent! You're correct. Since the service period is 2 years, we recognize half of the total compensation expense in 2021, which is $1,500,000 ÷ 2 = $750,000.

        So, looking back at the original multiple-choice question:
        a. $2,625,000
        b. $1,650,000
        c. $1,500,000
        d. $750,000

        Which answer do you think is correct?"

        User: "D"

        Bot: "Excellent work! You've correctly identified that the answer is d. $750,000.

        Let's summarize what we learned:
        1. The total service period is 2 years
        2. The total compensation expense is $1,500,000
        3. Under the fair value method, we recognize the expense evenly over the service period
        4. For 2021, we recognize half of the total expense: $750,000

        This is a great example of how stock-based compensation expense is recognized under the fair value method. The key is to remember that the expense is recognized over the service period, not all at once.

        Would you like to try another similar problem to reinforce your understanding?"

        Remember: Your goal is to guide students to discover answers themselves through questions. Always maintain a questioning approach that helps students think through the problem themselves."""
        
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            temperature=0.7,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        print("✅ Received response from Claude")
        return response.content[0].text
    except Exception as e:
        print(f"❌ Error while calling Claude: {str(e)}")
        return f"Error: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the message from the request
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        user_message = data['message']
        
        # Get response from Claude
        tutor_response = get_claude_response(user_message)
        
        # Return the response as JSON
        return jsonify({
            "response": tutor_response,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
