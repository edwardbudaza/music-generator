import "@/styles/globals.css";

import { type Metadata } from "next";
import { Inter } from "next/font/google";
import Provider from "./provider";

export const metadata: Metadata = {
  title: "Music Generator",
  description: "AI-powered music generation platform",
  keywords: ["AI", "music", "generation", "audio", "creative"],
  authors: [{ name: "Edward Budaza" }],
};

const font = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${font.className}`}>
      <body>
        <Provider>{children}</Provider>
      </body>
    </html>
  );
}
