<script>
  import { PageHeader } from 'svelte-adminlte';
  import { _ } from 'svelte-i18n';
  import { onMount, onDestroy, getContext, setContext } from 'svelte';

  import { setCustomPageTitle, customPageTitleUsed } from '../stores/page-title';
  import { fetchRelays, deleteRelay, toggleRelay, dimRelay, manualRelay, updateSystemSettings } from '../providers/api';
  import { successNotification, errorNotification } from '../providers/notification-provider';

  import RelayCard from '../user-controls/RelayCard.svelte';

  let relays = [];

  const { confirmModal } = getContext('confirm');

  const loadData = () => {
    fetchRelays(false, (data) => (relays = data));
  };

  const deleteRelayAction = (relay) => {
    confirmModal(
      $_('relays.delete.confirm.message', {
        default: "Are you sure you want to delete the relay ''{name}''?",
        values: { name: relay.name },
      }),
      async () => {
        try {
          await deleteRelay(relay.id);
          successNotification(
            $_('relays.delete.ok.message', { default: "The relay ''{name}'' is deleted.", values: { name: relay.name } }),
            $_('notification.delete.ok.title', { default: 'OK' })
          );
          loadData();
        } catch (e) {
          errorNotification(
            $_('relays.delete.error.message', {
              default: "The relay ''{name}'' could not be deleted!\nError: {error}",
              values: { name: relay.name, error: e.message },
            }),
            $_('notification.delete.error.title', { default: 'ERROR' })
          );
        }
      }
    );
  };

  const ignoreRelayAction = (relay) => {
    confirmModal(
      $_('relays.confirm.ignore.message', {
        default: "Are you sure you want to ignore the relay ''{name}''?",
        values: { name: relay.name },
      }),
      async () => {
        try {
          await updateSystemSettings({ exclude_ids: relay.id });
          successNotification(
            $_('relays.exclude.ok.message', { default: "The relay ''{name}'' is ignored.", values: { name: relay.name } }),
            $_('notification.exclude.ok.title', { default: 'OK' })
          );
          loadData();
        } catch (e) {
          errorNotification(
            $_('relays.exclude.error.message', {
              default: "The relay ''{name}'' could not be ignored!\nError: {error}",
              values: { name: relay.name, error: e.message },
            }),
            $_('notification.exclude.error.title', { default: 'ERROR' })
          );
        }
      }
    );
  };

  const replaceHardware = (relay) => {};

  const relayManualMode = (relay) => {
    confirmModal(
      $_('relays.confirm.manual_mode.message', { default: "Toggle manual mode for relay ''{name}''?", values: { name: relay.name } }),
      async () => {
        try {
          await manualRelay(relay.id);
          successNotification(
            $_('relays.manual_mode.ok.message', {
              default: "The manual mode for relay ''{name}'' is changed.",
              values: { name: relay.name },
            }),
            $_('notification.manual_mode.ok.title', { default: 'OK' })
          );
          loadData();
        } catch (e) {
          errorNotification(
            $_('relays.manual_mode.error.message', {
              default: "Error changing manual mode for relay ''{name}''.\nError: {error}",
              values: { name: relay.name, error: e.message },
            }),
            $_('notification.manual_mode.error.title', { default: 'ERROR' })
          );
        }
      }
    );
  };

  const toggleRelayAction = async (relay, state) => {
    try {
      let result = '';
      if (relay.dimmer) {
        await dimRelay(relay.id, state, (data) => (result = data));
      } else {
        await toggleRelay(relay.id, (data) => (result = data));
      }
      result = relay.dimmer ? result.value + '%' : result.value > 0 ? 'on' : 'off';
      successNotification(
        $_('relays.toggle.ok.message', {
          default: "Toggled relay ''{name}'' to state {value}",
          values: { name: relay.name, value: result },
        }),
        $_('notification.toggle.ok.title', { default: 'OK' })
      );
    } catch (e) {
      errorNotification(
        $_('relays.toggle.error.message', {
          default: "Error toggling relay ''{name}''.\nError: {error}",
          values: { name: relay.name, error: e.message },
        }),
        $_('notification.toggle.error.title', { default: 'ERROR' })
      );
    }
  };

  setContext('relayActions', {
    toggleAction: (relay, state) => toggleRelayAction(relay, state),
    deleteAction: (relay) => deleteRelayAction(relay),
    ignoreAction: (relay) => ignoreRelayAction(relay),
    replaceAction: (relay) => replaceHardware(relay),
    manualAction: (relay) => relayManualMode(relay),
  });

  onMount(() => {
    setCustomPageTitle($_('relays.title', { default: 'Relays' }));
    loadData();
  });

  onDestroy(() => {
    customPageTitleUsed.set(false);
  });
</script>

<PageHeader>
  {$_(`relays.title`)}
</PageHeader>
<div class="container-fluid">
  <div class="row">
    {#if relays.length > 0}
      <!-- Sort based on translated names -->
      {#each relays.sort((a, b) => a.name.localeCompare(b.name)) as relay}
        <div class="col-12">
          <RelayCard relay="{relay}" />
        </div>
      {/each}
    {/if}
  </div>
</div>
