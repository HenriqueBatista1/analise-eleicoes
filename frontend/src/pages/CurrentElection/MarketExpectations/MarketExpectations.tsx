import { useState } from 'react';

import {
  MetricCard,
  ModuleHeader,
  ModulePanel,
  MultiSelect,
  PlaceholderChart,
  SegmentedControl,
  SourceBadge,
} from '~/components/ui';

const mockCandidateOptions = [
  { label: 'Candidato A', value: 'candidate-a' },
  { label: 'Candidato B', value: 'candidate-b' },
  { label: 'Candidato C', value: 'candidate-c' },
  { label: 'Candidato D', value: 'candidate-d' },
];

const mockIntervalOptions = [
  { label: '1h', value: '1h' },
  { label: '4h', value: '4h' },
  { label: '1d', value: '1d' },
  { label: '1 sem.', value: '1w' },
];

export default function MarketExpectations() {
  const [selectedCandidates, setSelectedCandidates] = useState<string[]>([]);

  return (
    <ModulePanel>
      <div className="flex flex-col gap-5">
        <ModuleHeader badges={<SourceBadge label="Polymarket" />} title="Expectativa de mercado" />

        <div className="flex flex-wrap gap-3">
          <SegmentedControl label="Intervalo" options={mockIntervalOptions} value="1h" />

          <MultiSelect
            label="Candidatos"
            onChange={setSelectedCandidates}
            options={mockCandidateOptions}
            value={selectedCandidates}
          />
        </div>

        <div className="flex flex-col gap-5 lg:flex-col-reverse">
          <PlaceholderChart
            imageAlt="Placeholder de gráfico temporal das probabilidades"
            imageSrc="/chart-placeholders/market-expectations.png"
            label="Placeholder de gráfico temporal das probabilidades"
            variant="line"
          />

          <div className="gap-3 grid md:grid-cols-4">
            <MetricCard label="Líder atual" value="Implementação futura" />

            <MetricCard label="Margem" value="Implementação futura" />

            <MetricCard label="Maior variação" value="Implementação futura" />

            <MetricCard label="Evento recente" value="Implementação futura" />
          </div>
        </div>
      </div>
    </ModulePanel>
  );
}
