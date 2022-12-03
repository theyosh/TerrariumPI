<script>
  import { PageHeader } from 'svelte-adminlte';
  import { _ } from 'svelte-i18n';
  import { onMount, onDestroy, getContext, setContext } from 'svelte';

  import { setCustomPageTitle, customPageTitleUsed } from '../stores/page-title';
  import { fetchWebcams, deleteWebcam, updateSystemSettings } from '../providers/api';
  import { successNotification, errorNotification } from '../providers/notification-provider';

  import WebcamCard from '../user-controls/WebcamCard.svelte';

  let webcams = [];

  const { confirmModal } = getContext('confirm');

  const loadData = () => {
    fetchWebcams(false, (data) => (webcams = data));
  };

  const deleteWebcamAction = (webcam) => {
    confirmModal(
      $_('webcams.delete.confirm.message', {
        default: "Are you sure you want to delete the webcam ''{name}''?",
        values: { name: webcam.name },
      }),
      async () => {
        try {
          await deleteWebcam(webcam.id);
          successNotification(
            $_('webcams.delete.ok.message', { default: "The webcam ''{name}'' is deleted.", values: { name: webcam.name } }),
            $_('notification.delete.ok.title', { default: 'OK' })
          );
          loadData();
        } catch (e) {
          errorNotification(
            $_('webcams.delete.error.message', {
              default: "The webcam ''{name}'' could not be deleted!\nError: {error}",
              values: { name: webcam.name, error: e.message },
            }),
            $_('notification.delete.error.title', { default: 'ERROR' })
          );
        }
      }
    );
  };

  const ignoreWebcamAction = (webcam) => {
    confirmModal(
      $_('webcams.confirm.ignore.message', {
        default: "Are you sure you want to ignore the webcam ''{name}''?",
        values: { name: webcam.name },
      }),
      async () => {
        try {
          await updateSystemSettings({ exclude_ids: webcam.id });
          successNotification(
            $_('webcams.exclude.ok.message', { default: "The webcam ''{name}'' is ignored.", values: { name: webcam.name } }),
            $_('notification.exclude.ok.title', { default: 'OK' })
          );
          loadData();
        } catch (e) {
          errorNotification(
            $_('webcams.exclude.error.message', {
              default: "The webcam ''{name}'' could not be ignored!\nError: {error}",
              values: { name: webcam.name, error: e.message },
            }),
            $_('notification.exclude.error.title', { default: 'ERROR' })
          );
        }
      }
    );
  };

  setContext('webcamActions', {
    deleteAction: (webcam) => deleteWebcamAction(webcam),
    ignoreAction: (webcam) => ignoreWebcamAction(webcam),
  });

  onMount(() => {
    setCustomPageTitle($_('webcams.title', { default: 'Webcams' }));
    loadData();
  });

  onDestroy(() => {
    customPageTitleUsed.set(false);
  });
</script>

<PageHeader>
  {$_('webcams.title', { default: 'Webcams' })}
</PageHeader>
<div class="container-fluid">
  <div class="row">
    {#if webcams.length > 0}
      <!-- Sort based on translated names -->
      {#each webcams.sort((a, b) => a.name.localeCompare(b.name)) as webcam}
        <div class="col-12 col-md-12 col-lg-6 col-xl-4">
          <WebcamCard webcam="{webcam}" />
        </div>
      {/each}
    {/if}
  </div>
</div>
