<script>
  import { onMount } from 'svelte';
  import { Card as BaseCard } from 'svelte-adminlte';

  import CardDefaultTools from '../components/common/CardDefaultTools.svelte';
  import { getRandomString } from '../helpers/string-helpers';

  export let loading;
  export let noPadding = false;
  export let noTools = false;
  export let removeParent = false;

  let loadingDiv = null;
  let card = null;
  const cardClassID = 'crd' + getRandomString(6).toLocaleLowerCase();

  onMount(() => {
    loadingDiv.parentElement.parentElement.appendChild(loadingDiv);

    // Destroy the inner Svelte components as well.
    // This will stop the loaded setInterval timers and stop reloading not needed data...
    if (!noTools) {
      document.querySelector(`div.card.${cardClassID} button[data-card-widget="remove"]`).addEventListener('click', (event) => {
        let parent = null;
        if (removeParent) {
          parent = document.querySelector(`div.card.${cardClassID}`).parentElement;
        }

        setTimeout(() => {
          if (parent !== null) {
            parent.remove();
          }
          card.$destroy();
        }, 550);
      });
    }
    if (!$$slots.header) {
      document.querySelector(`div.card.${cardClassID} div.card-header`).remove();
    }
  });
</script>

<BaseCard noPadding="{noPadding}" class="{cardClassID} {$$props.class || ''}" bind:this="{card}">
  <svelte:fragment slot="header">
    <slot name="header" />
  </svelte:fragment>

  <svelte:fragment slot="tools">
    <slot name="tools" />
    {#if !noTools}
      <CardDefaultTools />
    {/if}
  </svelte:fragment>

  <slot />

  <div class="overlay" class:d-none="{!loading}" bind:this="{loadingDiv}">
    <i class="fas fa-2x fa-sync-alt fa-spin"></i>
  </div>
</BaseCard>
