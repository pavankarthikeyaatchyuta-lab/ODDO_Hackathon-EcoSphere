import { Leaf } from "lucide-react";
import { ReactNode } from "react";
import Button from "./Button";

interface EmptyStateProps {
  message?: string;
  action?: { label: string; onClick: () => void };
  icon?: ReactNode;
}

export default function EmptyState({
  message = "Nothing here yet.",
  action,
  icon,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-16 text-[var(--text-muted)]">
      <div className="opacity-30">{icon || <Leaf size={48} />}</div>
      <p className="text-sm">{message}</p>
      {action && (
        <Button variant="ghost" onClick={action.onClick}>
          {action.label}
        </Button>
      )}
    </div>
  );
}
