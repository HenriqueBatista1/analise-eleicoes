import CandidateSelector from '~/components/ui/CandidateSelector';
import MetricCard from '~/components/ui/MetricCard';
import ModuleHeader from '~/components/ui/ModuleHeader';
import ModulePanel from '~/components/ui/ModulePanel';
import PlaceholderChart from '~/components/ui/PlaceholderChart';
import SegmentedControl from '~/components/ui/SegmentedControl';
import SourceBadge from '~/components/ui/SourceBadge';
import { candidateOptions, periodOptions } from '~/pages/CurrentElection/modules/filterOptions';

export default function ShareOfSearch() {
  return (
    <ModulePanel>
      <div className="flex h-full flex-col gap-5">
        <ModuleHeader
          actions={<SourceBadge label="Google Trends" />}
          description="Distribuição proporcional da atenção entre candidatos."
          label="Share of Search"
          title="Concentração de buscas"
        />

        <div className="grid gap-3">
          <SegmentedControl label="Período" options={periodOptions} value="7d" />

          <CandidateSelector candidates={candidateOptions} label="Candidatos" value="all" />
        </div>

        <div className="grid gap-3">
          <MetricCard label="Top 2" value="Implementação futura" />

          <MetricCard label="Maior participação" value="Implementação futura" />
        </div>

        <PlaceholderChart
          className="min-h-56"
          imageAlt="Placeholder de gráfico proporcional"
          imageSrc="/chart-placeholders/share-of-search.png"
          label="Placeholder de gráfico proporcional"
          variant="bar"
        />
      </div>
    </ModulePanel>
  );
}
