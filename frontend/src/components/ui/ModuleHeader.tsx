import type { ReactNode } from 'react';

type ModuleHeaderProps = {
  actions?: ReactNode;
  description?: string;
  label?: string;
  title: string;
};

export default function ModuleHeader({ actions, description, label, title }: ModuleHeaderProps) {
  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
      <div className="flex flex-col gap-1">
        {label ? <p className="font-medium text-muted text-xs uppercase">{label}</p> : null}

        <div>
          <h2 className="font-semibold text-lg">{title}</h2>

          {description ? <p className="mt-1 text-muted text-sm">{description}</p> : null}
        </div>
      </div>

      {actions ? <div className="flex shrink-0 flex-wrap gap-2">{actions}</div> : null}
    </div>
  );
}
