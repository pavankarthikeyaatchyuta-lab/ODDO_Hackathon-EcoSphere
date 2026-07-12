import type { Metadata } from "next";
import "./globals.css";
import NatureBackground from "./components/background/NatureBackground";
import CustomCursor from "./components/cursor/CustomCursor";
import { ToastProvider } from "./components/ui/Toast";

export const metadata: Metadata = {
  title: "EcoSphere — ESG Management",
  description: "ESG Performance Management Platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <NatureBackground />
        <CustomCursor />
        <ToastProvider>{children}</ToastProvider>
      </body>
    </html>
  );
}
