import { useQuery } from '@tanstack/react-query';

import { fetchTrendsRows, type TrendsRow } from '~/services/googleTrends';

const ONE_HOUR = 1000 * 60 * 60;

/** Loads the full Google Trends long table once and caches it. */
export function useGoogleTrends() {
  return useQuery<TrendsRow[]>({
    queryKey: ['google-trends'],
    queryFn: fetchTrendsRows,
    staleTime: ONE_HOUR,
  });
}
