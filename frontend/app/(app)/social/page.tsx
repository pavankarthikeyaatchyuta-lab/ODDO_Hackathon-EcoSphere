"use client";
import { useEffect, useState } from "react";
import GlassCard from "@/app/components/ui/GlassCard";
import Navbar from "@/app/components/layout/Navbar";
import Button from "@/app/components/ui/Button";
import Skeleton from "@/app/components/ui/Skeleton";
import EmptyState from "@/app/components/ui/EmptyState";
import { useToast } from "@/app/components/ui/Toast";
import api from "@/app/services/api";
import { useAuthStore } from "@/app/stores/authStore";

export default function SocialPage() {
  const [activities, setActivities] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const { show } = useToast();
  const { user } = useAuthStore();

  const load = async () => {
    try {
      const res = await api.get("/api/social/csr");
      setActivities(res.data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const join = async (activityId: number) => {
    try {
      await api.post("/api/social/csr/join", { activity_id: activityId });
      show("Joined CSR activity!", "success");
    } catch (e: any) {
      show(e?.response?.data?.detail || "Error joining", "error");
    }
  };

  return (
    <div>
      <Navbar title="Social" />
      <div className="p-6 space-y-4">
        <h2 className="text-lg font-semibold text-[var(--text-primary)]">CSR Activities</h2>

        {loading ? <Skeleton /> : activities.length === 0 ? (
          <EmptyState message="No CSR activities yet." />
        ) : (
          <div className="grid gap-3 sm:grid-cols-2">
            {activities.map((a) => (
              <GlassCard key={a.id} hover>
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <p className="text-sm font-medium text-[var(--text-primary)]">{a.title}</p>
                    <p className="text-xs text-[var(--text-muted)] mt-1">{a.description}</p>
                    <div className="flex items-center gap-2 mt-2">
                      <span className="text-xs text-[var(--accent-gold)]">+{a.xp_reward} XP</span>
                      <span className="text-xs text-[var(--text-muted)]">
                        {new Date(a.start_date).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                  <Button size="sm" variant="ghost" onClick={() => join(a.id)}>Join</Button>
                </div>
              </GlassCard>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
