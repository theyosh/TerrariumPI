<script>
  import { Modal, ModalCloseButton } from 'svelte-adminlte';
  import { onMount } from 'svelte';
  import { _ } from 'svelte-i18n';

  export let loading = false;

  let wrapper_show;
  let wrapper_hide;
  let loadingDiv = null;

  export const show = () => {
    // Toggle loading div
    // loading = true

    // Show the modal
    wrapper_show();
  };

  export const hide = () => {
    // Delay the loading div
    // setTimeout(() => {
    //   loading = false
    // }, 1000)

    // Hide modal
    wrapper_hide();
  };

  onMount(() => {
    // GUI hack: Move loading div after model content div, so we get a full modal loading div
    loadingDiv.parentElement.parentElement.parentElement.appendChild(loadingDiv);
  });
</script>

<Modal xlarge bind:show="{wrapper_show}" bind:hide="{wrapper_hide}">
  <svelte:fragment slot="header">
    <slot name="header" />
  </svelte:fragment>

  <slot />

  <svelte:fragment slot="actions">
    <div class="d-flex justify-content-between w-100">
      <ModalCloseButton>
        {$_('modal.general.close')}
      </ModalCloseButton>
      <slot name="actions" />
    </div>
  </svelte:fragment>

  <!-- Hack using d-none class. Else can't move the div to a different location in the DOM -->
  <div class="overlay" class:d-none="{!loading}" bind:this="{loadingDiv}">
    <i class="fas fa-2x fa-sync-alt fa-spin"></i>
  </div>
</Modal>
