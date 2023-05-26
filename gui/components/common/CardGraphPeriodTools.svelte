<script>
  import { _ } from 'svelte-i18n';

  import { graphs } from '../../stores/terrariumpi';
  import { toggleGraphPeriod } from '../../helpers/graph-helpers';

  export let id;
  export let replaced = false;
</script>

<div class="btn-group">
  <button type="button" class="btn btn-tool dropdown-toggle" data-toggle="dropdown">
    <i class="fas fa-calendar-alt"></i>
  </button>
  <div class="dropdown-menu dropdown-menu-right" role="menu" style="min-width: auto !important;">
    <button class="dropdown-item" class:active="{$graphs[id].period === 'day'}" on:click="{() => toggleGraphPeriod(id, 'day')}"
      >{$_('graph.period.day', { default: 'Day' })}</button>
    <button class="dropdown-item" class:active="{$graphs[id].period === 'week'}" on:click="{() => toggleGraphPeriod(id, 'week')}"
      >{$_('graph.period.week', { default: 'Week' })}</button>
    <button class="dropdown-item" class:active="{$graphs[id].period === 'month'}" on:click="{() => toggleGraphPeriod(id, 'month')}"
      >{$_('graph.period.month', { default: 'Month' })}</button>
    <button class="dropdown-item" class:active="{$graphs[id].period === 'year'}" on:click="{() => toggleGraphPeriod(id, 'year')}"
      >{$_('graph.period.year', { default: 'Year' })}</button>
    {#if replaced}
      <button class="dropdown-item" class:active="{$graphs[id].period === 'replaced'}" on:click="{() => toggleGraphPeriod(id, 'replaced')}"
        >{$_('graph.period.replaced', { default: 'Replaced' })}</button>
    {/if}
  </div>
</div>
