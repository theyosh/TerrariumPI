<script>
  import { onMount } from 'svelte';
  import { Line } from 'svelte-chartjs';
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    TimeScale,
    LinearScale,
    PointElement,
    LineElement,
    Filler,
  } from 'chart.js';
  ChartJS.register(Title, Tooltip, Legend, TimeScale, LinearScale, PointElement, LineElement, Filler);
  import 'chartjs-adapter-dayjs-4';
  import { _ } from 'svelte-i18n';

  import { smoothing, extendGraphData, convertTimestamps } from '../../helpers/graph-helpers';
  import { graphDefaultOpts, graphTypes } from '../../constants/graph';
  import { fetchGraphData } from '../../providers/api';
  import { graphs, updateSensor } from '../../stores/terrariumpi';
  import { getCustomConfig } from '../../config';

  export let id;
  export let type;
  export let mode;

  let settings = getCustomConfig();

  const _dynamicColor = (type, context) => {
    if (!context.raw) {
      return;
    }
    if (context.raw.value < context.raw.alarm_min) {
      return 'border' === type ? graphTypes.alarm_min.colors.line : graphTypes.alarm_min.colors.background;
    }
    if (context.raw.value > context.raw.alarm_max) {
      return 'border' === type ? graphTypes.alarm_max.colors.line : graphTypes.alarm_max.colors.background;
    }
    return 'border' === type ? graphTypes.value.colors.line : graphTypes.value.colors.background;
  };

  const dynamicBackgroundColor = (context) => {
    return _dynamicColor('background', context);
  };

  const dynamicBorderColor = (context) => {
    return _dynamicColor('border', context);
  };

  const updateGraph = (new_data, init) => {
    init = init || false;

    // Inverse the magnetic door data for better graphing
    if (mode === 'buttons' && type === 'magnetic') {
      new_data = new_data.map((item) => {
        item.value = item.value === 1 ? 0 : 1;
        return item;
      });
    }

    if (['relays', 'buttons'].indexOf(mode) !== -1) {
      let period = 1;
      if ($graphs[id].period === 'week') {
        period = 7;
      } else if ($graphs[id].period === 'month') {
        period = 30;
      } else if ($graphs[id].period === 'year') {
        period = 365;
      }

      new_data = extendGraphData(new_data, period);
    }

    if (mode === 'sensors' && settings.graph_smooth_value > 0) {
      new_data = smoothing(new_data, settings.graph_smooth_value);
    }

    if (init) {
      graphData = {
        labels: null,
        datasets: [],
      };

      for (let graphValue in new_data[0]) {
        if (graphValue === 'timestamp' || (graphValue === 'value' && ['sensors', 'buttons'].indexOf(mode) === -1)) {
          continue;
        }

        let dataset = {
          graphType:
            ['sensors', 'buttons'].indexOf(mode) !== -1 ? type : graphValue === 'flow' ? 'water_flow' : graphValue, // TODO: Make the flow field to water_flow field in the API
          label: $_(graphTypes[mode === 'buttons' ? type : graphValue].label),
          tension: mode === 'sensors' ? 0.4 : 0,
          data: new_data,
          parsing: {
            xAxisKey: 'timestamp',
            yAxisKey: graphValue,
          },
          yAxisID: 'y',
          fill: mode !== 'sensors',
          stepped: mode !== 'sensors',
          borderColor: graphTypes[mode === 'buttons' ? type : graphValue].colors.line,
          backgroundColor: graphTypes[mode === 'buttons' ? type : graphValue].colors.background,
        };

        if (graphValue === 'flow') {
          dataset.yAxisID = 'y2';
        }
        graphData.datasets.push(dataset);

        if (graphValue === 'value') {
          graphData.datasets[graphData.datasets.length - 1].pointRadius = 1;

          graphData.datasets[graphData.datasets.length - 1].pointBorderColor = dynamicBorderColor;
          graphData.datasets[graphData.datasets.length - 1].pointBackgroundColor = dynamicBackgroundColor;
        }
      }
    } else {
      graphOpts.animation = { duration: 0 };
      for (let counter = 0; counter < graphData.datasets.length; counter++) {
        graphData.datasets[counter].data = new_data;
      }
      graphData.labels = new_data.map((point) => {
        return point.timestamp;
      });
    }

    if (mode === 'sensors') {
      if (settings.graph_limit_min_max) {
        let last = new_data.length - 1;
        graphOpts.scales.y.min =
          new_data[last].alarm_min - Math.abs(new_data[last].alarm_min === 0 ? 20 : new_data[last].alarm_min * 0.2);
        graphOpts.scales.y.max =
          new_data[last].alarm_max + Math.abs(new_data[last].alarm_max === 0 ? 20 : new_data[last].alarm_max * 0.2);
        graphOpts.scales.y.ticks.includeBounds = false;
      }
      if (settings.show_min_max_gauge) {
        let values = new_data.map((point) => {
          return point.value;
        });
        updateSensor({
          id: id,
          measure_min: Math.min(...values),
          measure_max: Math.max(...values),
        });
      }
    }

    if ($graphs[id].period === 'day') {
      graphOpts.scales.x.time.unit = 'minute';
      graphOpts.scales.x.time.displayFormats.minute = 'LT';
    } else if ($graphs[id].period === 'week') {
      graphOpts.scales.x.time.unit = 'hour';
      graphOpts.scales.x.time.displayFormats.hour = 'dd LT';
    } else if ($graphs[id].period === 'month') {
      graphOpts.scales.x.time.unit = 'hour';
      graphOpts.scales.x.time.displayFormats.hour = 'D/M LT';
    } else if ($graphs[id].period === 'year') {
      graphOpts.scales.x.time.unit = 'day';
      graphOpts.scales.x.time.displayFormats.day = 'D/M LT';
    }
  };

  // Init graph through store
  $graphs[id] = {
    period: 'day',
    changed: true, // This will trigger the initial loading when the page loads :)
  };

  // Make a clone of the general graph settings ??? Not really working :(
  let graphOpts = { ...graphDefaultOpts };
  graphOpts.scales.y2.display = ['relays'].indexOf(mode) !== -1;
  graphOpts.scales.y.ticks.stepSize = ['buttons'].indexOf(mode) !== -1 ? 1 : null;
  graphOpts.scales.y.min = ['buttons', 'relays'].indexOf(mode) !== -1 ? 0 : null;
  graphOpts.scales.y2.min = ['relays'].indexOf(mode) !== -1 ? 0 : null;

  let graphData;
  let loading = true;
  let nodata = false;

  onMount(() => {
    // Start the graph updater once every 1 minute
    const interval = setInterval(async () => {
      if (!loading) {
        let new_data;
        await fetchGraphData(mode, id, $graphs[id].period, (data) => (new_data = convertTimestamps(data)));
        nodata = new_data.length === 0;

        if (!nodata) {
          updateGraph(new_data, false);
        }
      }
    }, 60 * 1000);

    return () => {
      clearInterval(interval);
    };
  });

  $: {
    if ($graphs[id].changed) {
      (async () => {
        $graphs[id].changed = false;
        loading = true;
        let new_data;
        await fetchGraphData(mode, id, $graphs[id].period, (data) => (new_data = convertTimestamps(data)));
        nodata = new_data.length === 0;

        if (!nodata) {
          updateGraph(new_data, true);
        }

        loading = false;
      })();
    }
  }
</script>

<div class="d-block w-100 h-100 text-center" style="min-height:150px">
  {#if loading}
    <br />
    <i class="fas fa-2x fa-sync-alt fa-spin mt-5"></i>
  {:else if nodata}
    <h1 class="mt-5">{$_('graph.no-data')}</h1>
  {:else}
    <Line data="{graphData}" options="{graphOpts}" />
  {/if}
</div>
