<script>
  import { onMount, onDestroy, getContext, setContext } from 'svelte';
  import { PageHeader } from 'svelte-adminlte';
  import { _ } from 'svelte-i18n';

  import { setCustomPageTitle, customPageTitleUsed } from '../stores/page-title';
  import { fetchSensors, deleteSensor, updateSystemSettings } from '../providers/api';
  import { successNotification, errorNotification } from '../providers/notification-provider';

  import SensorCard from '../user-controls/SensorCard.svelte';

  export let params = null;

  let sensors = [];
  let translate_sensor_type = '';
  let enableGraph = params && params.type ? true : false;

  const { confirmModal } = getContext('confirm');

  const loadData = () => {
    fetchSensors(params && params.type ? params.type : false, (data) => (sensors = data));
  };

  const deleteSensorAction = function (sensor) {
    confirmModal(
      $_('sensors.delete.confirm.message', {
        default: "Are you sure you want to delete the sensor ''{name}''?",
        values: { name: sensor.name },
      }),
      async () => {
        try {
          await deleteSensor(sensor.id);
          successNotification(
            $_('sensors.delete.ok.message', { default: "The sensor ''{name}'' is deleted.", values: { name: sensor.name } }),
            $_('notification.delete.ok.title', { default: 'OK' })
          );
          loadData();
        } catch (e) {
          errorNotification(
            $_('sensors.delete.error.message', {
              default: "The sensor ''{name}'' could not be deleted!\nError: {error}",
              values: { name: sensor.name, error: e.message },
            }),
            $_('notification.delete.error.title', { default: 'ERROR' })
          );
        }
      }
    );
  };

  const ignoreSensorAction = function (sensor) {
    confirmModal(
      $_('sensors.confirm.ignore.message', {
        default: "Are you sure you want to ignore the sensor ''{name}''?",
        values: { name: sensor.name },
      }),
      async () => {
        try {
          await updateSystemSettings({ exclude_ids: sensor.id });
          successNotification(
            $_('sensors.exclude.ok.message', { default: "The sensor ''{name}'' is ignored.", values: { name: sensor.name } }),
            $_('notification.exclude.ok.title', { default: 'OK' })
          );
          loadData();
        } catch (e) {
          errorNotification(
            $_('sensors.exclude.error.message', {
              default: "The sensor ''{name}'' could not be ignored!\nError: {error}",
              values: { name: sensor.name, error: e.message },
            }),
            $_('notification.exclude.error.title', { default: 'ERROR' })
          );
        }
      }
    );
  };

  setContext('sensorActions', {
    deleteAction: (sensor) => deleteSensorAction(sensor),
    ignoreAction: (sensor) => ignoreSensorAction(sensor),
  });

  onMount(() => {
    // Page title will be set based on the params.type and enableGraph settings
    loadData();
  });

  $: {
    translate_sensor_type = params && params.type !== '' ? `.${params.type}` : !enableGraph ? '.all' : '';
    setCustomPageTitle($_(`sensors${translate_sensor_type}.title`));
    sensors = [];
    loadData();
  }

  onDestroy(() => {
    customPageTitleUsed.set(false);
  });
</script>

<PageHeader>
  {$_(`sensors${translate_sensor_type}.title`)}
</PageHeader>
<div class="container-fluid">
  <div class="row">
    {#if sensors.length > 0}
      <!-- Sort based on translated names -->
      {#each sensors.sort((a, b) => a.name.localeCompare(b.name)) as sensor}
        <div class="col" class:col-12="{enableGraph}" class:col-3="{!enableGraph}">
          <SensorCard sensor="{sensor}" enableGraph="{enableGraph}" removeParent="{true}" />
        </div>
      {/each}
    {/if}
  </div>
</div>
