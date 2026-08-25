export function DimensionDivider({ label }: { label?: string }) {
    return (
      <div className="my-6 flex select-none items-center gap-3">
        <svg width="12" height="12" viewBox="0 0 12 12" className="shrink-0 text-line">
          <line x1="6" y1="0" x2="6" y2="12" stroke="currentColor" strokeWidth="1.5" />
        </svg>
        <div className="h-px flex-1 bg-line" />
        {label && (
          <span className="whitespace-nowrap font-mono text-xs uppercase tracking-wider text-ink/50">{label}</span>
        )}
        <div className="h-px flex-1 bg-line" />
        <svg width="12" height="12" viewBox="0 0 12 12" className="shrink-0 text-line">
          <line x1="6" y1="0" x2="6" y2="12" stroke="currentColor" strokeWidth="1.5" />
        </svg>
      </div>
    );
  }