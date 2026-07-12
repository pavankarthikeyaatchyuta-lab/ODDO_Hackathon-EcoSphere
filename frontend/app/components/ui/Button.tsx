import { ReactNode, ButtonHTMLAttributes } from "react";
import clsx from "clsx";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: "primary" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
}

const variants = {
  primary: "btn-primary",
  ghost: "border border-[var(--border-glass)] text-[var(--text-muted)] hover:border-[var(--accent-moss)] hover:text-[var(--text-primary)] rounded-xl px-4 py-2 transition-all",
  danger: "bg-red-900/30 border border-red-500/30 text-red-300 hover:bg-red-800/40 rounded-xl px-4 py-2 transition-all",
};

const sizes = {
  sm: "text-xs px-3 py-1.5",
  md: "text-sm px-4 py-2",
  lg: "text-base px-6 py-3",
};

export default function Button({ children, variant = "primary", size = "md", className, ...props }: ButtonProps) {
  return (
    <button className={clsx(variants[variant], sizes[size], className)} {...props}>
      {children}
    </button>
  );
}
