<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import { writable } from 'svelte/store';
  import { _ } from 'svelte-i18n';
  import { createForm } from 'felte';

  import { fetchButtons, fetchWebcams, fetchEnclosures, updateEnclosure, uploadFile } from '../providers/api';
  import { successNotification, errorNotification } from '../providers/notification-provider';
  import { formToJSON, invalid_form_fields } from '../helpers/form-helpers';

  import ModalForm from '../user-controls/ModalForm.svelte';
  import Field from '../components/form/Field.svelte';
  import Helper from '../components/form/Helper.svelte';
  import Select from '../components/form/Select.svelte';
  import WysiwygArea from '../components/form/WysiwygArea.svelte';
  import FileUpload from '../components/form/FileUpload.svelte';

  let wrapper_show;
  let wrapper_hide;
  let loading = false;
  let validated = false;

  let doors = [];
  let webcams = [];
  let formData = writable({});

  let editForm;

  const dispatch = createEventDispatcher();

  const successAction = () => {
    dispatch('save');
  };

  async function _processForm(values, context) {
    validated = true;

    if (context.form.checkValidity()) {
      loading = true;
      values = formToJSON(editForm);

      if (values.file_image) {
        // Upload first image to make sure it is valid
        try {
          values.image = await uploadFile(context.form.file_image);
          values.delete_image = false;
        } catch (error) {
          errorNotification(error.message, $_('notification.form.save.error.title', { default: 'Save Error' }));

          loading = false;
          validated = false;

          // Return to current form
          return;
        }
      }

      delete values.areas;
      delete values.file_image;

      try {
        // Post data
        await updateEnclosure(values, (data) => (values = data));
        // Notifify OK!
        successNotification(
          $_('enclosures.settings.save.ok.message', { default: "Enclosure ''{name}'' is updated", values: { name: values.name } }),
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
      let error_message = $_('enclosures.settings.save.error.required_fields', {
        default: 'Not all required fields are entered correctly.',
      });
      error_message += "\n'" + invalid_form_fields(editForm).join("'\n'") + "'";
      errorNotification(error_message, $_('notification.form.save.error.title', { default: 'Save Error' }));
    }
  }

  const { form, setFields, isSubmitting, createSubmitHandler, reset } = createForm({
    onSubmit: _processForm,
  });

  const formSubmit = createSubmitHandler({
    onSubmit: _processForm,
  });

  export const show = async (enclosureId, cb) => {
    // Anonymous (Async) functions always as first!!
    (async () => {
      // Load all doors and webcams
      await Promise.all([
        fetchButtons(
          false,
          (data) =>
            (doors = data.map((item) => {
              return { value: item.id, text: item.name };
            }))
        ),
        fetchWebcams(
          false,
          (data) =>
            (webcams = data.map((item) => {
              return { value: item.id, text: item.name };
            }))
        ),
      ]);

      // If ID is given, load existing data
      if (enclosureId) {
        await fetchEnclosures(enclosureId, (data) => {
          data.doors = data.doors.map((item) => {
            return item.id;
          });
          data.webcams = data.webcams.map((item) => {
            return item.id;
          });
          $formData = data;
        });
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
    <i class="fas fa-globe mr-2"></i>
    {$_('enclosures.settings.title', { default: 'Enclosure settings' })}
    <Helper moreInfo="https://theyosh.github.io/TerrariumPI/setup/#enclosures" />
  </svelte:fragment>

  <form class="needs-validation" class:was-validated="{validated}" use:form bind:this="{editForm}">
    <input type="hidden" name="id" disabled="{$formData.id && $formData.id !== '' ? null : true}" />

    <div class="row">
      <div class="col-12 col-sm-6 col-md-6 col-lg-6">
        <Field
          type="text"
          name="name"
          required="{true}"
          label="{$_('enclosures.settings.name.label', { default: 'Name' })}"
          placeholder="{$_('enclosures.settings.name.placeholder', { default: 'Enter a name' })}"
          help="{$_('enclosures.settings.name.help', { default: 'Enter an easy to remember name.' })}"
          invalid="{$_('enclosures.settings.name.invalid', { default: 'The entered name is not valid. It cannot be empty.' })}" />
      </div>
      <div class="col-12 col-sm-6 col-md-6 col-lg-6">
        <FileUpload
          name="image"
          value="{$formData.image}"
          accept="image/*"
          label="{$_('enclosures.settings.image.label', { default: 'Image' })}"
          placeholder="{$_('enclosures.settings.image.placeholder', { default: 'Select an image file' })}"
          help="{$_('enclosures.settings.image.help', { default: 'Upload a JPG or PNG.' })}"
          invalid="{$_('enclosures.settings.image.invalid', { default: 'The selected file is not valid. It is not an image file.' })}" />
      </div>
    </div>
    <div class="row">
      <div class="col-12 col-sm-12 col-md-9 col-lg-9">
        <WysiwygArea
          name="description"
          value="{$formData.description}"
          label="{$_('enclosures.settings.description.label', { default: 'Description' })}"
          placeholder="{$_('enclosures.settings.description.placeholder', { default: 'Enter a description' })}"
          help="{$_('enclosures.settings.description.help', { default: 'Enter some description text about this enclosure.' })}" />
      </div>
      <div class="col-12 col-sm-12 col-md-3 col-lg-3">
        <Select
          name="doors"
          value="{$formData.doors}"
          multiple="{true}"
          options="{doors}"
          label="{$_('enclosures.settings.doors.label', { default: 'Doors' })}"
          help="{$_('enclosures.settings.doors.help', { default: 'Select the door(s) for this enclosure.' })}" />
        <Select
          name="webcams"
          value="{$formData.webcams}"
          multiple="{true}"
          options="{webcams}"
          label="{$_('enclosures.settings.webcams.label', { default: 'Webcams' })}"
          help="{$_('enclosures.settings.webcams.help', { default: 'Select the webcam(s) for this enclosure.' })}" />
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
