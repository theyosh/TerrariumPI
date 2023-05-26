<script>
  import { onMount, createEventDispatcher, setContext, getContext } from 'svelte';
  import { writable } from 'svelte/store';
  import { _ } from 'svelte-i18n';
  import { createForm } from 'felte';
  import L from 'leaflet';

  import { sensors } from '../stores/terrariumpi';
  import { fetchRelays, fetchWebcams, fetchWebcamsHardware, updateWebcam } from '../providers/api';
  import { successNotification, errorNotification } from '../providers/notification-provider';
  import { getCustomConfig } from '../config';
  import { roundToPrecision } from '../helpers/number-helpers';
  import { formToJSON, invalid_form_fields } from '../helpers/form-helpers';
  import { ApiUrl } from '../constants/urls';

  import WebcamMarkerModal from '../modals/WebcamMarkerModal.svelte';
  import ModalForm from '../user-controls/ModalForm.svelte';
  import Webcam from '../components/common/Webcam.svelte';
  import Field from '../components/form/Field.svelte';
  import Helper from '../components/form/Helper.svelte';
  import Select from '../components/form/Select.svelte';

  const settings = getCustomConfig();

  let wrapper_show;
  let wrapper_hide;
  let loading = false;
  let validated = false;

  let hardware = [];
  let relays = [];
  let webcamMap = null;

  let motion_settings = false; // Calibration is always enabled due to offset setting
  let hardware_type = null;
  let formData = writable({});

  let markerModal;
  let editForm;

  const rotations = [
    { value: '0', text: $_('webcams.settings.rotation.options.degrees_0', { default: '0 degrees' }) },
    { value: '90', text: $_('webcams.settings.rotation.options.degrees_90', { default: '90 degrees' }) },
    { value: '180', text: $_('webcams.settings.rotation.options.degrees_180', { default: '180 degrees' }) },
    { value: '270', text: $_('webcams.settings.rotation.options.degrees_270', { default: '270 degrees' }) },
    { value: 'H', text: $_('webcams.settings.rotation.options.flip_h', { default: 'Flip horizontal' }) },
    { value: 'V', text: $_('webcams.settings.rotation.options.flip_v', { default: 'Flip vertical' }) },
  ];

  const white_balances = [
    { value: 'off', text: $_('webcams.settings.awb.options.off', { default: 'Off' }) },
    { value: 'auto', text: $_('webcams.settings.awb.options.auto', { default: 'Off' }) },
    { value: 'sunlight', text: $_('webcams.settings.awb.options.sunlight', { default: 'Sunlight' }) },
    { value: 'cloudy', text: $_('webcams.settings.awb.options.cloudy', { default: 'Cloudy' }) },
    { value: 'shade', text: $_('webcams.settings.awb.options.shade', { default: 'Shade' }) },
    { value: 'tungsten', text: $_('webcams.settings.awb.options.tungsten', { default: 'Tungsten' }) },
    { value: 'fluorescent', text: $_('webcams.settings.awb.options.fluorescent', { default: 'Fluorescent' }) },
    { value: 'incandescent', text: $_('webcams.settings.awb.options.incandescent', { default: 'Incandescent' }) },
    { value: 'flash', text: $_('webcams.settings.awb.options.flash', { default: 'Flash' }) },
    { value: 'horizon', text: $_('webcams.settings.awb.options.horizon', { default: 'Horizon' }) },
    { value: 'greyworld', text: $_('webcams.settings.awb.options.greyworld', { default: 'Greyworld' }) },
  ];

  const archiving = [
    { value: 'disabled', text: $_('webcams.settings.archive.options.disabled', { default: 'Disabled' }) },
    { value: 'motion', text: $_('webcams.settings.archive.options.motion', { default: 'Motion' }) },
    { value: '60', text: $_('webcams.settings.archive.options.minute_1', { default: '1 Minute' }) },
    { value: '300', text: $_('webcams.settings.archive.options.minute_5', { default: '5 Minutes' }) },
    { value: '900', text: $_('webcams.settings.archive.options.minute_15', { default: '15 Minutes' }) },
    { value: '1800', text: $_('webcams.settings.archive.options.minute_30', { default: '30 Minutes' }) },
    { value: '3600', text: $_('webcams.settings.archive.options.hour_1', { default: 'Disabled' }) },
    { value: '10800', text: $_('webcams.settings.archive.options.hour_3', { default: '3 Hours' }) },
    { value: '21600', text: $_('webcams.settings.archive.options.hour_6', { default: '6 Hours' }) },
    { value: '43200', text: $_('webcams.settings.archive.options.hour_12', { default: '12 Hours' }) },
    { value: '86400', text: $_('webcams.settings.archive.options.day_1', { default: '1 Day' }) },
  ];

  const { confirmModal } = getContext('confirm');
  const dispatch = createEventDispatcher();

  const successAction = () => {
    dispatch('save');
  };

  // Dummy needed for Webcam.svelte
  setContext('loading', {
    setLoading: (state) => {},
  });

  const setMarker = (data) => {
    if (data.markerid) {
      // Update
      let marker = _get_marker(data.markerid);
      marker.options.sensors = data.sensors;
      marker._tooltip.setContent(_update_marker_tooltip(data.sensors));
    } else {
      // add
      L.marker([0, 0], {
        draggable: true,
        icon: L.icon(webcamMap.iconOptions),
        sensors: data.sensors,
      })
        .on('move', markerLocations)
        .on('dblclick', markerModal.show)
        .bindTooltip(_update_marker_tooltip(data.sensors), webcamMap.toolTipOptions)
        .addTo(webcamMap.getWebcamMap());
    }
    markerLocations();
  };

  const deleteMarker = (id) => {
    let marker = _get_marker(id);
    if (marker) {
      confirmModal($_('webcams.marker.delete.confirm.message'), async () => {
        try {
          webcamMap.getWebcamMap().removeLayer(marker);
          markerModal.hide();
          markerLocations();
        } catch (e) {
          errorNotification($_('webcams.marker.delete.error.message'), $_('notification.delete.error.title'));
        }
      });
    } else {
      errorNotification($_('webcams.marker.delete.invalid.message'), $_('notification.delete.invalid.title'));
    }
  };

  const _update_marker_tooltip = (all_sensors) => {
    return (
      `<div><strong>${$sensors[all_sensors[0]].name}</strong><br />` +
      all_sensors
        .map((item) => {
          return (
            `${settings.units[$sensors[item].type].name.toLowerCase().slice(0, 4)} ` +
            `${roundToPrecision($sensors[item].value)} ` +
            `${settings.units[$sensors[item].type].value}`
          );
        })
        .join('<br />') +
      '</div>'
    );
  };

  const _get_marker = (id) => {
    let item = null;
    webcamMap.getWebcamMap().eachLayer((layer) => {
      if (item === null && layer instanceof L.Marker) {
        if (id === layer._leaflet_id) {
          item = layer;
        }
      }
    });
    return item;
  };

  const markerLocations = () => {
    let markers = [];
    webcamMap.getWebcamMap().eachLayer((layer) => {
      if (layer instanceof L.Marker) {
        markers.push({
          lat: layer.getLatLng().lat,
          long: layer.getLatLng().lng,
          sensors: layer.options.sensors,
        });
      }
    });
    editForm.elements['markers'].value = JSON.stringify(markers);
  };

  setContext('webcamMarker', {
    showModal: (marker) => markerModal.show(marker),
    setMarker: (marker) => setMarker(marker),
    deleteMarker: (marker) => deleteMarker(marker),
    markerLocations: () => markerLocations(),
  });

  const hardwareType = (device) => {
    hardware_type = device;

    if (!editForm.elements) {
      return;
    }

    switch (device) {
      case 'rpicam':
        editForm.elements['address'].value = 'rpicam';
        editForm.elements['width'].value = 3280;
        editForm.elements['height'].value = 2464;
        break;
      case 'rpicam-live':
        editForm.elements['address'].value = 'rpicam_live';
        editForm.elements['width'].value = 1920;
        editForm.elements['height'].value = 1080;
        break;
    }
  };

  const archivingCalibration = (state) => {
    motion_settings = state === 'motion';
  };

  const _processForm = async (values, context) => {
    validated = true;

    if (context.form.checkValidity()) {
      loading = true;
      values = formToJSON(editForm);

      // Make some fields exclusive string values
      values.address += '';
      values.rotation += '';

      delete values.value;

      try {
        values.markers = JSON.parse(values.markers);
      } catch (error) {
        values.markers = [];
      }

      try {
        // Post data
        await updateWebcam(values, (data) => (values = data));

        // Notify OK!
        successNotification(
          $_('webcams.settings.save.ok.message', { default: "Webcam ''{name}'' is updated", values: { name: values.name } }),
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
      let error_message = $_('webcams.settings.save.error.required_fields', { default: 'Not all required fields are entered correctly.' });
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

  export const show = (webcamId, cb) => {
    // Anonymous (Async) functions always as first!!
    (async () => {
      await fetchRelays(
        false,
        (data) =>
          (relays = data.map((item) => {
            return { value: item.hardware, text: item.name };
          }))
      );
      // Load all avaliable hardware
      await fetchWebcamsHardware(
        (data) =>
          (hardware = data.map((item) => {
            return { value: item.hardware, text: item.name };
          }))
      );
      // If ID is given, load existing data
      if (webcamId) {
        await fetchWebcams(webcamId, (data) => ($formData = data));
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
    {$_('webcams.settings.title', { default: 'Webcam settings' })}
    <Helper moreInfo="https://theyosh.github.io/TerrariumPI/setup/#webcams" />
  </svelte:fragment>

  <form class="needs-validation" class:was-validated="{validated}" use:form bind:this="{editForm}">
    <input type="hidden" name="id" disabled="{$formData.id && $formData.id !== '' ? null : true}" />
    <input type="hidden" name="markers" readonly="readonly" />

    <div class="row">
      <div class="col-12 col-sm-12 col-md-12 col-lg-7">
        <div class="row">
          <div class="col-12 col-sm-12 col-md-3 col-lg-4">
            <Select
              name="hardware"
              value="{$formData.hardware}"
              readonly="{$formData.id && $formData.id !== ''}"
              on:change="{(value) => hardwareType(value.detail)}"
              required="{true}"
              options="{hardware}"
              label="{$_('webcams.settings.hardware.label', { default: 'Hardware' })}"
              placeholder="{$_('webcams.settings.hardware.placeholder', { default: 'Select hardware' })}"
              help="{$_('webcams.settings.hardware.help', { default: 'Select the hardware type for this button.' })}"
              invalid="{$_('webcams.settings.hardware.invalid', { default: 'Please select a hardware type.' })}" />
          </div>
          <div class="col-12 col-sm-12 col-md-5 col-lg-4">
            <Field
              type="text"
              name="address"
              required="{true}"
              readonly="{['rpicam', 'rpicam-live'].indexOf(hardware_type) !== -1}"
              label="{$_('webcams.settings.address.label', { default: 'Address' })}"
              placeholder="{$_('webcams.settings.address.placeholder', { default: 'Enter an address' })}"
              help="{$_('webcams.settings.address.help', { default: 'For more information see online.' })}"
              invalid="{$_('webcams.settings.address.invalid', { default: 'The entered address is not valid. It cannot be empty.' })}" />
          </div>
          <div class="col-12 col-sm-12 col-md-4 col-lg-4">
            <Field
              type="text"
              name="name"
              required="{true}"
              label="{$_('webcams.settings.name.label', { default: 'Name' })}"
              placeholder="{$_('webcams.settings.name.placeholder', { default: 'Enter a name' })}"
              help="{$_('webcams.settings.name.help', { default: 'Enter an easy to remember name.' })}"
              invalid="{$_('webcams.settings.name.invalid', { default: 'The entered name is not valid. It cannot be empty.' })}" />
          </div>
        </div>
        <div class="row">
          <div class="col-12 col-sm-12 col-md-6 col-lg-6">
            <div class="row">
              <div class="col-5">
                <Field
                  type="number"
                  min="0"
                  step="1"
                  name="width"
                  required="{true}"
                  label="{$_('webcams.settings.width.label', { default: 'Width' })}"
                  help="{$_('webcams.settings.width.help', { default: 'Enter the resolution width in pixels.' })}"
                  invalid="{$_('webcams.settings.width.invalid', {
                    default: 'Please enter a minimum value of {value}.',
                    values: { value: 0 },
                  })}" />
              </div>
              <div class="col-2 pt-5 text-center text-bold">X</div>
              <div class="col-5">
                <Field
                  type="number"
                  min="0"
                  step="1"
                  name="height"
                  required="{true}"
                  label="{$_('webcams.settings.height.label', { default: 'Height' })}"
                  help="{$_('webcams.settings.height.help', { default: 'Enter the resolution height in pixels.' })}"
                  invalid="{$_('webcams.settings.height.invalid', {
                    default: 'Please enter a minimum value of {value}.',
                    values: { value: 0 },
                  })}" />
              </div>
            </div>
          </div>
          <div class="col-6 col-sm-6 col-md-3 col-lg-3">
            <Select
              name="rotation"
              value="{$formData.rotation}"
              required="{true}"
              options="{rotations}"
              label="{$_('webcams.settings.rotation.label', { default: 'Rotation' })}"
              placeholder="{$_('webcams.settings.rotation.placeholder', { default: 'Select rotation' })}"
              help="{$_('webcams.settings.rotation.help', { default: 'Select a rotation.' })}"
              invalid="{$_('webcams.settings.rotation.invalid', { default: 'Please make a choice.' })}" />
          </div>
          <div class="col-6 col-sm-6 col-md-3 col-lg-3">
            <Select
              name="awb"
              value="{$formData.awb}"
              required="{true}"
              options="{white_balances}"
              label="{$_('webcams.settings.awb.label', { default: 'White balance' })}"
              placeholder="{$_('webcams.settings.awb.placeholder', { default: 'Select white balance' })}"
              help="{$_('webcams.settings.awb.help', { default: 'Select a white balance.' })}"
              invalid="{$_('webcams.settings.awb.invalid', { default: 'Please make a choice.' })}" />
          </div>
        </div>
        <div class="row">
          <div class="col-6 col-sm-6 col-md-3 col-lg-3">
            <Select
              name="archive.state"
              value="{$formData.archive ? $formData.archive.state : null}"
              on:change="{(value) => archivingCalibration(value.detail)}"
              options="{archiving}"
              label="{$_('webcams.settings.archive.state.label', { default: 'Archiving' })}"
              placeholder="{$_('webcams.settings.archive.state.placeholder', { default: 'Select archiving' })}"
              help="{$_('webcams.settings.archive.state.help', { default: 'Select the duration between archived images.' })}"
              invalid="{$_('webcams.settings.archive.state.invalid', { default: 'Please make a choice.' })}" />
          </div>
          <div class="col-6 col-sm-6 col-md-3 col-lg-3">
            <Select
              name="archive.light"
              value="{$formData.archive ? $formData.archive.light : ''}"
              options="{[
                { value: 'ignore', text: $_('webcams.settings.archive.light.options.ignore', { default: 'Ignore' }) },
                { value: 'on', text: $_('webcams.settings.archive.light.options.on', { default: 'When on' }) },
                { value: 'off', text: $_('webcams.settings.archive.light.options.off', { default: 'When off' }) },
              ]}"
              label="{$_('webcams.settings.archive.light.label', { default: 'Archive light state' })}"
              placeholder="{$_('webcams.settings.archive.light.placeholder', { default: 'Select archive light state' })}"
              help="{$_('webcams.settings.archive.light.help', { default: 'Light status for taking an archive image.' })}"
              invalid="{$_('webcams.settings.archive.light.invalid', { default: 'Please make a choice.' })}" />
          </div>
          <div class="col-6 col-sm-6 col-md-3 col-lg-3">
            <Select
              name="archive.door"
              value="{$formData.archive ? $formData.archive.door : ''}"
              options="{[
                { value: 'ignore', text: $_('webcams.settings.archive.door.options.ignore', { default: 'Ignore' }) },
                { value: 'close', text: $_('webcams.settings.archive.door.options.close', { default: 'Close' }) },
                { value: 'open', text: $_('webcams.settings.archive.door.options.open', { default: 'Open' }) },
              ]}"
              label="{$_('webcams.settings.archive.door.label', { default: 'Archive door state' })}"
              placeholder="{$_('webcams.settings.archive.door.placeholder', { default: 'Select archive door state' })}"
              help="{$_('webcams.settings.archive.door.help', { default: 'Door status for taking an archive image.' })}"
              invalid="{$_('webcams.settings.archive.door.invalid', { default: 'Please make a choice.' })}" />
          </div>
          <div class="col-6 col-sm-6 col-md-3 col-lg-3">
            <Select
              name="flash"
              value="{$formData.flash}"
              multiple="{true}"
              options="{relays}"
              label="{$_('webcams.settings.archive.flash.label', { default: 'Flash' })}"
              placeholder="{$_('webcams.settings.archive.flash.placeholder', { default: 'Select optional relay for flash' })}"
              help="{$_('webcams.settings.archive.flash.help', { default: 'Select a relay that will act as a flasher.' })}"
              invalid="{$_('webcams.settings.archive.flash.invalid', { default: 'Please make a choice.' })}" />
          </div>
        </div>
      </div>
      <div class="col-12 col-sm-12 col-md-12 col-lg-5">
        <div class="form-group">
          <label for="button_address">{$_('webcams.settings.preview.label', { default: 'Preview' })}</label>
          <div class="embed-responsive embed-responsive-16by9">
            <img
              src="{$formData.raw_image ? `${ApiUrl}/${$formData.raw_image}` : 'img/webcam_offline.png'}"
              class="img-fluid embed-responsive-item"
              style="position:absolute"
              alt="Offline preview" />
            {#if $formData.id}
              <div class="embed-responsive-item">
                <Webcam webcam="{$formData}" edit="{true}" bind:this="{webcamMap}" />
              </div>
            {/if}
          </div>
        </div>
      </div>
    </div>
    {#if motion_settings}
      <div class="row">
        <div class="col-6 col-sm-6 col-md-3 col-lg-3">
          <Select
            name="motion.boxes"
            value="{$formData.motion ? $formData.motion.boxes : ''}"
            required={motion_settings}
            options="{[
              { value: '-1', text: $_('webcams.settings.motion.boxes.options.none', { default: 'None' }) },
              { value: 'red', text: $_('webcams.settings.motion.boxes.options.red', { default: 'Red' }) },
              { value: 'green', text: $_('webcams.settings.motion.boxes.options.green', { default: 'Green' }) },
              { value: 'blue', text: $_('webcams.settings.motion.boxes.options.blue', { default: 'Blue' }) },
            ]}"
            label="{$_('webcams.settings.motion.boxes.label', { default: 'Show motion boxes' })}"
            placeholder="{$_('webcams.settings.motion.boxes.placeholder', { default: 'Show the motion boxes' })}"
            help="{$_('webcams.settings.motion.boxes.help', { default: 'Show motion boxes on the archived images.' })}"
            invalid="{$_('webcams.settings.motion.boxes.invalid', { default: 'Please make a choice.' })}" />
        </div>
        <div class="col-6 col-sm-6 col-md-3 col-lg-3">
          <Field
            type="number"
            name="motion.threshold"
            step="1"
            min="0"
            required={motion_settings}
            label="{$_('webcams.settings.motion.threshold.label', { default: 'Motion delta threshold' })}"
            placeholder="{$_('webcams.settings.motion.threshold.placeholder', { default: 'Enter number' })}"
            help="{$_('webcams.settings.motion.threshold.help', { default: 'Enter the motion threshold.' })}"
            invalid="{$_('webcams.settings.motion.threshold.invalid', {
              default: 'Please enter a minimum value of {value}.',
              values: { value: 0 },
            })}" />
        </div>
        <div class="col-6 col-sm-6 col-md-3 col-lg-3">
          <Field
            type="number"
            name="motion.area"
            min="0"
            required={motion_settings}
            label="{$_('webcams.settings.motion.area.label', { default: 'Motion minimum area' })}"
            placeholder="{$_('webcams.settings.motion.area.placeholder', { default: 'Enter number' })}"
            help="{$_('webcams.settings.motion.area.help', { default: 'Enter an area size.' })}"
            invalid="{$_('webcams.settings.motion.area.invalid', {
              default: 'Please enter a minimum value of {value}.',
              values: { value: 0 },
            })}" />
        </div>
        <div class="col-6 col-sm-6 col-md-3 col-lg-3">
          <Select
            name="motion.frame"
            value="{$formData.motion ? $formData.motion.frame : ''}"
            required={motion_settings}
            options="{[
              { value: 'last', text: $_('webcams.settings.motion.frame.options.last', { default: 'Last frame' }) },
              { value: 'archived', text: $_('webcams.settings.motion.frame.options.archived', { default: 'Last archived frame' }) },
            ]}"
            label="{$_('webcams.settings.motion.frame.label', { default: 'Motion comparison frame' })}"
            placeholder="{$_('webcams.settings.motion.frame.placeholder', { default: 'Select which frame to comparison' })}"
            help="{$_('webcams.settings.motion.frame.help', { default: 'Which frame to use for motion detection.' })}"
            invalid="{$_('webcams.settings.motion.frame.invalid', { default: 'Please make a choice.' })}" />
        </div>
      </div>
    {/if}

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
<WebcamMarkerModal bind:this="{markerModal}" />
