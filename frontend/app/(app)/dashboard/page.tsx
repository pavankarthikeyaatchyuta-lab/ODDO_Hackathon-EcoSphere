"use client";
import { useEffect, useState } from "react";
import {
  RadialBarChart, RadialBar, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, LineChart, Line,
} from "recharts";
import GlassCard from "@/app/components/ui/GlassCard";
import Navbar from "@/app/components/layout/Navbar";
import Skeleton from "@/app/components/ui/Skeleton";
import api from "@/app/services/api";

interface DeptScore {
  department_id: number;
  department_name: string;
  environmental_score: number;
  social_score: number;
  governance_score: number;
  total_score: number;
}

interface ESGData {
  org_score: number;
  department_scores: DeptScore[];
  weights: { environmental: number; social: number; governance: number };
}

interface ActivityItem {
  type: string;
  timestamp: string;
  title: string;
  icon: string;
}

interface LeaderboardUser {
  id: number;
  full_name: string;
  xp_points: number;
  department_id: number | null;
}

export default function DashboardPage() {
  const [esg, setEsg] = useState<ESGData | null>(null);
  const [activity, setActivity] = useState<ActivityItem[]>([]);
  const [leaderboard, setLeaderboard] = useState<LeaderboardUser[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [esgRes, actRes, lbRes] = await Promise.all([
          api.get("/api/dashboard/esg-score"),
          api.get("/api/dashboard/activity?limit=10"),
          api.get("/api/gamification/leaderboard?limit=5"),
        ]);
        setEsg(esgRes.data);
        setActivity(actRes.data);
        setLeaderboard(lbRes.data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) return (
    <div className="p-6">
      <Navbar title="Dashboard" />
      <Skeleton count={4} className="mt-6" />
    </div>
  );

  const kpis = [
    { label: "Org ESG Score", value: esg?.org_score ?? 0, color: "var(--accent-teal)" },
    { label: "Departments", value: esg?.department_scores.length ?? 0, color: "var(--accent-moss)" },
    { label: "Env Weight", value: `${esg?.weights.environmental}%`, color: "#4ade80" },
    { label: "Social Weight", value: `${esg?.weights.social}%`, color: "var(--accent-gold)" },
  ];

  const chartData = esg?.department_scores.map((d) => ({
    name: d.department_name.slice(0, 8),
    Environmental: d.environmental_score,
    Social: d.social_score,
    Governance: d.governance_score,
  })) ?? [];

  return (
    <div>
      <Navbar title="ESG Dashboard" />
      <div className="p-6 space-y-6">
        {/* KPI row */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {kpis.map((k) => (
            <GlassCard key={k.label} hover>
              <p className="text-xs text-[var(--text-muted)] mb-1">{k.label}</p>
              <p className="text-2xl font-bold" style={{ color: k.color }}>{k.value}</p>
            </GlassCard>
          ))}
        </div>

        {/* Charts row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <GlassCard>
            <h3 className="text-sm font-semibold mb-4 text-[var(--text-muted)]">Department ESG Breakdown</h3>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: "#8ba888" }} />
                <YAxis tick={{ fontSize: 11, fill: "#8ba888" }} />
                <Tooltip contentStyle={{ background: "#0f1f18", border: "1px solid rgba(78,160,100,0.2)" }} />
                <Bar dataKey="Environmental" fill="var(--accent-teal)" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Social" fill="var(--accent-gold)" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Governance" fill="var(--accent-moss)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </GlassCard>

          <GlassCard>
            <h3 className="text-sm font-semibold mb-4 text-[var(--text-muted)]">Top Performers</h3>
            <div className="space-y-3">
              {leaderboard.length === 0 && <p className="text-xs text-[var(--text-muted)]">No data yet</p>}
              {leaderboard.map((u, i) => (
                <div key={u.id} className="flex items-center gap-3">
                  <span className="text-xs w-5 text-[var(--text-muted)]">#{i + 1}</span>
                  <div className="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white"
                    style={{ background: "var(--accent-moss)" }}>
                    {u.full_name[0]}
                  </div>
                  <span className="text-sm flex-1 text-[var(--text-primary)] truncate">{u.full_name}</span>
                  <span className="text-xs font-semibold" style={{ color: "var(--accent-gold)" }}>{u.xp_points} XP</span>
                </div>
              ))}
            </div>
          </GlassCard>
        </div>

        {/* Activity feed */}
        <GlassCard>
          <h3 className="text-sm font-semibold mb-4 text-[var(--text-muted)]">Activity Feed</h3>
          <div className="space-y-3">
            {activity.length === 0 && <p className="text-xs text-[var(--text-muted)]">No recent activity</p>}
            {activity.map((a, i) => (
              <div key={i} className="flex items-start gap-3 text-sm">
                <span className="text-base">{a.icon}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-[var(--text-primary)] text-xs">{a.title}</p>
                  <p className="text-[var(--text-muted)] text-xs mt-0.5">
                    {new Date(a.timestamp).toLocaleString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
