"use client";
import { useEffect, useRef } from "react";

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  opacity: number;
  type: "leaf" | "firefly";
  angle: number;
  angleSpeed: number;
  glowPhase: number;
}

export default function NatureBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d")!;
    let animationId: number;
    let particles: Particle[] = [];
    const mouse = { x: 0, y: 0 };

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener("resize", resize);
    window.addEventListener("mousemove", (e) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    });

    const init = () => {
      particles = [];
      for (let i = 0; i < 50; i++) {
        particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          vx: (Math.random() - 0.5) * 0.4,
          vy: Math.random() * 0.5 + 0.2,
          size: Math.random() * 6 + 3,
          opacity: Math.random() * 0.5 + 0.2,
          type: i < 35 ? "leaf" : "firefly",
          angle: Math.random() * Math.PI * 2,
          angleSpeed: (Math.random() - 0.5) * 0.02,
          glowPhase: Math.random() * Math.PI * 2,
        });
      }
    };
    init();

    const drawLeaf = (ctx: CanvasRenderingContext2D, p: Particle) => {
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(p.angle);
      ctx.globalAlpha = p.opacity;
      ctx.fillStyle = `hsl(${130 + Math.random() * 40}, 60%, 35%)`;
      ctx.beginPath();
      ctx.ellipse(0, 0, p.size, p.size * 0.5, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    };

    const drawFirefly = (ctx: CanvasRenderingContext2D, p: Particle) => {
      const glow = (Math.sin(p.glowPhase) + 1) / 2;
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.globalAlpha = 0.3 + glow * 0.5;
      const gradient = ctx.createRadialGradient(0, 0, 0, 0, 0, p.size * 3);
      gradient.addColorStop(0, "#d4a017");
      gradient.addColorStop(1, "transparent");
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(0, 0, p.size * 3, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    };

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Gradient forest background
      const bg = ctx.createLinearGradient(0, 0, 0, canvas.height);
      bg.addColorStop(0, "#0b1410");
      bg.addColorStop(0.6, "#0f1f18");
      bg.addColorStop(1, "#162b20");
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Subtle canopy glow at top
      const canopy = ctx.createRadialGradient(
        canvas.width / 2, -50, 0,
        canvas.width / 2, -50, canvas.width * 0.7
      );
      canopy.addColorStop(0, "rgba(74, 124, 89, 0.08)");
      canopy.addColorStop(1, "transparent");
      ctx.fillStyle = canopy;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      particles.forEach((p) => {
        p.angle += p.angleSpeed;
        p.glowPhase += 0.03;

        if (p.type === "leaf") {
          p.x += p.vx + Math.sin(p.angle) * 0.3;
          p.y += p.vy;
          drawLeaf(ctx, p);
          if (p.y > canvas.height + 20) {
            p.y = -20;
            p.x = Math.random() * canvas.width;
          }
        } else {
          p.x += Math.sin(p.glowPhase * 0.5) * 0.8;
          p.y += Math.cos(p.glowPhase * 0.3) * 0.5;
          drawFirefly(ctx, p);
          if (p.x < 0) p.x = canvas.width;
          if (p.x > canvas.width) p.x = 0;
          if (p.y < 0) p.y = canvas.height;
          if (p.y > canvas.height) p.y = 0;
        }
      });

      animationId = requestAnimationFrame(animate);
    };

    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!prefersReducedMotion) {
      animate();
    } else {
      // Just paint background, no animation
      const bg = ctx.createLinearGradient(0, 0, 0, canvas.height);
      bg.addColorStop(0, "#0b1410");
      bg.addColorStop(1, "#162b20");
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener("resize", resize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 -z-10 pointer-events-none"
      aria-hidden
    />
  );
}
