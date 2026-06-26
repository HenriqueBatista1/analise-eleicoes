import { useQuery } from '@tanstack/react-query';

import { getMarketExpectationFilters } from '~/fetchers/marketExpectations';
import { marketExpectationKeys } from '~/fetchers/hooks/marketExpectationKeys';

const MARKET_EXPECTATION_FILTERS_STALE_TIME = 60 * 60 * 1000;

export function useMarketExpectationFilters() {
  return useQuery({
    queryFn: getMarketExpectationFilters,
    queryKey: marketExpectationKeys.filters,
    staleTime: MARKET_EXPECTATION_FILTERS_STALE_TIME,
  });
}
