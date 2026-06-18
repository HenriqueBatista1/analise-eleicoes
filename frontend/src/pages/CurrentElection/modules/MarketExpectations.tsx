import CandidateSelector from '~/components/ui/CandidateSelector';
import MetricCard from '~/components/ui/MetricCard';
import ModuleHeader from '~/components/ui/ModuleHeader';
import ModulePanel from '~/components/ui/ModulePanel';
import PlaceholderChart from '~/components/ui/PlaceholderChart';
import SegmentedControl from '~/components/ui/SegmentedControl';
import SourceBadge from '~/components/ui/SourceBadge';
import { candidateOptions, intervalOptions, periodOptions } from '~/pages/CurrentElection/modules/filterOptions';

export default function MarketExpectations() {
  return (
    <ModulePanel>
      <div className="flex flex-col gap-5">
        <ModuleHeader
          actions={<SourceBadge label="Polymarket" />}
          description="Evolução da probabilidade de vitória por candidato na eleição atual."
          label="Expectativa de mercado"
          title="Probabilidades de vitória"
        />

        <div className="grid gap-3 lg:grid-cols-3">
          <SegmentedControl label="Período" options={periodOptions} value="7d" />

          <SegmentedControl label="Intervalo" options={intervalOptions} value="1h" />

          <CandidateSelector candidates={candidateOptions} label="Candidatos" value="all" />
        </div>

        <div className="grid gap-3 md:grid-cols-4">
          <MetricCard label="Líder atual" value="Implementação futura" />

          <MetricCard label="Margem" value="Implementação futura" />

          <MetricCard label="Maior variação" value="Implementação futura" />

          <MetricCard label="Evento recente" value="Implementação futura" />
        </div>

        <PlaceholderChart
          imageAlt="Placeholder de gráfico temporal das probabilidades"
          imageSrc="/chart-placeholders/market-expectations.png"
          label="Placeholder de gráfico temporal das probabilidades"
          variant="line"
        />
      </div>
    </ModulePanel>
  );
}
