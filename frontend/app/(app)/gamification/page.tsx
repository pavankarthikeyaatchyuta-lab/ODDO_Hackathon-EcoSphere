"use client";
import { useEffect, useState } from "react";
import GlassCard from "@/app/components/ui/GlassCard";
import Navbar from "@/app/components/layout/Navbar";
import Button from "@/app/components/ui/Button";
import Skeleton from "@/app/components/ui/Skeleton";
import EmptyState from "@/app/components/ui/EmptyState";
import { useToast } from "@/app/components/ui/Toast";
import { Trophy, Medal, Gift, Zap } from "lucide-react";
import api from "@/app/services/api";

export default function GamificationPage() {
  const [tab, setTab] = useState<"challenges" | "badges" | "rewards" | "leaderboard">("challenges");
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const { show } = useToast();

  const endpoints: Record<string, string> = {
    challenges: "/api/gamification/challenges",
    badges: "/api/gamification/badges",
    rewards: "/api/gamification/rewards",
    leaderboard: "/api/gamification/leaderboard",
  };

  const load = async () => {
    setLoading(true);
    try {
      const res = await api.get(endpoints[tab]);
      setData(res.data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [tab]);

  const joinChallenge = async (id: number) => {
    try {
      await api.post(`/api/gamification/challenges/${id}/join`);
      show("Joined challenge!", "success");
    } catch (e: any) {
      show(e?.response?.data?.detail || "Error", "error");
    }
  };

  const redeem = async (id: number) => {
    try {
      await api.post(`/api/gamification/rewards/${id}/redeem`);
      show("Reward redeemed! 🎁", "success");
      load();
    } catch (e: any) {
      show(e?.response?.data?.detail || "Error", "error");
    }
  };

  return (
    <div>
      <Navbar title="Gamification" />
      <div className="p-6 space-y-4">
        <div className="flex gap-2 flex-wrap">
          {(["challenges", "badges", "rewards", "leaderboard"] as const).map(t => (
            <Button key={t} variant={tab === t ? "primary" : "ghost"} size="sm" onClick={() => setTab(t)}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </Button>
          ))}
        </div>

        {loading ? <Skeleton /> : data.length === 0 ? (
          <EmptyState message={`No ${tab} yet.`} />
        ) : (
          <div className="space-y-2">
            {data.map((item: any, i: number) => (
              <GlassCard key={item.id || i} hover>
                <div className="flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3">
                    {tab === "leaderboard" && (
                      <span className="text-lg text-[var(--accent-gold)]">#{i + 1}</span>
                    )}
                    <div>
                      <p className="text-sm font-medium text-[var(--text-primary)]">
                        {item.title || item.name || item.full_name}
                      </p>
                      <p className="text-xs text-[var(--text-muted)] mt-0.5">
                        {item.description || item.status || ""}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {item.xp_reward && (
                      <span className="flex items-center gap-1 text-xs" style={{ color: "var(--accent-gold)" }}>
                        <Zap size={12} />{item.xp_reward} XP
                      </span>
                    )}
                    {item.xp_points !== undefined && (
                      <span className="flex items-center gap-1 text-xs font-bold" style={{ color: "var(--accent-gold)" }}>
                        <Zap size={12} />{item.xp_points}
                      </span>
                    )}
                    {item.xp_cost && (
                      <span className="text-xs text-[var(--text-muted)]">Cost: {item.xp_cost} XP</span>
                    )}
                    {tab === "challenges" && (
                      <Button size="sm" variant="ghost" onClick={() => joinChallenge(item.id)}>Join</Button>
                    )}
                    {tab === "rewards" && (
                      <Button size="sm" onClick={() => redeem(item.id)}>Redeem</Button>
                    )}
                    {item.stock !== undefined && (
                      <span className="text-xs text-[var(--text-muted)]">Stock: {item.stock}</span>
                    )}
                  </div>
                </div>
              </GlassCard>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
