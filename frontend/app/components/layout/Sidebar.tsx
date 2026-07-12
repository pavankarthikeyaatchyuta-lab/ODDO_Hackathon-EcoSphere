"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard, Leaf, Users, Shield, Trophy, FileText,
  Cpu, Settings, LogOut, TreePine
} from "lucide-react";
import clsx from "clsx";
import { useAuthStore } from "@/app/stores/authStore";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/environmental", label: "Environmental", icon: Leaf },
  { href: "/social", label: "Social", icon: Users },
  { href: "/governance", label: "Governance", icon: Shield },
  { href: "/gamification", label: "Gamification", icon: Trophy },
  { href: "/reports", label: "Reports", icon: FileText },
  { href: "/ai-insights", label: "AI Insights", icon: Cpu },
  { href: "/settings", label: "Settings", icon: Settings, adminOnly: true },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuthStore();

  const visibleItems = navItems.filter(
    (item) => !item.adminOnly || user?.role === "admin"
  );

  return (
    <aside className="w-64 h-screen fixed left-0 top-0 glass-card rounded-none border-r border-[var(--border-glass)] flex flex-col z-50">
      <div className="p-6 border-b border-[var(--border-glass)]">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl flex items-center justify-center"
            style={{ background: "linear-gradient(135deg, var(--accent-moss), var(--accent-teal))" }}>
            <TreePine size={18} className="text-white" />
          </div>
          <div>
            <p className="font-bold text-sm text-[var(--text-primary)]">EcoSphere</p>
            <p className="text-xs text-[var(--text-muted)]">ESG Platform</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 py-4 overflow-y-auto scrollbar-thin">
        {visibleItems.map(({ href, label, icon: Icon }) => {
          const active = pathname.startsWith(href);
          return (
            <Link
              key={href}
              href={href}
              className={clsx(
                "flex items-center gap-3 px-5 py-3 mx-2 rounded-xl text-sm transition-all",
                active
                  ? "bg-[var(--accent-moss)]/20 text-[var(--text-primary)] border border-[var(--accent-moss)]/30"
                  : "text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-white/5"
              )}
            >
              <Icon size={16} />
              {label}
            </Link>
          );
        })}
      </nav>

      {user && (
        <div className="p-4 border-t border-[var(--border-glass)]">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white"
              style={{ background: "var(--accent-moss)" }}>
              {user.full_name?.[0]?.toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium text-[var(--text-primary)] truncate">{user.full_name}</p>
              <p className="text-xs text-[var(--text-muted)] capitalize">{user.role}</p>
            </div>
          </div>
          <button
            onClick={logout}
            className="flex items-center gap-2 text-xs text-[var(--text-muted)] hover:text-red-400 transition-colors"
          >
            <LogOut size={13} /> Sign out
          </button>
        </div>
      )}
    </aside>
  );
}
