<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import { writable } from 'svelte/store';
  import { _ } from 'svelte-i18n';
  import { createForm } from 'felte';

  import {
    fetchNotificationMessageTypes,
    fetchNotificationMessages,
    updateNotificationMessage,
    fetchNotificationServices,
  } from '../providers/api';
  import { template_sensor_type_icon } from '../helpers/icon-helpers';
  import { successNotification, errorNotification } from '../providers/notification-provider';
  import { formToJSON, invalid_form_fields } from '../helpers/form-helpers';

  import ModalForm from '../user-controls/ModalForm.svelte';
  import Field from '../components/form/Field.svelte';
  import Helper from '../components/form/Helper.svelte';
  import Select from '../components/form/Select.svelte';
  import Switch from '../components/form/Switch.svelte';
  import TextArea from '../components/form/TextArea.svelte';
  import FormGroup from '../components/form/FormGroup.svelte';

  let wrapper_show;
  let wrapper_hide;
  let loading = false;
  let validated = false;

  let message_types = [];
  let services = [];
  let placeholders = [];

  let formData = writable({});

  let editForm;

  let enabled_services = [];

  const updatePlaceholders = (message_type) => {
    let message = message_types.filter((item) => {
      return item.value === message_type;
    });

    if (message && message.length === 1) {
      placeholders = Object.keys(message[0].placeholder)
        .sort()
        .map((item) => {
          return { key: item, value: message[0].placeholder[item] };
        });
    } else {
      placeholders = [];
    }
  };

  const toggleService = (service_id) => {
    if (enabled_services.indexOf(service_id) === -1) {
      // Enable
      enabled_services.push(service_id);
    } else {
      // Disable
      enabled_services.splice(enabled_services.indexOf(service_id), 1);
    }
    enabled_services = enabled_services; // This is needed to make Svelte aware of new data and reactively update it
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
        await updateNotificationMessage(values, (data) => (values = data));

        // Notifify OK!
        successNotification(
          $_('messages.settings.save.ok.message', { default: "Message ''{name}'' is updated", values: { name: values.name } }),
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
      let error_message = $_('messages.settings.save.error.required_fields', { default: 'Not all required fields are entered correctly.' });
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

  export const show = (messageId, cb) => {
    // Anonymous (Async) functions always as first!!
    (async () => {
      // Load all avaliable hardware
      await fetchNotificationMessageTypes(
        (data) =>
          (message_types = data.map((item) => {
            return { value: item.type, text: item.name, placeholder: item.placeholders };
          }))
      );

      // Load all the services
      await fetchNotificationServices(null, (data) => (services = data));

      // If ID is given, load existing data
      if (messageId) {
        await fetchNotificationMessages(messageId, (data) => ($formData = data));
        setFields($formData);
        enabled_services = $formData.services.map((item) => {
          return item.id;
        });
      }

      // Loading done
      loading = false;
    })();

    // Reset form validation
    reset();
    enabled_services = [];
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

  $: updatePlaceholders($formData.type);
</script>

<ModalForm bind:show="{wrapper_show}" bind:hide="{wrapper_hide}" loading="{loading}">
  <svelte:fragment slot="header">
    <i class="fas fa-bell mr-2"></i>
    {$_('messages.settings.title', { default: 'Message settings' })}
    <Helper />
  </svelte:fragment>

  <form class="needs-validation" class:was-validated="{validated}" use:form bind:this="{editForm}">
    <input type="hidden" name="id" disabled="{$formData.id && $formData.id !== '' ? null : true}" />
    <input type="hidden" name="services" value="{enabled_services.join(',')}" />
    <div class="row">
      <div class="col">
        <Select
          name="type"
          value="{$formData.type}"
          readonly="{$formData.id && $formData.id !== ''}"
          required="{true}"
          options="{message_types}"
          on:change="{(value) => ($formData.type = value.detail)}"
          label="{$_('messages.settings.type.label', { default: 'Message type' })}"
          placeholder="{$_('messages.settings.type.placeholder', { default: 'Select type' })}"
          help="{$_('messages.settings.type.help', { default: 'Select the notification message type.' })}"
          invalid="{$_('messages.settings.type.invalid', { default: 'Please make a choice.' })}" />
      </div>
      <div class="col">
        <Field
          type="text"
          name="title"
          required="{true}"
          label="{$_('messages.settings.subject.label', { default: 'Subject' })}"
          placeholder="{$_('messages.settings.subject.placeholder', { default: 'Enter a subject' })}"
          help="{$_('messages.settings.subject.help', { default: 'Enter a short subject. You can use placeholder values here.' })}"
          invalid="{$_('messages.settings.subject.invalid', { default: 'The subject cannot be empty.' })}" />
      </div>
      <div class="col-2">
        <Field
          type="number"
          name="rate_limit"
          value="0"
          required="{true}"
          min="0"
          step="1"
          label="{$_('messages.settings.rate_limit.label', { default: 'Rate limit' })}"
          placeholder="{$_('messages.settings.rate_limit.placeholder', { default: 'Messages per minute' })}"
          help="{$_('messages.settings.rate_limit.help', {
            default: 'Maximum number of messages per minute for this message. Use 0 for unlimited.',
          })}"
          invalid="{$_('messages.settings.rate_limit.invalid', {
            default: 'The entered value is not valid. Enter a valid number higher than {min}.',
            values: { min: 0 },
          })}" />
      </div>
      <div class="col-1">
        <Switch
          name="enabled"
          value="{$formData.enabled || true}"
          label="{$_('messages.settings.enabled.label', { default: 'Enabled' })}"
          help="{$_('messages.settings.enabled.help', { default: 'Enable/disable this notification message.' })}" />
      </div>
    </div>
    <div class="row">
      <div class="col-7">
        <TextArea
          name="message"
          value="{$formData.message || null}"
          rows="10"
          label="{$_('messages.settings.message.label', { default: 'Message' })}"
          placeholder="{$_('messages.settings.message.placeholder', { default: 'Enter a message' })}"
          help="{$_('messages.settings.message.help', { default: 'Enter a message. You can use placeholder values here.' })}" />
        <FormGroup
          id="available_services"
          label="{$_('messages.settings.available_services.label', { default: 'Services' })}"
          help="{$_('messages.settings.available_services.help', { default: 'Select the service to use for this notification message.' })}">
          {#each services as service, counter}
            <button
              type="button"
              id="{service.id}"
              title="{service.name}"
              class="btn btn-app"
              class:ml-0="{counter === 0}"
              disabled="{!service.enabled}"
              on:click="{() => toggleService(service.id)}">
              <i class="{`${template_sensor_type_icon(service.type)}`}" class:text-warning="{enabled_services.indexOf(service.id) !== -1}"
              ></i>
            </button>
          {/each}
        </FormGroup>
      </div>
      <div class="col">
        <FormGroup
          id="placeholders"
          label="{$_('messages.settings.placeholders.label', { default: 'Place holders' })}"
          help="{$_('messages.settings.placeholders.help', { default: 'List of available placeholders.' })}">
          <small class="text-muted mb-2 d-block">
            {@html $_('messages.settings.placeholders.format', {
              default: 'Use {placeholder} format to use a placeholder below in your message.{new_line}Number values can be rounded using the {link_start}`.:2f` format{link_end}',
              values: {
                placeholder: '<strong>${placeholder_name}</strong>',
                new_line: '<br />',
                link_start: '<a href="https://docs.python.org/3.8/library/string.html#formatspec" target="_blank">',
                link_end: '</a>',
              },
            })}
          </small>
          {#each placeholders as placeholder}
            <div>
              <strong>{placeholder.key}</strong>: {placeholder.value}
            </div>
          {/each}
        </FormGroup>
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
