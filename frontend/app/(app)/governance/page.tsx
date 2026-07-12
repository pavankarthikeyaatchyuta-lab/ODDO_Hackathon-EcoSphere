"use client";
import { useEffect, useState } from "react";
import GlassCard from "@/app/components/ui/GlassCard";
import Navbar from "@/app/components/layout/Navbar";
import Button from "@/app/components/ui/Button";
import Skeleton from "@/app/components/ui/Skeleton";
import EmptyState from "@/app/components/ui/EmptyState";
import { useToast } from "@/app/components/ui/Toast";
import api from "@/app/services/api";

const statusColors: Record<string, string> = {
  open: "text-yellow-400 border-yellow-500/30 bg-yellow-900/20",
  in_progress: "text-blue-400 border-blue-500/30 bg-blue-900/20",
  resolved: "text-green-400 border-green-500/30 bg-green-900/20",
  overdue: "text-red-400 border-red-500/30 bg-red-900/20",
};

export default function GovernancePage() {
  const [tab, setTab] = useState<"policies" | "audits" | "compliance">("policies");
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const { show } = useToast();

  const load = async () => {
    setLoading(true);
    try {
      const res = await api.get(`/api/governance/${tab}`);
      setData(res.data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [tab]);

  const checkOverdue = async () => {
    try {
      await api.post("/api/governance/compliance/check-overdue");
      show("Overdue check completed", "info");
      load();
    } catch {
      show("Failed", "error");
    }
  };

  return (
    <div>
      <Navbar title="Governance" />
      <div className="p-6 space-y-4">
        <div className="flex gap-2">
          {(["policies", "audits", "compliance"] as const).map(t => (
            <Button key={t} variant={tab === t ? "primary" : "ghost"} size="sm" onClick={() => setTab(t)}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </Button>
          ))}
          {tab === "compliance" && (
            <Button variant="ghost" size="sm" onClick={checkOverdue}>Check Overdue</Button>
          )}
        </div>

        {loading ? <Skeleton /> : data.length === 0 ? (
          <EmptyState message={`No ${tab} yet.`} />
        ) : (
          <div className="space-y-2">
            {data.map((item: any) => (
              <GlassCard key={item.id} hover>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-[var(--text-primary)]">{item.title}</p>
                    <p className="text-xs text-[var(--text-muted)] mt-0.5">
                      {item.category || item.severity || item.status || ""}
                    </p>
                  </div>
                  {item.status && (
                    <span className={`text-xs px-2 py-0.5 rounded-full border ${statusColors[item.status] || ""}`}>
                      {item.status.replace("_", " ")}
                    </span>
                  )}
                </div>
                {item.due_date && (
                  <p className="text-xs text-[var(--text-muted)] mt-1">
                    Due: {new Date(item.due_date).toLocaleDateString()}
                  </p>
                )}
              </GlassCard>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
