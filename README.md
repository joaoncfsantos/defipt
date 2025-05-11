
# DeFiPT - ETH Lisbon 2025 Hackathon Project

Welcome to **DeFiPT**, your personal DeFi Personal Trainer. Our product is an AI-powered chatbot that learns from each user's portfolio to deliver a highly personalised financial experience. It offers tailored investment advice and identifies the most promising opportunities within the Gnosis Chain.

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Technologies](#technologies)
* [Getting Started](#getting-started)
* [Server API Endpoints](#server-api-endpoints)
* [Usage](#usage)

## Overview

DeFiPT is designed to integrate AI-driven recommendations with real-time data from major DeFi protocols on the Gnosis Chain. It uses **OpenAI's GPT-4 Turbo** to engage with users in a conversational interface, helping them optimize their DeFi portfolio based on their current holdings and user-defined risk parameters.

The platform pulls data from the Gnosis chain from popular DeFi protocols like Aave, Agave, and Balancer, and uses that data to provide personalized suggestions for yield farming, liquidity pools, borrowing, and lending. You can interact with the platform via a chat-based interface to get tailored investment strategies, all while being informed about the risk levels associated with each option.

## Features

* **Wallet Integration**: Connect your Gnosis wallet to fetch real-time data about your holdings and positions (using Dynamic).
* **Chat-Based Interface**: Easily interact with the AI agent to explore and optimize your DeFi portfolio.
* **Real-Time Data Integration**: Fetch live data from multiple rpc calls of some DeFi protocols such as Aave, Agave, and Balancer.
* **Risk-Based Portfolio Optimization**: With risk parameters evaluation. DeFiPT recommend the best investment opportunities.
* **Yield Strategies**: DeFiPT generates lists of strategies and and opportunities to your portfolio and preferences.
* **Cross-Protocol Data Integration**: Combines data from multiple DeFi platforms to offer a comprehensive view of the DeFi landscape.

## Technologies

* **Wallet Integration**: Dynamic
* **Backend Framework**: Python, Flask
* **AI Integration**: OpenAI GPT-4 Turbo API
* **Protocols**: The most popular on Gnosis chains: Aave, Agave and  Balancer.
* **Data**: On-chain Protocol data from Gnosis Chain and for tokens data from GraphQL APIs
* **Frontend**: Next.js, React

## Getting Started

To get started with **DeFiPT**, clone this repository and set up the environment.

### Prerequisites

* Python 3.7+
* pip
* An OpenAI API key

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/joaoncfsantos/defipt.git
   cd defipt
   ```

3. Create a `.env` file in the root of the project and add your OpenAI API key:

   ```bash
   OPENAI_API_KEY=your_openai_api_key
   ```

4. Run the Flask app inside the pynovasafe directory:

   ```bash
   python server.py
   ```

   The server will start, and you can make API calls to interact with the chatbot interface.


5. Run the Frontend app inside the frontend directory:

   ```bash
   npm install
   npm run dev
   ```

   The frontend will be available at [http://localhost:3000](http://localhost:3000).

## Server API Endpoints

### `/reset_chat` (POST)

Resets the chat history.

**Request Body**:

```json
{
  "message": "Reset chat"
}
```

**Response**:

```json
{
  "message": "Chat history has been reset."
}
```

### `/chat` (POST)

Send a user query and receive a response from the AI agent. This query can be used to interact with your DeFi portfolio and ask for recommendations.

**Query Parameters**:

* `user_input`: The input provided by the user (e.g., "Optimize my portfolio for low risk").
* `wallet_address`: The user's Gnosis wallet address.
* `wallet_tokens`: The list of tokens in the user's wallet.

**Example Request**:

```json
{
  "user_input": "What are the best yield strategies for my portfolio?",
  "wallet_address": "0xYourWalletAddress",
  "wallet_tokens": {"token1": 100, "token2": 50}
}
```

**Response**:

```json
{
  "response": "Based on your current portfolio, I recommend the following yield strategies..."
}
```

## Usage

Once your Flask server and the frontend is up and running, you can interact with DeFiPT through the chatbot interface to ask for personalized DeFi recommendations. Here are a few things you can ask DeFiPT:

* "Accordingly to my wallet holdings, what are the best investments that I can do?"
* "Tell me my AAVE supply positions."
* "Optimize my portfolio for low risk."
* "What are the interest rates for lending on Agave?"


## For the Future

* Implement more DeFi protocols to provide a wider range of investment opportunities and analysis.
* Implement writing functions inside the bot, so the user can execute the on chain transactions directly from the chat interface.
* If we added more protocols, we needed a new way of scalling the context window of the AI. So using a vector database and devide the data in chuncks of embeddings it is the right direction.

