import type { ReactNode } from 'react';

type ModuleHeaderProps = {
  badges?: ReactNode;
  description?: string;
  eyebrow?: string;
  title: string;
};

export default function ModuleHeader({ badges, description, eyebrow, title }: ModuleHeaderProps) {
  return (
    <div className="border-border flex flex-col gap-3 border-b pb-4 sm:flex-row sm:items-start sm:justify-between">
      <div className="flex flex-col gap-1">
        {eyebrow ? (
          <span className="font-mono text-[11px] text-muted uppercase tracking-[0.12em]">{eyebrow}</span>
        ) : null}

        <h2 className="font-semibold text-lg tracking-tight">{title}</h2>

        {description ? <p className="max-w-[60ch] text-muted text-sm">{description}</p> : null}
      </div>

      {badges ? <div className="flex shrink-0 flex-wrap gap-2">{badges}</div> : null}
    </div>
  );
}
