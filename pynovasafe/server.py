import os
import openai
from dotenv import load_dotenv
from tokens.tokens import Tokens
from protocols.aave import AaveData
from protocols.agave import AgaveData
from flask import Flask, request, jsonify
from protocols.balancer import BalancerData
from flask_cors import CORS

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

app = Flask(__name__)
CORS(app)

# Global variable to store the chat history
chat_history = []


def parse_intent(user_input: str, chat_history: list):
    chat_history.append({"role": "user", "content": user_input})
    full_response = ""

    try:
        # Call OpenAI API for chat completion
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
        )

        full_response = response.choices[0].message.content
    except Exception as e:
        print(f"Error in API request: {e}")
        full_response = "Sorry, I couldn't process your request."

    chat_history.append({"role": "assistant", "content": full_response})
    return full_response, chat_history


def setup_chat_context():
    balancer_data = BalancerData().setup_data()
    aave_data = AaveData().setup_data()
    agave_data = AgaveData().setup_data()
    tokens_data = Tokens().get_tokens_data()
    yau = [
        {
            "role": "system",
            "content": (
                "You are a knowledgeable and friendly DeFi Assistant. "
                "Your goal is to help users identify the best opportunities and strategies in decentralized finance"
                "such as lending, borrowing, liquidity pools across various protocols."
                "Note: the User already knows the risk of Defi and all other risks. You don't need to explain it and do not say it, give only the suggestions you have about the data and be creative."
            ),
        },
        {
            "role": "system",
            "content": (
                "Do not say the risks and do not say to be careful, the user already knows the risks of DeFi."
            ),
        },
        {
            "role": "system",
            "content": (
                "Here is a dict of the current token information, the key is the token address and the value is a dict with the token name and price:\n"
                + str(tokens_data)
            ),
        },
        {
            "role": "system",
            "content": (
                "The following dict is current Aave lending and borrowing market data, "
                "including interest rates for borrow, available assets, and apr for supply/collateral:\n"
                + str(aave_data)
            ),
        },
        {
            "role": "system",
            "content": (
                "Here is up-to-date Balancer pool data, including pool compositions, fees, and liquidity:\n"
                + str(balancer_data)
            ),
        },
        {
            "role": "system",
            "content": (
                "Here is up-to-date Agave lending and borrowing market data,including interest rates for borrow, available assets, and apr for supply/collateral:\n"
                + str(agave_data)
            ),
        },
    ]
    return yau


@app.route("/")
def home():
    return "Hello from Flask!"


@app.route("/chat", methods=["POST"])
def chat():
    global chat_history

    user_input = request.json.get("user_input")

    if not chat_history:
        # Initialize the chat context only once if history is empty
        chat_history = setup_chat_context()

    if user_input:
        # Process the user input with current chat history
        response, updated_history = parse_intent(user_input, chat_history)
        chat_history = updated_history  # Update the global chat history

        return jsonify({"response": response})
    else:
        return jsonify({"error": "No user input provided"}), 400


def main():
    chat_history = setup_chat_context()
    while True:
        user_prompt = input("You: ")
        if user_prompt.lower() in {"exit", "quit"}:
            break
        args, chat_history = parse_intent(user_prompt, chat_history)
        print("Parsed arguments:", args)


if __name__ == "__main__":
    app.run(debug=True)
    # main()
