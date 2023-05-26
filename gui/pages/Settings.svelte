<script>
  import { onMount, onDestroy } from 'svelte';
  import { writable } from 'svelte/store';
  import { _, number } from 'svelte-i18n';
  import { PageHeader, BreadcrumbItem } from 'svelte-adminlte';
  import { createForm } from 'felte';
  import { setConfig } from 'svelte-adminlte/src/config.js';

  import { setCustomPageTitle, customPageTitleUsed } from '../stores/page-title';
  import { successNotification, errorNotification } from '../providers/notification-provider';
  import { formToJSON, invalid_form_fields } from '../helpers/form-helpers';
  import { languageFlag } from '../helpers/string-helpers';
  import { fetchSystemSettings, updateSystemSettings, uploadFile } from '../providers/api';
  import { changeLang, languages, currencies, currency } from '../locale/i18n';

  import Card from '../user-controls/Card.svelte';
  import CardSettingsTools from '../components/common/CardSettingsTools.svelte';
  import Field from '../components/form/Field.svelte';
  import FileUpload from '../components/form/FileUpload.svelte';
  import Select from '../components/form/Select.svelte';
  import Switch from '../components/form/Switch.svelte';
  import Helper from '../components/form/Helper.svelte';

  let formData = writable({});
  let editForm = null;

  const units = {
    temperature: [
      { value: 'celsius', text: 'Celsius' },
      { value: 'fahrenheit', text: 'Fahrenheit' },
      { value: 'kelvin', text: 'Kelvin' },
    ],
    distance: [
      { value: 'cm', text: 'Centimetre' },
      { value: 'inch', text: 'Inch' },
    ],
    liquid_volume: [
      { value: 'l', text: 'Litre' },
      { value: 'ukgall', text: 'UK Gallons' },
      { value: 'usgall', text: 'US Gallons' },
    ],
    wind_speed: [
      { value: 'm/s', text: 'Metre per second' },
      { value: 'km/h', text: 'Kilometre per hour' },
      { value: 'beaufort', text: 'Beaufort' },
    ],
  };

  const { form, setFields, isSubmitting, reset } = createForm({
    onSubmit: async (values, context) => {
      // Extra check on the password
      if (values.password !== '' && values.password2 !== '' && values.password !== values.password2) {
        context.form.elements['password2'].setCustomValidity('dummy');
      } else {
        // Reset error
        context.form.elements['password2'].setCustomValidity('');
      }

      validated = true;
      if (context.form.checkValidity()) {
        loading = true;
        values = formToJSON(context.form);

        if (values.file_profile_image) {
          // Upload first image to make sure it is valid
          try {
            values.profile_image = await uploadFile(context.form.file_profile_image);
            values.delete_image = false;
          } catch (error) {
            errorNotification(error.message, $_('notification.form.upload.error.title', { default: 'Upload error' }));

            loading = false;
            validated = false;

            // Return to current form
            return;
          }
        }

        delete values.file_profile_image;
        // TODO: Fix this. We need to convert to string, so that backend settings will work.... not handy or nice
        Object.keys(values).forEach((key) => {
          if (key === 'exclude_ids') {
            values[key] = values[key].join(',');
          } else {
            values[key] = values[key] + '';
          }
        });

        try {
          await updateSystemSettings(values);
          successNotification(
            $_('system.settings.save.ok.message', { default: 'Settings are updated.' }),
            $_('notification.form.save.ok.title', { default: 'Update OK' })
          );

          changeLang(values.language);
          currency.set(values.currency);
          setConfig(formToJSON(context.form));
        } catch (error) {
          errorNotification(error.message, $_('notification.form.save.error.title', { default: 'Save Error' }));
        }
        loading = false;
        validated = false;
      } else {
        let error_message = $_('webcams.settings.save.error.required_fields', { default: 'Not all required fields are entered correctly.' });
        error_message += "\n'" + invalid_form_fields(editForm).join("'\n'") + "'";
        errorNotification(error_message, $_('notification.form.save.error.title', { default: 'Save Error' }));
      }
    },
  });

  //let languages    = []
  let loading = true;
  let validated = false;
  let excluded_ids = [];

  onMount(() => {
    (async () => {
      await fetchSystemSettings(null, (settings) => {
        for (let field of settings) {
          $formData[field.id] = field.value;

          // TODO: Fix json data to real true and false values
          $formData[field.id] = $formData[field.id] === 'true' ? true : $formData[field.id] === 'false' ? false : $formData[field.id];

          if (field.id === 'exclude_ids') {
            excluded_ids = $formData[field.id].map((item) => {
              return { value: item.id, text: item.name };
            });
            $formData[field.id] = $formData[field.id].map((item) => {
              return item.id;
            });
          } else if (field.id === 'language') {
            $formData[field.id] = $formData[field.id].replace(/_/gm,'-');
          } else if (field.id === 'always_authenticate' && ($formData[field.id] === true || $formData[field.id] === false)) {
            $formData[field.id] = $formData[field.id] ? 1 : 0
          }
        }
        setFields($formData);
        loading = false;
      });
    })();

    // Reset form validation
    reset();
    $formData = formToJSON(editForm);
    validated = false;

    // Toggle loading div
    loading = true;

    setCustomPageTitle($_('system.settings.page.title', { default: 'System settings' }));
    editForm.setAttribute('novalidate', 'novalidate');
  });

  onDestroy(() => {
    customPageTitleUsed.set(false);
  });
</script>

<PageHeader>
  {$_('system.settings.page.title', { default: 'System settings' })}
  <svelte:fragment slot="breadcrumbs">
    <BreadcrumbItem>
      <Helper button="{false}" showMessage="{true}" />
    </BreadcrumbItem>
  </svelte:fragment>
</PageHeader>
<div class="container-fluid">
  <form class="form-horizontal needs-validation" class:was-validated="{validated}" use:form bind:this="{editForm}">
    <div class="row">
      <div class="col">
        <Card loading="{loading}">
          <svelte:fragment slot="header">
            <i class="fas fa-cog mr-2"></i>{$_('system.settings.header.system', { default: 'System' })}
          </svelte:fragment>

          <svelte:fragment slot="tools">
            <CardSettingsTools />
          </svelte:fragment>

          <Field
            type="number"
            name="pi_wattage"
            required="{true}"
            min="0.00"
            step="0.01"
            horizontal="{true}"
            label="{$_('system.settings.pi-wattage.label', { default: 'Pi power usage' })}"
            help="{$_('system.settings.pi-wattage.help', {
              default: 'Enter the total power usage of the Pi with all its USB devices connected.',
            })}"
            invalid="{$_('system.settings.pi-wattage.invalid', {
              values: { value: 0 },
              default: 'Please enter a minimum value of {value}',
            })}" />

          <Field
            type="text"
            name="host"
            required="{true}"
            horizontal="{true}"
            label="{$_('system.settings.host.label', { default: 'IP number' })}"
            help="{$_('system.settings.host.help', { default: 'Enter the IP to listen for connections. Default 0.0.0.0' })}"
            invalid="{$_('system.settings.host.invalid', { default: 'Please enter a valid IP address' })}" />

          <Field
            type="number"
            name="port"
            required="{true}"
            min="1024"
            step="1"
            horizontal="{true}"
            label="{$_('system.settings.port.label', { default: 'Port number' })}"
            help="{$_('system.settings.port.help', { default: 'Enter the port number to listen for connections. Default 8090' })}"
            invalid="{$_('system.settings.port.invalid', {
              values: { value: 1024 },
              default: 'Please enter a minimum value of {value}',
            })}" />

          <Select
            name="always_authenticate"
            value="{$formData.always_authenticate}"
            required="{true}"
            horizontal="{true}"
            options="{[
              { value: 1, text: $_('system.settings.authenticate.options.full', { default: 'Full authentication' }) },
              { value: 0, text: $_('system.settings.authenticate.options.changes', { default: 'Only for changes' }) },
              { value: -1, text: $_('system.settings.authenticate.options.no_authentication', { default: 'No authentication' }) },
            ]}"
            label="{$_('system.settings.authenticate.label', { default: 'Authentication mode' })}"
            help="{$_('system.settings.authenticate.help', { default: 'Always authenticate or only when changes are being made.' })}"
            invalid="{$_('system.settings.authenticate.invalid', { default: 'Please make a choice' })}" />

          <Field
            type="text"
            name="username"
            required="{true}"
            horizontal="{true}"
            label="{$_('system.settings.username.label', { default: 'Username' })}"
            help="{$_('system.settings.username.help', { default: 'Enter the username for authentication.' })}"
            invalid="{$_('system.settings.username.invalid', { default: 'The username cannot be empty.' })}" />

          <Field
            type="password"
            name="password"
            horizontal="{true}"
            label="{$_('system.settings.password.label', { default: 'New password' })}"
            help="{$_('system.settings.password.help', { default: 'Enter a password for authentication.' })}"
            invalid="{$_('system.settings.password.invalid', { default: 'The password cannot be empty.' })}" />

          <Field
            type="password"
            name="password2"
            horizontal="{true}"
            label="{$_('system.settings.password2.label', { default: 'Confirm new password' })}"
            help="{$_('system.settings.password2.help', { default: 'Enter the new password again.' })}"
            invalid="{$_('system.settings.password2.invalid', { default: 'The new password do not match.' })}" />

          <Select
            name="exclude_ids"
            multiple="{true}"
            options="{excluded_ids}"
            value="{$formData.exclude_ids}"
            horizontal="{true}"
            label="{$_('system.settings.exclude-ids.label', { default: 'Excluded ids' })}"
            help="{$_('system.settings.exclude-ids.help', { default: 'IDs that are excluded.' })}" />
        </Card>
      </div>
      <div class="col">
        <Card loading="{loading}">
          <svelte:fragment slot="header">
            <i class="fas fa-language mr-2"></i>{$_('system.settings.header.locale', { default: 'Locale' })}
          </svelte:fragment>

          <svelte:fragment slot="tools">
            <CardSettingsTools />
          </svelte:fragment>

          <Select
            name="language"
            value="{$formData.language}"
            required="{true}"
            options="{languages.map((item) => {
              return { value: item.code, text: languageFlag(item.code) + ' ' + item.title };
            })}"
            horizontal="{true}"
            label="{$_('system.settings.language.label', { default: 'Language' })}"
            help="{$_('system.settings.language.help', { default: 'Select the interface language.' })}"
            invalid="{$_('system.settings.language.invalid', { default: 'Please make a choice.' })}" />
          <Select
            name="currency"
            value="{$formData.currency}"
            required="{true}"
            options="{currencies.map((item) => {
              return { value: item, text: $number(1000, { style: 'currency', currency: item }) };
            })}"
            horizontal="{true}"
            label="{$_('system.settings.currency.label', { default: 'Currency' })}"
            help="{$_('system.settings.currency.help', { default: 'Select the interface currency.' })}"
            invalid="{$_('system.settings.currency.invalid', { default: 'Please make a choice.' })}" />
          <Select
            name="temperature_indicator"
            value="{$formData.temperature_indicator}"
            required="{true}"
            options="{units.temperature}"
            horizontal="{true}"
            label="{$_('system.settings.temperature_indicator.label', { default: 'Temperature type' })}"
            help="{$_('system.settings.temperature_indicator.help', {
              default: 'Select the temperature indicator. Only affects the current values.',
            })}"
            invalid="{$_('system.settings.temperature_indicator.invalid', { default: 'Please make a choice.' })}" />
          <Select
            name="distance_indicator"
            value="{$formData.distance_indicator}"
            required="{true}"
            options="{units.distance}"
            horizontal="{true}"
            label="{$_('system.settings.distance_indicator.label', { default: 'Distance type' })}"
            help="{$_('system.settings.distance_indicator.help', {
              default: 'Select the distance indicator. Only affects the current values.',
            })}"
            invalid="{$_('system.settings.distance_indicator.invalid', { default: 'Please make a choice.' })}" />
          <Select
            name="water_volume_indicator"
            value="{$formData.water_volume_indicator}"
            required="{true}"
            options="{units.liquid_volume}"
            horizontal="{true}"
            label="{$_('system.settings.water_volume_indicator.label', { default: 'Liquid volume type' })}"
            help="{$_('system.settings.water_volume_indicator.help', {
              default: 'Select the liquid volume indicator. Only affects the current values.',
            })}"
            invalid="{$_('system.settings.water_volume_indicator.invalid', { default: 'Please make a choice.' })}" />
          <Select
            name="wind_speed_indicator"
            value="{$formData.wind_speed_indicator}"
            required="{true}"
            options="{units.wind_speed}"
            horizontal="{true}"
            label="{$_('system.settings.wind_speed_indicator.label', { default: 'Wind speed type' })}"
            help="{$_('system.settings.wind_speed_indicator.help', {
              default: 'Select the wind speed indicator. Only affects the current values.',
            })}"
            invalid="{$_('system.settings.wind_speed_indicator.invalid', { default: 'Please make a choice.' })}" />
          <Field
            type="number"
            name="power_price"
            required="{true}"
            min="0.0000"
            step="0.0001"
            horizontal="{true}"
            label="{$_('system.settings.power_price.label', { default: 'Power price' })}"
            help="{$_('system.settings.power_price.help', { default: 'Enter the price in euro/dollar/pound per kWh.' })}"
            invalid="{$_('system.settings.power_price.invalid', {
              values: { value: 0 },
              default: 'Please enter a minimum value of {value}.',
            })}" />
          <Field
            type="number"
            name="water_price"
            required="{true}"
            min="0.0000"
            step="0.0001"
            horizontal="{true}"
            label="{$_('system.settings.water_price.label', { default: 'Water price' })}"
            help="{$_('system.settings.water_price.help', { default: 'Enter the price in euro/dollar/pound per L/Gallon.' })}"
            invalid="{$_('system.settings.water_price.invalid', {
              values: { value: 0 },
              default: 'Please enter a minimum value of {value}.',
            })}" />
        </Card>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <Card loading="{loading}">
          <svelte:fragment slot="header">
            <i class="fas fa-marker mr-2"></i>{$_('system.settings.header.gui', { default: 'GUI' })}
          </svelte:fragment>

          <svelte:fragment slot="tools">
            <CardSettingsTools />
          </svelte:fragment>

          <Field
            type="text"
            name="title"
            required="{true}"
            horizontal="{true}"
            label="{$_('system.settings.title.label', { default: 'Title' })}"
            help="{$_('system.settings.title.help', { default: 'Enter a custom title.' })}"
            invalid="{$_('system.settings.title.invalid', { default: 'The title cannot be empty.' })}" />

          <FileUpload
            name="profile_image"
            value="{$formData.profile_image}"
            horizontal="{true}"
            accept="image/*"
            label="{$_('system.settings.profile_image.label', { default: 'Profile image' })}"
            help="{$_('system.settings.profile_image.help', { default: 'Update a custom image used in the menu.' })}"
            invalid="{$_('system.settings.profile_image.invalid', { default: 'Invalid profile image format.' })}" />

          <Field
            type="number"
            name="graph_smooth_value"
            required="{true}"
            min="0"
            step="1"
            horizontal="{true}"
            label="{$_('system.settings.graph_smooth_value.label', { default: 'Graph smoothing' })}"
            help="{$_('system.settings.graph_smooth_value.help', {
              default: 'Enter the amount of data points to average. 0 will disable this feature.',
            })}"
            invalid="{$_('system.settings.graph_smooth_value.invalid', {
              values: { value: 0 },
              default: 'Please enter a minimum value of {value}.',
            })}" />

          <Select
            name="dashboard_mode"
            value="{$formData.dashboard_mode}"
            required="{false}"
            options="{[
              { value: 0, text: $_('system.settings.dashboard_mode.options.normal', { default: 'Graphs and enclosures' }) },
              { value: 1, text: $_('system.settings.dashboard_mode.options.only_graphs', { default: 'Only graphs' }) },
              { value: 2, text: $_('system.settings.dashboard_mode.options.only_enclosures', { default: 'Only enclosures' }) },
            ]}"
            horizontal="{true}"
            label="{$_('system.settings.dashboard_mode.label', { default: 'Dashboard mode' })}"
            help="{$_('system.settings.dashboard_mode.help', { default: 'Select how the dashboard looks like.' })}"
            invalid="{$_('system.settings.dashboard_mode.invalid', { default: 'Please make a choice.' })}" />

          <Switch
            name="auto_dark_mode"
            value="{$formData.auto_dark_mode}"
            horizontal="{true}"
            label="{$_('system.settings.auto_dark_mode.label', { default: 'Auto dark mode' })}"
            help="{$_('system.settings.auto_dark_mode.help', { default: 'Toggle dark mode when the night starts.' })}" />

          <Switch
            name="show_min_max_gauge"
            value="{$formData.show_min_max_gauge}"
            horizontal="{true}"
            label="{$_('system.settings.show_min_max_gauge.label', { default: 'Show min and max values in gauge graphs' })}"
            help="{$_('system.settings.show_min_max_gauge.help', { default: 'Show the minimum and maximum value on the gauges.' })}" />

          <Switch
            name="all_gauges_on_single_page"
            value="{$formData.all_gauges_on_single_page}"
            horizontal="{true}"
            label="{$_('system.settings.all_gauges_on_single_page.label', { default: 'All gauges on a single page' })}"
            help="{$_('system.settings.all_gauges_on_single_page.help', {
              default: 'Add extra menu item for all sensors on a single page.',
            })}" />
        </Card>
      </div>
      <div class="col">
        <Card loading="{loading}">
          <svelte:fragment slot="header">
            <i class="fas fa-cloud-download-alt mr-2"></i>{$_('system.settings.header.cloud', { default: 'Cloud' })}
          </svelte:fragment>

          <svelte:fragment slot="tools">
            <CardSettingsTools />
          </svelte:fragment>

          <Field
            type="text"
            name="meross_cloud_username"
            horizontal="{true}"
            label="{$_('system.settings.meross_cloud_username.label', { default: 'Meross username' })}"
            help="{$_('system.settings.meross_cloud_username.help', { default: 'Enter the username to login into Meross cloud.' })}" />

          <Field
            type="password"
            name="meross_cloud_password"
            horizontal="{true}"
            label="{$_('system.settings.meross_cloud_password.label', { default: 'Meross password' })}"
            help="{$_('system.settings.meross_cloud_password.help', { default: 'Enter the password to login into Meross cloud.' })}" />
        </Card>
      </div>
    </div>
    <div class="row pb-2">
      <div class="col">
        <div class="d-flex justify-content-center">
          <button type="submit" class="btn btn-primary" disabled="{loading || $isSubmitting}">
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" class:d-none="{!$isSubmitting}"></span>
            {$_('modal.general.save', { default: 'Save' })}
          </button>
        </div>
      </div>
    </div>
  </form>
</div>
