import { fetcher } from '~/fetchers/fetcher';
import type {
  MarketExpectationFilters,
  MarketExpectationInterval,
  MarketExpectationMetadata,
  MarketExpectationSeries,
  MarketExpectationSummary,
} from '~/models/marketExpectations';

type MarketExpectationFiltersResponse = MarketExpectationFilters;

export function getMarketExpectationFilters() {
  return fetcher<MarketExpectationFiltersResponse>('current-election/market-expectations/filters');
}

type MarketExpectationsResponse = {
  metadata: MarketExpectationMetadata;
  series: MarketExpectationSeries[];
  sources: string[];
  summary: MarketExpectationSummary;
};

export type MarketExpectationsParams = {
  candidateCatalogIds?: number[];
  fromDate?: string;
  interval?: MarketExpectationInterval;
  toDate?: string;
};

export function getMarketExpectations(params?: MarketExpectationsParams) {
  return fetcher<MarketExpectationsResponse>('current-election/market-expectations', {
    queryParams: params,
  });
}
