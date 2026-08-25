import { type ReactNode } from "react";
import { NavLink } from "react-router-dom";
import { FolderOpen, Ruler, Tag } from "lucide-react";
import clsx from "clsx";

const nav = [
    { to: "/", label: "Projets", icon: FolderOpen, end: true },
    { to: "/catalogue", label: "Catalogue de prix", icon: Tag, end: true },
   ];

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <aside className="w-64 shrink-0 border-r border-line bg-blueprint-grid bg-white">
        <div className="flex items-center gap-2 border-b border-line px-6 py-6">
          <Ruler className="h-5 w-5 text-forest" />
          <span className="font-display text-lg font-semibold tracking-tight">BuildSense</span>
        </div>
        <nav className="space-y-1 px-3 py-4">
          {nav.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                clsx(
                  "flex items-center gap-2.5 rounded-sm px-3 py-2 text-sm font-medium",
                  isActive ? "bg-forest text-paper" : "text-ink/70 hover:bg-forest/10 hover:text-ink"
                )
              }
            >
              <Icon className="h-4 w-4" />
              {label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="flex-1 px-10 py-8">{children}</main>
    </div>
  );
}