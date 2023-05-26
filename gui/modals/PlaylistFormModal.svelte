<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import { writable } from 'svelte/store';
  import { _ } from 'svelte-i18n';
  import { createForm } from 'felte';

  import { fetchAudiofiles, fetchPlaylists, updatePlaylist } from '../providers/api';
  import { successNotification, errorNotification } from '../providers/notification-provider';
  import { formToJSON, invalid_form_fields } from '../helpers/form-helpers';

  import ModalForm from '../user-controls/ModalForm.svelte';
  import Field from '../components/form/Field.svelte';
  import Helper from '../components/form/Helper.svelte';
  import Select from '../components/form/Select.svelte';
  import Switch from '../components/form/Switch.svelte';
  import Slider from '../components/form/Slider.svelte';

  let wrapper_show;
  let wrapper_hide;
  let loading = false;
  let validated = false;

  let songs = [];
  let formData = writable({});

  let editForm;

  const formatter = (value) => {
    return $_('audio.playlists.settings.volume.formatter', { default: "Volume level {value}", values: { value: value } });
  };

  const dispatch = createEventDispatcher();

  const successAction = () => {
    dispatch('save');
  };

  const _processForm = async (values, context) => {
    validated = true;

    if (context.form.checkValidity()) {
      loading = true;
      values = formToJSON(editForm);

      // Delete generated attributes from object
      delete values.duration;
      delete values.length;

      try {
        // Post data
        await updatePlaylist(values, (data) => (values = data));
        // Notifify OK!
        successNotification(
          $_('audio.playlists.settings.save.ok.message', { default: "Playlist ''{name}'' is updated", values: { name: values.name } }),
          $_('notification.form.save.ok.title', { default: 'Save OK' })
        );

        // Done, close window
        hide();

        // Signal the save callback
        successAction();

        // TODO: Somehow, either the save signal callback or here, we have to reload the buttons
      } catch (error) {
        // Some kind of an error
        loading = false;
        errorNotification(error.message, $_('notification.form.save.error.title', { default: 'Save Error' }));
      } finally {
        // Cleanup
        validated = false;
      }
    } else {
      let error_message = $_('audio.playlists.settings.save.error.required_fields', {
        default: 'Not all required fields are entered correctly.',
      });
      error_message += "\n'" + invalid_form_fields(editForm).join("'\n'") + "'";
      errorNotification(error_message, $_('notification.form.save.error.title', { default: 'Save Error' }));
    }
  };

  const { form, setFields, isSubmitting, createSubmitHandler, reset } = createForm({
    onSubmit: _processForm,
  });

  const formSubmit = createSubmitHandler({
    onSubmit: _processForm,
  });

  export const show = (playlistId, cb) => {
    // Anonymous (Async) functions always as first!!
    (async () => {
      // Load all avaliable hardware
      await fetchAudiofiles(
        (data) =>
          (songs = data.map((item) => {
            return { value: item.id, text: item.name + '(' + item.filename.split('/').pop() + ')' };
          }))
      );

      // If ID is given, load existing data
      if (playlistId) {
        await fetchPlaylists(playlistId, (data) => ($formData = data));
        setFields($formData);
      }

      // Loading done
      loading = false;
    })();

    // Reset form validation
    reset();
    $formData = formToJSON(editForm);
    validated = false;

    // Toggle loading div
    loading = true;

    // Show the modal
    wrapper_show();
  };

  export const hide = () => {
    // Delay the loading div
    setTimeout(() => {
      loading = false;
    }, 1000);

    // Hide modal
    wrapper_hide();
  };

  onMount(() => {
    editForm.setAttribute('novalidate', 'novalidate');
  });
</script>

<ModalForm bind:show="{wrapper_show}" bind:hide="{wrapper_hide}" loading="{loading}">
  <svelte:fragment slot="header">
    <i class="fas fa-play mr-2"></i>
    {$_('audio.playlists.settings.title', { default: 'Playlist settings' })}
    <Helper moreInfo="https://theyosh.github.io/TerrariumPI/setup/#playlists" />
  </svelte:fragment>

  <form class="needs-validation" class:was-validated="{validated}" use:form bind:this="{editForm}">
    <input type="hidden" name="id" disabled="{$formData.id && $formData.id !== '' ? null : true}" />

    <div class="row">
      <div class="col-10 col-sm-10 col-md-8 col-lg-4">
        <Field
          type="text"
          name="name"
          required="{true}"
          label="{$_('audio.playlists.settings.name.label', { default: 'Name' })}"
          placeholder="{$_('audio.playlists.settings.name.placeholder', { default: 'Enter a name' })}"
          help="{$_('audio.playlists.settings.name.help', { default: 'Enter an easy to remember name.' })}"
          invalid="{$_('audio.playlists.settings.name.invalid', { default: 'The entered name is not valid. It cannot be empty.' })}" />
      </div>
      <div class="col-10 col-sm-10 col-md-8 col-lg-4">
        <Slider
          name="volume"
          required="{true}"
          value="{$formData.volume && $formData.volume !== '' ? $formData.volume : 0}"
          formatter={formatter}
          label="{$_('audio.playlists.settings.volume.label', { default: 'Audio volume' })}"
          help="{$_('audio.playlists.settings.volume.help', { default: 'Select the volume for this playlist.' })}" />
      </div>
      <div class="col-10 col-sm-10 col-md-8 col-lg-2">
        <Switch
          name="shuffle"
          value="{$formData.shuffle}"
          label="{$_('audio.playlists.settings.shuffle.label', { default: 'Shuffle' })}"
          help="{$_('audio.playlists.settings.shuffle.help', { default: 'Shuffle this playlist every time it is played.' })}" />
      </div>
      <div class="col-10 col-sm-10 col-md-8 col-lg-2">
        <Switch
          name="repeat"
          value="{$formData.repeat}"
          label="{$_('audio.playlists.settings.repeat.label', { default: 'Repeat' })}"
          help="{$_('audio.playlists.settings.repeat.help', { default: 'Play this playlist in repeat mode.' })}" />
      </div>
      <div class="col-12 col-sm-12 col-md-12 col-lg-12">
        <Select
          name="files"
          value="{$formData.files}"
          required="{true}"
          multiple="{true}"
          options="{songs}"
          label="{$_('audio.playlists.settings.files.label', { default: 'Audio files' })}"
          placeholder="{$_('audio.playlists.settings.files.placeholder', { default: 'Select audio files' })}"
          help="{$_('audio.playlists.settings.files.help', { default: 'Select all audio files for this playlist.' })}"
          invalid="{$_('audio.playlists.settings.files.invalid', { default: 'Select at least 1 audio file.' })}" />
      </div>
    </div>
    <!-- We need this nasty hack to make submit with enter key to work -->
    <button type="submit" style="display:none"> </button>
  </form>

  <svelte:fragment slot="actions">
    <button type="button" class="btn btn-primary" disabled="{loading || $isSubmitting}" on:click="{formSubmit}">
      <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" class:d-none="{!$isSubmitting}"></span>
      {$_('modal.general.save', { default: 'Save' })}
    </button>
  </svelte:fragment>
</ModalForm>
