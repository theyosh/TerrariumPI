<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import { writable } from 'svelte/store';
  import { _ } from 'svelte-i18n';
  import { createForm } from 'felte';

  import { fetchRelays, fetchRelaysHardware, updateRelay } from '../providers/api';
  import { successNotification, errorNotification } from '../providers/notification-provider';
  import { formToJSON, invalid_form_fields } from '../helpers/form-helpers';

  import ModalForm from '../user-controls/ModalForm.svelte';
  import Field from '../components/form/Field.svelte';
  import Helper from '../components/form/Helper.svelte';
  import Select from '../components/form/Select.svelte';

  let wrapper_show;
  let wrapper_hide;
  let loading = false;
  let validated = false;

  let hardware = [];

  let calibration = false;
  let hardware_type = null;
  let formData = writable({});

  let editForm;

  const dispatch = createEventDispatcher();

  const successAction = () => {
    dispatch('save');
  };

  const hardwareType = (hardware) => {
    hardware_type = hardware;
    if (hardware_type === 'brightpi-dimmer') {
      // Change to a fixed default value
      editForm.elements['address'].value = 'fixed';
    }
    calibration = hardware_type.endsWith('-dimmer');
  };

  const _processForm = async (values, context) => {
    validated = true;

    if (context.form.checkValidity()) {
      loading = true;
      values = formToJSON(editForm);
      values.address += '';

      delete values.value;
      delete values.dimmer;

      // If all items of the calibration object are empty, then reset the complete calibration object.
      if (!Object.values(values.calibration).some(Boolean)) {
        values.calibration = {};
      }

      try {
        // Post data
        await updateRelay(values, (data) => (values = data));
        // Notifify OK!
        successNotification(
          $_('relays.settings.save.ok.message', { default: "Relay ''{name}'' is updated", values: { name: values.name } }),
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
        validated = false;
      }
    } else {
      let error_message = $_('relays.settings.save.error.required_fields', { default: 'Not all required fields are entered correctly.' });
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

  export const show = (relayId, cb) => {
    // Anonymous (Async) functions always as first!!
    (async () => {
      // Load all avaliable hardware
      await fetchRelaysHardware(
        (data) =>
          (hardware = data.map((item) => {
            return { value: item.hardware, text: item.name };
          }))
      );

      // If ID is given, load existing data
      if (relayId) {
        await fetchRelays(relayId, (data) => ($formData = data));
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
    {$_('relays.settings.title', { default: 'Relay settings' })}
    <Helper moreInfo="https://theyosh.github.io/TerrariumPI/setup/#relays" />
  </svelte:fragment>

  <form class="needs-validation" class:was-validated="{validated}" use:form bind:this="{editForm}">
    <input type="hidden" name="id" disabled="{$formData.id && $formData.id !== '' ? null : true}" />

    <div class="row">
      <div class="col-12 col-sm-12 col-md-6 col-lg-2">
        <Select
          name="hardware"
          value="{$formData.hardware}"
          readonly="{$formData.id && $formData.id !== ''}"
          on:change="{(value) => hardwareType(value.detail)}"
          required="{true}"
          options="{hardware}"
          label="{$_('relays.settings.hardware.label', { default: 'Hardware' })}"
          placeholder="{$_('relays.settings.hardware.placeholder', { default: 'Select hardware' })}"
          help="{$_('relays.settings.hardware.help', { default: 'Select the hardware type for this relay.' })}"
          invalid="{$_('relays.settings.hardware.invalid', { default: 'Please select a hardware type.' })}" />
      </div>
      <div class="col-12 col-sm-12 col-md-6 col-lg-3">
        <Field
          type="text"
          name="address"
          min="1"
          max="40"
          required="{true}"
          readonly="{hardware_type === 'brightpi-dimmer'}"
          label="{$_('relays.settings.address.label', { default: 'Address' })}"
          placeholder="{$_('relays.settings.address.placeholder', { default: 'Enter an address' })}"
          help="{$_('relays.settings.address.help', { default: 'For more information see online.' })}"
          invalid="{$_('relays.settings.address.invalid', { default: 'The entered address is not valid. It cannot be empty.' })}" />
      </div>
      <div class="col-12 col-sm-12 col-md-12 col-lg-3">
        <Field
          type="text"
          name="name"
          required="{true}"
          label="{$_('relays.settings.name.label', { default: 'Name' })}"
          placeholder="{$_('relays.settings.name.placeholder', { default: 'Enter a name' })}"
          help="{$_('relays.settings.name.help', { default: 'Enter an easy to remember name.' })}"
          invalid="{$_('relays.settings.name.invalid', { default: 'The entered name is not valid. It cannot be empty.' })}" />
      </div>

      <div class="col-12 col-sm-12 col-md-12 col-lg-3">
        <div class="row">
          <div class="col-6">
            <Field
              type="number"
              min="0"
              step="0.001"
              name="wattage"
              required="{true}"
              label="{$_('relays.settings.wattage.label', { default: 'Wattage' })}"
              help="{$_('relays.settings.wattage.help', { default: 'Enter the (max) wattage when switched on.' })}"
              invalid="{$_('relays.settings.wattage.invalid', {
                default: 'Please enter a minimum value of {value}.',
                values: { value: 0 },
              })}" />
          </div>
          <div class="col-6">
            <Field
              type="number"
              min="0"
              step="0.001"
              name="flow"
              required="{true}"
              label="{$_('relays.settings.flow.label', { default: 'Water flow' })}"
              help="{$_('relays.settings.flow.help', { default: 'Enter the (max) water flow when switched on.' })}"
              invalid="{$_('relays.settings.flow.invalid', {
                default: 'Please enter a minimum value of {value}.',
                values: { value: 0 },
              })}" />
          </div>
        </div>
      </div>
      <div class="col-12 col-sm-12 col-md-12 col-lg-1">
        <Field
          type="text"
          name="value"
          readonly
          label="{$_('relays.settings.current.label', { default: 'Current' })}"
          placeholder="{$_('relays.settings.current.placeholder', { default: 'Current value' })}"
          help="{$_('relays.settings.current.help', { default: 'The current state of the relay.' })}" />
      </div>
    </div>

    <div class="row button_callibration" class:d-block="{calibration}" class:d-none="{!calibration}">
      <a
        data-toggle="collapse"
        href="#callibration"
        role="button"
        aria-expanded="false"
        aria-controls="callibration"
        class:d-none="{!calibration}">
        <hr class="hr-text" data-content="calibration" />
      </a>
      <div class="col">
        <div class="collapse row pt-3" id="callibration">
          <div
            class="col-6 col-sm-6 col-md-6 col-lg-3"
            class:d-none="{['brightpi-dimmer', 'remote-dimmer', 'script-dimmer', 'sonoff_d1-dimmer'].indexOf(hardware_type) !== -1}">
            <Field
              type="number"
              name="calibration.dimmer_frequency"
              step="1"
              min="1"
              label="{$_('relays.settings.calibration.dimmer_frequency.label', { default: 'Dimmer frequency in Hz' })}"
              help="{$_('relays.settings.calibration.dimmer_frequency.help', { default: 'The frequency on which the dimmer operates.' })}"
              invalid="{$_('relays.settings.calibration.dimmer_frequency.invalid', {
                default: 'Please enter a minimum value of {value}.',
                values: { value: 0 },
              })}" />
          </div>
          <div class="col-6 col-sm-6 col-md-6 col-lg-3">
            <Field
              type="number"
              name="calibration.dimmer_max_power"
              step="1"
              min="1"
              max="100"
              label="{$_('relays.settings.calibration.dimmer_max_power.label', { default: 'Max power in %' })}"
              help="{$_('relays.settings.calibration.dimmer_max_power.help', { default: 'The maximum power for this dimmer.' })}"
              invalid="{$_('relays.settings.calibration.dimmer_max_power.invalid', {
                default: 'The entered value is not valid. Enter a valid number between {min} and {max}.',
                values: { min: 1, max: 40 },
              })}" />
          </div>
          <div class="col-6 col-sm-6 col-md-6 col-lg-3">
            <Field
              type="number"
              name="calibration.dimmer_offset"
              step="0.1"
              min="0"
              max="100"
              label="{$_('relays.settings.calibration.dimmer_offset.label', { default: 'Dimmer offset in %' })}"
              help="{$_('relays.settings.calibration.dimmer_offset.help', { default: 'The dimmer offset.' })}"
              invalid="{$_('relays.settings.calibration.dimmer_offset.invalid', {
                default: 'Please enter a minimum value of {value}.',
                values: { value: 0 },
              })}" />
          </div>
          {#if ['brightpi-dimmer', 'PCA9685-dimmer', 'remote-dimmer', 'script-dimmer', 'sonoff_d1-dimmer'].indexOf(hardware_type) === -1}
            <div class="col-6 col-sm-6 col-md-6 col-lg-3">
              <Field
                type="number"
                name="calibration.dimmer_max_dim"
                step="1"
                min="0"
                label="{$_('relays.settings.calibration.dimmer_max_dim.label', { default: 'Maximum dimmer value' })}"
                help="{$_('relays.settings.calibration.dimmer_max_dim.help', { default: 'Maximum dimmer value (Legacy).' })}"
                invalid="{$_('relays.settings.calibration.dimmer_max_dim.invalid', {
                  default: 'Please enter a minimum value of {value}.',
                  values: { value: 0 },
                })}" />
            </div>
          {/if}
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
