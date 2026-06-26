import { keepPreviousData, useQuery } from '@tanstack/react-query';

import { getMarketExpectations, type MarketExpectationsParams } from '~/fetchers/marketExpectations';
import { marketExpectationKeys } from '~/fetchers/hooks/marketExpectationKeys';

const MARKET_EXPECTATIONS_STALE_TIME = 60 * 60 * 1000;

export function useMarketExpectations(params?: MarketExpectationsParams) {
  return useQuery({
    placeholderData: keepPreviousData,
    queryFn: () => getMarketExpectations(params),
    queryKey: marketExpectationKeys.marketExpectations(params),
    staleTime: MARKET_EXPECTATIONS_STALE_TIME,
  });
}
