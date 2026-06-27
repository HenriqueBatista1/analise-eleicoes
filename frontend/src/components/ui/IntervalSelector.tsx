import { cn } from '~/utils/cn';

type IntervalSelectorOption = {
  label: string;
  value: string;
};

type IntervalSelectorProps = {
  disabled?: boolean;
  label?: string;
  onChange: (value: string) => void;
  options: IntervalSelectorOption[];
  value: string;
};

export default function IntervalSelector({
  disabled = false,
  label = 'Intervalo',
  onChange,
  options,
  value,
}: IntervalSelectorProps) {
  return (
    <div className="flex w-fit max-w-full flex-col gap-2">
      <span className="font-mono text-[11px] text-muted uppercase tracking-wide">{label}</span>

      <div className="border-line-strong bg-surface inline-flex max-w-full overflow-hidden rounded-md border">
        {options.map((option, index) => {
          const isSelected = option.value === value;

          return (
            <button
              className={cn(
                'rounded px-2.5 py-1.5 text-sm transition-colors whitespace-nowrap',
                isSelected ? 'bg-surface shadow-sm text-foreground' : 'text-muted',
                !disabled && 'cursor-pointer',
                !disabled && !isSelected && 'hover:text-foreground',
                'disabled:cursor-not-allowed disabled:opacity-60',
              )}
              disabled={disabled}
              key={option.value}
              onClick={() => onChange(option.value)}
              type="button"
            >
              {option.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}
