import CandidateSelector from '~/components/ui/CandidateSelector';
import MetricCard from '~/components/ui/MetricCard';
import ModuleHeader from '~/components/ui/ModuleHeader';
import ModulePanel from '~/components/ui/ModulePanel';
import PlaceholderChart from '~/components/ui/PlaceholderChart';
import SegmentedControl from '~/components/ui/SegmentedControl';
import SourceBadge from '~/components/ui/SourceBadge';
import { candidateOptions, periodOptions } from '~/pages/CurrentElection/modules/filterOptions';

export default function PublicAttention() {
  return (
    <ModulePanel>
      <div className="flex flex-col gap-5">
        <ModuleHeader
          actions={
            <>
              <SourceBadge label="Google Trends" />
              <SourceBadge label="Wikipedia" />
            </>
          }
          description="Interesse público por candidato ao longo do tempo."
          label="Atenção pública"
          title="Interesse por candidato"
        />

        <div className="grid gap-3 lg:grid-cols-2">
          <SegmentedControl label="Período" options={periodOptions} value="7d" />

          <CandidateSelector candidates={candidateOptions} label="Candidatos" value="all" />
        </div>

        <div className="grid gap-3 sm:grid-cols-2">
          <MetricCard label="Maior atenção" value="Implementação futura" />

          <MetricCard label="Maior pico" value="Implementação futura" />
        </div>

        <PlaceholderChart
          imageAlt="Placeholder de gráfico temporal de atenção pública"
          imageSrc="/chart-placeholders/public-attention.png"
          label="Placeholder de gráfico temporal de atenção pública"
        />
      </div>
    </ModulePanel>
  );
}
