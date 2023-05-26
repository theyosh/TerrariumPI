<script>
  import EnclosureDoorIcon from '../components/enclosure/EnclosureDoorIcon.svelte';
  import Enclosure from '../components/enclosure/Enclosure.svelte';

  export let enclosures = [];
</script>

{#if enclosures.length > 0}
  <div id="accordion">
    {#each enclosures.sort((a, b) => a.name.localeCompare(b.name)) as enclosure, counter}
      <div class="card card-secondary">
        <div class="card-header">
          <h4 class="card-title w-100">
            <a data-toggle="collapse" class="d-block" style="margin-bottom:-1.2rem" href="#enclosure_{enclosure.id}">{enclosure.name}</a>
            <span class="float-right">
              <EnclosureDoorIcon enclosure_id="{enclosure.id}" />
            </span>
          </h4>
        </div>
        <div id="enclosure_{enclosure.id}" class="collapse" class:show="{counter === 0}" data-parent="#accordion">
          <Enclosure enclosure="{enclosure}" />
        </div>
      </div>
    {/each}
  </div>
{/if}
