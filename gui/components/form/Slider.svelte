<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import Slider from 'bootstrap-slider';

  import FormGroup from './FormGroup.svelte';
  import { getRandomString } from '../../helpers/string-helpers';

  export let name;
  export let id = name + getRandomString(6); // Create a unique ID
  export let label = null;

  export let value = null;

  export let required = null;
  export let readonly = false;
  export let help = null;
  export let invalid = null;

  export let min = 0;
  export let max = 100;
  export let step = 1;

  export let horizontal = null;

  export let formatter = (value) => {
   return value;
  };

  let slider;

  let old_data;

  const dispatch = createEventDispatcher();

  function changeAction() {
    dispatch('change');
  }

  onMount(() => {
    slider = new Slider(slider, {
      value: value,
      range: Array.isArray(value),
      enabled: true,
      formatter: formatter,
    });

    slider.on('change', (data) => {
      if (old_data !== data) {
        old_data === data;
        changeAction();
      }
    });
    slider.setValue(value);
    return () => {
      slider.destroy();
      slider = null;
    };
  });

  $: if (slider) {
      if (Array.isArray(value) && value.length === 1) {
        value.push(0);
      }
      try {
        slider.setValue(value);
      } catch (e) {
        // Just ignore
      }
  }
</script>

<FormGroup
  id="{id}"
  label="{label}"
  required="{required}"
  help="{help}"
  invalid="{invalid}"
  horizontal="{horizontal}"
  class="{$$props.class || ''}">
  <input
    type="text"
    class="form-control range_slider"
    id="{id}"
    name="{name}"
    data-value="{Array.isArray(value) ? `[${value[0]},${value[1]}]` : value}"
    required="{required}"
    readonly="{readonly}"
    data-slider-min="{min}"
    data-slider-max="{max}"
    data-slider-step="{step}"
    bind:this="{slider}" />
</FormGroup>

<style>
  @import '../../../node_modules/bootstrap-slider/dist/css/bootstrap-slider.min.css';
</style>
