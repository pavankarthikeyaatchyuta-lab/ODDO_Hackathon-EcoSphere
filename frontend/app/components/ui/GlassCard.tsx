import { ReactNode } from "react";
import clsx from "clsx";

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
  onClick?: () => void;
}

export default function GlassCard({ children, className, hover, onClick }: GlassCardProps) {
  return (
    <div
      onClick={onClick}
      className={clsx(
        "glass-card p-5",
        hover && "glass-card-hover",
        onClick && "cursor-pointer",
        className
      )}
    >
      {children}
    </div>
  );
}
