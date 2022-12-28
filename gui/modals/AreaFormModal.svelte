<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import { writable } from 'svelte/store';
  import { _ } from 'svelte-i18n';
  import { createForm } from 'felte';
  import { dayjs } from 'svelte-time';

  import {
    fetchEnclosures,
    fetchAreaTypes,
    fetchRelays,
    fetchSoundcards,
    fetchPlaylists,
    fetchSensors,
    fetchAreas,
    fetchWeatherData,
    updateArea,
  } from '../providers/api';
  import { successNotification, errorNotification } from '../providers/notification-provider';
  import { formToJSON, invalid_form_fields } from '../helpers/form-helpers';
  import { arrIdentical } from '../helpers/number-helpers';

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

  let enclosures = [];
  let area_types = [];
  let relays = [];
  let soundcards = [];
  let playlists = [];
  let sensors = [];
  let areas = [];

  let sensor_filter = [];
  let showSensorDeviation = false;
  let weather = null;

  let formData = writable({});

  let editForm;

  const dispatch = createEventDispatcher();

  const successAction = () => {
    dispatch('save');
  };

  const relayName = (id) => {
    let relay = relays.filter((item) => {
      return item.id == id;
    });
    return relay.length == 1 ? relay[0].name : '';
  };

  const relayDimmer = (id) => {
    let relay = relays.filter((item) => {
      return item.id == id;
    });
    return relay.length == 1 ? relay[0].dimmer : false;
  };

  const tweakValue = (value, defaultValue) => {
    if (value === undefined) {
      return defaultValue;
    }

    try {
      return value.split(',').map((item) => {
        return item * 1.0;
      });
    } catch (e) {
      return value;
    }
  };

  const updateTweakRelays = (part, new_relays) => {
    let tweaks = $formData.setup && $formData.setup[part].tweaks ? $formData.setup[part].tweaks : [];
    let existing_relays = tweaks.map((item) => {
      return item.id;
    });

    if (!arrIdentical(new_relays, existing_relays)) {
      // Cleanup deleted relays (filter out non selected relays)
      if (tweaks.length > 0) {
        tweaks = tweaks.filter((relay) => {
          return new_relays.indexOf(relay.id) != -1;
        });
      }
      // Add new relays (filter out non existing relays and add them)
      new_relays
        .filter((relay_id) => {
          return existing_relays.length == 0 || existing_relays.indexOf(relay_id) == -1;
        })
        .map((item) => {
          tweaks.push({ id: item });
        });
      $formData.setup[part].relays = new_relays;
      $formData.setup[part].tweaks = tweaks;
    }
  };

  const updateTweakSliders = () => {
    // Store form data in store. Need to get the slider values
    let form = formToJSON(editForm);

    $formData.setup.low.tweaks = form.setup.low.tweaks;
    $formData.setup.high.tweaks = form.setup.high.tweaks;
  };

  const addVariation = () => {
    $formData.setup.variation = [...(formToJSON(editForm).setup.variation ?? null), ...[{ when: '', period: '', value: null }]];
  };

  const removeVariation = (index) => {
    // Remove row
    $formData.setup.variation.splice(index, 1);
    // This is needed in order to Svelte to update the arrays in the template https://svelte.dev/tutorial/updating-arrays-and-objects
    $formData.setup.variation = $formData.setup.variation;
  };

  const areaType = (area) => {
    $formData.type = area;
    sensor_filter = [];
    area_types
      .filter((item) => item.value == area)
      .map((item) => {
        sensor_filter = [...sensor_filter, ...item.sensors];
      });
  };

  const areaMode = (mode) => {
    $formData.mode = mode;
    let on_duration = 0;
    let off_duration = 0;

    switch ($formData.mode) {
      case 'weather':
        on_duration = (weather.sun.set - weather.sun.rise) / 60;
        off_duration = 24 * 60 - on_duration;

        editForm.elements['setup.low.begin'].value = dayjs.unix(weather.sun.rise).format('HH:mm');
        editForm.elements['setup.low.end'].value = dayjs.unix(weather.sun.set).format('HH:mm');
        editForm.elements['setup.low.on_duration'].value = on_duration;
        editForm.elements['setup.low.off_duration'].value = off_duration;

        editForm.elements['setup.high.begin'].value = dayjs.unix(weather.sun.set).format('HH:mm');
        editForm.elements['setup.high.end'].value = dayjs.unix(weather.sun.rise).format('HH:mm');
        editForm.elements['setup.high.on_duration'].value = off_duration;
        editForm.elements['setup.high.off_duration'].value = on_duration;
        break;
      case 'weather_inverse':
        off_duration = (weather.sun.set - weather.sun.rise) / 60;
        on_duration = 24 * 60 - off_duration;

        editForm.elements['setup.low.begin'].value = dayjs.unix(weather.sun.set).format('HH:mm');
        editForm.elements['setup.low.end'].value = dayjs.unix(weather.sun.rise).format('HH:mm');
        editForm.elements['setup.low.on_duration'].value = on_duration;
        editForm.elements['setup.low.off_duration'].value = off_duration;

        editForm.elements['setup.high.begin'].value = dayjs.unix(weather.sun.rise).format('HH:mm');
        editForm.elements['setup.high.end'].value = dayjs.unix(weather.sun.set).format('HH:mm');
        editForm.elements['setup.high.on_duration'].value = off_duration;
        editForm.elements['setup.high.off_duration'].value = on_duration;
        break;
    }
  };

  const _processForm = async (values, context) => {
    validated = true;

    // Reset custom error trigger
    try {
      editForm.elements['setup.low.relays[]'].setCustomValidity('');
      editForm.elements['setup.high.relays[]'].setCustomValidity('');
    } catch (e) {
      editForm.elements['setup.low.playlists[]'].setCustomValidity('');
      editForm.elements['setup.high.playlists[]'].setCustomValidity('');
    }

    if (editForm.checkValidity()) {
      values = formToJSON(editForm);
      // Check if we have selected relays multiple times in the low and high alarm parts
      if (!values.setup.low.relays.some((item) => values.setup.high.relays.includes(item))) {
        loading = true;

        if (values.type == 'lights' || values.type == 'audio') {
          values.setup.day = { ...values.setup.low };
          values.setup.night = { ...values.setup.high };

          delete values.setup.low;
          delete values.setup.high;
        }

        if (values.setup.variation.length == 1 && values.setup.variation[0].period == '' && values.setup.variation[0].value == '' && values.setup.variation[0].when == '') {
          delete values.setup.variation;
        }

        try {
          // Post data
          await updateArea(values, (data) => (values = data));
          // Notifify OK!
          successNotification(
            $_('areas.settings.save.ok.message', { default: "Area ''{name}'' is updated", values: { name: values.name } }),
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
        // A relay is used in both low and high alarm
        loading = false;

        try {
          editForm.elements['setup.low.relays[]'].setCustomValidity('Not valid');
          editForm.elements['setup.high.relays[]'].setCustomValidity('Not valid');
        } catch (e) {
          editForm.elements['setup.low.playlists[]'].setCustomValidity('Not valid');
          editForm.elements['setup.high.playlists[]'].setCustomValidity('Not valid');
        }

        editForm.checkValidity();

        let error_message = $_('areas.settings.save.error.duplicate_relays', {
          default: 'You have selected the same relay(s) in both the low and high alarm. This is not valid.',
        });
        errorNotification(error_message, $_('notification.form.save.error.title', { default: 'Save Error' }));
      }
    } else {
      let error_message = $_('areas.settings.save.error.required_fields', { default: 'Not all required fields are entered correctly.' });
      error_message += "\n'" + [...new Set(invalid_form_fields(editForm))].join("'\n'") + "'";
      errorNotification(error_message, $_('notification.form.save.error.title', { default: 'Save Error' }));
    }
  };

  const { form, setFields, isSubmitting, createSubmitHandler, reset, data } = createForm({
    onSubmit: _processForm,
  });

  const formSubmit = createSubmitHandler({
    onSubmit: _processForm,
  });

  export const show = async (areaId, cb) => {
    // Anonymous (Async) functions always as first!!
    (async () => {
      // Load all available enclosures, area types, relays, sensors and more
      await Promise.all([
        fetchEnclosures(
          false,
          (data) =>
            (enclosures = data.map((item) => {
              return { value: item.id, text: item.name };
            }))
        ),
        fetchAreaTypes(
          (data) =>
            (area_types = data.map((item) => {
              return { value: item.type, text: item.name, sensors: item.sensors };
            }))
        ),
        fetchRelays(false, (data) => (relays = data)),
        fetchSoundcards(
          (data) =>
            (soundcards = data.map((item) => {
              return { value: item.index, text: item.name };
            }))
        ),
        fetchPlaylists(
          false,
          (data) =>
            (playlists = data.map((item) => {
              return { value: item.id, text: item.name };
            }))
        ),
        fetchSensors(
          false,
          (data) =>
            (sensors = data.map((item) => {
              return { value: item.id, text: item.name, type: item.type };
            }))
        ),
        fetchAreas(
          false,
          (data) =>
            (areas = data.map((item) => {
              return { value: item.id, text: item.name };
            }))
        ),
        fetchWeatherData((data) => (weather = data)),
      ]);

      // If ID is given, load existing data
      if (areaId) {
        await fetchAreas(areaId, (data) => {
          // If we have lights or audio type, we need to translate day to low, and night to high
          // Do it also here, before assigning to `$formData`. Else you will get errors... :(
          if (data.type == 'lights' || data.type == 'audio') {
            data.setup.low = { ...data.setup.day };
            data.setup.high = { ...data.setup.night };

            delete data.setup.day;
            delete data.setup.night;
          }

          data.setup.variation = [...(data.setup.variation ?? []), ...[{ when: '', period: '', value: null }]];

          // We do not care about the actual area state, so delete it
          delete data.state;

          // Legacy tweaks, convert to new values
          /* Old data
          {
            "id": "a8e5190f-1913-4da7-8aa1-e34655c3e76d",
            "name": "Day light",
            "type": "lights",
            "mode": "weather",
            "setup": {
              "day": {
                "begin": "06:19",
                "dimmer_duration_off_0e0cf978ca6bdb8eb994c186434a628e": "0,30",
                "dimmer_duration_on_0e0cf978ca6bdb8eb994c186434a628e": "0,45",
                "end": "20:43",
                "off_duration": 0,
                "on_duration": 863.3,
                "relay_delay_off_97c45c98476b1807a4bfa7bb4d249b14": "0",
                "relay_delay_on_97c45c98476b1807a4bfa7bb4d249b14": "40",
                "relays": [
                  "97c45c98476b1807a4bfa7bb4d249b14",
                  "0e0cf978ca6bdb8eb994c186434a628e"
                ]
              },
              "main_lights": true,
              "max_day_hours": 16,
              "min_day_hours": 10,
              "night": {
                "begin": "20:43",
                "end": "06:19",
                "off_duration": 0,
                "on_duration": 576.7,
                "relays": []
              },
              "shift_day_hours": 0
            },
            "state": {
              "day": {
                "alarm_count": 0,
                "begin": 1667542592,
                "duration": 36000,
                "end": 1667578592
                "last_powered_on": 1667456201,
                "powered": false,
                "timer_on": false
              },
              "is_day": false,
              "last_update": 1667505376,
              "powered": false
            },
            "enclosure": "daa150fc-dd48-4b96-991c-eb27cb6de596"
          }
          */

          let tweak_settings = { low: {}, high: {} };
          const tweak_regex = /(?:dimmer|relay)_(?:duration|delay)_(on|off)_([a-z0-9]+)/i;
          for (let period of ['low', 'high']) {
            if (data.setup[period]['tweaks']) {
              // Skip if there are already tweaks, so new setup and they should be correct.
              continue;
            }

            for (let field of Object.keys(data.setup[period])) {
              const tweaks = field.match(tweak_regex);
              if (tweaks) {
                if (!tweak_settings[period][tweaks[2]]) {
                  tweak_settings[period][tweaks[2]] = {
                    id: tweaks[2],
                    on: 0,
                    off: 0,
                  };
                }
                tweak_settings[period][tweaks[2]][tweaks[1]] =
                  data.setup[period][field].indexOf(',') === -1 ? data.setup[period][field] * 1 : data.setup[period][field];
                delete data.setup[period][field];
              }
            }
            // Convert object to an array
            data.setup[period]['tweaks'] = Object.keys(tweak_settings[period]).map((key) => {
              return structuredClone(tweak_settings[period][key]);
            });
          }

          // First set formdata which will trigger if statements to show fields
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
    $formData.setup.variation = [{ when: '', period: '', value: null }];
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
    <i class="fas fa-map mr-2"></i>
    {$_('areas.settings.title', { default: 'Area settings' })}
    <Helper moreInfo="https://theyosh.github.io/TerrariumPI/setup/#areas" />
  </svelte:fragment>

  <form class="needs-validation" class:was-validated="{validated}" use:form bind:this="{editForm}">
    <input type="hidden" name="id" disabled="{$formData.id && $formData.id != '' ? null : true}" />

    <div class="row">
      <div class="col-12 col-sm-3 col-md-3 col-lg-3">
        <Select
          name="enclosure"
          value="{$formData.enclosure}"
          readonly="{$formData.id && $formData.id != ''}"
          required="{true}"
          options="{enclosures}"
          sort="{true}"
          label="{$_('areas.settings.enclosure.label', { default: 'Enclosure' })}"
          placeholder="{$_('areas.settings.enclosure.placeholder', { default: 'Select enclosure' })}"
          help="{$_('areas.settings.enclosure.help', { default: 'Select the enclosure where this area belongs to.' })}"
          invalid="{$_('areas.settings.enclosure.invalid', { default: 'Please make a choice.' })}" />
      </div>
      <div class="col-12 col-sm-3 col-md-3 col-lg-3">
        <Select
          name="type"
          value="{$formData.type}"
          readonly="{$formData.id && $formData.id != ''}"
          on:change="{(value) => areaType(value.detail)}"
          required="{true}"
          options="{area_types}"
          label="{$_('areas.settings.type.label', { default: 'Type' })}"
          placeholder="{$_('areas.settings.type.placeholder', { default: 'Select type' })}"
          help="{$_('areas.settings.type.help', { default: 'Select the type of area. Each type has its own extra options and logic.' })}"
          invalid="{$_('areas.settings.type.invalid', { default: 'Please make a choice.' })}" />
      </div>
      <div class="col">
        <Field
          type="text"
          name="name"
          required="{true}"
          label="{$_('areas.settings.name.label', { default: 'Name' })}"
          placeholder="{$_('areas.settings.name.placeholder', { default: 'Enter a name' })}"
          help="{$_('areas.settings.name.help', { default: 'Enter an easy to remember name.' })}"
          invalid="{$_('areas.settings.name.invalid', { default: 'The entered name is not valid. It cannot be empty.' })}" />
      </div>

      {#if $formData.type != 'lights'}
        <div class="col-12 col-sm-3 col-md-3 col-lg-3">
          <Select
            name="setup.depends_on"
            value="{$formData.setup?.depends_on}"
            multiple="{true}"
            options="{areas.filter((item) => {
              return item.value != $formData.id;
            })}"
            sort="{true}"
            label="{$_('areas.settings.depends_on.label', { default: 'Depends on' })}"
            placeholder="{$_('areas.settings.depends_on.placeholder', { default: 'Select depending areas' })}"
            help="{$_('areas.settings.depends_on.help', { default: 'Select the areas where this area depends on.' })}"
            invalid="{$_('areas.settings.depends_on.invalid', { default: 'Please make a choice.' })}" />
        </div>
      {/if}
    </div>

    <div class="row">
      <div
        class="col-12 col-sm-6"
        class:col-md-4="{['lights', 'audio'].indexOf($formData.type) != -1}"
        class:col-lg-4="{['lights', 'audio'].indexOf($formData.type) != -1}"
        class:col-md-3="{['lights', 'audio'].indexOf($formData.type) == -1}"
        class:col-lg-3="{['lights', 'audio'].indexOf($formData.type) == -1}">
        <Select
          name="mode"
          value="{$formData.mode}"
          on:change="{(value) => areaMode(value.detail)}"
          required="{true}"
          options="{[
            { value: 'disabled', text: $_('areas.settings.mode.options.disabled', { default: 'Disabled' }) },
            {
              value: 'main_lights',
              text: $_('areas.settings.mode.options.main_lights', { default: 'Main lights' }),
              disabled: ['lights'].indexOf($formData.type) != -1,
            },
            {
              value: 'sensors',
              text: $_('areas.settings.mode.options.sensors', { default: 'Sensors' }),
              disabled: ['lights', 'audio'].indexOf($formData.type) != -1,
            },
            { value: 'timer', text: $_('areas.settings.mode.options.timer', { default: 'Timer' }) },
            { value: 'weather', text: $_('areas.settings.mode.options.weather', { default: 'Weather day/night' }), disabled : weather === null || weather.location === undefined },
            { value: 'weather_inverse', text: $_('areas.settings.mode.options.weather_inverse', { default: 'Weather night/day' }), disabled : weather === null || weather.location === undefined },
          ]}"
          label="{$_('areas.settings.mode.label', { default: 'Mode' })}"
          placeholder="{$_('areas.settings.mode.placeholder', { default: 'Select mode' })}"
          help="{$_('areas.settings.mode.help', {
            default: 'Select the mode of this area. This will change the timing and duration of the relays.',
          })}"
          invalid="{$_('areas.settings.mode.invalid', { default: 'Please make a choice.' })}" />
      </div>

      <!-- Lights area  -->
      {#if ['lights'].indexOf($formData.type) != -1}
        <div class="col-12 col-sm-6 col-md-3 col-lg-2">
          <Field
            type="number"
            name="setup.min_day_hours"
            step="0.001"
            min="0"
            max="24"
            required="{['weather', 'weather_inverse'].indexOf($formData.mode) != -1}"
            readonly="{['weather', 'weather_inverse'].indexOf($formData.mode) == -1}"
            label="{$_('areas.settings.setup.min_day_hours.label', { default: 'Minimum hours' })}"
            placeholder="{$_('areas.settings.setup.min_day_hours.placeholder', { default: 'Enter number' })}"
            help="{$_('areas.settings.setup.min_day_hours.help', {
              default:
                'The minimum amount of hours that the lights are turned on. This is only valid in weather mode. When the day is shorter then this minimum value, the day will be extended to this minimum value.',
            })}"
            invalid="{$_('areas.settings.setup.min_day_hours.invalid', {
              default: 'The entered value is not valid. Enter a valid number between {min} and {max}.',
              values: { min: 0, max: 24 },
            })}" />
        </div>
        <div class="col-12 col-sm-6 col-md-3 col-lg-2">
          <Field
            type="number"
            name="setup.max_day_hours"
            step="0.001"
            min="0"
            max="24"
            required="{['weather', 'weather_inverse'].indexOf($formData.mode) != -1}"
            readonly="{['weather', 'weather_inverse'].indexOf($formData.mode) == -1}"
            label="{$_('areas.settings.setup.max_day_hours.label', { default: 'Maximum hours' })}"
            placeholder="{$_('areas.settings.setup.max_day_hours.placeholder', { default: 'Enter number' })}"
            help="{$_('areas.settings.setup.max_day_hours.help', {
              default:
                'The maximum amount of hours that the lights are turned on. This is only valid in weather mode. When the day is longer then this maximum value, the day will be shortened to this maximum value.',
            })}"
            invalid="{$_('areas.settings.setup.max_day_hours.invalid', {
              default: 'The entered value is not valid. Enter a valid number between {min} and {max}.',
              values: { min: 0, max: 24 },
            })}" />
        </div>
        <div class="col-12 col-sm-6 col-md-3 col-lg-2">
          <Field
            type="number"
            name="setup.shift_day_hours"
            step="0.001"
            min="-12"
            max="12"
            required="{['weather', 'weather_inverse'].indexOf($formData.mode) != -1}"
            readonly="{['weather', 'weather_inverse'].indexOf($formData.mode) == -1}"
            label="{$_('areas.settings.setup.shift_day_hours.label', { default: 'Hours shift' })}"
            placeholder="{$_('areas.settings.setup.shift_day_hours.placeholder', { default: 'Enter number' })}"
            help="{$_('areas.settings.setup.shift_day_hours.help', {
              default: 'The amount of time to shift in hours based on the sun rise time. Negative values will make the day start earlier.',
            })}"
            invalid="{$_('areas.settings.setup.shift_day_hours.invalid', {
              default: 'The entered value is not valid. Enter a valid number between {min} and {max}.',
              values: { min: -12, max: 12 },
            })}" />
        </div>
        <div class="col-12 col-sm-6 col-md-3 col-lg-2">
          <Switch
            name="setup.main_lights"
            value="{$formData.setup?.main_lights}"
            label="{$_('areas.settings.setup.main_lights.label', { default: 'Main lights' })}"
            help="{$_('areas.settings.setup.main_lights.help', {
              default: 'Toggle this if this is the main lights for this enclosure. This is used for the light checks in other areas.',
            })}" />
        </div>
      {/if}
      <!-- End Lights area  -->

      <!-- Audio area  -->
      {#if $formData.type == 'audio'}
        <div class="col-12 col-sm-9 col-md-8 col-lg-8">
          <Select
            name="setup.soundcard"
            value="{$formData.setup?.soundcard}"
            required="{true}"
            options="{soundcards}"
            label="{$_('areas.settings.setup.soundcard.label', { default: 'Sound card' })}"
            placeholder="{$_('areas.settings.setup.soundcard.placeholder', { default: 'Select a sound card' })}"
            help="{$_('areas.settings.setup.soundcard.help', { default: 'Select the sound card that is used for this area.' })}"
            invalid="{$_('areas.settings.setup.soundcard.invalid', { default: 'Please make a choice.' })}" />
        </div>
      {/if}
      <!-- End Audio area  -->

      {#if ['lights', 'audio'].indexOf($formData.type) == -1}
        <div class="col-12 col-sm-6 col-md-3 col-lg-3">
          <Select
            name="setup.sensors"
            value="{$formData.setup?.sensors}"
            multiple="{true}"
            required="{$formData.mode == 'sensors'}"
            options="{sensors.filter((item) => sensor_filter.length == 0 || sensor_filter.indexOf(item.type) != -1)}"
            on:change="{(value) => (showSensorDeviation = value.detail.length > 0)}"
            label="{$_('areas.settings.setup.sensors.label', { default: 'Sensors' })}"
            placeholder="{$_('areas.settings.setup.sensors.placeholder', { default: 'Select sensors' })}"
            help="{$_('areas.settings.setup.sensors.help', { default: 'Select sensors to use for sensor based mode.' })}"
            invalid="{$_('areas.settings.setup.sensors.invalid', { default: 'Please make a choice.' })}" />
        </div>
      {/if}

      {#if ['lights', 'audio', 'watertank'].indexOf($formData.type) == -1}
        <div class="col col-12 col-sm-6 col-md-3 col-lg-3">
          <Field
            type="number"
            name="setup.day_night_difference"
            step="0.001"
            value="0"
            label="{$_('areas.settings.setup.day_night_difference.label', { default: 'Day/night difference' })}"
            placeholder="{$_('areas.settings.setup.day_night_difference.placeholder', { default: 'Enter number' })}"
            help="{$_('areas.settings.setup.day_night_difference.help', { default: 'Amount to change between day and night.' })}"
            invalid="{$_('areas.settings.setup.day_night_difference.invalid', { default: 'Enter a valid number.' })}" />
        </div>

        <div class="col col-12 col-sm-6 col-md-3 col-lg-3">
          <Select
            name="setup.day_night_source"
            value="{$formData.setup?.day_night_source}"
            options="{[
              { value: 'lights', text: $_('areas.settings.setup.day_night_source.options.lights', { default: 'Lights' }) },
              { value: 'weather', text: $_('areas.settings.setup.day_night_source.options.weather', { default: 'Weather' }) },
            ]}"
            label="{$_('areas.settings.setup.day_night_source.label', { default: 'Day/night source' })}"
            placeholder="{$_('areas.settings.setup.day_night_source.placeholder', { default: 'Select a day/night source' })}"
            help="{$_('areas.settings.setup.day_night_source.help', { default: "Select source when it is 'day'." })}"
            invalid="{$_('areas.settings.setup.day_night_source.invalid', { default: 'Please make a choice.' })}" />
        </div>
      {/if}

      <!-- Watertank -->
      {#if $formData.type == 'watertank'}
        <div class="col col-12 col-sm-6 col-md-2 col-lg-2">
          <Field
            type="number"
            name="setup.watertank_volume"
            step="0.001"
            min="0"
            label="{$_('areas.settings.setup.watertank_volume.label', { default: 'Water volume' })}"
            placeholder="{$_('areas.settings.setup.watertank_volume.placeholder', { default: 'Enter number' })}"
            help="{$_('areas.settings.setup.watertank_volume.help', { default: 'Enter the volume of the water tank.' })}"
            invalid="{$_('areas.settings.setup.watertank_volume.invalid', {
              default: 'Please enter a minimum value of {value}.',
              values: { value: 0 },
            })}" />
        </div>
        <div class="col col-12 col-sm-6 col-md-2 col-lg-2">
          <Field
            type="number"
            name="setup.watertank_height"
            step="0.001"
            min="0"
            label="{$_('areas.settings.setup.watertank_height.label', { default: 'Height' })}"
            placeholder="{$_('areas.settings.setup.watertank_height.placeholder', { default: 'Enter number' })}"
            help="{$_('areas.settings.setup.watertank_height.help', { default: 'Enter the height of the water tank.' })}"
            invalid="{$_('areas.settings.setup.watertank_height.invalid', {
              default: 'Please enter a minimum value of {value}.',
              values: { value: 0 },
            })}" />
        </div>
        <div class="col col-12 col-sm-6 col-md-2 col-lg-2">
          <Field
            type="number"
            name="setup.watertank_offset"
            step="0.001"
            min="0"
            label="{$_('areas.settings.setup.watertank_offset.label', { default: 'Offset' })}"
            placeholder="{$_('areas.settings.setup.watertank_offset.placeholder', { default: 'Enter number' })}"
            help="{$_('areas.settings.setup.watertank_offset.help', { default: 'Enter the offset between sensor and water height.' })}"
            invalid="{$_('areas.settings.setup.watertank_offset.invalid', {
              default: 'Please enter a minimum value of {value}.',
              values: { value: 0 },
            })}" />
        </div>
      {/if}
      <!-- End Watertank -->
    </div>
    {#if showSensorDeviation}
      <div class="row">
        <div class="col">
          <Field
            type="number"
            name="setup.deviation_low_alarm"
            step="0.1"
            label="{$_('areas.settings.setup.deviation_low_alarm.label', { default: 'Low alarm deviation' })}"
            placeholder="{$_('areas.settings.setup.deviation_low_alarm.placeholder', { default: 'Low alarm deviation' })}"
            help="{$_('areas.settings.setup.deviation_low_alarm.help', { default: 'Increase of decrease low alarm value.' })}"
            invalid="{$_('areas.settings.setup.deviation_low_alarm.invalid', { default: 'Enter a valid number.' })}" />
        </div>
        <div class="col">
          <Field
            type="number"
            name="setup.deviation_high_alarm"
            step="0.1"
            label="{$_('areas.settings.setup.deviation_high_alarm.label', { default: 'High alarm deviation' })}"
            placeholder="{$_('areas.settings.setup.deviation_high_alarm.placeholder', { default: 'High alarm deviation' })}"
            help="{$_('areas.settings.setup.deviation_high_alarm.help', { default: 'Increase of decrease high alarm value.' })}"
            invalid="{$_('areas.settings.setup.deviation_high_alarm.invalid', { default: 'Enter a valid number.' })}" />
        </div>
      </div>
    {/if}
    <div class="row">
      <div class="col">
        <span class="text-muted">
          <small
            >{$_('areas.settings.setup.periods.info', {
              default: 'Below you can per select the relays and timer settings per period daytime and nighttime.',
            })}</small>
        </span>
        <nav class="mb-2">
          <div class="nav nav-tabs" role="tablist">
            <a class="nav-item nav-link active" id="low-tab" data-toggle="tab" href="#low-tab-pane" role="tab" aria-controls="day">
              {#if ['lights', 'audio'].indexOf($formData.type) != -1}
                <i class="fas fa-sun"></i> {$_('areas.settings.setup.periods.day', { default: 'Day settings' })}
              {:else}
                <i class="fas fa-battery-empty"></i> {$_('areas.settings.setup.periods.low', { default: 'Low alarm' })}
              {/if}
            </a>
            <a class="nav-item nav-link" id="high-tab" data-toggle="tab" href="#high-tab-pane" role="tab" aria-controls="night">
              {#if ['lights', 'audio'].indexOf($formData.type) != -1}
                <i class="fas fa-moon"></i> {$_('areas.settings.setup.periods.night', { default: 'Night settings' })}
              {:else}
                <i class="fas fa-battery-full"></i> {$_('areas.settings.setup.periods.high', { default: 'High alarm' })}
              {/if}
            </a>
            {#if ['lights', 'audio'].indexOf($formData.type) == -1}
              <a class="nav-item nav-link" id="variation-tab" data-toggle="tab" href="#area_variation" role="tab" aria-controls="high">
                <i class="fas fa-exchange-alt"></i>
                {$_('areas.settings.setup.periods.varation', { default: 'Variation' })}
              </a>
            {/if}
          </div>
        </nav>
        <div class="tab-content">
          <div class="tab-pane fade show active" id="low-tab-pane" role="tabpanel" aria-labelledby="low-tab">
            <div class="row" class:d-none="{['timer', 'weather', 'weather_inverse'].indexOf($formData.mode) == -1}">
              <div class="col">
                <Field
                  type="time"
                  name="setup.low.begin"
                  required="{$formData.mode == 'timer' &&
                    ($formData.setup.low.relays?.length > 0 || $formData.setup.low.playlists?.length > 0)}"
                  readonly="{$formData.mode != 'timer'}"
                  label="{$_('areas.settings.setup.low.begin.label', { default: 'Begin time' })}"
                  placeholder="{$_('areas.settings.setup.low.begin.placeholder', { default: 'Enter begin time' })}"
                  help="{$_('areas.settings.setup.low.begin.help', {
                    default: 'The time of the day when the relays are toggled on each night.',
                  })}"
                  invalid="{$_('areas.settings.setup.low.begin.invalid', { default: 'Enter a valid time.' })}" />
              </div>
              <div class="col">
                <Field
                  type="time"
                  name="setup.low.end"
                  required="{$formData.mode == 'timer' &&
                    ($formData.setup.low.relays?.length > 0 || $formData.setup.low.playlists?.length > 0)}"
                  readonly="{$formData.mode != 'timer'}"
                  label="{$_('areas.settings.setup.low.end.label', { default: 'End time' })}"
                  placeholder="{$_('areas.settings.setup.low.end.placeholder', { default: 'Enter end time' })}"
                  help="{$_('areas.settings.setup.low.end.help', {
                    default: 'The time of the day when the relays are toggled off each night.',
                  })}"
                  invalid="{$_('areas.settings.setup.low.end.invalid', { default: 'Enter a valid time.' })}" />
              </div>
              <div class="col">
                <Field
                  type="number"
                  name="setup.low.on_duration"
                  step="0.1"
                  min="0"
                  readonly="{$formData.mode != 'timer'}"
                  label="{$_('areas.settings.setup.low.on_duration.label', { default: 'On duration' })}"
                  placeholder="{$_('areas.settings.setup.low.on_duration.placeholder', { default: 'On duration' })}"
                  help="{$_('areas.settings.setup.low.on_duration.help', {
                    default:
                      "The duration when the relays should be on. If this is shorter then all day, you will get a timer functionality. Enter '0' to have a full night.",
                  })}"
                  invalid="{$_('areas.settings.setup.low.on_duration.invalid', { default: 'Enter a valid duration in minutes.' })}" />
              </div>
              <div class="col">
                <Field
                  type="number"
                  name="setup.low.off_duration"
                  step="0.1"
                  min="0"
                  readonly="{$formData.mode != 'timer'}"
                  label="{$_('areas.settings.setup.low.off_duration.label', { default: 'Off duration' })}"
                  placeholder="{$_('areas.settings.setup.low.off_duration.placeholder', { default: 'Off duration' })}"
                  help="{$_('areas.settings.setup.low.off_duration.help', {
                    default: "The duration when the relays should be stay off when switched off. Enter '0' to disable.",
                  })}"
                  invalid="{$_('areas.settings.setup.low.off_duration.invalid', { default: 'Enter a valid duration in minutes.' })}" />
              </div>
            </div>
            <div class="row">
              {#if ['lights', 'audio', 'watertank'].indexOf($formData.type) == -1}
                <div class="col">
                  <Field
                    type="number"
                    name="setup.low.power_on_time"
                    step="0.1"
                    min="0"
                    label="{$_('areas.settings.setup.low.power_on_time.label', { default: 'Power on time' })}"
                    placeholder="{$_('areas.settings.setup.low.power_on_time.placeholder', { default: 'Power on time' })}"
                    help="{$_('areas.settings.setup.low.power_on_time.help', {
                      default: 'The duration in seconds to toggle on the relay.',
                    })}"
                    invalid="{$_('areas.settings.setup.low.power_on_time.invalid', { default: 'Enter a valid number.' })}" />
                </div>
                <div class="col">
                  <Field
                    type="number"
                    name="setup.low.settle_time"
                    step="0.1"
                    min="0"
                    label="{$_('areas.settings.setup.low.settle_time.label', { default: 'Settle time' })}"
                    placeholder="{$_('areas.settings.setup.low.settle_time.placeholder', { default: 'Settle time' })}"
                    help="{$_('areas.settings.setup.low.settle_time.help', { default: 'The duration in seconds between two actions.' })}"
                    invalid="{$_('areas.settings.setup.low.settle_time.invalid', { default: 'Enter a valid number.' })}" />
                </div>
              {/if}
              {#if ['lights', 'audio', 'watertank'].indexOf($formData.type) == -1}
                <div class="col">
                  <Select
                    name="setup.low.light_status"
                    value="{$formData.setup?.low.light_status}"
                    options="{[
                      { value: 'ignore', text: $_('areas.settings.setup.low.light_status.options.ignore', { default: 'Ignored' }) },
                      { value: 'on', text: $_('areas.settings.setup.low.light_status.options.on', { default: 'On' }) },
                      { value: 'off', text: $_('areas.settings.setup.low.light_status.options.off', { default: 'Off' }) },
                    ]}"
                    label="{$_('areas.settings.setup.low.light_status.label', { default: 'Light status' })}"
                    placeholder="{$_('areas.settings.setup.low.light_status.placeholder', { default: 'Select a state' })}"
                    help="{$_('areas.settings.setup.low.light_status.help', { default: 'Select the lights status.' })}"
                    invalid="{$_('areas.settings.setup.low.light_status.invalid', { default: 'Please make a choice.' })}" />
                </div>
                <div class="col">
                  <Select
                    name="setup.low.door_status"
                    value="{$formData.setup?.low.door_status}"
                    options="{[
                      { value: 'ignore', text: $_('areas.settings.setup.low.door_status.options.ignore', { default: 'Ignored' }) },
                      { value: 'open', text: $_('areas.settings.setup.low.door_status.options.open', { default: 'Open' }) },
                      { value: 'closed', text: $_('areas.settings.setup.low.door_status.options.closed', { default: 'Closed' }) },
                    ]}"
                    label="{$_('areas.settings.setup.low.door_status.label', { default: 'Door status' })}"
                    placeholder="{$_('areas.settings.setup.low.door_status.placeholder', { default: 'Select a state' })}"
                    help="{$_('areas.settings.setup.low.door_status.help', { default: 'Select the door status.' })}"
                    invalid="{$_('areas.settings.setup.low.door_status.invalid', { default: 'Please make a choice.' })}" />
                </div>
                <div class="col">
                  <Field
                    type="number"
                    name="setup.low.trigger_threshold"
                    step="1"
                    min="0"
                    label="{$_('areas.settings.setup.low.trigger_threshold.label', { default: 'Alarm threshold' })}"
                    placeholder="{$_('areas.settings.setup.low.trigger_threshold.placeholder', { default: 'Threshold' })}"
                    help="{$_('areas.settings.setup.low.trigger_threshold.help', {
                      default: 'Enter the amount of alarms before action take place.',
                    })}"
                    invalid="{$_('areas.settings.setup.low.trigger_threshold.invalid', { default: 'Enter a valid number.' })}" />
                </div>
                <div class="col">
                  <Switch
                    name="setup.low.ignore_low"
                    value="{$formData.setup?.low.ignore_low}"
                    label="{$_('areas.settings.setup.low.ignore_low.label', { default: 'Ignore low alarm' })}"
                    help="{$_('areas.settings.setup.low.ignore_low.help', {
                      default: 'Toggle to ignore the low alarm value of the sensors, and use high alarm value only.',
                    })}" />
                </div>
              {/if}
              {#if $formData.type === 'audio'}
                <div class="col-12">
                  <Select
                    name="setup.low.playlists"
                    value="{$formData.setup?.low.playlists ?? null}"
                    multiple="{true}"
                    on:change="{(value) => ($formData.setup.low.playlists = value.detail)}"
                    required="{$formData.mode !== 'disabled' &&
                      ($formData.setup?.low.playlists?.length ?? 0) === 0 &&
                      ($formData.setup?.high.playlists?.length ?? 0) === 0}"
                    readonly="{$formData.mode === 'disabled'}"
                    options="{playlists}"
                    label="{$_('areas.settings.setup.low.playlists.label', { default: 'Playlists' })}"
                    placeholder="{$_('areas.settings.setup.low.playlists.placeholder', { default: 'Select playlists' })}"
                    help="{$_('areas.settings.setup.low.playlists.help', { default: 'Select the playlist(s) to be played.' })}"
                    invalid="{$_('areas.settings.setup.low.playlists.invalid', { default: 'Please make a choice.' })}" />
                </div>
              {:else}
                <div class="col-12">
                  <Select
                    name="setup.low.relays"
                    value="{$formData.setup?.low.relays ?? null}"
                    multiple="{true}"
                    sort="{true}"
                    on:change="{(value) => updateTweakRelays('low', value.detail)}"
                    required="{$formData.mode !== 'disabled' &&
                      $formData.mode !== 'sensors' &&
                      ($formData.setup?.low.relays?.length ?? 0) === 0 &&
                      ($formData.setup?.high.relays?.length ?? 0) === 0}"
                    options="{relays.map((item) => {
                      return { value: item.id, text: item.name, disabled: $formData.setup?.high.relays?.indexOf(item.id) !== -1 };
                    })}"
                    label="{$_('areas.settings.setup.low.relays.label', { default: 'Relays' })}"
                    placeholder="{$_('areas.settings.setup.low.relays.placeholder', { default: 'Select relays' })}"
                    help="{$_('areas.settings.setup.low.relays.help', { default: 'Select the relays to toggle.' })}"
                    invalid="{$_('areas.settings.setup.low.relays.invalid', { default: 'Please make a choice.' })}" />
                </div>
              {/if}
            </div>

            {#if $formData.setup?.low?.tweaks ?? false}
              <div class="row">
                <div class="col-12">
                  <ul class="nav nav-tabs mb-2" role="tablist">
                    {#each $formData.setup.low.tweaks as relay, index}
                      <li class="nav-item">
                        <a
                          class="nav-link"
                          class:active="{index == 0}"
                          id="{`relay_low_setting_${relay.id}-tab`}"
                          href="{`#relay_low_setting_${relay.id}`}"
                          data-toggle="tab"
                          role="tab"
                          aria-controls="{`relay_low_setting_${relay.id}`}">
                          <i class="fas fa-bolt mr-1"></i>{relayName(relay.id)}
                        </a>
                      </li>
                    {/each}
                  </ul>
                </div>
                <div class="tab-content w-100">
                  {#each $formData.setup.low.tweaks as relay, index}
                    <div
                      class="tab-pane fade"
                      class:active="{index == 0}"
                      class:show="{index == 0}"
                      id="{`relay_low_setting_${relay.id}`}"
                      role="tabpanel"
                      aria-labelledby="{`relay_low_setting_${relay.id}-tab`}">
                      <div class="row">
                        <input type="hidden" name="{`setup.low.tweaks.${index}.id`}" value="{relay.id}" readonly />
                        <div class="col pl-3">
                          <Slider
                            name="{`setup.low.tweaks.${index}.on`}"
                            horizontal="{true}"
                            required="{true}"
                            max=180
                            on:change="{updateTweakSliders}"
                            value="{tweakValue($formData.setup.low.tweaks[index].on, relayDimmer(relay.id) ? [0, 30] : 0)}"
                            label="{relayDimmer(relay.id)
                              ? $_('areas.settings.setup.low.tweaks.on.dimmer.label', { default: 'Dimmer on duration' })
                              : $_('areas.settings.setup.low.tweaks.on.relay.label', { default: 'Relay delay on' })}" />
                        </div>
                        <div class="col pr-3">
                          <Slider
                            name="{`setup.low.tweaks.${index}.off`}"
                            horizontal="{true}"
                            required="{true}"
                            max=180
                            on:change="{updateTweakSliders}"
                            value="{tweakValue($formData.setup.low.tweaks[index].off, relayDimmer(relay.id) ? [0, 30] : 0)}"
                            label="{relayDimmer(relay.id)
                              ? $_('areas.settings.setup.low.tweaks.off.dimmer.label', { default: 'Dimmer off duration' })
                              : $_('areas.settings.setup.low.tweaks.off.relay.label', { default: 'Relay delay off' })}" />
                        </div>
                      </div>
                      <div class="row">
                        <div class="col-12 pl-3">
                          <small class="text-muted d-none">
                            {#if relayDimmer(relay.id)}
                              {$_('areas.settings.setup.low.tweaks.dimmer.info', {
                                default:
                                  'Select the delay and duration for the dimmer to go to on or off in minutes. Max duration is 180 minutes.',
                              })}
                            {:else}
                              {$_('areas.settings.setup.low.tweaks.relay.info', {
                                default: 'Select the delay in minutes that a relay waits before it turns on. Max delay is 180 minutes.',
                              })}
                            {/if}
                          </small>
                        </div>
                      </div>
                    </div>
                  {/each}
                </div>
              </div>
            {/if}
          </div>
          <div class="tab-pane fade" id="high-tab-pane" role="tabpanel" aria-labelledby="high-tab">
            <div class="row" class:d-none="{['timer', 'weather', 'weather_inverse'].indexOf($formData.mode) == -1}">
              <div class="col">
                <Field
                  type="time"
                  name="setup.high.begin"
                  required="{$formData.mode == 'timer' &&
                    ($formData.setup.high.relays?.length > 0 || $formData.setup.high.playlists?.length > 0)}"
                  readonly="{$formData.mode != 'timer'}"
                  label="{$_('areas.settings.setup.high.begin.label', { default: 'Begin time' })}"
                  placeholder="{$_('areas.settings.setup.high.begin.placeholder', { default: 'Enter begin time' })}"
                  help="{$_('areas.settings.setup.high.begin.help', {
                    default: 'The time of the day when the relays are toggled on each night.',
                  })}"
                  invalid="{$_('areas.settings.setup.high.begin.invalid', { default: 'Enter a valid time.' })}" />
              </div>
              <div class="col">
                <Field
                  type="time"
                  name="setup.high.end"
                  required="{$formData.mode == 'timer' &&
                    ($formData.setup.high.relays?.length > 0 || $formData.setup.high.playlists?.length > 0)}"
                  readonly="{$formData.mode != 'timer'}"
                  label="{$_('areas.settings.setup.high.end.label', { default: 'End time' })}"
                  placeholder="{$_('areas.settings.setup.high.end.placeholder', { default: 'Enter end time' })}"
                  help="{$_('areas.settings.setup.high.end.help', {
                    default: 'The time of the day when the relays are toggled off each night.',
                  })}"
                  invalid="{$_('areas.settings.setup.high.end.invalid', { default: 'Enter a valid time.' })}" />
              </div>
              <div class="col">
                <Field
                  type="number"
                  name="setup.high.on_duration"
                  step="0.1"
                  min="0"
                  readonly="{$formData.mode != 'timer'}"
                  label="{$_('areas.settings.setup.high.on_duration.label', { default: 'On duration' })}"
                  placeholder="{$_('areas.settings.setup.high.on_duration.placeholder', { default: 'On duration' })}"
                  help="{$_('areas.settings.setup.high.on_duration.help', {
                    default:
                      "The duration when the relays should be on. If this is shorter then all day, you will get a timer functionality. Enter '0' to have a full night.",
                  })}"
                  invalid="{$_('areas.settings.setup.high.on_duration.invalid', { default: 'Enter a valid duration in minutes.' })}" />
              </div>
              <div class="col">
                <Field
                  type="number"
                  name="setup.high.off_duration"
                  step="0.1"
                  min="0"
                  readonly="{$formData.mode != 'timer'}"
                  label="{$_('areas.settings.setup.high.off_duration.label', { default: 'Off duration' })}"
                  placeholder="{$_('areas.settings.setup.high.off_duration.placeholder', { default: 'Off duration' })}"
                  help="{$_('areas.settings.setup.high.off_duration.help', {
                    default: "The duration when the relays should be stay off when switched off. Enter '0' to disable.",
                  })}"
                  invalid="{$_('areas.settings.setup.high.off_duration.invalid', { default: 'Enter a valid duration in minutes.' })}" />
              </div>
            </div>

            <div class="row">
              {#if ['lights', 'audio', 'watertank'].indexOf($formData.type) == -1}
                <div class="col">
                  <Field
                    type="number"
                    name="setup.high.power_on_time"
                    step="0.1"
                    min="0"
                    label="{$_('areas.settings.setup.high.power_on_time.label', { default: 'Power on time' })}"
                    placeholder="{$_('areas.settings.setup.high.power_on_time.placeholder', { default: 'Power on time' })}"
                    help="{$_('areas.settings.setup.high.power_on_time.help', {
                      default: 'The duration in seconds to toggle on the relay.',
                    })}"
                    invalid="{$_('areas.settings.setup.high.power_on_time.invalid', { default: 'Enter a valid number.' })}" />
                </div>
                <div class="col">
                  <Field
                    type="number"
                    name="setup.high.settle_time"
                    step="0.1"
                    min="0"
                    label="{$_('areas.settings.setup.high.settle_time.label', { default: 'Settle time' })}"
                    placeholder="{$_('areas.settings.setup.high.settle_time.placeholder', { default: 'Settle time' })}"
                    help="{$_('areas.settings.setup.high.settle_time.help', { default: 'The duration in seconds between two actions.' })}"
                    invalid="{$_('areas.settings.setup.high.settle_time.invalid', { default: 'Enter a valid number.' })}" />
                </div>
              {/if}
              {#if ['lights', 'audio', 'watertank'].indexOf($formData.type) == -1}
                <div class="col">
                  <Select
                    name="setup.high.light_status"
                    value="{$formData.setup?.high.light_status}"
                    options="{[
                      { value: 'ignore', text: $_('areas.settings.setup.high.light_status.options.ignore', { default: 'Ignored' }) },
                      { value: 'on', text: $_('areas.settings.setup.high.light_status.options.on', { default: 'On' }) },
                      { value: 'off', text: $_('areas.settings.setup.high.light_status.options.off', { default: 'Off' }) },
                    ]}"
                    label="{$_('areas.settings.setup.high.light_status.label', { default: 'Light status' })}"
                    placeholder="{$_('areas.settings.setup.high.light_status.placeholder', { default: 'Select a state' })}"
                    help="{$_('areas.settings.setup.high.light_status.help', { default: 'Select the lights status.' })}"
                    invalid="{$_('areas.settings.setup.high.light_status.invalid', { default: 'Please make a choice.' })}" />
                </div>
                <div class="col">
                  <Select
                    name="setup.high.door_status"
                    value="{$formData.setup?.high.door_status}"
                    options="{[
                      { value: 'ignore', text: $_('areas.settings.setup.high.door_status.options.ignore', { default: 'Ignored' }) },
                      { value: 'open', text: $_('areas.settings.setup.high.door_status.options.open', { default: 'Open' }) },
                      { value: 'closed', text: $_('areas.settings.setup.high.door_status.options.closed', { default: 'Closed' }) },
                    ]}"
                    label="{$_('areas.settings.setup.high.door_status.label', { default: 'Door status' })}"
                    placeholder="{$_('areas.settings.setup.high.door_status.placeholder', { default: 'Select a state' })}"
                    help="{$_('areas.settings.setup.high.door_status.help', { default: 'Select the door status.' })}"
                    invalid="{$_('areas.settings.setup.high.door_status.invalid', { default: 'Please make a choice.' })}" />
                </div>
                <div class="col">
                  <Field
                    type="number"
                    name="setup.high.trigger_threshold"
                    step="1"
                    min="0"
                    label="{$_('areas.settings.setup.high.trigger_threshold.label', { default: 'Alarm threshold' })}"
                    placeholder="{$_('areas.settings.setup.high.trigger_threshold.placeholder', { default: 'Threshold' })}"
                    help="{$_('areas.settings.setup.high.trigger_threshold.help', {
                      default: 'Enter the amount of alarms before action take place.',
                    })}"
                    invalid="{$_('areas.settings.setup.high.trigger_threshold.invalid', { default: 'Enter a valid number.' })}" />
                </div>
                <div class="col">
                  <Switch
                    name="setup.high.ignore_high"
                    value="{$formData.setup?.high.ignore_high}"
                    label="{$_('areas.settings.setup.high.ignore_high.label', { default: 'Ignore high alarm' })}"
                    help="{$_('areas.settings.setup.high.ignore_high.help', {
                      default: 'Toggle to ignore the high alarm value of the sensors, and use high alarm value only.',
                    })}" />
                </div>
              {/if}
              {#if $formData.type === 'audio'}
                <div class="col-12">
                  <Select
                    name="setup.high.playlists"
                    value="{$formData.setup?.high.playlists ?? null}"
                    multiple="{true}"
                    sort="{true}"
                    on:change="{(value) => ($formData.setup.high.playlists = value.detail)}"
                    required="{$formData.mode !== 'disabled' &&
                      ($formData.setup?.low.playlists?.length ?? 0) === 0 &&
                      ($formData.setup?.high.playlists?.length ?? 0) === 0}"
                    readonly="{$formData.mode === 'disabled'}"
                    options="{playlists}"
                    label="{$_('areas.settings.setup.high.playlists.label', { default: 'Playlists' })}"
                    placeholder="{$_('areas.settings.setup.high.playlists.placeholder', { default: 'Select playlists' })}"
                    help="{$_('areas.settings.setup.high.playlists.help', { default: 'Select the playlist(s) to be played.' })}"
                    invalid="{$_('areas.settings.setup.high.playlists.invalid', { default: 'Please make a choice.' })}" />
                </div>
              {:else}
                <div class="col-12">
                  <Select
                    name="setup.high.relays"
                    value="{$formData.setup?.high.relays ?? null}"
                    multiple="{true}"
                    sort="{true}"
                    on:change="{(value) => updateTweakRelays('high', value.detail)}"
                    required="{$formData.mode !== 'disabled' &&
                      $formData.mode !== 'sensors' &&
                      ($formData.setup?.low.relays?.length ?? 0) === 0 &&
                      ($formData.setup?.high.relays?.length ?? 0) === 0}"
                    options="{relays.map((item) => {
                      return { value: item.id, text: item.name, disabled: $formData.setup?.low.relays?.indexOf(item.id) !== -1 };
                    })}"
                    label="{$_('areas.settings.setup.high.relays.label', { default: 'Relays' })}"
                    placeholder="{$_('areas.settings.setup.high.relays.placeholder', { default: 'Select relays' })}"
                    help="{$_('areas.settings.setup.high.relays.help', { default: 'Select the relays to toggle.' })}"
                    invalid="{$_('areas.settings.setup.high.relays.invalid', { default: 'Please make a choice.' })}" />
                </div>
              {/if}
            </div>
            {#if $formData.setup?.high?.tweaks ?? false}
              <div class="row">
                <div class="col-12">
                  <ul class="nav nav-tabs mb-2" role="tablist">
                    {#each $formData.setup.high.tweaks as relay, index}
                      <li class="nav-item">
                        <a
                          class="nav-link"
                          class:active="{index == 0}"
                          id="{`relay_high_setting_${relay.id}-tab`}"
                          href="{`#relay_high_setting_${relay.id}`}"
                          data-toggle="tab"
                          role="tab"
                          aria-controls="{`relay_high_setting_${relay.id}`}">
                          <i class="fas fa-bolt mr-1"></i>{relayName(relay.id)}
                        </a>
                      </li>
                    {/each}
                  </ul>
                </div>
                <div class="tab-content w-100">
                  {#each $formData.setup.high.tweaks as relay, index}
                    <div
                      class="tab-pane fade"
                      class:active="{index == 0}"
                      class:show="{index == 0}"
                      id="{`relay_high_setting_${relay.id}`}"
                      role="tabpanel"
                      aria-labelledby="{`relay_high_setting_${relay.id}-tab`}">
                      <div class="row">
                        <input type="hidden" name="{`setup.high.tweaks.${index}.id`}" value="{relay.id}" readonly />
                        <div class="col pl-3">
                          <Slider
                            name="{`setup.high.tweaks.${index}.on`}"
                            horizontal="{true}"
                            required="{true}"
                            max=180
                            on:change="{updateTweakSliders}"
                            value="{tweakValue($formData.setup.high.tweaks[index].on, relayDimmer(relay.id) ? [0, 30] : 0)}"
                            label="{relayDimmer(relay.id)
                              ? $_('areas.settings.setup.high.tweaks.on.dimmer.label', { default: 'Dimmer on duration' })
                              : $_('areas.settings.setup.high.tweaks.on.relay.label', { default: 'Relay delay on' })}" />
                        </div>
                        <div class="col pr-3">
                          <Slider
                            name="{`setup.high.tweaks.${index}.off`}"
                            horizontal="{true}"
                            required="{true}"
                            max=180
                            on:change="{updateTweakSliders}"
                            value="{tweakValue($formData.setup.high.tweaks[index].off, relayDimmer(relay.id) ? [0, 30] : 0)}"
                            label="{relayDimmer(relay.id)
                              ? $_('areas.settings.setup.high.tweaks.off.dimmer.label', { default: 'Dimmer off duration' })
                              : $_('areas.settings.setup.high.tweaks.off.relay.label', { default: 'Relay delay off' })}" />
                        </div>
                      </div>
                      <div class="row">
                        <div class="col-12 pl-3">
                          <small class="text-muted d-none">
                            {#if relayDimmer(relay.id)}
                              {$_('areas.settings.setup.high.tweaks.dimmer.info', {
                                default:
                                  'Select the delay and duration for the dimmer to go to on or off in minutes. Max duration is 180 minutes.',
                              })}
                            {:else}
                              {$_('areas.settings.setup.high.tweaks.relay.info', {
                                default: 'Select the delay in minutes that a relay waits before it turns on. Max delay is 180 minutes.',
                              })}
                            {/if}
                          </small>
                        </div>
                      </div>
                    </div>
                  {/each}
                </div>
              </div>
            {/if}
          </div>
          <div class="tab-pane fade" id="area_variation" role="tabpanel" aria-labelledby="variation-tab">
            <div class="row text-muted">
              <div class="col">
                <span class="text-muted">
                  <small
                    >Here you can enter periods where the sensors will change their values according to the list below. Make sure the
                    periods are in chronological order!</small>
                </span>
              </div>
            </div>
            <div class="row">
              <div class="col-3 col-sm-3 col-md-3 col-lg-3">
                <div class="form-group no-margin">
                  <label for="variation_when">Source</label>
                </div>
              </div>
              {#if $formData.setup && ['external', 'script', 'weather'].indexOf($formData.setup.variation[$formData.setup.variation.length - 1].when ?? null) === -1}
                <div class="col-4 col-sm-4 col-md-4 col-lg-4">
                  <div class="form-group no-margin">
                    <label for="alarm_low_end">Period/duration</label>
                  </div>
                </div>
              {/if}
              {#if $formData.setup && ['external', 'script'].indexOf($formData.setup.variation[$formData.setup.variation.length - 1].when ?? null) !== -1}
                <div class="col-7 col-sm-7 col-md-7 col-lg-7">
                  <div class="form-group no-margin">
                    <label for="alarm_low_end">External source url</label>
                  </div>
                </div>
              {:else if $formData.setup && ['weather'].indexOf($formData.setup.variation[$formData.setup.variation.length - 1].when ?? null) !== -1}
                <div class="col-7 col-sm-7 col-md-7 col-lg-7">
                  <div class="form-group no-margin">
                    <label for="alarm_low_end">Offset</label>
                  </div>
                </div>
              {:else}
                <div class="col-3 col-sm-3 col-md-3 col-lg-3">
                  <div class="form-group no-margin">
                    <label for="variant_value">Difference</label>
                  </div>
                </div>
              {/if}
              <div class="col-1 col-sm-1 col-md-1 col-lg-1">
                <div class="form-group no-margin">
                  <label for="action">Action</label>
                </div>
              </div>
              <div class="col-1 col-sm-1 col-md-1 col-lg-1">
                <div class="form-group no-margin">
                  <label for="action">&nbsp;</label>
                </div>
              </div>
            </div>
            {#if $formData.setup?.variation}
              {#each $formData.setup.variation as variation, index}
                <div class="row">
                  <div class="col-3 col-sm-3 col-md-3 col-lg-3">
                    <Select
                      name="{`setup.variation.${index}.when`}"
                      value="{variation.when ?? null}"
                      sort="{true}"
                      on:change="{(value) => {
                        $formData.setup.variation[index].when = value.detail;
                      }}"
                      options="{[
                        { value: 'after', text: $_('areas.settings.setup.variation.when.options.after', { default: 'After x minutes' }) },
                        { value: 'at', text: $_('areas.settings.setup.variation.when.options.at', { default: 'At time' }) },
                        {
                          value: 'weather',
                          text: $_('areas.settings.setup.variation.when.options.weather', { default: 'Using current weather' }),
                          disabled: $formData.setup.variation.length >= 2,
                        },
                        {
                          value: 'external',
                          text: $_('areas.settings.setup.variation.when.options.external', { default: 'Use JSON source' }),
                          disabled: $formData.setup.variation.length >= 2,
                        },
                        {
                          value: 'script',
                          text: $_('areas.settings.setup.variation.when.options.script', { default: 'Use script' }),
                          disabled: $formData.setup.variation.length >= 2,
                        },
                      ]}"
                      placeholder="{$_('areas.settings.setup.variation.when.placeholder', { default: 'Select action' })}"
                      invalid="{$_('areas.settings.setup.variation.when.invalid', { default: 'Please make a choice.' })}" />
                  </div>
                  {#if $formData.setup && ['external', 'script'].indexOf($formData.setup.variation[index].when ?? null) !== -1}
                    <div class="col-7 col-sm-7 col-md-7 col-lg-7">
                      <Field
                        type="text"
                        name="{`setup.variation.${index}.source`}"
                        placeholder="{$_('areas.settings.setup.variation.period.source', {
                          default: 'Enter a full url, local JSON file or script file',
                        })}"
                        invalid="{$_('areas.settings.setup.variation.period.source', {
                          default: 'Enter a valid url, local JSON file or script file.',
                        })}" />
                    </div>
                  {:else if $formData.setup && ['weather'].indexOf($formData.setup.variation[index].when ?? null) !== -1}
                    <div class="col-7 col-sm-7 col-md-7 col-lg-7">
                      <Field
                        type="number"
                        name="{`setup.variation.${index}.offset`}"
                        placeholder="{$_('areas.settings.setup.variation.period.offset', { default: 'Offset' })}"
                        invalid="{$_('areas.settings.setup.variation.offset.invalid', { default: 'Enter a valid number.' })}" />
                    </div>
                  {:else}
                    <div class="col-4 col-sm-4 col-md-4 col-lg-4">
                      <Field
                        type="text"
                        name="{`setup.variation.${index}.period`}"
                        placeholder="{$_('areas.settings.setup.variation.period.placeholder', { default: 'Threshold' })}"
                        invalid="{$_('areas.settings.setup.variation.period.invalid', {
                          default: 'Enter a valid number or timestamp.',
                        })}" />
                    </div>
                    <div class="col-3 col-sm-3 col-md-3 col-lg-3">
                      <Field
                        type="number"
                        name="{`setup.variation.${index}.value`}"
                        placeholder="{$_('areas.settings.setup.variation.value.placeholder', { default: 'Difference' })}"
                        invalid="{$_('areas.settings.setup.variation.value.invalid', { default: 'Enter a valid number.' })}" />
                    </div>
                  {/if}
                  <div class="col-1 col-sm-1 col-md-1 col-lg-1">
                    <div class="form-group">
                      <button type="button" class="form-control" on:click="{addVariation}"><i class="fas fa-plus"></i></button>
                    </div>
                  </div>
                  <div class="col-1 col-sm-1 col-md-1 col-lg-1">
                    <div class="form-group">
                      <button
                        type="button"
                        class="form-control"
                        disabled="{index === 0 && $formData.setup.variation.length <= 1}"
                        on:click="{() => {
                          removeVariation(index);
                        }}"><i class="fas fa-minus"></i></button>
                    </div>
                  </div>
                </div>
              {/each}
            {/if}
            <div class="row">
              <div
                class="col-3 col-sm-3 col-md-3 col-lg-3"
                class:d-none="{!(
                  $formData.setup &&
                  ['external', 'script', 'weather'].indexOf(
                    $formData.setup.variation[$formData.setup.variation.length - 1].when ?? null
                  ) === -1
                )}">
                <div class="form-group">
                  <small class="text-muted d-none"> After x minutes change to value or at exactly a time stamp. </small>
                </div>
              </div>
              <div
                class="col-4 col-sm-4 col-md-4 col-lg-4"
                class:d-none="{$formData.setup &&
                  ['weather', 'external', 'script'].indexOf(
                    $formData.setup.variation[$formData.setup.variation.length - 1].when ?? null
                  ) !== -1}">
                <div class="form-group">
                  <small class="text-muted d-none"> Enter a duration in minutes or the actual time of the day. </small>
                </div>
              </div>
              <div
                class="col-3 col-sm-3 col-md-3 col-lg-3"
                class:d-none="{$formData.setup &&
                  ['weather', 'external', 'script'].indexOf(
                    $formData.setup.variation[$formData.setup.variation.length - 1].when ?? null
                  ) !== -1}">
                <div class="form-group">
                  <small class="text-muted d-none">
                    Enter a negative or positive value for a relative action. A number is treated as an absolute value.
                  </small>
                </div>
              </div>
              <div
                class="col-3 col-sm-3 col-md-3 col-lg-3"
                class:d-none="{!(
                  $formData.setup &&
                  ['external', 'script'].indexOf($formData.setup.variation[$formData.setup.variation.length - 1].when ?? null) !== -1
                )}">
                <div class="form-group">
                  <small class="text-muted d-none"> Remote data. </small>
                </div>
              </div>
              <div
                class="col-7 col-sm-7 col-md-7 col-lg-7"
                class:d-none="{!(
                  $formData.setup &&
                  ['external', 'script'].indexOf($formData.setup.variation[$formData.setup.variation.length - 1].when ?? null) !== -1
                )}">
                <div class="form-group">
                  <small class="text-muted d-none"> Enter a full url to the external source according to the Remote data feature. </small>
                </div>
              </div>
              <div
                class="col-3 col-sm-3 col-md-3 col-lg-3"
                class:d-none="{!(
                  $formData.setup &&
                  ['weather'].indexOf($formData.setup.variation[$formData.setup.variation.length - 1].when ?? null) !== -1
                )}">
                <div class="form-group">
                  <small class="text-muted d-none"> Climate mirroring. </small>
                </div>
              </div>
              <div
                class="col-7 col-sm-7 col-md-7 col-lg-7"
                class:d-none="{!(
                  $formData.setup &&
                  ['weather'].indexOf($formData.setup.variation[$formData.setup.variation.length - 1].when ?? null) !== -1
                )}">
                <div class="form-group">
                  <small class="text-muted d-none"> Enter a negative or positive offset value. </small>
                </div>
              </div>
              <div class="col-1 col-sm-1 col-md-1 col-lg-1">
                <div class="form-group">
                  <small class="text-muted d-none"> Add a new row </small>
                </div>
              </div>
              <div class="col-1 col-sm-1 col-md-1 col-lg-1">
                <div class="form-group">
                  <small class="text-muted d-none"> Remove row </small>
                </div>
              </div>
            </div>
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
