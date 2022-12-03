<script>
  import { onMount, onDestroy, getContext, setContext } from 'svelte';
  import { PageHeader } from 'svelte-adminlte';
  import { _ } from 'svelte-i18n';

  import { setCustomPageTitle, customPageTitleUsed } from '../stores/page-title';
  import { fetchButtons, deleteButton, updateSystemSettings } from '../providers/api';
  import { successNotification, errorNotification } from '../providers/notification-provider';

  import ButtonCard from '../user-controls/ButtonCard.svelte';

  let buttons = [];

  const { confirmModal } = getContext('confirm');

  const loadData = () => {
    fetchButtons(false, (data) => (buttons = data));
  };

  const deleteButtonAction = (button) => {
    confirmModal(
      $_('buttons.delete.confirm.message', {
        default: "Are you sure you want to delete the button ''{name}''?",
        values: { name: button.name },
      }),
      async () => {
        try {
          await deleteButton(button.id);
          successNotification(
            $_('buttons.delete.ok.message', { default: "The button ''{name}'' is deleted.", values: { name: button.name } }),
            $_('notification.delete.ok.title', { default: 'OK' })
          );
          loadData();
        } catch (e) {
          errorNotification(
            $_('buttons.delete.error.message', {
              default: "The button ''{name}'' could not be deleted!\nError: {error}",
              values: { name: button.name, error: e.message },
            }),
            $_('notification.delete.error.title', { default: 'ERROR' })
          );
        }
      }
    );
  };

  const ignoreButtonAction = (button) => {
    confirmModal(
      $_('buttons.ignore.confirm.message', {
        default: "Are you sure you want to ignore the button ''{name}''?",
        values: { name: button.name },
      }),
      async () => {
        try {
          await updateSystemSettings({ exclude_ids: button.id });
          successNotification(
            $_('buttons.ignore.ok.message', { default: "The button ''{name}'' is ignored.", values: { name: button.name } }),
            $_('notification.exclude.ok.title')
          );
          loadData();
        } catch (e) {
          errorNotification(
            $_('buttons.ignore.error.message', {
              default: "The button ''{name}'' could not be ignored!\nError: {error}",
              values: { name: button.name, error: e.message },
            }),
            $_('notification.exclude.error.title')
          );
        }
      }
    );
  };

  setContext('buttonActions', {
    deleteAction: (button) => deleteButtonAction(button),
    ignoreAction: (button) => ignoreButtonAction(button),
  });

  onMount(() => {
    setCustomPageTitle($_('buttons.title', { default: 'Buttons' }));
    loadData();
  });

  onDestroy(() => {
    customPageTitleUsed.set(false);
  });
</script>

<PageHeader>
  {$_('buttons.title')}
</PageHeader>
<div class="container-fluid">
  <div class="row">
    {#if buttons.length > 0}
      <!-- Sort based on translated names -->
      {#each buttons.sort((a, b) => a.name.localeCompare(b.name)) as button}
        <div class="col-12">
          <ButtonCard button="{button}" />
        </div>
      {/each}
    {/if}
  </div>
</div>
