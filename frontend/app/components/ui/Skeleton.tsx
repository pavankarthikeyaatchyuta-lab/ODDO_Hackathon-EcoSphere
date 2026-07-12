import clsx from "clsx";

interface SkeletonProps {
  className?: string;
  count?: number;
}

export function SkeletonLine({ className }: { className?: string }) {
  return (
    <div className={clsx("animate-pulse rounded bg-white/5 h-4", className)} />
  );
}

export default function Skeleton({ className, count = 3 }: SkeletonProps) {
  return (
    <div className={clsx("space-y-3", className)}>
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="glass-card p-4 space-y-2">
          <SkeletonLine className="w-1/3" />
          <SkeletonLine className="w-2/3" />
          <SkeletonLine className="w-1/2" />
        </div>
      ))}
    </div>
  );
}
