<script>
  import { getContext } from 'svelte';
  import { _, date, time } from 'svelte-i18n';

  import { template_sensor_type_icon } from '../helpers/icon-helpers';
  import { relays, updateRelay } from '../stores/terrariumpi';
  import { exportGraphPeriod } from '../helpers/graph-helpers';

  import Card from '../user-controls/Card.svelte';
  import Relay from '../components/common/Relay.svelte';
  import Graph from '../components/common/Graph.svelte';
  import CardSettingsTools from '../components/common/CardSettingsTools.svelte';
  import CardGraphPeriodTools from '../components/common/CardGraphPeriodTools.svelte';

  export let enableGraph = true;
  export let relay;

  const { editRelay } = getContext('modals');
  const { deleteAction, ignoreAction, replaceAction, manualAction } = getContext('relayActions');

  let exporting = false;
  const exportAction = async () => {
    exporting = true;
    await exportGraphPeriod('relays', relay.id);
    exporting = false;
  };

  $: updateRelay(relay);
</script>

{#if relay}
  <Card loading="{false}" noPadding="{true}" class="{relay.id}">
    <svelte:fragment slot="header">
      <i class="fas {template_sensor_type_icon(relay.type)} mr-2"></i>{relay.name}
      {#if $relays[relay.id]}
        <small class="ml-2 text-muted"
          >{$_('gauge.last_update', { default: 'Last update' })}: {$date($relays[relay.id].last_update, { format: 'long' }) +
            ' ' +
            $time($relays[relay.id].last_update, { format: 'short' })}</small>
        {#if $relays[relay.id].manual_mode}
          <small class="badge badge-primary">{$_('relays.manual-mode', { default: 'Manual mode' })}</small>
        {/if}
        {#if $relays[relay.id].error}
          <small class="badge badge-danger">{$_('gauge.error', { default: 'Error' })}</small>
        {/if}
      {/if}
    </svelte:fragment>

    <svelte:fragment slot="tools">
      <CardGraphPeriodTools id="{relay.id}" replaced="{true}" />
      <CardSettingsTools>
        <button class="dropdown-item" title="{$_('relays.actions.export', { default: 'Export relay' })}" on:click="{exportAction}">
          <i class="fas mr-2" class:fa-file-export="{!exporting}" class:fa-spinner="{exporting}" class:fa-spin="{exporting}"></i>{$_(
            'relays.actions.export',
            { default: 'Export relay' }
          )}
        </button>

        <button
          class="dropdown-item"
          title="{$_('relays.actions.replace_hardware', { default: 'Replace hardware' })}"
          on:click="{() => replaceAction(relay)}">
          <i class="fas fa-tools mr-2"></i>{$_('relays.actions.replace_hardware', { default: 'Replace hardware' })}
        </button>

        <button
          class="dropdown-item"
          title="{$_('relays.actions.manual_mode', { default: 'Manual mode relay' })}"
          on:click="{() => manualAction(relay)}">
          <i class="fas fa-hand-paper mr-2"></i>{$_('relays.actions.manual_mode', { default: 'Manual mode relay' })}
        </button>

        <button
          class="dropdown-item"
          title="{$_('relays.actions.ignore', { default: 'Ignore relay' })}"
          on:click="{() => ignoreAction(relay)}">
          <i class="fas fa-ban mr-2"></i>{$_('relays.actions.ignore', { default: 'Ignore relay' })}
        </button>

        <button
          class="dropdown-item"
          title="{$_('relays.actions.settings', { default: 'Edit relay' })}"
          on:click="{() => editRelay(relay)}">
          <i class="fas fa-wrench mr-2"></i>{$_('relays.actions.settings', { default: 'Edit relay' })}
        </button>

        <button
          class="dropdown-item text-danger"
          title="{$_('relays.actions.delete', { default: 'Delete relay' })}"
          on:click="{() => deleteAction(relay)}">
          <i class="fas fa-trash-alt mr-2"></i>{$_('relays.actions.delete', { default: 'Delete relay' })}
        </button>
      </CardSettingsTools>
    </svelte:fragment>

    <div class="row" style="min-height: 180px">
      <div class="col-12 col-sm-12 col-md-3 col-lg-2 text-center">
        <Relay relay="{relay}" />
      </div>
      {#if enableGraph}
        <div class="col-12 col-sm-12 col-md-9 col-lg-10 pr-3">
          <Graph id="{relay.id}" type="{relay.dimmer}" mode="relays" />
        </div>
      {/if}
    </div>
  </Card>
{/if}
