"use client";
import { Bell, Zap } from "lucide-react";
import { useAuthStore } from "@/app/stores/authStore";

export default function Navbar({ title }: { title?: string }) {
  const { user } = useAuthStore();

  return (
    <header className="h-16 glass-card rounded-none border-b border-[var(--border-glass)] flex items-center px-6 gap-4 sticky top-0 z-40">
      <h1 className="text-base font-semibold text-[var(--text-primary)] flex-1">{title || "EcoSphere"}</h1>

      {user && (
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full border border-[var(--border-glass)]"
            style={{ color: "var(--accent-gold)" }}>
            <Zap size={12} />
            <span>{user.xp_points ?? 0} XP</span>
          </div>
          <button className="w-8 h-8 flex items-center justify-center rounded-full text-[var(--text-muted)] hover:text-[var(--text-primary)] border border-[var(--border-glass)]">
            <Bell size={15} />
          </button>
        </div>
      )}
    </header>
  );
}
