import CandidateSelector from '~/components/ui/CandidateSelector';
import ModuleHeader from '~/components/ui/ModuleHeader';
import ModulePanel from '~/components/ui/ModulePanel';
import PlaceholderChart from '~/components/ui/PlaceholderChart';
import SegmentedControl from '~/components/ui/SegmentedControl';
import SourceBadge from '~/components/ui/SourceBadge';
import { candidateOptions, periodOptions } from '~/pages/CurrentElection/modules/filterOptions';

export default function AttentionMarketComparison() {
  return (
    <ModulePanel>
      <div className="flex flex-col gap-5">
        <ModuleHeader
          actions={
            <>
              <SourceBadge label="Google Trends" />
              <SourceBadge label="Wikipedia" />
              <SourceBadge label="Polymarket" />
            </>
          }
          description="Comparação entre atenção pública e probabilidade de mercado."
          label="Síntese"
          title="Atenção pública x expectativa de mercado"
        />

        <div className="grid gap-3 lg:grid-cols-2">
          <SegmentedControl label="Período" options={periodOptions} value="7d" />

          <CandidateSelector candidates={candidateOptions} label="Candidatos" value="all" />
        </div>

        <PlaceholderChart
          imageAlt="Placeholder de dispersão entre Share of Search e probabilidade de mercado"
          imageSrc="/chart-placeholders/attention-market-comparison.png"
          label="Placeholder de dispersão entre Share of Search e probabilidade de mercado"
          variant="scatter"
        />
      </div>
    </ModulePanel>
  );
}
