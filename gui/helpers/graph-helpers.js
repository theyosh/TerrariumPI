import { graphs } from '../stores/terrariumpi';
import { get } from 'svelte/store';
import { fetchExportData } from '../providers/api';

// https://stackoverflow.com/a/63348486
export const smoothing = (data, smoothingValue) => {
  if (smoothingValue == 0) {
    return data;
  }

  const countBefore = Math.round(smoothingValue/2);
  const countAfter = smoothingValue - countBefore;
  const new_data = [];

  for (let i = 0; i < data.length; i++) {

    const range = data.slice(Math.max(i - countBefore, 0), Math.min(i + countAfter + 1, data.length));
    const new_data_point = structuredClone(data[i]);

    new_data_point.value = range.reduce((a, b) => a.value + (isNaN(b) ? a.value : b.value), 0) / range.length;
    new_data.push(new_data_point);

  }

  return new_data;
};

export const toggleGraphPeriod = (graph, period) => {
  period = period || 'day';

  const store = get(graphs);
  store[graph].period = period;
  store[graph].changed = true;
  graphs.set(store);
};

export const convertTimestamps = (data) => {
    return data.map((point) => {
        point.timestamp *= 1000;
        return point;
      });
}


export const extendGraphData = (data) => {
    let now = new Date();

    let end = structuredClone(data[data.length-1]);
    end.timestamp = Math.round(now.getTime() / 1000);

    now.setDate(now.getDate() - 1);
    let start = structuredClone(data[0]);
    start.timestamp = Math.round(now.getTime() / 1000);

    return [end,...data,start]
}

export const exportGraphPeriod = async (type, graph) => {
  const store = get(graphs);
  const filename = `terrariumpi_export_${type}_${graph}_${store[graph].period}.csv`;

  let export_data = '';
  await fetchExportData(type, graph, store[graph].period, (data) => (export_data = data));

  const link = document.createElement('a');
  link.href = window.URL.createObjectURL(new Blob([export_data]));
  link.download = filename;
  link.click();
};
