"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { TreePine } from "lucide-react";
import { useAuthStore } from "@/app/stores/authStore";
import { useToast } from "@/app/components/ui/Toast";
import Button from "@/app/components/ui/Button";
import GlassCard from "@/app/components/ui/GlassCard";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuthStore();
  const { show } = useToast();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await login(email, password);
      show("Welcome back!", "success");
      router.push("/dashboard");
    } catch {
      show("Invalid email or password", "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <GlassCard className="w-full max-w-sm">
        <div className="flex flex-col items-center mb-8">
          <div className="w-14 h-14 rounded-2xl flex items-center justify-center mb-4"
            style={{ background: "linear-gradient(135deg, var(--accent-moss), var(--accent-teal))" }}>
            <TreePine size={28} className="text-white" />
          </div>
          <h1 className="text-xl font-bold text-[var(--text-primary)]">EcoSphere</h1>
          <p className="text-xs text-[var(--text-muted)] mt-1">ESG Management Platform</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-xs text-[var(--text-muted)] mb-1.5 block">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-white/5 border border-[var(--border-glass)] rounded-xl px-4 py-2.5 text-sm text-[var(--text-primary)] outline-none focus:border-[var(--accent-moss)]"
              placeholder="you@company.com"
              required
            />
          </div>
          <div>
            <label className="text-xs text-[var(--text-muted)] mb-1.5 block">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-white/5 border border-[var(--border-glass)] rounded-xl px-4 py-2.5 text-sm text-[var(--text-primary)] outline-none focus:border-[var(--accent-moss)]"
              placeholder="••••••••"
              required
            />
          </div>
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Signing in..." : "Sign In"}
          </Button>
        </form>

        <p className="text-center text-xs text-[var(--text-muted)] mt-6">
          Don&apos;t have an account?{" "}
          <Link href="/signup" className="text-[var(--accent-moss)] hover:underline">
            Sign Up
          </Link>
        </p>
      </GlassCard>
    </div>
  );
}
