<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import { writable } from 'svelte/store';
  import { _ } from 'svelte-i18n';
  import { createForm } from 'felte';

  import { fetchNotificationServiceTypes, fetchNotificationServices, updateNotificationService, fetchDisplayTypes } from '../providers/api';
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

  let service_types = [];
  let display_types = [];

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
      values = formToJSON(editForm);

      // Delete generated attributes from object
      delete values.duration;
      delete values.length;

      try {
        // Post data
        await updateNotificationService(values, (data) => (values = data));

        // Notifify OK!
        successNotification(
          $_('services.settings.save.ok.message', { default: "Service ''{name}'' is updated", values: { name: values.name } }),
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
      let error_message = $_('services.settings.save.error.required_fields', { default: 'Not all required fields are entered correctly.' });
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

  export const show = (serviceId, cb) => {
    // Anonymous (Async) functions always as first!!
    (async () => {
      // Load all avaliable hardware
      await fetchNotificationServiceTypes(
        (data) =>
          (service_types = data.map((item) => {
            return { value: item.type, text: item.name };
          }))
      );

      // Load display hardware
      await fetchDisplayTypes(
        (data) =>
          (display_types = data.map((item) => {
            return { value: item.hardware, text: item.name };
          }))
      );

      // If ID is given, load existing data
      if (serviceId) {
        await fetchNotificationServices(serviceId, (data) => ($formData = data));
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
    <i class="fas fa-bell mr-2"></i>
    {$_('services.settings.title', { default: 'Notification service settings' })}
    <Helper />
  </svelte:fragment>

  <form class="needs-validation" class:was-validated="{validated}" use:form bind:this="{editForm}">
    <input type="hidden" name="id" disabled="{$formData.id && $formData.id !== '' ? null : true}" />
    <div class="row">
      <div class="col">
        <Select
          name="type"
          value="{$formData.type}"
          readonly="{$formData.id && $formData.id !== ''}"
          required="{true}"
          options="{service_types}"
          on:change="{(value) => ($formData.type = value.detail)}"
          label="{$_('services.settings.type.label', { default: 'Type' })}"
          placeholder="{$_('services.settings.type.placeholder', { default: 'Select type' })}"
          help="{$_('services.settings.type.help', { default: 'Select the notification service type.' })}"
          invalid="{$_('services.settings.type.invalid', { default: 'Please make a choice.' })}" />
      </div>
      <div class="col">
        <Field
          type="text"
          name="name"
          required="{true}"
          label="{$_('services.settings.name.label', { default: 'Name' })}"
          placeholder="{$_('services.settings.name.placeholder', { default: 'Enter a name' })}"
          help="{$_('services.settings.name.help', { default: 'Enter an easy to remember name.' })}"
          invalid="{$_('services.settings.name.invalid', { default: 'The entered name is not valid. It cannot be empty.' })}" />
      </div>
      <div class="col">
        <Field
          type="number"
          name="rate_limit"
          value="0"
          required="{true}"
          min="0"
          step="1"
          label="{$_('services.settings.rate_limit.label', { default: 'Rate limit' })}"
          placeholder="{$_('services.settings.rate_limit.placeholder', { default: 'Messages per minute' })}"
          help="{$_('services.settings.rate_limit.help', {
            default: 'Maximum number of messages per minute for this service. Use 0 for unlimited.',
          })}"
          invalid="{$_('services.settings.rate_limit.invalid', {
            default: 'The entered value is not valid. Enter a valid number higher than {min}.',
            values: { min: 0 },
          })}" />
      </div>
      <div class="col">
        <Switch
          name="enabled"
          value="{$formData.enabled || true}"
          label="{$_('services.settings.enabled.label', { default: 'Enabled' })}"
          help="{$_('services.settings.enabled.help', { default: 'Enable/disable this notification service.' })}" />
      </div>
    </div>

    {#if $formData.type === 'display'}
      <div class="row">
        <div class="col">
          <Select
            name="setup.hardware"
            value="{$formData.setup?.hardware}"
            required="{true}"
            options="{display_types}"
            label="{$_('services.settings.setup.hardware.label', { default: 'Hardware' })}"
            placeholder="{$_('services.settings.setup.hardware.placeholder', { default: 'Select hardware' })}"
            help="{$_('services.settings.setup.hardware.help', { default: 'Select the hardware type for this display.' })}"
            invalid="{$_('services.settings.setup.hardware.invalid', { default: 'Please make a choice.' })}" />
        </div>
        <div class="col">
          <Field
            type="text"
            name="setup.address"
            required="{true}"
            label="{$_('services.settings.setup.address.label', { default: 'Address' })}"
            placeholder="{$_('services.settings.setup.address.placeholder', { default: 'Enter an address' })}"
            help="{$_('services.settings.setup.address.help', { default: 'Enter an address.' })}"
            invalid="{$_('services.settings.setup.address.invalid', {
              default: 'The entered address is not valid. It cannot be empty.',
            })}" />
        </div>
        <div class="col-3">
          <Switch
            name="setup.show_title"
            value="{$formData.setup?.show_title || true}"
            label="{$_('services.settings.setup.show_title.label', { default: 'Show title' })}"
            help="{$_('services.settings.setup.show_title.help', { default: 'Show a name and version as title on the display.' })}" />
        </div>
      </div>
    {/if}

    {#if $formData.type === 'email'}
      <div class="row">
        <div class="col">
          <Field
            type="text"
            name="setup.receiver"
            required="{true}"
            label="{$_('services.settings.setup.receiver.label', { default: 'Receiver email' })}"
            placeholder="{$_('services.settings.setup.receiver.placeholder', { default: 'Enter an email address' })}"
            help="{$_('services.settings.setup.receiver.help', { default: 'Enter an email address.' })}"
            invalid="{$_('services.settings.setup.receiver.invalid', { default: 'The address cannot be empty.' })}" />
        </div>
        <div class="col">
          <Field
            type="text"
            name="setup.address"
            required="{true}"
            label="{$_('services.settings.setup.address.email.label', { default: 'Server address' })}"
            placeholder="{$_('services.settings.setup.address.placeholder', { default: 'Enter an address' })}"
            help="{$_('services.settings.setup.address.help', { default: 'Enter an address.' })}"
            invalid="{$_('services.settings.setup.address.invalid', {
              default: 'The entered address is not valid. It cannot be empty.',
            })}" />
        </div>
        <div class="col-2">
          <Field
            type="number"
            name="setup.port"
            value="25"
            required="{true}"
            min="0"
            step="1"
            label="{$_('services.settings.setup.port.label', { default: 'SMTP Server port' })}"
            placeholder="{$_('services.settings.setup.port.placeholder', { default: 'Enter a port number' })}"
            help="{$_('services.settings.setup.port.help', { default: 'Enter the server port number.' })}"
            invalid="{$_('services.settings.setup.port.invalid', {
              default: 'The entered port number is not valid. It cannot be empty.',
            })}" />
        </div>
        <div class="col">
          <Field
            type="text"
            name="setup.username"
            label="{$_('services.settings.setup.username.label', { default: 'SMTP Server username' })}"
            placeholder="{$_('services.settings.setup.username.placeholder', { default: 'Enter a username' })}"
            help="{$_('services.settings.setup.username.help', { default: 'Enter the server username.' })}" />
        </div>
        <div class="col">
          <Field
            type="text"
            name="setup.password"
            label="{$_('services.settings.setup.password.label', { default: 'SMTP Server password' })}"
            placeholder="{$_('services.settings.setup.password.placeholder', { default: 'Enter a username' })}"
            help="{$_('services.settings.setup.password.help', { default: 'Enter the server password.' })}" />
        </div>
      </div>
      <div class="row">
        <div class="col">
            <small class="text-muted d-none ml-2 w-100 text-center">
                {$_('services.settings.setup.ssl.email.label', {
                  default: 'The email notification service will auto detect SSL/TLS connections.',
                })}
            </small>
        </div>
      </div>
    {/if}

    {#if $formData.type === 'pushover'}
      <div class="row">
        <div class="col">
          <Field
            type="text"
            name="setup.api_token"
            required="{true}"
            label="{$_('services.settings.setup.api_token.label', { default: 'API Token' })}"
            placeholder="{$_('services.settings.setup.api_token.placeholder', { default: 'Enter the API Token' })}"
            help="{$_('services.settings.setup.api_token.help', { default: 'Enter the Pushover API token.' })}"
            invalid="{$_('services.settings.setup.api_token.invalid', {
              default: 'The entered API token is not valid. It cannot be empty.',
            })}" />
        </div>
        <div class="col">
          <Field
            type="text"
            name="setup.user_key"
            required="{true}"
            label="{$_('services.settings.setup.user_key.label', { default: 'User key' })}"
            placeholder="{$_('services.settings.setup.user_key.placeholder', { default: 'Enter the user key' })}"
            help="{$_('services.settings.setup.user_key.help', { default: 'Enter the Pushover user key.' })}"
            invalid="{$_('services.settings.setup.user_key.invalid', {
              default: 'The entered user key is not valid. It cannot be empty.',
            })}" />
        </div>
      </div>
      <div class="row">
        <div class="col">
            <small class="text-muted d-none ml-2 w-100 text-center">
                {@html $_('services.settings.setup.pushover.label', {
                    default: 'Create your tokens by registering TerrariumPI as an app {link}.',
                    values: { link: '<a href="https://pushover.net/api" target="_blank" rel="noopener">https://pushover.net/api</a>' },
                  })}
            </small>
        </div>
      </div>
    {/if}

    {#if $formData.type === 'traffic'}
      <div class="row">
        <div class="col">
          <Field
            type="number"
            name="setup.red"
            min="1"
            max="40"
            step="1"
            label="{$_('services.settings.setup.red.label', { default: 'Red' })}"
            placeholder="{$_('services.settings.setup.red.placeholder', { default: 'Enter red GPIO pin' })}"
            help="{$_('services.settings.setup.red.help', { default: 'Enter GPIO pin for red light.' })}"
            invalid="{$_('services.settings.setup.red.invalid', {
              default: 'The entered value is not valid. Enter a valid number between {min} and {max}.',
              values: { min: 1, max: 40 },
            })}" />
        </div>
        <div class="col">
          <Field
            type="number"
            name="setup.yellow"
            min="1"
            max="40"
            step="1"
            label="{$_('services.settings.setup.yellow.label', { default: 'Amber' })}"
            placeholder="{$_('services.settings.setup.yellow.placeholder', { default: 'Enter amber GPIO pin' })}"
            help="{$_('services.settings.setup.yellow.help', { default: 'Enter GPIO pin for amber light.' })}"
            invalid="{$_('services.settings.setup.yellow.invalid', {
              default: 'The entered value is not valid. Enter a valid number between {min} and {max}.',
              values: { min: 1, max: 40 },
            })}" />
        </div>
        <div class="col">
          <Field
            type="number"
            name="setup.green"
            min="1"
            max="40"
            step="1"
            label="{$_('services.settings.setup.green.label', { default: 'Green' })}"
            placeholder="{$_('services.settings.setup.green.placeholder', { default: 'Enter green GPIO pin' })}"
            help="{$_('services.settings.setup.green.help', { default: 'Enter GPIO pin for green light.' })}"
            invalid="{$_('services.settings.setup.green.invalid', {
              default: 'The entered value is not valid. Enter a valid number between {min} and {max}.',
              values: { min: 1, max: 40 },
            })}" />
        </div>
      </div>
    {/if}

    {#if $formData.type === 'buzzer'}
      <div class="row">
        <div class="col">
          <Field
            type="number"
            name="setup.address"
            min="1"
            max="40"
            step="1"
            required="{true}"
            label="{$_('services.settings.setup.address.label', { default: 'Address' })}"
            placeholder="{$_('services.settings.setup.address.placeholder', { default: 'Enter an address' })}"
            help="{$_('services.settings.setup.address.help', { default: 'Enter an address.' })}"
            invalid="{$_('services.settings.setup.address.invalid', {
              default: 'The entered address is not valid. It cannot be empty.',
            })}" />
        </div>
        <div class="col">
          <p>
            The following songs are supported. Copy the name exactly as written in the list below in the <strong>message subject</strong>.
          </p>
          <ul>
            <li>The Final Countdown</li>
            <li>Old MacDonald Had A Farm</li>
            <li>Manaderna (Symphony No. 9)</li>
            <li>Deck The Halls</li>
            <li>Crazy Frog (Axel F) Theme</li>
            <li>Twinkle, Twinkle, Little Star</li>
            <li>Popcorn</li>
            <li>SOS</li>
            <li>Star Wars</li>
            <li>Super Mario</li>
          </ul>
          <p>
            Original found at:
            <a href="https://github.com/gumslone/raspi_buzzer_player" target="_blank" rel="noopener noreferrer"
              >https://github.com/gumslone/raspi_buzzer_player</a>
          </p>
          <small class="text-muted d-none">
            {$_('services.settings.setup.buzzer.help', { default: 'List of available songs to use in the message subject.' })}
          </small>
        </div>
      </div>
    {/if}

    {#if $formData.type === 'webhook'}
      <div class="row">
        <div class="col">
          <Field
            type="text"
            name="setup.url"
            required="{true}"
            label="{$_('services.settings.setup.url.label', { default: 'Full post url' })}"
            placeholder="{$_('services.settings.setup.url.placeholder', { default: 'Enter the full post url' })}"
            help="{$_('services.settings.setup.url.help', { default: 'Enter the full post url.' })}"
            invalid="{$_('services.settings.setup.url.invalid', { default: 'The entered url is not valid. It cannot be empty.' })}" />
        </div>
      </div>
    {/if}

    {#if $formData.type === 'mqtt'}
      <div class="row">
        <div class="col">
          <Field
            type="text"
            name="setup.address"
            required="{true}"
            label="{$_('services.settings.setup.address.mqtt.label', { default: 'Server Address' })}"
            placeholder="{$_('services.settings.setup.address.placeholder', { default: 'Enter an address' })}"
            help="{$_('services.settings.setup.address.help', { default: 'Enter an address.' })}"
            invalid="{$_('services.settings.setup.address.invalid', {
              default: 'The entered address is not valid. It cannot be empty.',
            })}" />
        </div>
        <div class="col-2">
          <Field
            type="number"
            name="setup.port"
            value="25"
            required="{true}"
            min="0"
            step="1"
            label="{$_('services.settings.setup.port.label', { default: 'Server port' })}"
            placeholder="{$_('services.settings.setup.port.placeholder', { default: 'Enter a port number' })}"
            help="{$_('services.settings.setup.port.help', { default: 'Enter the server port number.' })}"
            invalid="{$_('services.settings.setup.port.invalid', {
              default: 'The entered port number is not valid. It cannot be empty.',
            })}" />
        </div>
        <div class="col">
          <Field
            type="text"
            name="setup.username"
            label="{$_('services.settings.setup.username.label', { default: 'Server username' })}"
            placeholder="{$_('services.settings.setup.username.placeholder', { default: 'Enter a username' })}"
            help="{$_('services.settings.setup.username.help', { default: 'Enter the server username.' })}" />
        </div>
        <div class="col">
          <Field
            type="text"
            name="setup.password"
            label="{$_('services.settings.setup.password.label', { default: 'Server password' })}"
            placeholder="{$_('services.settings.setup.password.placeholder', { default: 'Enter a username' })}"
            help="{$_('services.settings.setup.password.help', { default: 'Enter the server password.' })}" />
        </div>
      </div>
      <div class="row">
        <div class="col">
            <small class="text-muted d-none ml-2 w-100 text-center">
                {$_('services.settings.setup.ssl.mqtt.label', { default: 'The MQTT notification service will auto detect SSL/TLS connections.' })}
            </small>
        </div>
      </div>
    {/if}

    <!--
    <div class="row telegram">
      <div class="col-12 col-sm-12 col-md-4 col-lg-4">
        <div class="form-group">
          <label for="bot_token">{{ _('Bot Token') }}</label>
          <input type="text" class="form-control" id="bot_token" name="bot_token" required="required" >
        </div>
      </div>
      <div class="col-12 col-sm-12 col-md-4 col-lg-4">
        <div class="form-group">
          <label for="username">{{ _('Username') }}</label>
          <input type="text" class="form-control" id="username" name="username" required="required" >
        </div>
      </div>
      <div class="col-12 col-sm-12 col-md-4 col-lg-4">
        <div class="form-group">
          <label for="proxy">{{ _('HTTP Proxy') }}</label>
          <input type="text" class="form-control" id="proxy" name="proxy" >
        </div>
      </div>
    </div>
    -->
    <!--
    <div class="row twitter">
      <div class="col-12 col-sm-12 col-md-3 col-lg-3">
        <div class="form-group">
          <label for="bot_token">{{ _('Customer key') }}</label>
          <input type="text" class="form-control" id="bot_token" name="bot_token" required="required" >
        </div>
      </div>
      <div class="col-12 col-sm-12 col-md-3 col-lg-3">
        <div class="form-group">
          <label for="username">{{ _('Customer secret') }}</label>
          <input type="text" class="form-control" id="username" name="username" required="required">
        </div>
      </div>
      <div class="col-12 col-sm-12 col-md-3 col-lg-3">
        <div class="form-group">
          <label for="access_token">{{ _('Access token') }}</label>
          <input type="text" class="form-control" id="access_token" name="access_token" required="required" >
        </div>
      </div>
      <div class="col-12 col-sm-12 col-md-3 col-lg-3">
        <div class="form-group">
          <label for="access_secret">{{ _('Access token secret') }}</label>
          <input type="text" class="form-control" id="access_secret" name="access_secret" required="required">
        </div>
      </div>
    </div>
    -->

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
