<script>
  import { Modal, ModalCloseButton } from 'svelte-adminlte';
  import { createEventDispatcher } from 'svelte';
  import { _ } from 'svelte-i18n';

  export let confirmTitle = $_('modal.confirm.title', { default: 'Are you sure?' });
  export let confirmMessage = '';
  export let icon = 'fa-exclamation';

  let running = false;
  let wrapper_show;
  let wrapper_hide;

  const dispatch = createEventDispatcher();

  const confirmAction = () => {
    running = true;
    dispatch('confirm');
  };

  export const show = async () => {
    running = false;
    wrapper_show();
  };

  export const hide = () => {
    wrapper_hide();
    running = false;
  };
</script>

<Modal bind:show="{wrapper_show}" bind:hide="{wrapper_hide}">
  <svelte:fragment slot="header">
    <i class="fas {icon}"></i>
    {confirmTitle}
  </svelte:fragment>

  <p class="text-center">{@html confirmMessage}</p>

  <svelte:fragment slot="actions">
    <div class="d-flex justify-content-between w-100">
      <ModalCloseButton>
        {$_('modal.general.close', { default: 'Close' })}
      </ModalCloseButton>
      <button type="button" class="btn btn-danger" disabled="{running}" on:click="{confirmAction}">
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" class:d-none="{!running}"></span>
        {$_('modal.confirm.submit.title', { default: 'Confirm' })}
      </button>
    </div>
  </svelte:fragment>
</Modal>
