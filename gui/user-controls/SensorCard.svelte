<script>
  import { getContext } from 'svelte';
  import { _, date, time } from 'svelte-i18n';

  import { template_sensor_type_icon } from '../helpers/icon-helpers';
  import { exportGraphPeriod } from '../helpers/graph-helpers';
  import { sensors } from '../stores/terrariumpi';

  import Card from '../user-controls/Card.svelte';
  import Gauge from '../components/common/Gauge.svelte';
  import Graph from '../components/common/Graph.svelte';
  import CardSettingsTools from '../components/common/CardSettingsTools.svelte';
  import CardGraphPeriodTools from '../components/common/CardGraphPeriodTools.svelte';

  export let enableGraph = true;
  export let enableSettings = true;
  export let removeParent = false;
  export let sensor;

  const { editSensor } = getContext('modals');
  const { deleteAction, ignoreAction } = getContext('sensorActions');

  let exporting = false;
  const exportAction = async () => {
    exporting = true;
    await exportGraphPeriod('sensors', sensor.id);
    exporting = false;
  };

  $sensors[sensor.id] = sensor;
</script>

{#if sensor}
  <Card loading="{false}" noPadding="{true}" removeParent="{removeParent}" class="{sensor.id} {$$props.class || ''}">
    <svelte:fragment slot="header">
      <i class="fas {template_sensor_type_icon(sensor.type)} mr-2"></i>{sensor.name}
      {#if $sensors[sensor.id]}
        {#if $sensors[sensor.id].excluded}
          <small class="badge badge-primary">{$_('general.exclude.average', { default: 'Exlc. avg.' })}</small>
        {/if}
        {#if $sensors[sensor.id].error}
          <small class="badge badge-danger">{$_('gauge.error', { default: 'Error' })}</small>
        {/if}
        {#if $sensors[sensor.id].alarm}
          <small class="badge badge-warning">{$_('gauge.warning', { default: 'Warning' })}</small>
        {/if}
        <small class="text-muted" class:ml-2="{!$sensors[sensor.id].excluded && !$sensors[sensor.id].error && !$sensors[sensor.id].alarm}"
          >{$_('gauge.last_update', { default: 'Last update' })}: {$date($sensors[sensor.id].last_update, {
            format: enableGraph ? 'long' : 'medium',
          }) +
            ' ' +
            $time($sensors[sensor.id].last_update, { format: 'short' })}</small>
      {/if}
    </svelte:fragment>

    <svelte:fragment slot="tools">
      {#if enableGraph}
        <CardGraphPeriodTools id="{sensor.id}" />
      {/if}

      <CardSettingsTools>
        <button class="dropdown-item" title="{$_('sensors.actions.export', { default: 'Export sensor' })}" on:click="{exportAction}">
          <i class="fas mr-2" class:fa-file-export="{!exporting}" class:fa-spinner="{exporting}" class:fa-spin="{exporting}"></i>{$_(
            'sensors.actions.export',
            { default: 'Export sensor' }
          )}
        </button>

        {#if enableSettings}
          <button
            class="dropdown-item"
            title="{$_('sensors.actions.ignore', { default: 'Ignore sensor' })}"
            on:click="{() => ignoreAction(sensor)}">
            <i class="fas fa-ban mr-2"></i>{$_('sensors.actions.ignore', { default: 'Ignore sensor' })}
          </button>

          <button
            class="dropdown-item"
            title="{$_('sensors.actions.settings', { default: 'Edit sensor' })}"
            on:click="{() => editSensor(sensor)}">
            <i class="fas fa-wrench mr-2"></i>{$_('sensors.actions.settings', { default: 'Edit sensor' })}
          </button>

          <button
            class="dropdown-item text-danger"
            title="{$_('sensors.actions.delete', { default: 'Delete sensor' })}"
            on:click="{() => deleteAction(sensor)}">
            <i class="fas fa-trash-alt mr-2"></i>{$_('sensors.actions.delete', { default: 'Delete sensor' })}
          </button>
        {/if}
      </CardSettingsTools>
    </svelte:fragment>

    <div class="row">
      <div
        class="col-12 text-center p-0 pt-2"
        class:col-sm-12="{enableGraph}"
        class:col-md-4="{enableGraph}"
        class:col-lg-3="{enableGraph}">
        <Gauge
          id="{sensor.id}"
          type="{sensor.type}"
          value="{sensor.value}"
          alarm_min="{sensor.alarm_min}"
          alarm_max="{sensor.alarm_max}"
          limit_min="{sensor.limit_min}"
          limit_max="{sensor.limit_max}"
          error="{sensor.error}"
          excluded="{sensor.exclude_avg}"
          minmax="{enableGraph}" />
          {#if $sensors[sensor.id]?.calibration?.light_on_off_threshold > 0}
            <i class="fa-regular fa-lightbulb light_on_off_threshold" class:on={$sensors[sensor.id].value > $sensors[sensor.id].calibration.light_on_off_threshold}
                title="{$_('sensors.calibration.light_on_off_threshold.light_bulb', {
                  default: 'Light on of threshold value: {threshold}',
                  values: {
                    threshold: $sensors[sensor.id].calibration.light_on_off_threshold
                  }})}">
            </i>
          {/if}
      </div>
      {#if enableGraph}
        <div class="col-12 col-sm-12 col-md-8 col-lg-9 pr-3">
          <Graph id="{sensor.id}" type="{sensor.type}" mode="sensors" />
        </div>
      {/if}
    </div>
  </Card>
{/if}

<style>
  .row {
    max-height: 180px;
  }

  .light_on_off_threshold {
    position: absolute;
    top: 1.2rem;
    right: 5rem;
    font-size: 1.8rem;
    color: gray;
  }

  .light_on_off_threshold.on {
    color: yellow;
    text-shadow: 1px 1px 1px lightgray, 0 0 1em yellow, 0 0 0.2em orange
  }
</style>
