import {
  Brush,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

import type { ElectionEvent } from '~/data/electionEvents';
import type { MarketExpectationInterval, MarketExpectationSeries } from '~/models/marketExpectations';
import { EVENT_FLAG_COLOR, EVENT_LINE_COLOR } from '~/utils/events';
import { formatDateTime, formatProbability } from '~/utils/format';

type MarketExpectationsChartProps = {
  events: ElectionEvent[];
  interval: MarketExpectationInterval;
  series: MarketExpectationSeries[];
};

type ChartRow = {
  timestampMs: number;
} & Record<string, number | string>;

const CHART_COLORS = [
  'var(--color-chart-1)',
  'var(--color-chart-2)',
  'var(--color-chart-3)',
  'var(--color-chart-4)',
  'var(--color-chart-5)',
  'var(--color-chart-6)',
];

export default function MarketExpectationsChart({ events, interval, series }: MarketExpectationsChartProps) {
  const lines = series.map((candidateSeries, index) => ({
    color: CHART_COLORS[index % CHART_COLORS.length],
    key: getSeriesKey(candidateSeries),
    name: candidateSeries.displayName,
  }));
  const data = buildChartData(series, interval);
  const eventMarkers = getEventsInDataRange(events, data);

  return (
    <div className="h-72 min-w-0 sm:h-96">
      <ResponsiveContainer height="100%" width="100%">
        <LineChart data={data} margin={{ bottom: 20, left: 0, right: 8, top: 8 }}>
          <CartesianGrid stroke="var(--color-border)" strokeDasharray="4 4" vertical={false} />

          <XAxis
            dataKey="timestampMs"
            domain={['dataMin', 'dataMax']}
            minTickGap={12}
            scale="time"
            tick={{ fontSize: 10 }}
            tickFormatter={(value) => formatCompactDateTimeFromTimestamp(Number(value))}
            tickLine={false}
            tickMargin={6}
            type="number"
          />

          <YAxis
            domain={['auto', 'auto']}
            tick={{ fontSize: 10 }}
            tickFormatter={(value) => formatProbability(Number(value))}
            tickLine={false}
            tickMargin={4}
            width={52}
          />

          <Tooltip
            formatter={(value, name) => [formatProbability(Number(value)), name]}
            labelFormatter={(label) => formatDateTimeFromTimestamp(Number(label))}
            wrapperStyle={{ zIndex: 50 }}
          />

          <Legend iconSize={8} wrapperStyle={{ fontSize: 12, lineHeight: '16px' }} />

          {eventMarkers.map((event) => (
            <ReferenceLine
              key={`${event.date}-${event.title}`}
              label={{ fill: EVENT_FLAG_COLOR, fontSize: 10, position: 'top', value: '▾' }}
              stroke={EVENT_LINE_COLOR}
              strokeDasharray="3 4"
              x={Date.parse(event.date)}
            />
          ))}

          {lines.map((line) => (
            <Line
              dataKey={line.key}
              dot={false}
              key={line.name}
              name={line.name}
              stroke={line.color}
              strokeWidth={2}
              type="linear"
            />
          ))}

          <Brush
            dataKey="timestampMs"
            height={24}
            tickFormatter={(value) => formatCompactDateTimeFromTimestamp(Number(value))}
            travellerWidth={5}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

function buildChartData(series: MarketExpectationSeries[], interval: MarketExpectationInterval) {
  const rowsByTimestamp = new Map<number, ChartRow>();

  series.forEach((candidateSeries) => {
    const seriesKey = getSeriesKey(candidateSeries);

    candidateSeries.points.forEach((point) => {
      const timestampMs = getBucketTimestamp(point.timestamp, interval);
      const row = rowsByTimestamp.get(timestampMs) ?? { timestampMs };
      row[seriesKey] = point.probability;
      rowsByTimestamp.set(timestampMs, row);
    });
  });

  return Array.from(rowsByTimestamp.values()).toSorted(
    (firstRow, secondRow) => firstRow.timestampMs - secondRow.timestampMs,
  );
}

function getEventsInDataRange(events: ElectionEvent[], data: ChartRow[]) {
  const firstTimestamp = data[0]?.timestampMs;
  const lastTimestamp = data.at(-1)?.timestampMs;

  if (firstTimestamp == null || lastTimestamp == null) {
    return [];
  }

  return events.filter((event) => {
    const timestamp = Date.parse(event.date);

    return timestamp >= firstTimestamp && timestamp <= lastTimestamp;
  });
}

function formatDateTimeFromTimestamp(value: number) {
  return formatDateTime(new Date(value).toISOString());
}

function formatCompactDateTimeFromTimestamp(value: number) {
  const date = new Date(value);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');

  return `${day}/${month}`;
}

function getBucketTimestamp(value: string, interval: MarketExpectationInterval) {
  const date = new Date(value);

  if (interval === '1w') {
    const weekDay = date.getDay();
    const daysFromMonday = (weekDay + 6) % 7;
    date.setDate(date.getDate() - daysFromMonday);
    date.setHours(0, 0, 0, 0);

    return date.getTime();
  }

  if (interval === '1d') {
    date.setHours(0, 0, 0, 0);

    return date.getTime();
  }

  if (interval === '4h') {
    date.setHours(Math.floor(date.getHours() / 4) * 4, 0, 0, 0);

    return date.getTime();
  }

  date.setMinutes(0, 0, 0);

  return date.getTime();
}

function getSeriesKey(series: MarketExpectationSeries) {
  return `${series.candidateCatalogId}:${series.marketId}`;
}
