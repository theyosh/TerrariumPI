<script>
  import { dayjs } from 'svelte-time';
  import duration from 'dayjs/esm/plugin/duration';
  dayjs.extend(duration);
  import { onMount, getContext } from 'svelte';
  import { _, time, date } from 'svelte-i18n';

  import { Fancybox } from '@fancyapps/ui';
  import '@fancyapps/ui/dist/fancybox/fancybox.css';

  import { template_sensor_type_color, template_sensor_type_icon } from '../helpers/icon-helpers';
  import { roundToPrecision } from '../helpers/number-helpers';
  import { getCustomConfig } from '../config';
  import { ApiUrl } from '../constants/urls';
  import { fancyAppsLanguage } from '../constants/ui';
  import { updateButton, isDarkInterface } from '../stores/terrariumpi';
  import { isAuthenticated } from '../stores/authentication';
  import { externalLinks } from '../helpers/string-helpers';

  import Card from '../user-controls/Card.svelte';
  import CardSettingsTools from '../components/common/CardSettingsTools.svelte';
  import DoorIcon from '../components/common/DoorIcon.svelte';

  export let enclosure;

  const settings = getCustomConfig();
  const { editEnclosure, editArea } = getContext('modals');
  const { deleteAction, deleteArea } = getContext('enclosureActions');

  let last_update = null;

  onMount(() => {
    Fancybox.bind("[data-fancybox]", {
      l10n: fancyAppsLanguage(),
    });
  });

  $: if (enclosure.doors) {
    enclosure.doors.map((door) => updateButton({ ...door, ...{ enclosure: enclosure.id } }));
  }
  $: last_update = enclosure ? new Date() : null;
</script>

{#if enclosure}
  <Card loading="{false}" noPadding="{false}" class="{enclosure.id}">
    <svelte:fragment slot="header">
      <i class="fas fa-globe mr-2"></i>{enclosure.name}
      <small class="ml-2 text-muted"
        >{$_('gauge.last_update', { default: 'Last update' })}:
        {$date(last_update, { format: 'long' }) + ' ' + $time(last_update, { format: 'short' })}
      </small>
    </svelte:fragment>

    <svelte:fragment slot="tools">
      <CardSettingsTools>
        <button class="dropdown-item" on:click="{() => editEnclosure(enclosure)}">
          <i class="fas fa-wrench mr-2"></i>{$_('enclosures.actions.settings', { default: 'Edit enclosure' })}
        </button>

        <button class="dropdown-item text-danger" on:click="{() => deleteAction(enclosure)}">
          <i class="fas fa-trash-alt mr-2"></i>{$_('enclosures.actions.delete', { default: 'Delete enclosure' })}
        </button>
      </CardSettingsTools>
    </svelte:fragment>

    <div class="row">
      <div class="col-12 col-sm-12 col-md-12 col-lg-5">
        {#if enclosure.image}
          <img
            src="{ApiUrl}/{enclosure.image}"
            role="button"
            class="rounded float-left img-thumbnail mt-1 mr-2 profile_image"
            alt="{$_('enclosures.settings.image.label', { default: 'Image' })}"
            data-fancybox
            data-caption="{enclosure.name}" />
        {/if}
        {@html externalLinks(enclosure.description)}
      </div>
      <div class="col-12 col-sm-12 col-md-12 col-lg-7">
        <h4>{$_('enclosures.areas.title', { default: 'Areas' })}</h4>
        <table class="table table-sm">
          <thead>
            <tr>
              <th>{$_('table.header.name', { default: 'Name' })}</th>
              <th>{$_('table.header.type', { default: 'Type' })}</th>
              <th>{$_('table.header.mode', { default: 'Mode' })}</th>
              <th colspan="2">{$_('table.header.status', { default: 'Status' })}</th>
              {#if $isAuthenticated}
                <th class="text-center">{$_('table.header.actions', { default: 'Actions' })}</th>
              {/if}
            </tr>
          </thead>
          <tbody>
            {#each enclosure.areas.sort((a, b) => a.name.localeCompare(b.name)) as area}
              <tr>
                <td>
                  {area.name}
                </td>
                <td>
                  <i
                    class="mr-1 fas {template_sensor_type_icon(
                      (area.setup.main_lights ? 'main ' : '') + area.type
                    )} {template_sensor_type_color((area.setup.main_lights ? 'main ' : '') + area.type)}">
                  </i>
                  {$_(`enclosures.area.type.${area.setup.main_lights ? 'main_' : ''}${area.type}`, {
                    default: (area.setup.main_lights ? 'main ' : '') + area.type,
                  })}
                </td>
                <td>
                  {$_(`enclosures.area.mode.${area.mode}`, { default: area.mode })}
                </td>
                <td>
                  {#if area.state.sensors}
                    <span style="display:inline-block; width: 60px">{$_('enclosures.area.range', { default: 'Range' })}:</span>
                    {roundToPrecision(area.state.sensors.alarm_min)}
                    {settings.units[area.type].value} -
                    {roundToPrecision(area.state.sensors.alarm_max)}
                    {settings.units[area.type].value},
                    {$_('enclosures.area.now', { default: 'now' })}: {roundToPrecision(area.state.sensors.current)}
                    {settings.units[area.type].value}
                    <i class="fas fa-exclamation-triangle text-secondary mt-1 ml-2"
                        class:text-danger="{(area.state.sensors?.alarm_low  && area.setup.low.relays.length  > 0)
                                         || (area.state.sensors?.alarm_high && area.setup.high.relays.length > 0)}"
                        class:d-none="{!area.state.sensors.alarm}"> </i>
                  {:else}
                    {#each ['day', 'night', 'low', 'high'] as period}
                      {#if area.state[period] && area.state[period].begin}
                        <span style="display:inline-block; width: 60px"
                          >{$_(`enclosures.area.period.${period}`, { default: period })}:</span>
                        {$time(new Date(area.state[period].begin * 1000), { format: 'medium' })} -
                        {$time(new Date(area.state[period].end * 1000), { format: 'medium' })}
                        ({dayjs.duration(area.state[period].duration * 1000).humanize()}) <br />
                      {/if}
                    {/each}
                  {/if}
                </td>
                <td class="text-right">
                  {#if area.state.sensors}
                    <small
                      class="badge right mt-1"
                      class:mr-4="{!$isAuthenticated}"
                      class:badge-success="{area.state.powered === true}"
                      class:badge-secondary="{area.state.powered === false}"
                      title="{$_('enclosures.area.current_status', { default: 'Current status' })}">&nbsp;&nbsp;</small>
                  {:else}
                    {#each ['day', 'night', 'low', 'high'] as period}
                      {#if area.state[period] && area.state[period].begin}
                        <small
                          class="badge right mt-1"
                          class:mr-4="{!$isAuthenticated}"
                          class:badge-success="{area.state[period].powered === true}"
                          class:badge-secondary="{area.state[period].powered === false}"
                          title="{$_('enclosures.area.current_status', { default: 'Current status' })}">&nbsp;&nbsp;</small
                        ><br />
                      {/if}
                    {/each}
                  {/if}
                </td>
                {#if $isAuthenticated}
                  <td class="text-right text-nowrap">
                    <button
                      class="btn btn-sm"
                      title="{$_('enclosures.area.edit.title', { default: 'Edit area' })}"
                      class:btn-light="{!$isDarkInterface}"
                      class:btn-dark="{$isDarkInterface}"
                      on:click="{() => editArea(area)}">
                      <i class="fas fa-wrench"></i>
                    </button>
                    <button
                      class="btn btn-sm"
                      title="{$_('enclosures.area.delete.title', { default: 'Delete area' })}"
                      class:btn-light="{!$isDarkInterface}"
                      class:btn-dark="{$isDarkInterface}"
                      on:click="{() => deleteArea(area)}">
                      <i class="fas fa-trash-alt text-danger"></i>
                    </button>
                  </td>
                {/if}
              </tr>
            {/each}
          </tbody>
        </table>

        <h4>{$_('enclosures.doors.title', { default: 'Doors' })}</h4>
        <table class="table table-sm">
          <thead>
            <th style="width: 90%">{$_('table.header.name', { default: 'Name' })}</th>
            <th class="text-center">{$_('table.header.status', { default: 'Status' })}</th>
          </thead>
          <tbody>
            {#each enclosure.doors.sort((a, b) => a.name.localeCompare(b.name)) as door}
              <tr>
                <td>{door.name}</td>
                <td class="text-center">
                  <DoorIcon door_id="{door.id}" />
                </td>
              </tr>
            {/each}
          </tbody>
        </table>

        <h4>{$_('enclosures.webcams.title', { default: 'Webcams' })}</h4>
        <div class="row">
          {#each enclosure.webcams.sort((a, b) => a.name.localeCompare(b.name)) as webcam}
            <div class="col-4">
              <strong>{webcam.name}</strong>
              <img
                src="{`${ApiUrl}/${webcam.raw_image}?_t=${new Date().getTime()}`}"
                role="button"
                class="rounded img-thumbnail"
                alt="{`${webcam.name}, ${$date(new Date())} ${$time(new Date())}`}"
                data-fancybox
                data-caption="{`${webcam.name}, ${$date(new Date())} ${$time(new Date())}`}" />
            </div>
          {/each}
        </div>
      </div>
    </div>
  </Card>
{/if}

<style>
  .profile_image {
    width: 200px;
  }
</style>
