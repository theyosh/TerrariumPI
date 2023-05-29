<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import { writable } from 'svelte/store';
  import { _ } from 'svelte-i18n';
  import { createForm } from 'felte';
  import { fetchSensors, fetchSensorsHardware, updateSensor } from '../providers/api';
  import { successNotification, errorNotification } from '../providers/notification-provider';
  import { formToJSON, invalid_form_fields } from '../helpers/form-helpers';

  import ModalForm from '../user-controls/ModalForm.svelte';
  import Field from '../components/form/Field.svelte';
  import Helper from '../components/form/Helper.svelte';
  import Select from '../components/form/Select.svelte';
  import Switch from '../components/form/Switch.svelte';

  let wrapper_show;
  let wrapper_hide;
  let loading = false;
  let validated = false;

  let hardware = [];

  let calibration = true; // Calibration is always enabled due to offset setting
  let hardware_type = null;
  let sensor_type = null;

  let sensor_types = [];

  let ccs811_compensation_sensors = [];
  let formData = writable({});

  let editForm;

  const dispatch = createEventDispatcher();

  const successAction = () => {
    dispatch('save');
  };

  const hardwareType = (device) => {
    hardware_type = device;
    if (hardware_type === 'css811' && ccs811_compensation_sensors.length === 0) {
      fetchSensors(
        'temperature',
        (data) =>
          (ccs811_compensation_sensors = data.map((item) => {
            return { value: item.id, text: item.name };
          }))
      );
    }
    sensor_types = [];
    hardware.forEach((item) => {
      if (item.value === device) {
        sensor_types = item.types.map((sensor_type) => {
          return { value: sensor_type, text: sensor_type };
        });
      }
    });
    if (!$formData.id) {
      $formData.type = '';
    }
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
        await updateSensor(values, (data) => (values = data));
        // Notifify OK!
        successNotification(
          $_('sensors.settings.save.ok.message', { default: "Sensor ''{name}'' is updated", values: { name: values.name } }),
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
      let error_message = $_('sensors.settings.fields.error', { default: 'Not all required fields are entered correctly.' });
      error_message += "\n'" + invalid_form_fields(editForm).join("'\n'") + "'";
      errorNotification(error_message, $_('notification.form.save.error.title', { default: 'Save Error' }));
    }
  };

  const { form, data, setFields, isSubmitting, createSubmitHandler, reset } = createForm({
    onSubmit: _processForm,
  });

  const formSubmit = createSubmitHandler({
    onSubmit: _processForm,
  });

  export const show = (sensorId, cb) => {
    // Anonymous (Async) functions always as first!!
    (async () => {
      // Load all avaliable hardware
      await fetchSensorsHardware(
        (data) =>
          (hardware = data.map((item) => {
            return { value: item.hardware, text: item.name, types: item.types };
          }))
      );

      // If ID is given, load existing data
      if (sensorId) {
        await fetchSensors(sensorId, (data) => ($formData = data));
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
    <i class="fas fa-tint mr-2"></i>
    {$_('sensors.settings.title', { default: 'Sensor settings' })}
    <Helper moreInfo="https://theyosh.github.io/TerrariumPI/setup/#sensors" />
  </svelte:fragment>

  <form class="needs-validation" class:was-validated="{validated}" use:form bind:this="{editForm}">
    <input type="hidden" name="id" disabled="{$formData.id && $formData.id !== '' ? null : true}" />

    <div class="row">
      <div class="col-12 col-sm-6 col-md-4 col-lg-2">
        <Select
          name="hardware"
          value="{$formData.hardware}"
          readonly="{$formData.id && $formData.id !== ''}"
          on:change="{(value) => hardwareType(value.detail)}"
          required="{true}"
          options="{hardware}"
          label="{$_('sensors.settings.hardware.label', { default: 'Hardware' })}"
          placeholder="{$_('sensors.settings.hardware.placeholder', { default: 'Select hardware' })}"
          help="{$_('sensors.settings.hardware.help', { default: 'Select the hardware type for this button.' })}"
          invalid="{$_('sensors.settings.hardware.invalid', { default: 'Please select a hardware type.' })}" />
      </div>
      <div class="col-12 col-sm-6 col-md-4 col-lg-2">
        <Select
          name="type"
          value="{$formData.type}"
          readonly="{$formData.id && $formData.id !== ''}"
          on:change="{(value) => sensor_type = value.detail }"
          required="{true}"
          options="{sensor_types}"
          label="{$_('sensors.settings.type.label', { default: 'Type' })}"
          placeholder="{$_('sensors.settings.type.placeholder', { default: 'Select type' })}"
          help="{$_('sensors.settings.type.help', { default: 'Select the measurement type for this sensor.' })}"
          invalid="{$_('sensors.settings.type.invalid', { default: 'Please select a measurement type.' })}" />
      </div>
      <div class="col-12 col-sm-12 col-md-4 col-lg-3">
        <Field
          type="text"
          name="address"
          required="{true}"
          label="{$_('sensors.settings.address.label', { default: 'Address' })}"
          placeholder="{$_('sensors.settings.address.placeholder', { default: 'Enter an address' })}"
          help="{$_('sensors.settings.address.help', { default: 'Enter an address' })}"
          invalid="{$_('sensors.settings.address.invalid', { default: 'The entered address is not valid. It cannot be empty.' })}" />
      </div>
      <div class="col-10 col-sm-10 col-md-8 col-lg-3">
        <Field
          type="text"
          name="name"
          required="{true}"
          label="{$_('sensors.settings.name.label', { default: 'Name' })}"
          placeholder="{$_('sensors.settings.name.placeholder', { default: 'Enter a name' })}"
          help="{$_('sensors.settings.name.help', { default: 'Enter an easy to remember name.' })}"
          invalid="{$_('sensors.settings.name.invalid', { default: 'The entered name is not valid. It cannot be empty.' })}" />
      </div>
      <div class="col-2 col-sm-2 col-md-4 col-lg-2">
        <Field
          type="text"
          name="value"
          readonly
          label="{$_('sensors.settings.current.label', { default: 'Current' })}"
          placeholder="{$_('sensors.settings.current.placeholder', { default: 'Current value' })}"
          help="{$_('sensors.settings.current.help', { default: 'The current state of the sensor.' })}" />
      </div>
    </div>

    <div class="row">
      <div class="col-6 col-sm-6 col-md-6 col-lg-2">
        <Field
          type="number"
          name="alarm_min"
          step="0.0001"
          required="{true}"
          label="{$_('sensors.settings.alarm_min.label', { default: 'Alarm min' })}"
          help="{$_('sensors.settings.alarm_min.help', { default: 'Enter the minimum value for the alarm.' })}"
          invalid="{$_('sensors.settings.alarm_min.invalid', { default: 'The entered value is not valid. It needs to be number.' })}" />
      </div>
      <div class="col-6 col-sm-6 col-md-6 col-lg-2">
        <Field
          type="number"
          name="alarm_max"
          step="0.0001"
          required="{true}"
          label="{$_('sensors.settings.alarm_max.label', { default: 'Alarm max' })}"
          help="{$_('sensors.settings.alarm_max.help', { default: 'Enter the maximum value for the alarm.' })}"
          invalid="{$_('sensors.settings.alarm_max.invalid', { default: 'The entered value is not valid. It needs to be number.' })}" />
      </div>
      <div class="col-6 col-sm-6 col-md-6 col-lg-2">
        <Field
          type="number"
          name="limit_min"
          step="0.0001"
          required="{true}"
          label="{$_('sensors.settings.limit_min.label', { default: 'Limit min' })}"
          help="{$_('sensors.settings.limit_min.help', { default: 'Enter the minimum value that is valid.' })}"
          invalid="{$_('sensors.settings.limit_min.invalid', { default: 'The entered value is not valid. It needs to be number.' })}" />
      </div>
      <div class="col-6 col-sm-6 col-md-6 col-lg-2">
        <Field
          type="number"
          name="limit_max"
          step="0.0001"
          required="{true}"
          label="{$_('sensors.settings.limit_max.label', { default: 'Limit max' })}"
          help="{$_('sensors.settings.limit_max.help', { default: 'Enter the maximum value that is valid.' })}"
          invalid="{$_('sensors.settings.limit_max.invalid', { default: 'The entered value is not valid. It needs to be number.' })}" />
      </div>
      <div class="col-6 col-sm-6 col-md-6 col-lg-2">
        <Field
          type="number"
          name="max_diff"
          min="0"
          step="0.0001"
          required="{true}"
          label="{$_('sensors.settings.max_diff.label', { default: 'Max diff' })}"
          placeholder="{$_('sensors.settings.max_diff.placeholder', { default: 'Max difference' })}"
          help="{$_('sensors.settings.max_diff.help', {
            default: "Enter the max difference between two measurements that is valid. Enter '0' to disable.",
          })}"
          invalid="{$_('sensors.settings.max_diff.invalid', {
            default: 'The entered value is not valid. It needs to be number higher then {min}.',
            values: { min: 0 },
          })}" />
      </div>
      <div class="col-12 col-sm-12 col-md-12 col-lg-2">
        <Switch
          name="exclude_avg"
          value="{$formData.exclude_avg}"
          horizontal="{false}"
          label="{$_('sensors.settings.exclude_avg.label', { default: 'Excl. avg' })}"
          help="{$_('sensors.settings.exclude_avg.help', { default: 'Exclude this sensors from average calculations.' })}" />
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
          <div class="col-6 col-sm-6 col-md-6 col-lg-2">
            <Field
              type="number"
              name="calibration.offset"
              step="0.0001"
              horizontal="{false}"
              value="0.0"
              label="{$_('sensors.settings.calibration.offset.label', { default: 'Offset' })}"
              help="{$_('sensors.settings.calibration.offset.help', { default: 'Enter offset for this sensor.' })}"
              invalid="{$_('sensors.settings.calibration.offset.invalid', {
                default: 'The entered value is not valid. It needs to be number.',
              })}" />
          </div>
          <div class="col-6 col-sm-6 col-md-6 col-lg-2" class:d-none={sensor_type !== 'chirp'}>
            <Field
              type="number"
              name="calibration.chirp_min_moist"
              step="0.0001"
              min="0"
              horizontal="{false}"
              label="{$_('sensors.settings.calibration.chirp_min_moist.label', { default: 'Minimum moist value' })}"
              help="{$_('sensors.settings.calibration.chirp_min_moist.help', { default: 'Enter the minimum moist value.' })}"
              invalid="{$_('sensors.settings.calibration.chirp_min_moist.invalid', {
                default: 'The entered value is not valid. It needs to be number higher then {min}.',
                values: { min: 0 },
              })}" />
          </div>
          <div class="col-6 col-sm-6 col-md-6 col-lg-2" class:d-none={sensor_type !== 'chirp'}>
            <Field
              type="number"
              name="calibration.chirp_max_moist"
              step="0.0001"
              min="0"
              horizontal="{false}"
              label="{$_('sensors.settings.calibration.chirp_max_moist.label', { default: 'Maximum moist value' })}"
              help="{$_('sensors.settings.calibration.chirp_max_moist.help', { default: 'Enter the maximum moist value.' })}"
              invalid="{$_('sensors.settings.calibration.chirp_max_moist.invalid', {
                default: 'The entered value is not valid. It needs to be number higher then {min}.',
                values: { min: 0 },
              })}" />
          </div>
          <div class="col-6 col-sm-6 col-md-6 col-lg-4" class:d-none={sensor_type !== 'css811'}>
            <Select
              name="calibration.ccs811_compensation_sensors"
              multiple="{true}"
              options="{ccs811_compensation_sensors}"
              label="{$_('sensors.settings.calibration.ccs811_compensation_sensors.label', { default: 'Compensation sensors' })}"
              placeholder="{$_('sensors.settings.calibration.ccs811_compensation_sensors.placeholder', {
                default: 'Select compensation sensors',
              })}"
              help="{$_('sensors.settings.calibration.ccs811_compensation_sensors.help', {
                default: 'Select the sensors for the compensation calculation.',
              })}" />
          </div>
          <div class="col-6 col-sm-6 col-md-6 col-lg-2" class:d-none={sensor_type !== 'light'}>
            <Field
              type="number"
              name="calibration.light_on_off_threshold"
              step="0.0001"
              min="0"
              horizontal="{false}"
              label="{$_('sensors.settings.calibration.light_threshold.label', { default: 'Lights on threshold' })}"
              help="{$_('sensors.settings.calibration.light_threshold.help', { default: 'Enter the value when considered the lights are on.' })}"
              invalid="{$_('sensors.settings.calibration.light_threshold.invalid', {
                  default: 'The entered value is not valid. It needs to be number higher then {min}.',
                  values: { min: 0 },
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
