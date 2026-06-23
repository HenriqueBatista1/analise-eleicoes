import { keepPreviousData, useQuery } from '@tanstack/react-query';

import { getMarketExpectations, type MarketExpectationsParams } from '~/fetchers/marketExpectations';
import { marketExpectationKeys } from '~/fetchers/hooks/marketExpectationKeys';

export function useMarketExpectations(params?: MarketExpectationsParams) {
  return useQuery({
    placeholderData: keepPreviousData,
    queryFn: () => getMarketExpectations(params),
    queryKey: marketExpectationKeys.marketExpectations(params),
  });
}
