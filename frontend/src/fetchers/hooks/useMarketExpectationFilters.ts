import { useQuery } from '@tanstack/react-query';

import { getMarketExpectationFilters } from '~/fetchers/marketExpectations';
import { marketExpectationKeys } from '~/fetchers/hooks/marketExpectationKeys';

export function useMarketExpectationFilters() {
  return useQuery({
    queryFn: getMarketExpectationFilters,
    queryKey: marketExpectationKeys.filters,
  });
}
