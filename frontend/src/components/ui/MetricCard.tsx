type MetricCardProps = {
  label: string;
  value: string;
};

export default function MetricCard({ label, value }: MetricCardProps) {
  return (
    <div className="bg-navigation border-border rounded-md border p-4">
      <p className="font-mono text-[10.5px] text-muted uppercase tracking-wider">{label}</p>

      <p className="mt-2 font-mono font-semibold text-foreground text-sm tabular-nums">{value}</p>

      <div
        aria-hidden="true"
        className="mt-3 h-[5px]"
        style={{
          backgroundImage: 'repeating-linear-gradient(90deg, var(--color-line-strong) 0 1px, transparent 1px 12px)',
        }}
      />
    </div>
  );
}
