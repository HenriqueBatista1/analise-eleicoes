import AttentionMarketComparison from '~/pages/Dashboard/AttentionMarketComparison/AttentionMarketComparison';
import MarketExpectations from '~/pages/Dashboard/MarketExpectations/MarketExpectations';
import PublicAttention from '~/pages/Dashboard/PublicAttention/PublicAttention';
import ShareOfSearch from '~/pages/Dashboard/ShareOfSearch/ShareOfSearch';

export default function Dashboard() {
  return (
    <section className="grid gap-5">
      <MarketExpectations />

      <PublicAttention />

      <ShareOfSearch />

      <AttentionMarketComparison />
    </section>
  );
}
