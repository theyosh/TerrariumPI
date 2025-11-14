<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import { writable } from 'svelte/store';
  import { _ } from 'svelte-i18n';
  import { createForm } from 'felte';

  import { isDay } from '../stores/terrariumpi';
  import { fetchSystemSettings, updateSystemSettings, getWeatherOptions } from '../providers/api';
  import { formToJSON, invalid_form_fields } from '../helpers/form-helpers';
  import { successNotification, errorNotification } from '../providers/notification-provider';

  import ModalForm from '../user-controls/ModalForm.svelte';
  import Field from '../components/form/Field.svelte';
  import Helper from '../components/form/Helper.svelte';
  import Select from '../components/form/Select.svelte';

  let wrapper_show;
  let wrapper_hide;
  let loading = false;
  let validated = false;
  let weatherProviders = [];
  let weatherProviderInfo = { info: '', example: '' };

  let formData = writable({});

  let editForm;

  const dispatch = createEventDispatcher();

  const successAction = () => {
    dispatch('save');
  };

  const _processForm = async (values, context) => {
    validated = true;

    if (context.form.checkValidity()) {
      loading = true;
      values = formToJSON(editForm, ['weather_provider']);

      try {
        // Post data
        await updateSystemSettings(values);
        // Notifify OK!
        successNotification(
          $_('weather.settings.save.ok.message', { default: 'The weather setting is saved.' }),
          $_('notification.form.save.ok.title', { default: 'Save OK' }),
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
      let error_message = $_('weather.settings.fields.error', {
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

  const matchWeatherProvider = (a, b) => {
    return b.startsWith(a.substring(0, a.indexOf('/', 8)));
  };

  export const show = () => {
    // Anonymous (Async) functions always as first!!
    (async () => {
      await Promise.all([
        // Load available weather source partners
        getWeatherOptions((data) => (weatherProviders = data)),
        // Load current settings
        fetchSystemSettings('weather_source', (data) => ($formData = { weather_source: data.value })),
      ]);

      let currentWeatherProvider = weatherProviders.find((weatherProvider) =>
        matchWeatherProvider($formData.weather_source, weatherProvider.url),
      );
      if (currentWeatherProvider) {
        $formData.weather_provider = currentWeatherProvider.hardware;
      }

      setFields($formData);

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
    setTimeout(() => {
      loading = false;
    }, 1000);
    wrapper_hide();
  };

  const changeWeatherProvider = (partner) => {
    let weatherProviderData = weatherProviders.find((weatherProvider) => weatherProvider.hardware === partner);
    if (!weatherProviderData) {
      return;
    }
    weatherProviderInfo.example = weatherProviderData.url;

    if (partner === 'Openweathermap.org') {
      weatherProviderInfo.info = $_('weather.settings.information', {
        values: {
          source_link:
            '<a href="https://openweathermap.org/" target="_blank" rel="noopener noreferrer">OpenWeatherMap</a>',
        },
        default: 'In order to use the weather system, you need to create a free account at {source_link}.',
      });
    } else if (partner === 'Open-Meteo.com') {
      weatherProviderInfo.info = $_('weather.settings.open_meteo.information', {
        values: {
          source_link: '<a href="https://open-meteo.com/" target="_blank" rel="noopener noreferrer">Open-Meteo</a>',
        },
        default: 'Get your API url at {source_link} for free without an account.',
      });
    }
  };

  onMount(() => {
    editForm.setAttribute('novalidate', 'novalidate');
  });
</script>

<ModalForm bind:show="{wrapper_show}" bind:hide="{wrapper_hide}" {loading}>
  <svelte:fragment slot="header">
    <i class="fas mr-2" class:fa-cloud-sun="{$isDay}" class:fa-cloud-moon="{!$isDay}"></i>
    {$_('weather.settings.title', { default: 'Weather settings' })}
    <Helper moreInfo="https://theyosh.github.io/TerrariumPI/setup/#weather" />
  </svelte:fragment>
  <form class="needs-validation" class:was-validated="{validated}" use:form bind:this="{editForm}">
    <div class="row">
      <div class="col-12 col-sm-6 col-md-3 col-lg-3">
        <Select
          name="weather_provider"
          value="{$formData.weather_provider}"
          on:change="{(value) => changeWeatherProvider(value.detail)}"
          options="{weatherProviders.map((weatherProvider) => {
            return { value: weatherProvider.hardware, text: weatherProvider.hardware };
          })}"
          label="{$_('weather.settings.weather_provider.label', { default: 'Provider' })}"
          placeholder="{$_('weather.settings.weather_provider.placeholder', { default: 'Select a provider' })}"
          help="{$_('weather.settings.weather_provider.help', { default: 'Select provider to get more information.' })}"
        />
      </div>
      <div class="col-12 col-sm-6 col-md-9 col-lg-9">
        <Field
          type="text"
          name="weather_source"
          class="col-9"
          required="{true}"
          label="{$_('weather.settings.weather_source.label', { default: 'Source url' })}"
          help="{$_('weather.settings.weather_source.help', {
            default: 'Enter the full api url like: {api_url_example}',
            values: {
              api_url_example: weatherProviderInfo.example,
            },
          })}"
          invalid="{$_('weather.settings.weather_source.invalid', { default: 'The entered url is not valid.' })}"
        />
      </div>
    </div>
    <!-- We need this nasty hack to make submit with enter key to work -->
    <button type="submit" style="display:none"> </button>
  </form>
  <p>{@html weatherProviderInfo.info}</p>

  <svelte:fragment slot="actions">
    <button type="button" class="btn btn-primary" disabled="{loading || $isSubmitting}" on:click="{formSubmit}">
      <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" class:d-none="{!$isSubmitting}"
      ></span>
      {$_('modal.general.save')}
    </button>
  </svelte:fragment>
</ModalForm>
