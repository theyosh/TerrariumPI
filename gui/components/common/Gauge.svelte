<script>
  import { onMount } from 'svelte';
  import Gauge from 'gaugeJS';

  import { sensors, updateSensor } from '../../stores/terrariumpi';
  import { get_template_color } from '../../helpers/color-helpers';
  import { roundToPrecision } from '../../helpers/number-helpers';
  import { formatBytes } from '../../helpers/file-size-helpers';
  import { getCustomConfig } from '../../config';
  import { isDay } from '../../stores/terrariumpi';

  let settings = getCustomConfig();

  export let id;
  export let type;
  export let value = 0;

  export let alarm_min = 100;
  export let alarm_max = 800;
  export let limit_min = 0;
  export let limit_max = 1000;

  export let warning = false;
  export let error = false;
  export let excluded = false;
  export let minmax = true;

  // Set the initial gauge value
  updateSensor({
    id: id,
    value: value,
    alarm_min: alarm_min,
    alarm_max: alarm_max,
    limit_min: limit_min,
    limit_max: limit_max,
    measure_min: value,
    measure_max: value,
    alarm: warning || alarm_min > value || alarm_max < value,
    error: error,
    excluded: excluded,
  });

  const total_area = limit_max - limit_min;
  const opts = {
    angle: 0,
    lineWidth: 0.6,
    pointer: {
      length: 0.8,
      strokeWidth: 0.07,
      color: '#1D212A',
    },
    limitMax: false,
    limitMin: true,
    strokeColor: '#F0F3F3',
    generateGradient: true,
    highDpiSupport: true,
    percentColors: [
      [0.0, get_template_color('text-danger', false, true)],
      [(alarm_min - limit_min) / total_area, get_template_color('text-warning', false, true)],
      [((alarm_min + alarm_max) / 2 - limit_min) / total_area, get_template_color('text-success', false, true)],
      [(alarm_max - limit_min) / total_area, get_template_color('text-warning', false, true)],
      [1.0, get_template_color('text-danger', false, true)],
    ],
  };

  if (settings.graph_show_min_max_gauge && minmax && $sensors[id]['measure_min'] && $sensors[id]['measure_max']) {
    opts.staticLabels = {
      labels: [$sensors[id]['measure_min'], $sensors[id]['measure_max']],
      font: '10px Helvetica Neue,sans-serif',
      color: $isDay ? '#6c757d' : '#adb5bd',
      fractionDigits: 2,
    };
  }

  let gauge;
  let gauge_value = 'filesize' ? formatBytes(0) : roundToPrecision(0) + ' ' + settings.units[type].value;

  onMount(() => {
    gauge = new Gauge.Gauge(document.getElementById(`gauge_${id}`)).setOptions(opts); // create sexy gauge!
    gauge.maxValue = $sensors[id]['limit_max']; // set max gauge value
    gauge.setMinValue($sensors[id]['limit_min']); // set min value
  });

  // TODO: Not sure if we need to update min and max values in reactive mode... needs rethinking. As when you change this, you will reload the page.... and re-setup
  $: {
    if (gauge && $sensors[id].changed) {
      if (settings.graph_show_min_max_gauge && minmax && $sensors[id].measure_min && $sensors[id].measure_max) {
        gauge.options.staticLabels = {
          labels: [$sensors[id].measure_min, $sensors[id].measure_max],
          font: '10px Helvetica Neue,sans-serif',
          color: $isDay ? '#6c757d' : '#adb5bd',
          fractionDigits: 2,
        };
      }
      gauge.set($sensors[id].value); // set actual value
      gauge_value =
        type === 'filesize' ? formatBytes($sensors[id].value) : roundToPrecision($sensors[id].value) + ' ' + settings.units[type].value;
      $sensors[id].changed = false;
    }
  }
</script>

<canvas id="gauge_{id}" class="gauge"></canvas>
<small class="d-block">{gauge_value}</small>

<style lang="sass">
  canvas
    max-width: 280px
    width: 100%
</style>
