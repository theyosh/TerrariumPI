<script>
  import { onDestroy, onMount, getContext } from 'svelte';
  import { _ } from 'svelte-i18n';
  import { PageHeader } from 'svelte-adminlte';
  import { dayjs } from 'svelte-time';
  import duration from 'dayjs/esm/plugin/duration';
  dayjs.extend(duration);

  import { locale } from '../locale/i18n';
  import { setCustomPageTitle, customPageTitleUsed } from '../stores/page-title';
  import { isAuthenticated } from '../stores/authentication';
  import { fetchPlaylists, deletePlaylist } from '../providers/api';
  import { successNotification, errorNotification } from '../providers/notification-provider';
  import { isDay } from '../stores/terrariumpi';

  import Card from '../user-controls/Card.svelte';

  const { editPlaylist } = getContext('modals');

  const loadData = async () => {
    loading = true;
    if (dataTable) {
      dataTable.destroy();
    }
    await fetchPlaylists(false, (data) => (playlists = data));
    dataTable = jQuery('#playlists').DataTable({
      language: {
        url: `//cdn.datatables.net/plug-ins/1.12.1/i18n/${$locale}.json`,
      },
      columnDefs: [
        {
          targets: 'no-sort',
          orderable: false,
        },
      ],
    });
    loading = false;
  };

  const { confirmModal } = getContext('confirm');

  const deletePlaylistAction = (playlist) => {
    confirmModal(
      $_('audio.playlists.delete.confirm.message', {
        default: "Are you sure to delete the playlist ''{name}'' with {length} numbers?",
        values: { name: playlist.name, length: playlist.length },
      }),
      async () => {
        try {
          await deletePlaylist(playlist.id);
          successNotification(
            $_('audio.playlists.delete.ok.message', { default: "The playlist ''{name}'' is deleted.", values: { name: playlist.name } }),
            $_('notification.delete.ok.title')
          );
          loadData();
        } catch (e) {
          errorNotification(
            $_('audio.playlists.delete.error.message', {
              default: "The playlist ''{name}'' could not be deleted!\nError: {error}",
              values: { name: playlist.name, error: e.message },
            }),
            $_('notification.delete.error.title')
          );
        }
      }
    );
  };

  let playlists = [];
  let loading = true;
  let dataTable;

  onMount(() => {
    setCustomPageTitle($_('audio.playlists.title', { default: 'Playlists' }));
    loadData();
  });

  onDestroy(() => {
    customPageTitleUsed.set(false);
  });
</script>

<PageHeader>
  {$_('audio.playlists.title', { default: 'Playlists' })}
</PageHeader>
<div class="container-fluid">
  <div class="row">
    <div class="col-12">
      <Card loading="{loading}" noTools="{true}">
        <table id="playlists" class="table table-bordered table-striped table-hover">
          <thead>
            <tr>
              <th>{$_('table.header.name', { default: 'Name' })}</th>
              <th>{$_('table.header.duration', { default: 'Duration' })}</th>
              <th>{$_('table.header.number_files', { default: '# Files' })}</th>
              <th>{$_('table.header.volume', { default: 'Audio volume' })}</th>
              <th>{$_('table.header.shuffle', { default: 'Shuffle' })}</th>
              <th>{$_('table.header.repeat', { default: 'Repeat' })}</th>
              {#if $isAuthenticated}
                <th class="no-sort">{$_('table.header.actions', { default: 'Actions' })}</th>
              {/if}
            </tr>
          </thead>
          <tbody>
            {#each playlists as playlist}
              <tr>
                <td>{playlist.name}</td>
                <td data-order="{playlist.duration}">{dayjs.duration(playlist.duration * 1000).humanize()}</td>
                <td>{playlist.length}</td>
                <td>{playlist.volume}</td>
                <td data-order="{playlist.shuffle ? 1 : 0}"
                  ><i class="fas" class:fa-check="{playlist.shuffle}" class:fa-times="{!playlist.shuffle}"> </i></td>
                <td data-order="{playlist.repeat ? 1 : 0}"
                  ><i class="fas" class:fa-check="{playlist.repeat}" class:fa-times="{!playlist.repeat}"> </i></td>
                {#if $isAuthenticated}
                  <td class="d-flex justify-content-around">
                    <button
                      class="btn btn-sm"
                      class:btn-light="{$isDay}"
                      class:btn-dark="{!$isDay}"
                      on:click="{() => editPlaylist(playlist)}">
                      <i class="fas fa-wrench"></i>
                    </button>
                    <button
                      class="btn btn-sm"
                      class:btn-light="{$isDay}"
                      class:btn-dark="{!$isDay}"
                      on:click="{() => deletePlaylistAction(playlist)}">
                      <i class="fas fa-trash-alt text-danger"></i>
                    </button>
                  </td>
                {/if}
              </tr>
            {/each}
          </tbody>
          <tfoot>
            <tr>
              <th>{$_('table.header.name', { default: 'Name' })}</th>
              <th>{$_('table.header.duration', { default: 'Duration' })}</th>
              <th>{$_('table.header.number_files', { default: '# Files' })}</th>
              <th>{$_('table.header.volume', { default: 'Audio volume' })}</th>
              <th>{$_('table.header.shuffle', { default: 'Shuffle' })}</th>
              <th>{$_('table.header.repeat', { default: 'Repeat' })}</th>
              {#if $isAuthenticated}
                <th class="no-sort">{$_('table.header.actions', { default: 'Actions' })}</th>
              {/if}
            </tr>
          </tfoot>
        </table>
      </Card>
    </div>
  </div>
</div>
