<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import { writable } from 'svelte/store';
  import { _ } from 'svelte-i18n';
  import { createForm } from 'felte';

  import { fetchButtons, fetchButtonsHardware, updateButton } from '../providers/api';
  import { successNotification, errorNotification } from '../providers/notification-provider';
  import { formToJSON, invalid_form_fields } from '../helpers/form-helpers';

  import ModalForm from '../user-controls/ModalForm.svelte';
  import Field from '../components/form/Field.svelte';
  import Helper from '../components/form/Helper.svelte';
  import Select from '../components/form/Select.svelte';
  import Switch from '../components/form/Switch.svelte';

  let wrapper_show;
  let wrapper_hide;
  let loading = null;
  let validated = false;

  let hardware = [];
  let calibration = true;
  let selected_hardware = null;
  let formData = writable({});

  let editForm;

  const dispatch = createEventDispatcher();

  const successAction = () => {
    dispatch('save');
  };

  const hardwareType = (hardware) => {
    selected_hardware = hardware;
  };

  const _processForm = async (values, context) => {
    validated = true;

    if (context.form.checkValidity()) {
      loading = true;
      values = formToJSON(editForm);
      values.address += '';
      delete values.value;

      try {
        // Post data
        await updateButton(values, (data) => (values = data));
        // Notifify OK!
        successNotification(
          $_('buttons.settings.save.ok.message', { default: "Button ''{name}'' is updated", values: { name: values.name } }),
          $_('notification.form.save.ok.title', { default: 'Save OK' })
        );

        // Done, close window
        hide();

        // Signal the save callback
        successAction();
      } catch (error) {
        // Some kind of an error
        loading = false;
        errorNotification(error.message, $_('notification.form.save.error.title', { default: 'Save Error' }));
      } finally {
        // Cleanup
        validated = false;
      }
    } else {
      let error_message = $_('buttons.settings.save.error.required_fields', { default: 'Not all required fields are entered correctly.' });
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

  export const show = async (buttonId, cb) => {
    // Anonymous (Async) functions always as first!!
    (async () => {
      // Load all avaliable hardware
      await fetchButtonsHardware(
        (data) =>
          (hardware = data.map((item) => {
            return { value: item.hardware, text: item.name };
          }))
      );

      // If ID is given, load existing data
      if (buttonId) {
        // Load existing button data and fill form data
        await fetchButtons(buttonId, (data) => ($formData = data));
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
    <i class="fas fa-thumbtack mr-2"></i>
    {$_('buttons.settings.title', { default: 'Button settings' })}
    <Helper moreInfo="https://theyosh.github.io/TerrariumPI/setup/#buttons" />
  </svelte:fragment>

  <form class="needs-validation" class:was-validated="{validated}" use:form bind:this="{editForm}">
    <input type="hidden" name="id" disabled="{$formData.id && $formData.id !== '' ? null : true}" />

    <div class="row">
      <div class="col-12 col-sm-6 col-md-4 col-lg-3">
        <Select
          name="hardware"
          value="{$formData.hardware}"
          readonly="{$formData.id && $formData.id !== ''}"
          on:change="{(value) => hardwareType(value.detail)}"
          required="{true}"
          options="{hardware}"
          label="{$_('buttons.settings.hardware.label', { default: 'Hardware' })}"
          placeholder="{$_('buttons.settings.hardware.placeholder', { default: 'Select hardware' })}"
          help="{$_('buttons.settings.hardware.help', { default: 'Select the hardware type for this button.' })}"
          invalid="{$_('buttons.settings.hardware.invalid', { default: 'Please select a hardware type.' })}" />
      </div>
      <div class="col-12 col-sm-12 col-md-4 col-lg-4">
        <Field
          type="text"
          name="address"
          required="{true}"
          label="{$_('buttons.settings.address.label', { default: 'Address' })}"
          placeholder="{$_('buttons.settings.address.placeholder', { default: 'Enter an address' })}"
          help="{$_('buttons.settings.address.help', { default: 'Enter the phisycal GPIO pin number.' })}"
          invalid="{$_('buttons.settings.address.invalid', {
            default: 'The entered address is not valid. Enter a valid number between {min} and {max}.',
            values: { min: 1, max: 40 },
          })}" />
      </div>
      <div class="col-10 col-sm-10 col-md-8 col-lg-3">
        <Field
          type="text"
          name="name"
          required="{true}"
          label="{$_('buttons.settings.name.label', { default: 'Name' })}"
          placeholder="{$_('buttons.settings.name.placeholder', { default: 'Enter a name' })}"
          help="{$_('buttons.settings.name.help', { default: 'Enter an easy to remember name.' })}"
          invalid="{$_('buttons.settings.name.invalid', { default: 'The entered name is not valid. It cannot be empty.' })}" />
      </div>
      <div class="col-2 col-sm-2 col-md-4 col-lg-2">
        <Field
          type="text"
          name="value"
          readonly
          label="{$_('buttons.settings.current.label', { default: 'Current' })}"
          placeholder="{$_('buttons.settings.current.placeholder', { default: 'Current value' })}"
          help="{$_('buttons.settings.current.help', { default: 'The current state of the button.' })}" />
      </div>
    </div>
    <div class="row button_callibration" class:d-block="{calibration}" class:d-none="{!calibration}">
      <a
        data-toggle="collapse"
        href="#button_callibration"
        role="button"
        aria-expanded="false"
        aria-controls="button_callibration"
        class:d-none="{!calibration}">
        <hr class="hr-text" data-content="calibration" />
      </a>
      <div class="col">
        <div class="collapse row pt-3" id="button_callibration">
            <div class="col-6 col-sm-6 col-md-6 col-lg-3">
                <Switch
                  name="calibration.inverse"
                  value={$formData.calibration?.inverse}
                  label="{$_('buttons.settings.calibration.inverse.label', { default: 'Inverse value' })}"
                  help="{$_('buttons.settings.calibration.inverse.help', {
                    default: 'Toggle to inverse the remote value.',
                  })}" />
            </div>
            <div class="col-6 col-sm-6 col-md-6 col-lg-3"  class:d-none={selected_hardware !== 'ldr'}>
              <Field
                type="number"
                name="calibration.ldr_capacitor"
                min="1"
                max="100"
                required={selected_hardware === 'ldr'}
                disabled={selected_hardware !== 'ldr'}
                label="{$_('buttons.settings.calibration.ldr_capacitor.label', { default: 'Capacitor value in µF' })}"
                placeholder="{$_('buttons.settings.calibration.ldr_capacitor.placeholder', { default: 'Enter the capacitor value in µF' })}"
                help="{$_('buttons.settings.calibration.ldr_capacitor.help', {
                  default: 'Enter the capacitor value in µF as this will influence the light calculation.',
                })}"
                invalid="{$_('buttons.settings.calibration.ldr_capacitor.invalid', {
                  default: 'The entered capacitor value is not valid. Enter a valid number between {min} and {max}.',
                  values: { min: 1, max: 100 },
                })}" />
            </div>
            <div class="col-6 col-sm-6 col-md-6 col-lg-4" class:d-none={selected_hardware !== 'remote'}>
              <Field
                type="number"
                name="calibration.timeout"
                min="1"
                max="100"
                disabled={selected_hardware !== 'remote'}
                label="{$_('buttons.settings.calibration.timeout.label', { default: 'Time out in seconds' })}"
                placeholder="{$_('buttons.settings.calibration.timeout.placeholder', { default: 'Enter the time out in seconds' })}"
                help="{$_('buttons.settings.calibration.timeout.help', {
                  default: 'Enter the timeout in seconds between remote checks.',
                })}"
                invalid="{$_('buttons.settings.calibration.timeout.invalid', {
                  default: 'The entered timeout value is not valid. Enter a valid number between {min} and {max}.',
                  values: { min: 1, max: 100 },
                })}" />
            </div>
        </div>
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
