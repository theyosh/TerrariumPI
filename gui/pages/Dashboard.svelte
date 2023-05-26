<script>
  import { PageHeader, InfoBox } from 'svelte-adminlte';
  import { _, number } from 'svelte-i18n';
  import { onMount, onDestroy, setContext } from 'svelte';
  import { dayjs } from 'svelte-time';
  import duration from 'dayjs/esm/plugin/duration';
  dayjs.extend(duration);

  import { setCustomPageTitle, customPageTitleUsed } from '../stores/page-title';
  import {
    uptime,
    systemLoad,
    currentPower,
    maxPower,
    currentWater,
    maxWater,
    totalPower,
    totalPowerCosts,
    totalPowerDuration,
    totalWater,
    totalWaterCosts,
    totalWaterDuration,
    updateButton,
    buttons,
    updateSensor,
  } from '../stores/terrariumpi';
  import { uptime_format, average } from '../helpers/number-helpers';
  import { animateHourglass } from '../helpers/animation-helpers';
  import { fetchEnclosures, fetchSensors } from '../providers/api';
  import { getCustomConfig } from '../config';
  import { websocket } from '../providers/websocket';
  import { currency } from '../locale/i18n';

  import Card from '../user-controls/Card.svelte';
  import Enclosure from '../components/enclosure/Enclosure.svelte';
  import EnclosureAccordion from '../user-controls/EnclosureAccordion.svelte';
  import SensorCard from '../user-controls/SensorCard.svelte';
  import EnclosureDoorIcon from '../components/enclosure/EnclosureDoorIcon.svelte';

  let settings = getCustomConfig();
  let sensor_types;
  let enclosures = [];
  let loading_enclosures = settings.dashboard_mode !== 1;
  let enclosures_doors = {};

  const updateEnclosureDoors = (buttons) => {
    Object.keys(enclosures_doors).map((enclosure_id) => {
      enclosures_doors[enclosure_id].closed = enclosures_doors[enclosure_id].doors.every(
        (doorid) => !buttons[doorid] || buttons[doorid].value === 1
      );
    });
  };

  // Set some dummy actions, else sensor cards are crashing
  setContext('sensorActions', {
    deleteAction: (sensor) => {},
    ignoreAction: (sensor) => {},
  });

  onMount(() => {
    // Load dashboard data
    $websocket = { type: 'load_dashboard' };

    // Load REST API data async
    if (loading_enclosures) {
      (async () => {
        // Store data in a enclosure store
        await fetchEnclosures(false, (data) => (enclosures = data));
        if (Array.isArray(enclosures) && enclosures.length > 0) {
          enclosures.map((enclosure) => {
            enclosures_doors[enclosure.id] = {
              doors: enclosure.doors.map((door) => {
                updateButton({ ...door, ...{ enclosure: enclosure.id } });
                return door.id;
              }), // Bad hack, but we get both door updates as enclosure door updates
              closed: true,
            };
          });
        }
        loading_enclosures = false;
      })();
    }

    (async () => {
      let averages = {};

      await fetchSensors(false, (data) => {
        data.map((sensor) => {
          updateSensor(sensor);
          if (!averages[sensor.type]) {
            averages[sensor.type] = {
              value: [],
              alarm_min: [],
              alarm_max: [],
              limit_min: [],
              limit_max: [],
              error: [],
            };
          }

          averages[sensor.type].error.push(sensor.error);

          if (!sensor.exclude_avg) {
            averages[sensor.type].value.push(sensor.value);
            averages[sensor.type].alarm_min.push(sensor.alarm_min);
            averages[sensor.type].alarm_max.push(sensor.alarm_max);
            averages[sensor.type].limit_min.push(sensor.limit_min);
            averages[sensor.type].limit_max.push(sensor.limit_max);
          }
        });

        Object.keys(averages).map((sensor_type) => {
          if (averages[sensor_type]['value'].length === 0) {
            // All sensors are excluded from average. Ignore this sensor type
            delete(averages[sensor_type]);
          } else {
            averages[sensor_type]['type'] = sensor_type;
            averages[sensor_type]['id'] = sensor_type;
            averages[sensor_type]['name'] = $_(`sensors.average.${sensor_type}`, { default: `Average ${sensor_type}` });
            averages[sensor_type]['exclude_avg'] = false;
            averages[sensor_type]['error'] =
              averages[sensor_type]['error'].filter((item) => {
                return item === true;
              }).length > 0;

            for (let value of ['value', 'alarm_min', 'alarm_max', 'limit_min', 'limit_max']) {
              averages[sensor_type][value] = average(averages[sensor_type][value]);
            }
            averages[sensor_type]['alarm'] =
              averages[sensor_type]['alarm_min'] > averages[sensor_type]['value'] ||
              averages[sensor_type]['value'] > averages[sensor_type]['alarm_max'];
          }
        });

        sensor_types = averages;
      });
    })();

    setCustomPageTitle($_('dashboard.title'));

    // CSS Hacks :(
    document.querySelectorAll('div.info-box div.info-box-content').forEach((item) => {
      item.style.lineHeight = 1.2;
    });
    document.querySelector('.content-header').innerHTML = '';

    // TODO: Make a PR for info box icon color
    document.querySelectorAll('div.info-box span.info-box-icon').forEach((item, counter) => {
      item.classList.remove('bg-transparent');
      item.classList.add('elevation-1');
      item.classList.add('float');
      switch (counter) {
        case 0:
          item.classList.add('bg-secondary');
          break;

        case 1:
          item.classList.add('bg-danger');
          break;

        case 2:
          item.classList.add('bg-info');
          break;

        case 3:
          item.classList.add('bg-danger');
          break;

        case 4:
          item.classList.add('bg-info');
          break;

        default:
          break;
      }
    });
    animateHourglass();

    let interval = null;
    if (settings.dashboard_mode !== 1) {
      // Reload every 30 seconds the enclosure data
      interval = setInterval(async () => {
        fetchEnclosures(false, (data) => (enclosures = data));
      }, 30 * 1000);
    }

    //If a function is returned from onMount, it will be called when the component is unmounted.
    return () => {
      clearInterval(interval);
    };
  });

  onDestroy(() => {
    customPageTitleUsed.set(false);
  });

  $: updateEnclosureDoors($buttons);
</script>

<PageHeader />

<div class="container-fluid">
  <div class="row">
    <div class="col-12 col-lg-4">
      <InfoBox>
        <svelte:fragment slot="image">
          <i class="fas fa-hourglass-end hourglass-animation animate"></i>
        </svelte:fragment>
        {$_('dashboard.infobox.uptime.title', { default: 'Up time' })}

        <div class="position-absolute right top">
          <div class="progress vertical progress-sm" title="{$systemLoad[0]}%" style="height: 55px">
            <div
              class="progress-bar bg-success progress-bar-striped"
              role="progressbar"
              aria-valuenow="0"
              aria-valuemin="0"
              aria-valuemax="100"
              style="height: {$systemLoad[0]}%">
              <span class="sr-only">{$systemLoad[0]}%</span>
            </div>
          </div>
          <div class="progress vertical progress-sm" title="{$systemLoad[1]}%" style="height: 55px">
            <div
              class="progress-bar bg-warning progress-bar-striped"
              role="progressbar"
              aria-valuenow="0"
              aria-valuemin="0"
              aria-valuemax="100"
              style="height: {$systemLoad[1]}%">
              <span class="sr-only">{$systemLoad[1]}%</span>
            </div>
          </div>
          <div class="progress vertical progress-sm" title="{$systemLoad[2]}%" style="height: 55px">
            <div
              class="progress-bar bg-danger progress-bar-striped"
              role="progressbar"
              aria-valuenow="0"
              aria-valuemin="0"
              aria-valuemax="100"
              style="height: {$systemLoad[2]}%">
              <span class="sr-only">{$systemLoad[2]}%</span>
            </div>
          </div>
        </div>

        <svelte:fragment slot="number">
          {uptime_format($uptime)}
        </svelte:fragment>
      </InfoBox>
    </div>

    <div class="col-12 col-sm-6 col-md-3 col-lg-2">
      <InfoBox>
        <svelte:fragment slot="image">
          <i class="fas fa-bolt"></i>
        </svelte:fragment>
        <span>{$_('dashboard.infobox.current_power_usage.title', { default: 'Power usage in Watt' })}</span>
        <svelte:fragment slot="number">
          <span>{$number($currentPower)} / {$number($maxPower)}</span>
          <div class="progress" title="{($currentPower / $maxPower) * 100}%">
            <div class="progress-xxs bg-danger" style="width: {($currentPower / $maxPower) * 100}%"></div>
          </div>
        </svelte:fragment>
      </InfoBox>
    </div>

    <div class="col-12 col-sm-6 col-md-3 col-lg-2">
      <InfoBox>
        <svelte:fragment slot="image">
          <i class="fas fa-tint"></i>
        </svelte:fragment>
        <span
          >{$_('dashboard.infobox.current_water_flow.title', {
            default: 'Water flow in {water_flow_indicator}',
            values: { water_flow_indicator: settings.units.water_flow.value },
          })}</span>
        <svelte:fragment slot="number">
          <span>{$number($currentWater)} / {$number($maxWater)}</span>
          <div class="progress" title="{($currentWater / $maxWater) * 100}%">
            <div class="progress-xxs bg-info" style="width: {($currentWater / $maxWater) * 100}%"></div>
          </div>
        </svelte:fragment>
      </InfoBox>
    </div>

    <div class="col-12 col-sm-6 col-md-3 col-lg-2">
      <InfoBox>
        <svelte:fragment slot="image">
          <i class="fas fa-bolt"></i>
        </svelte:fragment>
        <span>{$_('dashboard.infobox.total_power_usage.title', { default: 'Total power usage' })}</span>
        <svelte:fragment slot="number">
          <span>{$number($totalPower)} {settings.units.powerusage.value}</span>
          <div class="text-nowrap text-truncate">
            <span class="text-success">{$number($totalPowerCosts, { style: 'currency', currency: $currency })}</span>
            <small>
              {$_('dashboard.infobox.total_power_usage.duration', {
                values: { duration: dayjs.duration($totalPowerDuration * 1000).humanize() },
              })}
            </small>
          </div>
        </svelte:fragment>
      </InfoBox>
    </div>

    <div class="col-12 col-sm-6 col-md-3 col-lg-2">
      <InfoBox>
        <svelte:fragment slot="image">
          <i class="fas fa-tint"></i>
        </svelte:fragment>
        <span>{$_('dashboard.infobox.total_water_usage.title', { default: 'Total water usage' })}</span>
        <svelte:fragment slot="number">
          <span>{$number($totalWater)} {settings.units.water_volume.value}</span>
          <div class="text-nowrap text-truncate">
            <span class="text-success">{$number($totalWaterCosts, { style: 'currency', currency: $currency })}</span>
            <small>
              {$_('dashboard.infobox.total_water_usage.duration', {
                values: { duration: dayjs.duration($totalWaterDuration * 1000).humanize() },
              })}
            </small>
          </div>
        </svelte:fragment>
      </InfoBox>
    </div>
  </div>

  <div class="row" class:flex-row-reverse="{settings.dashboard_mode === 0}">
    {#if settings.dashboard_mode === 0}
      <div class="col-12 col-md-4 col-lg-3">
        <Card loading="{loading_enclosures}" removeParent="{true}">
          <svelte:fragment slot="header">
            <i class="fas fa-globe mr-2"></i>{$_('dashboard.enclosures.title', { default: 'Enclosures' })}
          </svelte:fragment>

          <svelte:fragment slot="tools" />

          <EnclosureAccordion enclosures="{enclosures}" />
        </Card>
      </div>
    {/if}

    {#if settings.dashboard_mode === 2 && enclosures}
      {#each enclosures.sort((a, b) => a.name.localeCompare(b.name)) as enclosure, counter}
        <div class="col-12 col-md-6 col-lg-3">
          <Card loading="{loading_enclosures}">
            <svelte:fragment slot="header">
              <i class="fas fa-globe mr-2"></i>{enclosure.name}
            </svelte:fragment>

            <svelte:fragment slot="tools">
              <EnclosureDoorIcon enclosure_id="{enclosure.id}" />
            </svelte:fragment>

            <Enclosure enclosure="{enclosure}" />
          </Card>
        </div>
      {/each}
    {/if}

    {#if [0, 1].indexOf(settings.dashboard_mode) !== -1 && sensor_types && Object.keys(sensor_types).length > 0}
      <div class="col">
        <!-- Sort based on translated names -->
        {#each Object.keys(sensor_types).sort( (a, b) => $_(`sensors.average.${a}`).localeCompare($_(`sensors.average.${b}`)) ) as sensor_type}
          <SensorCard sensor="{sensor_types[sensor_type]}" enableSettings="{false}" />
        {/each}
      </div>
    {/if}
  </div>
</div>

<style lang="sass">
	.right
		right: 0.5rem

	.top
		top: 0.5rem

	.text-truncate
		max-width: 95%

	.animate
		transition: 1s linear
		transform: rotate(180deg)
</style>
