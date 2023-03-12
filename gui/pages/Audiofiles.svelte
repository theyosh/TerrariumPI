<script>
  import { dayjs } from 'svelte-time';
  import duration from 'dayjs/esm/plugin/duration';
  dayjs.extend(duration);
  import { onMount, onDestroy, getContext } from 'svelte';
  import { _ } from 'svelte-i18n';
  import { PageHeader, FileInput } from 'svelte-adminlte';

  import { locale } from '../locale/i18n';
  import { setCustomPageTitle, customPageTitleUsed } from '../stores/page-title';
  import { isAuthenticated } from '../stores/authentication';
  import { ApiUrl } from '../constants/urls';
  import { fetchAudiofiles, deleteAudioFile } from '../providers/api';
  import { formatBytes } from '../helpers/file-size-helpers';
  import { errorNotification, successNotification } from '../providers/notification-provider';
  import { isDay } from '../stores/terrariumpi';

  import Card from '../user-controls/Card.svelte';
  import Player from '../components/common/Player.svelte';

  let audiofiles = [];
  let loading = true;
  let dataTable;
  let fileUploader;
  let percent_completed = 0;

  const { confirmModal } = getContext('confirm');

  const loadData = async () => {
    loading = true;
    if (dataTable) {
      dataTable.destroy();
    }
    await fetchAudiofiles((data) => (audiofiles = data));
    dataTable = jQuery('#audio_files').DataTable({
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

  const deleteAudiofileAction = (audiofile) => {
    confirmModal(
      $_('audio.files.delete.confirm.message', {
        default: "Are you sure to delete audio file ''{name}'' ({filename})?",
        values: { name: audiofile.name, filename: audiofile.filename },
      }),
      async () => {
        try {
          await deleteAudioFile(audiofile.id);
          successNotification(
            $_('audio.files.delete.ok.message', { default: "The audio file ''{name}'' is deleted.", values: { name: audiofile.name } }),
            $_('notification.delete.ok.title')
          );
          loadData();
        } catch (e) {
          errorNotification(
            $_('audio.files.delete.error.message', {
              default: "The audio file ''{name}'' could not be deleted!\nError: {error}",
              values: { name: audiofile.name, error: e.message },
            }),
            $_('notification.delete.error.title')
          );
        }
      }
    );
  };

  const uploadFiles = async (files) => {
    if (!$isAuthenticated) {
      let error_message = $_('audio.files.settings.upload.error.nologin', { default: 'Please login to upload files.' });
      errorNotification(error_message, $_('notification.form.upload.error.title', { default: 'Upload Error' }));
      return;
    }

    if (!fileUploader.isValid()) {
      let error_message = $_('audio.files.settings.save.error.invalid_file', { default: 'Invalid audio file(s)' });
      errorNotification(error_message, $_('notification.form.save.error.title', { default: 'Save Error' }));
      return;
    }

    let formData = new FormData();
    for (let i = 0; i < files.detail.length; i++) {
      formData.append('audiofiles', files.detail[i]);
    }

    let request = new XMLHttpRequest();
    request.open('POST', `${ApiUrl}/api/audio/files/`);
    request.withCredentials = true;

    // upload progress event
    request.upload.addEventListener('progress', function (e) {
      // upload progress as percentage
      percent_completed = (e.loaded / e.total) * 100;
    });

    // request finished event
    request.addEventListener('load', (e) => {
      switch (request.status) {
        case 200:
          successNotification(
            $_('audio.files.settings.save.ok.message', {
              default: 'Uploaded {amount, plural, =1 {# audio file} other {# audio files}}',
              values: { amount: files.detail.length },
            }),
            $_('notification.form.save.ok.title', { default: 'Save OK' })
          );
          percent_completed = 0;
          loadData();
          break;
        default:
          errorNotification(request.response, $_('notification.form.save.error.title', { default: 'Save Error' }));
          break;
      }
    });

    // send POST request to server
    request.send(formData);
  };

  onMount(() => {
    setCustomPageTitle($_('audio.files.title', { default: 'Audio files' }));
    loadData();
  });

  onDestroy(() => {
    customPageTitleUsed.set(false);
  });
</script>

<PageHeader>
  {$_('audio.files.title', { default: 'Audio files' })}
</PageHeader>
<div class="container-fluid">
  <div class="row">
    <div class="col-12">
      <Card loading="{loading}" noTools="{true}">
        <table id="audio_files" class="table table-bordered table-striped table-hover">
          <thead>
            <tr>
              <th>{$_('table.header.name', { default: 'Name' })}</th>
              <th>{$_('table.header.duration', { default: 'Duration' })}</th>
              <th>{$_('table.header.filename', { default: 'File name' })}</th>
              <th>{$_('table.header.filesize', { default: 'File size' })}</th>
              <th class="no-sort">{$_('table.header.actions', { default: 'Actions' })}</th>
            </tr>
          </thead>
          <tbody>
            {#each audiofiles as audiofile}
              <tr>
                <td>{audiofile.name}</td>
                <td data-order="{audiofile.duration}"
                  >{dayjs.duration(audiofile.duration * 1000).format(audiofile.duration > 3600 ? 'H:mm:ss' : 'm:ss')}</td>
                <td>{audiofile.filename.split('/').pop()}</td>
                <td data-order="{audiofile.filesize}">{formatBytes(audiofile.filesize)}</td>
                <td class="d-flex justify-content-around">
                  <Player src="{ApiUrl}/media/{audiofile.filename.split('/').pop()}" />
                  {#if $isAuthenticated}
                    <button
                      class="btn btn-sm"
                      class:btn-light="{$isDay}"
                      class:btn-dark="{!$isDay}"
                      on:click="{() => deleteAudiofileAction(audiofile)}">
                      <i class="fas fa-trash-alt text-danger"></i>
                    </button>
                  {/if}
                </td>
              </tr>
            {/each}
          </tbody>
          <tfoot>
            <tr>
              <th>{$_('table.header.name', { default: 'Name' })}</th>
              <th>{$_('table.header.duration', { default: 'Duration' })}</th>
              <th>{$_('table.header.filename', { default: 'File name' })}</th>
              <th>{$_('table.header.filesize', { default: 'File size' })}</th>
              <th class="no-sort">{$_('table.header.actions', { default: 'Actions' })}</th>
            </tr>
          </tfoot>
        </table>
        <div class:disabled="{!$isAuthenticated}">
          <div class="input-group mt-3">
            <div class="input-group-prepend">
              <span class="input-group-text" id="upload_new_file_label"
                >{$_('audio.files.settings.audiofiles.label', { default: 'Upload new audio file' })}</span>
            </div>
            <FileInput
              on:input="{uploadFiles}"
              bind:this="{fileUploader}"
              readonly="{!$isAuthenticated}"
              placeholder="{$_('audio.files.settings.audiofiles.placeholder', { default: 'Upload new audio file' })}"
              name="audiofiles"
              id="audiofiles"
              pattern="/.*\.(?:aac|mp3|ogg|wav|m4a|flac)$/i"
              multiple>{$_('audio.files.settings.audiofiles.placeholder', { default: 'Upload new audio file' })}</FileInput>
          </div>
          <div class="progress progress-xs active mt-2 upload_progress">
            <div
              class="progress-bar bg-success progress-bar-striped"
              role="progressbar"
              aria-valuenow="{percent_completed}"
              aria-valuemin="0"
              aria-valuemax="100"
              style="width: {percent_completed}%">
              <span class="sr-only"></span>
            </div>
          </div>
        </div>
      </Card>
    </div>
  </div>
</div>
