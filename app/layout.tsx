import "./globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Providers from "@/lib/providers";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "DefiPT",
  description: "Your DeFi Personal Trainer",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body
        className={`${inter.className} bg-gradient-to-br from-[#3d6958] to-[#325447] min-h-screen`}
      >
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
