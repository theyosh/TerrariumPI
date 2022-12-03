<script>
  import { _ } from 'svelte-i18n';

  export let showMessage = false;
  export let button = true;
  export let moreInfo = null;

  let buttonBold = false;

  const toggleHelp = () => {
    for (let helptext of document.querySelectorAll('form small.text-muted')) {
      helptext.classList.toggle('d-none');
    }
    buttonBold = !buttonBold;
  };
</script>

{#if button}
  <button
    type="button"
    class="btn btn-rounded text-secondary"
    title="{$_('modal.form.toggle.info', { default: 'Show/hide help information' })}"
    on:click|preventDefault="{toggleHelp}">
    <i class="far fa-question-circle" class:font-weight-bold="{buttonBold}" aria-hidden="true"></i>
  </button>
  {#if moreInfo && buttonBold}
    <small class="text-muted">
      <a href="{moreInfo}" target="_blank" rel="noopener noreferrer">{$_('about.online.help', { default: 'More help online' })}</a>
    </small>
  {/if}
{:else}
  <a href="{'#'}" on:click|preventDefault="{toggleHelp}">
    <i class="fas fa-question-circle"></i>
    {#if showMessage}
      {$_('modal.form.toggle.info', { default: 'Show/hide help information' })}
    {/if}
  </a>
{/if}

<style>
  .text-muted {
    font-size: 50% !important;
  }
</style>
