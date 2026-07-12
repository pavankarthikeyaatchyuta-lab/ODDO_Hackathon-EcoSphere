"use client";
import { useState } from "react";
import GlassCard from "@/app/components/ui/GlassCard";
import Navbar from "@/app/components/layout/Navbar";
import Button from "@/app/components/ui/Button";
import { useToast } from "@/app/components/ui/Toast";
import api from "@/app/services/api";

const reports = [
  { key: "environmental", label: "Environmental", endpoint: "/api/reports/environmental" },
  { key: "social", label: "Social", endpoint: "/api/reports/social" },
  { key: "governance", label: "Governance", endpoint: "/api/reports/governance" },
  { key: "summary", label: "ESG Summary", endpoint: "/api/reports/summary" },
];

export default function ReportsPage() {
  const [format, setFormat] = useState<"csv" | "xlsx" | "pdf">("csv");
  const [loading, setLoading] = useState<string | null>(null);
  const { show } = useToast();

  const download = async (endpoint: string, label: string) => {
    setLoading(label);
    try {
      const res = await api.get(`${endpoint}?fmt=${format}`, { responseType: "blob" });
      const url = URL.createObjectURL(res.data);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${label.toLowerCase().replace(" ", "_")}.${format}`;
      a.click();
      URL.revokeObjectURL(url);
      show(`${label} report downloaded`, "success");
    } catch {
      show("Download failed", "error");
    } finally {
      setLoading(null);
    }
  };

  return (
    <div>
      <Navbar title="Reports" />
      <div className="p-6 space-y-6">
        <GlassCard>
          <h3 className="text-sm font-semibold mb-3 text-[var(--text-muted)]">Export Format</h3>
          <div className="flex gap-2">
            {(["csv", "xlsx", "pdf"] as const).map(f => (
              <Button key={f} variant={format === f ? "primary" : "ghost"} size="sm" onClick={() => setFormat(f)}>
                {f.toUpperCase()}
              </Button>
            ))}
          </div>
        </GlassCard>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {reports.map(r => (
            <GlassCard key={r.key} hover>
              <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-1">{r.label} Report</h3>
              <p className="text-xs text-[var(--text-muted)] mb-4">
                Export all {r.label.toLowerCase()} data as {format.toUpperCase()}
              </p>
              <Button
                onClick={() => download(r.endpoint, r.label)}
                disabled={loading === r.label}
              >
                {loading === r.label ? "Exporting..." : `Export ${format.toUpperCase()}`}
              </Button>
            </GlassCard>
          ))}
        </div>
      </div>
    </div>
  );
}
