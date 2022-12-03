<script>
  import { onMount, onDestroy, setContext } from 'svelte';
  import { PageHeader } from 'svelte-adminlte';
  import { _ } from 'svelte-i18n';

  import { setCustomPageTitle, customPageTitleUsed } from '../stores/page-title';
  import { fetchSystemstats } from '../providers/api';
  import { uptime_format } from '../helpers/number-helpers';
  import { uptime } from '../stores/terrariumpi';

  import SensorCard from '../user-controls/SensorCard.svelte';
  import Card from '../user-controls/Card.svelte';

  let systemStats;
  let summary;

  // Dummy function for Sensor cards
  setContext('sensorActions', {
    deleteAction: (sensor) => {},
    ignoreAction: (sensor) => {},
  });

  onMount(() => {
    (async () => {
      await fetchSystemstats((data) => {
        systemStats = {
          load: {
            id: 'system_load',
            name: $_('system.status.load.title', { default: 'System load' }),
            type: 'humidity',
            error: false,
            value: data.load.percentage[0],
            alarm_min: 0,
            alarm_max: 100,
            limit_min: 0,
            limit_max: 100,
            exclude_avg: false,
          },
          cpu_temp: {
            id: 'cpu_temp',
            name: $_('system.status.cpu_temp.title', { default: 'CPU Temperature' }),
            type: 'temperature',
            error: false,
            value: data.cpu_temperature,
            alarm_min: 30,
            alarm_max: 80,
            limit_min: 0,
            limit_max: 100,
            exclude_avg: false,
          },
          memory: {
            id: 'memory',
            name: $_('system.status.memory.title', { default: 'Memory usage' }),
            type: 'filesize',
            error: false,
            value: data.memory.used,
            alarm_min: 0,
            alarm_max: 0.6 * data.memory.total,
            limit_min: 0,
            limit_max: data.memory.total,
            exclude_avg: false,
          },
          disk: {
            id: 'disk',
            name: $_('system.status.disk.title', { default: 'Disk usage' }),
            type: 'filesize',
            error: false,
            value: data.storage.used,
            alarm_min: 0,
            alarm_max: 0.8 * data.storage.total,
            limit_min: 0,
            limit_max: data.storage.total,
            exclude_avg: false,
          },
        };
        summary = data.summary;
      });

      // GUI hacks
      for (let card of document.querySelectorAll('h3.card-title > i.fas')) {
        card.classList = 'fas fa-microchip mr-2';
      }
      for (let text of document.querySelectorAll('h3.card-title > small.text-muted')) {
        text.remove();
      }
      for (let tools of document.querySelectorAll('.card-tools i.fa-wrench')) {
        tools.parentNode.remove();
      }
    })();
    setCustomPageTitle($_('system.status.title', { default: 'System status' }));

    // Reload every 30 seconds the enclosure data
    let interval = setInterval(async () => {
      fetchSystemstats((data) => (summary = data.summary));
    }, 30 * 1000);

    //If a function is returned from onMount, it will be called when the component is unmounted.
    return () => clearInterval(interval);
  });

  onDestroy(() => {
    customPageTitleUsed.set(false);
  });
</script>

<PageHeader>
  {$_('system.status.title', { default: 'System status' })}
</PageHeader>
<div class="container-fluid">
  {#if systemStats}
    <div class="row">
      <div class="col">
        <SensorCard sensor="{systemStats.load}" enableGraph="{false}" removeParent="{true}" />
      </div>
      <div class="col">
        <SensorCard sensor="{systemStats.cpu_temp}" enableGraph="{false}" removeParent="{true}" />
      </div>
      <div class="col">
        <SensorCard sensor="{systemStats.memory}" enableGraph="{false}" removeParent="{true}" />
      </div>
      <div class="col">
        <SensorCard sensor="{systemStats.disk}" enableGraph="{false}" removeParent="{true}" />
      </div>
    </div>
    <div class="row">
      <div class="col">
        <Card loading="{false}" noPadding="{false}">
          <svelte:fragment slot="header">
            <i class="fas fa-microchip mr-2"></i>{$_('system.status.uptime.title', { default: 'System uptime' })}
          </svelte:fragment>
          <div class="text-center">
            {@html uptime_format($uptime).replace(/(\d+) (\S)/gm, '&nbsp;&nbsp;<span class="h1">$1$2</span>')}
          </div>
        </Card>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <Card loading="{false}" noPadding="{false}">
          <svelte:fragment slot="header">
            <i class="fas fa-microchip mr-2"></i>{$_('system.status.summary.title', { default: 'System summary' })}
          </svelte:fragment>
          <div class="d-flex justify-content-center">
            {@html summary}
          </div>
        </Card>
      </div>
    </div>
  {/if}
</div>
