import { type ButtonHTMLAttributes, type HTMLAttributes, forwardRef } from "react";
import clsx from "clsx";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "ghost";
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", ...props }, ref) => (
    <button
      ref={ref}
      className={clsx(
        "inline-flex items-center justify-center gap-2 rounded-sm px-4 py-2 text-sm font-medium transition-colors disabled:opacity-50 disabled:pointer-events-none",
        variant === "primary" && "bg-forest text-paper hover:bg-forest-deep",
        variant === "secondary" && "border border-line bg-white text-ink hover:border-forest",
        variant === "ghost" && "text-forest hover:bg-forest/10",
        className
      )}
    {...props}
  />
));
Button.displayName = "Button";

export function Card({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div className={clsx("rounded-md border border-line bg-white", className)} {...props} />;
}

export function StatusPill({ status }: { status: "pending" | "processing" | "completed" | "failed" }) {
  const map = {
    pending: { label: "En attente", cls: "bg-line/50 text-ink/70" },
    processing: { label: "En cours", cls: "bg-amber/10 text-amber" },
    completed: { label: "Terminé", cls: "bg-mint/15 text-forest-deep" },
    failed: { label: "Échec", cls: "bg-brick/10 text-brick" },
  } as const;
  const s = map[status];
  return (
    <span className={clsx("inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-mono uppercase tracking-wide", s.cls)}>
      {s.label}
    </span>
  );
}