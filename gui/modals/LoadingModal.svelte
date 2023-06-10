<script>
  import { Modal } from 'svelte-adminlte';

  import { _ } from 'svelte-i18n';

  let wrapper_show;
  let wrapper_hide;
  let message;

  export const show = () => {
    wrapper_show();
  };

  export const hide = () => {
    wrapper_hide();
  };

  export const setMessage = (msg) => {
    message = msg;
  }
</script>

<Modal center bind:show="{wrapper_show}" bind:hide="{wrapper_hide}">
  <svelte:fragment slot="header">
    <i class="fas fa-sync-alt fa-spin mr-2"></i>
    {$_('modal.loading.title', { default: 'Loading' })}
  </svelte:fragment>
  <p>{message}</p>
  <svelte:fragment slot="actions">
    <div class="d-flex justify-content-between w-100"> </div>
  </svelte:fragment>
</Modal>
