<script>
  import { getContext } from 'svelte';
  import { _, date, time } from 'svelte-i18n';

  import Card from '../user-controls/Card.svelte';
  import Button from '../components/common/Button.svelte';
  import Graph from '../components/common/Graph.svelte';
  import CardSettingsTools from '../components/common/CardSettingsTools.svelte';
  import CardGraphPeriodTools from '../components/common/CardGraphPeriodTools.svelte';

  import { buttons } from '../stores/terrariumpi';
  import { exportGraphPeriod } from '../helpers/graph-helpers';

  export let enableGraph = true;
  export let button;

  const { editButton } = getContext('modals');
  const { deleteAction, ignoreAction } = getContext('buttonActions');

  let exporting = false;
  const exportAction = async () => {
    exporting = true;
    await exportGraphPeriod('buttons', button.id);
    exporting = false;
  };

  $buttons[button.id] = button;
</script>

{#if button}
  <Card loading="{false}" noPadding="{true}" class="{button.id}">
    <svelte:fragment slot="header">
      <i class="fas fa-thumbtack mr-2"></i>{button.name}
      {#if $buttons[button.id]}
        <small class="ml-2 text-muted"
          >{$_('gauge.last_update', { default: 'Last update' })}: {$date($buttons[button.id].last_update, { format: 'long' }) +
            ' ' +
            $time($buttons[button.id].last_update, { format: 'short' })}</small>
      {/if}

      {#if $buttons[button.id].error}
        <small class="badge badge-danger">{$_('gauge.error', { default: 'Error' })}</small>
      {/if}
    </svelte:fragment>

    <svelte:fragment slot="tools">
      <CardGraphPeriodTools id="{button.id}" />

      <CardSettingsTools>
        <button class="dropdown-item" on:click="{exportAction}">
          <i class="fas mr-2" class:fa-file-export="{!exporting}" class:fa-spinner="{exporting}" class:fa-spin="{exporting}"></i>{$_(
            'buttons.actions.export',
            { default: 'Export button' }
          )}
        </button>

        <button class="dropdown-item" on:click="{() => ignoreAction(button)}">
          <i class="fas fa-ban mr-2"></i>{$_('buttons.actions.ignore', { default: 'Ignore button' })}
        </button>

        <button class="dropdown-item" on:click="{() => editButton(button)}">
          <i class="fas fa-wrench mr-2"></i>{$_('buttons.actions.settings', { default: 'Edit button' })}
        </button>

        <button class="dropdown-item text-danger" on:click="{() => deleteAction(button)}">
          <i class="fas fa-trash-alt mr-2"></i>{$_('buttons.actions.delete', { default: 'Delete button' })}
        </button>
      </CardSettingsTools>
    </svelte:fragment>

    <div class="row" style="min-height: 180px">
      <div class="col-12 col-sm-12 col-md-3 col-lg-2 text-center">
        <Button button="{button}" />
      </div>
      {#if enableGraph}
        <div class="col-12 col-sm-12 col-md-9 col-lg-10 pr-3">
          <Graph id="{button.id}" type="{button.hardware}" mode="buttons" />
        </div>
      {/if}
    </div>
  </Card>
{/if}
