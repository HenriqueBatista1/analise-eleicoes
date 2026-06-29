import { Outlet } from 'react-router';

export default function AppLayout() {
  return (
    <div className="min-h-screen text-foreground">
      <header className="bg-surface border-line-strong border-b">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-6 py-5 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex items-baseline gap-3">
            <span className="font-extrabold text-2xl tracking-tight">
              <span>VOTO</span>
              <span className="font-black text-accent-2">·</span>
              <span className="text-accent">METRIA</span>
            </span>

            <span className="hidden font-mono text-[11px] text-muted uppercase tracking-wide sm:inline">
              instrumento de leitura eleitoral
            </span>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-6 py-8">
        <Outlet />
      </main>
    </div>
  );
}
