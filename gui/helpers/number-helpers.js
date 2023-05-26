import { dayjs } from "svelte-time";
import { get } from 'svelte/store';
import { _ } from 'svelte-i18n';
import duration from "dayjs/esm/plugin/duration";
dayjs.extend(duration);

export const roundToPrecision = (number, precision = 2) => {
  const coefficient = Math.pow(10, precision);
  return Math.round((number + Number.EPSILON) * coefficient) / coefficient;
};

export const average = (numbers) => {
  return numbers.length === 0 ? 0 : numbers.reduce((a, b) => (a + b)) / numbers.length;
};

export const uptime_format = (duration) => {
  duration = duration || 0;
  const dur = dayjs.duration(duration * 1000);
  const $_ = get(_);

  let uptime_text = [];
  for (const [key, value] of Object.entries(dur.$d)) {
    if (['milliseconds'].indexOf(key) !== -1) {
      continue;
    }
    if (value > 0 || uptime_text.length > 0 || 'seconds' === key) {
      uptime_text.push($_(`general.uptime_format.${key}`, { values: { number: Math.round(value) } }));
    }
  }
  return uptime_text.join(', ');
};

/*
    Simple compare. Assumes single-dimension arrays.
*/
export const arrIdentical = (a1, a2) => {
  // Tim Down: http://stackoverflow.com/a/7837725/308645
  if (!Array.isArray(a1) || !Array.isArray(a2)) return false;

  let i = a1.length;
  if (i !== a2.length) return false;

  // Add sorting to the arrays, as order is not an issue
  a1.sort();
  a2.sort();
  while (i--) {
    if (a1[i] !== a2[i]) return false;
  }
  return true;
};