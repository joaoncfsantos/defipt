"use client";

import { DynamicWidget } from "@/lib/dynamic";
import { useState, useEffect } from "react";
import DynamicMethods from "@/app/components/Methods";
import { useDarkMode } from "@/lib/useDarkMode";
import Image from "next/image";
import "./../src/output.css";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ChevronRight } from "lucide-react";
import { cardsData } from "@/data/cards-data";
import { Card } from "@/app/components/Card";
import { useDynamicContext } from "@dynamic-labs/sdk-react-core";
import { UserInfo } from "./components/UserInfo";
import Chat from "./components/Chat";

export default function Main() {
  const { primaryWallet } = useDynamicContext();

  const [userInput, setUserInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [response, setResponse] = useState("");

  const handleSendRequest = async () => {
    if (!userInput.trim()) return;

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
        }),
      });

      const data = await response.json();
      console.log(data);
      setResponse(data.response);
      setUserInput("");
    } catch (error) {
      console.error("Error sending request:", error);
      setResponse("Error sending request. Please try again.");
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="min-h-screen relative">
      <div className="fixed top-0 left-0 right-0 py-4 px-14 bg-background">
        <div className="max-w-screen-xl mx-auto flex justify-between items-center">
          <h1 className="text-4xl text-neutral-800 font-bold">NovaSafe</h1>
          <DynamicWidget />
        </div>
      </div>
      <main className="flex flex-col gap-[32px] items-center p-8 sm:p-20 font-[family-name:var(--font-geist-sans)]">
        <div className="max-w-screen-xl mx-auto">
          <h1 className="text-2xl text-neutral-800 font-bold">
            How can we help you?
          </h1>
          <UserInfo />
        </div>
        <div className="flex max-w-screen-xl mx-auto gap-4">
          {cardsData.map((card) => (
            <Card
              key={card.title}
              title={card.title}
              description={card.description}
            />
          ))}
        </div>
        <p>{response}</p>
        <Chat />
      </main>
      <div className="fixed bottom-12 left-0 right-0 py-4 px-14 bg-background">
        <div className="max-w-screen-xl mx-auto">
          <div className="relative">
            <Input
              type="text"
              placeholder="Ask me anything"
              className="pr-24"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === "Enter") {
                  handleSendRequest();
                }
              }}
            />
            <Button
              className="absolute right-1 top-1/2 -translate-y-1/2 h-8 bg-neutral-800 text-white"
              onClick={handleSendRequest}
              disabled={isSending}
            >
              <ChevronRight className="w-4 h-4 " />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
