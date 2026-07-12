"use client";
import { useState } from "react";
import GlassCard from "@/app/components/ui/GlassCard";
import Navbar from "@/app/components/layout/Navbar";
import Button from "@/app/components/ui/Button";
import { useToast } from "@/app/components/ui/Toast";
import { Cpu, Leaf, Shield, FileText } from "lucide-react";
import api from "@/app/services/api";

const insights = [
  { key: "esg-summary", label: "ESG Executive Summary", icon: Cpu, endpoint: "/api/ai/esg-summary" },
  { key: "carbon-insights", label: "Carbon Insights", icon: Leaf, endpoint: "/api/ai/carbon-insights" },
  { key: "audit-summary", label: "Audit & Compliance Summary", icon: Shield, endpoint: "/api/ai/audit-summary" },
];

export default function AIInsightsPage() {
  const [results, setResults] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState<string | null>(null);
  const { show } = useToast();

  const fetch = async (key: string, endpoint: string, label: string) => {
    setLoading(key);
    try {
      const res = await api.get(endpoint);
      setResults(prev => ({ ...prev, [key]: res.data.result }));
      show(`${label} generated`, "success");
    } catch {
      show("AI request failed", "error");
    } finally {
      setLoading(null);
    }
  };

  return (
    <div>
      <Navbar title="AI Insights" />
      <div className="p-6 space-y-4">
        <p className="text-sm text-[var(--text-muted)]">
          AI-powered analysis powered by Gemini. Results are based on real data from your ESG records.
        </p>

        {insights.map(({ key, label, icon: Icon, endpoint }) => (
          <GlassCard key={key}>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Icon size={16} style={{ color: "var(--accent-teal)" }} />
                <h3 className="text-sm font-semibold text-[var(--text-primary)]">{label}</h3>
              </div>
              <Button size="sm" onClick={() => fetch(key, endpoint, label)} disabled={loading === key}>
                {loading === key ? "Generating..." : "Generate"}
              </Button>
            </div>

            {results[key] ? (
              <div className="bg-white/5 rounded-xl p-4">
                <p className="text-sm text-[var(--text-primary)] leading-relaxed whitespace-pre-wrap">{results[key]}</p>
              </div>
            ) : (
              <p className="text-xs text-[var(--text-muted)]">Click Generate to get AI-powered insights.</p>
            )}
          </GlassCard>
        ))}
      </div>
    </div>
  );
}
