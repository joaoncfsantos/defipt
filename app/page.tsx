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

export default function Main() {
  const { primaryWallet } = useDynamicContext();

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
      </main>
      <div className="fixed bottom-12 left-0 right-0 py-4 px-14 bg-background">
        <div className="max-w-screen-xl mx-auto">
          <div className="relative">
            <Input
              type="text"
              placeholder="Ask me anything"
              className="pr-24"
            />
            <Button className="absolute right-1 top-1/2 -translate-y-1/2 h-8 bg-neutral-800 text-white">
              <ChevronRight className="w-4 h-4 " />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
