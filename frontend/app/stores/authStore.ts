import { create } from "zustand";
import { persist } from "zustand/middleware";
import api from "@/app/services/api";

interface User {
  id: number;
  email: string;
  full_name: string;
  role: "admin" | "manager" | "employee";
  department_id: number | null;
  xp_points: number;
  is_active: boolean;
}

interface AuthState {
  token: string | null;
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  fetchMe: () => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      user: null,

      login: async (email, password) => {
        const form = new URLSearchParams();
        form.append("username", email);
        form.append("password", password);
        const res = await api.post("/api/auth/login", form, {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        });
        set({ token: res.data.access_token });
        await get().fetchMe();
      },

      logout: () => {
        set({ token: null, user: null });
        if (typeof window !== "undefined") window.location.href = "/login";
      },

      fetchMe: async () => {
        const { token } = get();
        if (!token) return;
        const res = await api.get("/api/auth/me", {
          headers: { Authorization: `Bearer ${token}` },
        });
        set({ user: res.data });
      },
    }),
    { name: "ecosphere-auth" }
  )
);
