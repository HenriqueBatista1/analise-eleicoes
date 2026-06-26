import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

import type { MarketExpectationSeries } from '~/models/marketExpectations';
import { formatDateTime, formatProbability } from '~/utils/format';

type MarketExpectationsChartProps = {
  series: MarketExpectationSeries[];
};

type ChartPoint = {
  probability: number;
  timestamp: string;
  timestampMs: number;
};

const CHART_COLORS = [
  'var(--color-chart-1)',
  'var(--color-chart-2)',
  'var(--color-chart-3)',
  'var(--color-chart-4)',
  'var(--color-chart-5)',
  'var(--color-chart-6)',
];

export default function MarketExpectationsChart({ series }: MarketExpectationsChartProps) {
  const lines = series.map((candidateSeries, index) => ({
    color: CHART_COLORS[index % CHART_COLORS.length],
    data: buildChartPoints(candidateSeries),
    name: candidateSeries.displayName,
  }));

  return (
    <div className="h-72 min-w-0">
      <ResponsiveContainer height="100%" width="100%">
        <LineChart margin={{ bottom: 8, left: 12, right: 16, top: 8 }}>
          <CartesianGrid stroke="var(--color-border)" strokeDasharray="4 4" vertical={false} />

          <XAxis
            dataKey="timestampMs"
            domain={['dataMin', 'dataMax']}
            minTickGap={24}
            scale="time"
            tickFormatter={(value) => formatDateTimeFromTimestamp(Number(value))}
            tickLine={false}
            tickMargin={8}
            type="number"
          />

          <YAxis
            domain={[0, 1]}
            tickFormatter={(value) => formatProbability(Number(value))}
            tickLine={false}
            tickMargin={8}
            width={76}
          />

          <Tooltip
            formatter={(value, name) => [formatProbability(Number(value)), name]}
            labelFormatter={(label) => formatDateTimeFromTimestamp(Number(label))}
          />

          <Legend />

          {lines.map((line) => (
            <Line
              data={line.data}
              dataKey="probability"
              dot={false}
              key={line.name}
              name={line.name}
              stroke={line.color}
              strokeWidth={2}
              type="linear"
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

function buildChartPoints(series: MarketExpectationSeries): ChartPoint[] {
  return series.points.map((point) => ({
    probability: point.probability,
    timestamp: point.timestamp,
    timestampMs: new Date(point.timestamp).getTime(),
  }));
}

function formatDateTimeFromTimestamp(value: number) {
  return formatDateTime(new Date(value).toISOString());
}
