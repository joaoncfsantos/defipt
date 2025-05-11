import os
import openai
from dotenv import load_dotenv
from protocols.aave_positions import AavePositionsData
from protocols.aave_borrow import AaveBorrowPositionsData
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


def parse_wallet_tokens(wallet_tokens: list, tokens_data: dict):
    res = []
    for (token,amount) in wallet_tokens:
        decimals = tokens_data.get(token, {}).get("decimals", 18)
        amount_converted = float(amount)/(10**float(decimals))
        res.append({"address": token, "balance": amount_converted})
    return res



def setup_chat_context(wallet_address, wallet_tokens):
    balancer_data = BalancerData().setup_data()
    aave_data = AaveData().setup_data()
    agave_data = AgaveData().setup_data()
    tokens_data = Tokens().get_tokens_data()
    aave_pos_data = AavePositionsData(wallet_address, tokens_data).get_user_positions()
    aave_borrow_pos_data = AaveBorrowPositionsData(
        wallet_address, tokens_data
    ).get_user_positions()
    setup_chat = [
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
        {
            "role": "system",
            "content": (
                "These are the supply positions the user added to Aave without marking them as collateral:\n"
                + str(aave_pos_data)
            ),
        },
        {
            "role": "system",
            "content": (
                "This is the borrow and lending market position of the user. The list can contain the assets given as collateral and assets borrowed. Interpret the position data and when ask analyse about the risk of the position (Do not forget when showing the balances you need to account and remove the token decimals):\n"
                + str(aave_borrow_pos_data)
            ),
        },
        {
            "role": "system",
            "content": (
                "Here is the user's wallet token data. When the user inquires, please analyze this data and recommend the best investment opportunities on the Gnosis chain based on the tokens held."
                + str(parse_wallet_tokens(wallet_tokens, tokens_data))
            ),
        },
    ]
    return setup_chat


@app.route("/")
def home():
    return "Hello from Flask!"


@app.route("/reset_chat", methods=["POST"])
def reset_chat():
    global chat_history

    chat_history = []  # Reset the chat history

    return jsonify({"message": "Chat history has been reset."})


@app.route("/chat", methods=["POST"])
def chat():
    global chat_history

    user_input = request.json.get("user_input")
    wallet_tokens = request.json.get("wallet_tokens")
    wallet_address = request.json.get("wallet_address")

    if not chat_history:
        # Initialize the chat context only once if history is empty
        chat_history = setup_chat_context(wallet_address, wallet_tokens)

    if user_input:
        # Process the user input with current chat history
        response, updated_history = parse_intent(user_input, chat_history)
        chat_history = updated_history  # Update the global chat history

        return jsonify({"response": response})
    else:
        return jsonify({"error": "No user input provided"}), 400


def main():
    chat_history = setup_chat_context(
        "0x77984Dc88AaB3D9c843256d7AaBDc82540c94F69", None
    )
    while True:
        user_prompt = input("You: ")
        if user_prompt.lower() in {"exit", "quit"}:
            break
        response, chat_history = parse_intent(user_prompt, chat_history)
        print(response)


if __name__ == "__main__":
    app.run(debug=True)
    # main()
