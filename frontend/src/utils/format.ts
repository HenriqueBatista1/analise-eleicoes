export const EMPTY_VALUE = '—';

export function formatProbability(value?: number | null) {
  if (value === undefined || value === null) {
    return EMPTY_VALUE;
  }

  return value.toLocaleString('pt-BR', {
    maximumFractionDigits: 2,
    minimumFractionDigits: 2,
    style: 'percent',
  });
}
