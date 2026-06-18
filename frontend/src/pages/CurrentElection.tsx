import AttentionMarketComparison from '~/pages/CurrentElection/modules/AttentionMarketComparison';
import MarketExpectations from '~/pages/CurrentElection/modules/MarketExpectations';
import PublicAttention from '~/pages/CurrentElection/modules/PublicAttention';
import ShareOfSearch from '~/pages/CurrentElection/modules/ShareOfSearch';

export default function CurrentElection() {
  return (
    <div className="flex flex-col gap-6">
      <section className="flex flex-col gap-3">
        <p className="font-medium text-muted text-sm">Eleição Atual</p>

        <h1 className="font-semibold text-3xl tracking-normal">Dashboard eleitoral comparativo</h1>

        <p className="leading-7 max-w-2xl text-base text-muted">
          Acompanhamento da atenção pública, expectativa de mercado e relação entre os principais indicadores da disputa
          presidencial.
        </p>
      </section>

      <section className="grid gap-5">
        <MarketExpectations />

        <div className="grid gap-5 lg:grid-cols-[minmax(0,2fr)_minmax(280px,1fr)]">
          <PublicAttention />

          <ShareOfSearch />
        </div>

        <AttentionMarketComparison />
      </section>
    </div>
  );
}
