import type { MarketExpectationsParams } from '~/fetchers/marketExpectations';

export const marketExpectationKeys = {
  filters: ['market-expectations', 'filters'] as const,
  marketExpectations: (params?: MarketExpectationsParams) => ['market-expectations', params] as const,
};
