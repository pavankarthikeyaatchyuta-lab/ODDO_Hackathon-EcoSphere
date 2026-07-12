"use client";
import { useEffect, useState } from "react";
import GlassCard from "@/app/components/ui/GlassCard";
import Navbar from "@/app/components/layout/Navbar";
import Button from "@/app/components/ui/Button";
import Skeleton from "@/app/components/ui/Skeleton";
import EmptyState from "@/app/components/ui/EmptyState";
import { useToast } from "@/app/components/ui/Toast";
import api from "@/app/services/api";

interface Emission {
  id: number;
  department_id: number;
  source_type: string;
  quantity: number;
  co2_equivalent: number;
  auto_generated: boolean;
  date: string;
}

export default function EnvironmentalPage() {
  const [emissions, setEmissions] = useState<Emission[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const { show } = useToast();
  const [form, setForm] = useState({
    department_id: "1",
    source_type: "manual",
    quantity: "0",
    description: "",
  });

  const load = async () => {
    try {
      const res = await api.get("/api/environmental/emissions");
      setEmissions(res.data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post("/api/environmental/emissions", {
        ...form,
        department_id: parseInt(form.department_id),
        quantity: parseFloat(form.quantity),
      });
      show("Carbon transaction recorded", "success");
      setShowForm(false);
      load();
    } catch {
      show("Failed to save transaction", "error");
    }
  };

  return (
    <div>
      <Navbar title="Environmental" />
      <div className="p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-[var(--text-primary)]">Carbon Transactions</h2>
          <Button onClick={() => setShowForm(!showForm)}>+ Add Transaction</Button>
        </div>

        {showForm && (
          <GlassCard>
            <form onSubmit={submit} className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs text-[var(--text-muted)] mb-1 block">Department ID</label>
                <input type="number" value={form.department_id}
                  onChange={e => setForm({ ...form, department_id: e.target.value })}
                  className="w-full bg-white/5 border border-[var(--border-glass)] rounded-xl px-3 py-2 text-sm text-[var(--text-primary)] outline-none" />
              </div>
              <div>
                <label className="text-xs text-[var(--text-muted)] mb-1 block">Source Type</label>
                <select value={form.source_type}
                  onChange={e => setForm({ ...form, source_type: e.target.value })}
                  className="w-full bg-[#0f1f18] border border-[var(--border-glass)] rounded-xl px-3 py-2 text-sm text-[var(--text-primary)] outline-none">
                  {["manual", "purchase", "manufacturing", "expense", "fleet"].map(t => (
                    <option key={t} value={t}>{t}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-xs text-[var(--text-muted)] mb-1 block">Quantity</label>
                <input type="number" step="0.01" value={form.quantity}
                  onChange={e => setForm({ ...form, quantity: e.target.value })}
                  className="w-full bg-white/5 border border-[var(--border-glass)] rounded-xl px-3 py-2 text-sm text-[var(--text-primary)] outline-none" />
              </div>
              <div>
                <label className="text-xs text-[var(--text-muted)] mb-1 block">Description</label>
                <input value={form.description}
                  onChange={e => setForm({ ...form, description: e.target.value })}
                  className="w-full bg-white/5 border border-[var(--border-glass)] rounded-xl px-3 py-2 text-sm text-[var(--text-primary)] outline-none" />
              </div>
              <div className="col-span-2 flex gap-2">
                <Button type="submit">Save</Button>
                <Button type="button" variant="ghost" onClick={() => setShowForm(false)}>Cancel</Button>
              </div>
            </form>
          </GlassCard>
        )}

        {loading ? <Skeleton /> : emissions.length === 0 ? (
          <EmptyState message="No carbon transactions yet." />
        ) : (
          <div className="space-y-2">
            {emissions.map(e => (
              <GlassCard key={e.id} hover className="flex items-center gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs px-2 py-0.5 rounded-full border border-[var(--border-glass)] text-[var(--text-muted)]">
                      {e.source_type}
                    </span>
                    {e.auto_generated && (
                      <span className="text-xs px-2 py-0.5 rounded-full bg-teal-900/30 text-teal-300 border border-teal-500/20">auto</span>
                    )}
                  </div>
                  <p className="text-xs text-[var(--text-muted)] mt-1">{new Date(e.date).toLocaleDateString()}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-semibold text-[var(--text-primary)]">{e.co2_equivalent} <span className="text-xs text-[var(--text-muted)]">kg CO₂</span></p>
                  <p className="text-xs text-[var(--text-muted)]">qty: {e.quantity}</p>
                </div>
              </GlassCard>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
