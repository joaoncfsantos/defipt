"use client";

import { DynamicWidget } from "@/lib/dynamic";
import { useState, useEffect, useRef } from "react";
import DynamicMethods from "@/app/components/Methods";
import { useDarkMode } from "@/lib/useDarkMode";
import Image from "next/image";
import "./../src/output.css";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ChevronRight } from "lucide-react";
import { cardsData } from "@/data/cards-data";
import { Card } from "@/app/components/Card";
import {
  useDynamicContext,
  useTokenBalances,
} from "@dynamic-labs/sdk-react-core";
import { UserInfo } from "./components/UserInfo";
import Chat from "./components/Chat";

type TokenBalanceTuple = [string, string]; // [address, rawBalance]

export default function Main() {
  const { primaryWallet } = useDynamicContext();
  const { tokenBalances, isLoading, isError, error } = useTokenBalances();
  const [userTokens, setUserTokens] = useState<TokenBalanceTuple[]>([]);
  const [userInput, setUserInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [response, setResponse] = useState("");
  const [chatHistory, setChatHistory] = useState<
    { role: string; content: string }[]
  >([]);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (primaryWallet) {
      console.log("Wallet connected:", primaryWallet);
    }
  }, [primaryWallet]);

  useEffect(() => {
    if (tokenBalances && primaryWallet) {
      const tokens: TokenBalanceTuple[] = tokenBalances.map((token) => [
        token.address,
        token.rawBalance.toString(),
      ]);
      setUserTokens(tokens);
      console.log("Token balances updated:", tokens);
    }
  }, [tokenBalances, primaryWallet]);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory]);

  const handleSendRequest = async (userInput: string) => {
    if (!userInput.trim()) return;

    // Add user message to chat history
    const userMessage = { role: "user", content: userInput };
    setChatHistory((prevHistory) => [...prevHistory, userMessage]);

    setIsSending(true);
    setResponse("");
    try {
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_input: userInput,
          wallet_address: primaryWallet?.address,
          wallet_tokens: userTokens,
        }),
      });

      const data = await response.json();
      console.log(data);
      setResponse(data.response);

      // Add assistant response to chat history
      const assistantMessage = { role: "assistant", content: data.response };
      setChatHistory((prevHistory) => [...prevHistory, assistantMessage]);

      setUserInput("");
    } catch (error) {
      console.error("Error sending request:", error);
      setResponse("Error sending request. Please try again.");
    } finally {
      setIsSending(false);
    }
  };

  const handleResetChat = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/reset_chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_address: primaryWallet?.address,
          tokens: userTokens,
        }),
      });

      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error("Error sending request:", error);
    } finally {
      window.location.reload();
    }
  };

  const handleCardClick = (card: { title: string; description: string }) => {
    handleSendRequest(card.description);
  };

  /* const handleRefreshPage = () => {
    window.location.reload();
    handleResetChat();
  }; */

  return (
    <div className="min-h-screen relative">
      <div className="fixed top-0 left-0 right-0 py-4 px-14 bg-transparent">
        <div className="max-w-screen-xl mx-auto flex justify-between items-center">
          <h1
            onClick={() => {
              handleResetChat();
            }}
            className="text-4xl text-white font-bold hover:text-gray-200 cursor-pointer"
          >
            DefiPT
          </h1>
          <DynamicWidget />
        </div>
      </div>
      <main
        ref={chatContainerRef}
        className="fixed top-24 bottom-40 left-0 right-0 overflow-y-auto scrollbar-hide"
      >
        <div className="flex flex-col gap-[32px] items-center p-8 sm:p-20 font-[family-name:var(--font-geist-sans)]">
          {chatHistory.length === 0 ? (
            <div className="flex-1 flex items-center justify-center">
              <div className="flex flex-col gap-8">
                <div className="max-w-screen-xl mx-auto text-center">
                  <h1 className="text-3xl text-white font-bold">
                    Your DeFi Personal Trainer 💪
                  </h1>
                  <p className="text-white">
                    Ask me anything about DeFi, crypto, and blockchain.
                  </p>
                </div>
                <div className="flex max-w-screen-xl mx-auto gap-4">
                  {cardsData.map((card) => (
                    <Card
                      key={card.title}
                      title={card.title}
                      description={card.description}
                      onClick={() => handleCardClick(card)}
                    />
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <Chat chatHistory={chatHistory} />
          )}
        </div>
      </main>
      <div className="fixed bottom-12 left-0 right-0 py-4 px-14 bg-transparent">
        <div className="max-w-screen-xl mx-auto">
          <div className="relative max-w-2xl mx-auto">
            <Input
              type="text"
              placeholder="Ask me anything"
              className={`pr-24 bg-white h-12 ${
                isSending ? "opacity-50 cursor-not-allowed" : ""
              }`}
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === "Enter") {
                  handleSendRequest(userInput);
                }
              }}
              disabled={isSending}
            />
            <Button
              className="absolute right-1 top-1/2 -translate-y-1/2 h-10 bg-neutral-800 text-white"
              onClick={() => handleSendRequest(userInput)}
              disabled={isSending}
            >
              {isSending ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <ChevronRight className="w-4 h-4" />
              )}
            </Button>
          </div>
        </div>
        <div className="flex items-center justify-center gap-1 mt-2">
          <p className="text-white text-sm">Powered by</p>
          <Image
            src="/gnosis.svg"
            alt="logo"
            width={96}
            height={96}
            className="brightness-0 invert"
          />
        </div>
      </div>
    </div>
  );
}
