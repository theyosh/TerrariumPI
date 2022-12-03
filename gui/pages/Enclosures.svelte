<script>
  import { onMount, onDestroy, getContext, setContext } from 'svelte';
  import { PageHeader } from 'svelte-adminlte';
  import { _ } from 'svelte-i18n';

  import { setCustomPageTitle, customPageTitleUsed } from '../stores/page-title';
  import { fetchEnclosures, deleteEnclosure, deleteArea } from '../providers/api';
  import { successNotification, errorNotification } from '../providers/notification-provider';

  import EnclosureCard from '../user-controls/EnclosureCard.svelte';

  let enclosures = [];

  const { confirmModal } = getContext('confirm');

  const loadData = () => {
    fetchEnclosures(false, (data) => (enclosures = data));
  };

  const deleteEnclosureAction = (enclosure) => {
    confirmModal(
      $_('enclosures.delete.confirm.message', {
        default: "Are you sure you want to delete the enclosure ''{name}''?",
        values: { name: enclosure.name },
      }),
      async () => {
        try {
          await deleteEnclosure(enclosure.id);
          successNotification(
            $_('enclosures.delete.ok.message', { default: "The enclosure ''{name}'' is deleted.", values: { name: enclosure.name } }),
            $_('notification.delete.ok.title', { default: 'OK' })
          );
          loadData();
        } catch (e) {
          errorNotification(
            $_('enclosures.delete.error.message', {
              default: "The enclosure ''{name}'' could not be deleted!\nError: {error}",
              values: { name: enclosure.name, error: e.message },
            }),
            $_('notification.delete.error.title', { default: 'ERROR' })
          );
        }
      }
    );
  };

  const deleteAreaAction = (area) => {
    confirmModal(
      $_('areas.delete.confirm.message', { default: "Are you sure you want to delete the area ''{name}''?", values: { name: area.name } }),
      async () => {
        try {
          await deleteArea(area.id);
          successNotification(
            $_('areas.delete.ok.message', { default: "The area ''{name}'' is deleted.", values: { name: area.name } }),
            $_('notification.delete.ok.title', { default: 'OK' })
          );
          loadData();
        } catch (e) {
          errorNotification(
            $_('areas.delete.error.message', {
              default: "The area ''{name}'' could not be deleted!\nError: {error}",
              values: { name: area.name, error: e.message },
            }),
            $_('notification.delete.error.title', { default: 'ERROR' })
          );
        }
      }
    );
  };

  setContext('enclosureActions', {
    deleteAction: (enclosure) => deleteEnclosureAction(enclosure),
    deleteArea: (area) => deleteAreaAction(area),
    //    reloadAction: () => loadData() // TODO: Figure this out. Reload can only be done when on the enclosure page... :(
  });

  onMount(() => {
    setCustomPageTitle($_('enclosures.title', { default: 'Enclosures' }));
    loadData();

    // Reload every 30 seconds the enclosure data
    const interval = setInterval(() => {
      loadData();
    }, 30 * 1000);

    //If a function is returned from onMount, it will be called when the component is unmounted.
    return () => clearInterval(interval);
  });

  onDestroy(() => {
    customPageTitleUsed.set(false);
  });
</script>

<PageHeader>
  {$_('enclosures.title', { default: 'Enclosures' })}
</PageHeader>
<div class="container-fluid">
  <div class="row">
    {#if enclosures.length > 0}
      <!-- Sort based on enclosure names natural sorting -->
      {#each enclosures.sort((a, b) => a.name.localeCompare(b.name)) as enclosure}
        <div class="col-12">
          <EnclosureCard enclosure="{enclosure}" />
        </div>
      {/each}
    {/if}
  </div>
</div>
