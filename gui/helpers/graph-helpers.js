import {graphs} from "../stores/terrariumpi"
import {get} from 'svelte/store'
import {fetchExportData} from "../providers/api"


// https://stackoverflow.com/a/63348486
export const smoothing = (array, countBefore, countAfter) => {
  countAfter = countAfter || 0

  const result = [];
  for (let i = 0; i < array.length; i++) {
    const subArr = array.slice(Math.max(i - countBefore, 0), Math.min(i + countAfter + 1, array.length));
    const avg = subArr.reduce((a, b) => a + (isNaN(b) ? 0 : b), 0) / subArr.length;
    result.push(avg);
  }
  return result;
}

export const toggleGraphPeriod = (graph, period) => {
  period = period || 'day'

  const store = get(graphs)
  store[graph].period = period
  store[graph].changed = true
  graphs.set(store)
}

export const exportGraphPeriod = async (type, graph) => {
  const store = get(graphs)
  const filename = `terrariumpi_export_${type}_${graph}_${store[graph].period}.csv`

  let export_data = ''
  await fetchExportData(type, graph, store[graph].period, data => export_data = data)

  const link = document.createElement('a')
  link.href = window.URL.createObjectURL(new Blob([export_data]))
  link.download = filename
  link.click()
}