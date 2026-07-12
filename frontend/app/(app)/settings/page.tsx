"use client";
import { useEffect, useState } from "react";
import GlassCard from "@/app/components/ui/GlassCard";
import Navbar from "@/app/components/layout/Navbar";
import Button from "@/app/components/ui/Button";
import { useToast } from "@/app/components/ui/Toast";
import api from "@/app/services/api";

const TOGGLES = [
  { key: "auto_emission_calculation", label: "Auto Emission Calculation", desc: "Auto-create carbon transactions from purchase/fleet/expense records" },
  { key: "evidence_requirement", label: "Evidence Requirement for CSR", desc: "CSR participation cannot be approved without a proof file" },
];

export default function SettingsPage() {
  const [settings, setSettings] = useState<Record<string, string>>({});
  const [departments, setDepartments] = useState<any[]>([]);
  const [newDeptName, setNewDeptName] = useState("");
  const { show } = useToast();

  const load = async () => {
    try {
      const [s, d] = await Promise.all([
        api.get("/api/settings/app"),
        api.get("/api/settings/departments"),
      ]);
      const map: Record<string, string> = {};
      s.data.forEach((item: any) => { map[item.key] = item.value; });
      setSettings(map);
      setDepartments(d.data);
    } catch {}
  };

  useEffect(() => { load(); }, []);

  const toggle = async (key: string) => {
    const current = settings[key] === "true";
    try {
      await api.put(`/api/settings/app/${key}`, { value: (!current).toString() });
      setSettings(prev => ({ ...prev, [key]: (!current).toString() }));
      show(`${key.replace(/_/g, " ")} ${!current ? "enabled" : "disabled"}`, "success");
    } catch {
      show("Failed to update setting", "error");
    }
  };

  const addDept = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newDeptName.trim()) return;
    try {
      await api.post("/api/settings/departments", { name: newDeptName });
      setNewDeptName("");
      show("Department created", "success");
      load();
    } catch {
      show("Failed to create department", "error");
    }
  };

  return (
    <div>
      <Navbar title="Settings" />
      <div className="p-6 space-y-6">
        <GlassCard>
          <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-4">Business Rule Toggles</h3>
          <div className="space-y-4">
            {TOGGLES.map(({ key, label, desc }) => (
              <div key={key} className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-[var(--text-primary)]">{label}</p>
                  <p className="text-xs text-[var(--text-muted)] mt-0.5">{desc}</p>
                </div>
                <button
                  onClick={() => toggle(key)}
                  className={`w-11 h-6 rounded-full transition-all relative ${settings[key] === "true" ? "bg-[var(--accent-moss)]" : "bg-white/10"}`}
                >
                  <span className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-all ${settings[key] === "true" ? "left-6" : "left-1"}`} />
                </button>
              </div>
            ))}
          </div>
        </GlassCard>

        <GlassCard>
          <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-4">Departments</h3>
          <form onSubmit={addDept} className="flex gap-2 mb-4">
            <input
              value={newDeptName}
              onChange={e => setNewDeptName(e.target.value)}
              placeholder="New department name"
              className="flex-1 bg-white/5 border border-[var(--border-glass)] rounded-xl px-3 py-2 text-sm text-[var(--text-primary)] outline-none"
            />
            <Button type="submit" size="sm">Add</Button>
          </form>
          <div className="space-y-2">
            {departments.map(d => (
              <div key={d.id} className="flex items-center gap-2 text-sm text-[var(--text-primary)]">
                <span className="w-6 h-6 rounded-full bg-[var(--accent-moss)]/20 flex items-center justify-center text-xs text-[var(--accent-moss)]">{d.id}</span>
                {d.name}
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
