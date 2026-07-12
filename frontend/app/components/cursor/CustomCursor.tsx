"use client";
import { useEffect, useRef } from "react";

export default function CustomCursor() {
  const dotRef = useRef<HTMLDivElement>(null);
  const ringRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Don't show on touch-only devices
    if (!window.matchMedia("(pointer: fine)").matches) return;

    const dot = dotRef.current;
    const ring = ringRef.current;
    if (!dot || !ring) return;

    let mouseX = 0, mouseY = 0;
    let ringX = 0, ringY = 0;

    const move = (e: MouseEvent) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      dot.style.transform = `translate(${mouseX - 4}px, ${mouseY - 4}px)`;
    };

    const hover = (e: MouseEvent) => {
      const el = e.target as HTMLElement;
      const isInteractive = el.closest("button, a, [role='button'], input, select, textarea");
      ring.style.width = isInteractive ? "40px" : "24px";
      ring.style.height = isInteractive ? "40px" : "24px";
      ring.style.opacity = isInteractive ? "0.8" : "0.5";
    };

    window.addEventListener("mousemove", move);
    window.addEventListener("mouseover", hover);

    let frame: number;
    const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

    const animate = () => {
      ringX = lerp(ringX, mouseX, 0.12);
      ringY = lerp(ringY, mouseY, 0.12);
      ring.style.transform = `translate(${ringX - 12}px, ${ringY - 12}px)`;
      frame = requestAnimationFrame(animate);
    };
    animate();

    return () => {
      window.removeEventListener("mousemove", move);
      window.removeEventListener("mouseover", hover);
      cancelAnimationFrame(frame);
    };
  }, []);

  return (
    <>
      <div
        ref={dotRef}
        className="fixed top-0 left-0 w-2 h-2 rounded-full bg-teal pointer-events-none z-[9999] transition-none"
        style={{ backgroundColor: "var(--accent-teal)" }}
      />
      <div
        ref={ringRef}
        className="fixed top-0 left-0 w-6 h-6 rounded-full border pointer-events-none z-[9998] transition-all duration-200"
        style={{
          borderColor: "var(--accent-teal)",
          opacity: 0.5,
        }}
      />
    </>
  );
}
