import { useState } from 'react';

import {
  IntervalSelector,
  MetricCard,
  ModuleHeader,
  ModulePanel,
  MultiSelect,
  PlaceholderChart,
  SourceBadge,
} from '~/components/ui';
import { useMarketExpectationFilters } from '~/fetchers/hooks/useMarketExpectationFilters';
import { useMarketExpectations } from '~/fetchers/hooks/useMarketExpectations';
import type { MarketExpectationInterval } from '~/models/marketExpectations';
import { EMPTY_VALUE, formatProbability } from '~/utils/format';

const DEFAULT_INTERVALS: MarketExpectationInterval[] = ['1h', '4h', '1d', '1w'];

const INTERVAL_LABELS: Partial<Record<MarketExpectationInterval, string>> = {
  '1w': '1 sem.',
};

export default function MarketExpectations() {
  const [selectedCandidates, setSelectedCandidates] = useState<string[]>([]);
  const [selectedInterval, setSelectedInterval] = useState<MarketExpectationInterval>('1h');

  const filtersQuery = useMarketExpectationFilters();

  const selectedCandidateCatalogIds = selectedCandidates.map(Number);
  const marketExpectationsQuery = useMarketExpectations({
    candidateCatalogIds: selectedCandidateCatalogIds.length > 0 ? selectedCandidateCatalogIds : undefined,
    interval: selectedInterval,
  });

  const isFiltersLoading = filtersQuery.isLoading;
  const isSeriesLoading = marketExpectationsQuery.isLoading;
  const hasError = filtersQuery.isError || marketExpectationsQuery.isError;
  const isLoading = isFiltersLoading || isSeriesLoading;
  const hasSeries = (marketExpectationsQuery.data?.series.length ?? 0) > 0;

  const candidateOptions =
    filtersQuery.data?.candidates.map((candidate) => ({
      label: candidate.displayName,
      value: String(candidate.candidateCatalogId),
    })) ?? [];

  const intervals = filtersQuery.data?.intervals ?? DEFAULT_INTERVALS;
  const intervalOptions = intervals.map((interval) => ({
    label: INTERVAL_LABELS[interval] ?? interval,
    value: interval,
  }));

  const summary = marketExpectationsQuery.data?.summary;
  const currentLeaderValue = summary?.currentLeader
    ? `${summary.currentLeader.displayName} (${formatProbability(summary.currentLeader.probability)})`
    : EMPTY_VALUE;
  const leaderMarginValue = formatProbability(summary?.leaderMargin?.value);
  const largestChangeValue = formatProbability(summary?.largestChange?.value);

  const chartFeedback = hasError
    ? 'Não foi possível carregar os dados de expectativa de mercado.'
    : isLoading
      ? 'Carregando dados de expectativa de mercado...'
      : hasSeries
        ? null
        : 'Nenhum dado encontrado para os filtros selecionados.';

  return (
    <ModulePanel>
      <div className="flex flex-col gap-5">
        <ModuleHeader badges={<SourceBadge label="Polymarket" />} title="Expectativa de mercado" />

        <div className="flex flex-wrap gap-3">
          <IntervalSelector
            disabled={isFiltersLoading || hasError}
            onChange={(value) => setSelectedInterval(value as MarketExpectationInterval)}
            options={intervalOptions}
            value={selectedInterval}
          />

          <MultiSelect
            disabled={hasError}
            label="Candidatos"
            loading={isFiltersLoading}
            onChange={setSelectedCandidates}
            options={candidateOptions}
            value={selectedCandidates}
          />
        </div>

        <div className="flex flex-col gap-5 lg:flex-col-reverse">
          {chartFeedback ? (
            <div className="bg-navigation grid min-h-72 place-items-center rounded-md px-4 py-8 text-muted text-sm">
              {chartFeedback}
            </div>
          ) : (
            <PlaceholderChart
              imageAlt="Placeholder de gráfico temporal das probabilidades"
              imageSrc="/chart-placeholders/market-expectations.png"
              label="Placeholder de gráfico temporal das probabilidades"
              variant="line"
            />
          )}

          <div className="gap-3 grid md:grid-cols-4">
            <MetricCard label="Líder atual" value={currentLeaderValue} />

            <MetricCard label="Margem" value={leaderMarginValue} />

            <MetricCard label="Maior variação" value={largestChangeValue} />

            <MetricCard label="Evento recente" value="Implementação futura" />
          </div>
        </div>
      </div>
    </ModulePanel>
  );
}
