<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import { writable } from 'svelte/store';
  import { _, date } from 'svelte-i18n';
  import { createForm } from 'felte';

  import { fetchCalendarEvents, updateCalendarEvent } from '../providers/api';
  import { successNotification, errorNotification } from '../providers/notification-provider';
  import { formToJSON, invalid_form_fields } from '../helpers/form-helpers';

  import ModalForm from '../user-controls/ModalForm.svelte';
  import FormGroup from '../components/form/FormGroup.svelte';
  import Field from '../components/form/Field.svelte';
  import Helper from '../components/form/Helper.svelte';
  import Select from '../components/form/Select.svelte';
  import WysiwygArea from '../components/form/WysiwygArea.svelte';

  let wrapper_show;
  let wrapper_hide;
  let loading = false;
  let validated = false;

  let repeat = false;
  let formData = writable({});
  let mode = 'reminder';

  let editForm;

  const event_periods = [
    {
      text:
        mode === 'repeat'
          ? $_('calendar.event.periods.no_repeat', { default: 'No repeat' })
          : $_('calendar.event.periods.no_reminder', { default: 'No reminder' }),
      value: '_',
    },
    {
      text: $_('calendar.event.periods.days', { default: 'Days' }),
      value: 'daily',
    },
    {
      text: $_('calendar.event.periods.weeks', { default: 'Weeks' }),
      value: 'weekly',
    },
    {
      text: $_('calendar.event.periods.months', { default: 'Months' }),
      value: 'monthly',
    },
    {
      text: $_('calendar.event.periods.years', { default: 'Years' }),
      value: 'yearly',
    },
  ];

  const dispatch = createEventDispatcher();

  const successAction = () => {
    dispatch('save');
  };

  const uselessEnterEnd = /<br[^>]*><\/p>$/gm;
  const _processForm = async (values, context) => {
    validated = true;

    if (context.form.checkValidity()) {
      loading = true;
      values = formToJSON(editForm);

      delete values.value;

      if (!repeat) {
        delete values.interval;
      }

      values.description = values.description.replace(uselessEnterEnd, `<\/p>`);
      values.dtstart /= 1000;
      values.dtend /= 1000;

      try {
        // Post data
        await updateCalendarEvent(values, (data) => (values = data));
        // Notifify OK!
        successNotification(
          $_('calendar.event.settings.save.ok.message', { default: "Event ''{name}'' is updated", values: { name: values.summary } }),
          $_('notification.form.save.ok.title', { default: 'Save OK' })
        );

        // Done, close window
        hide();

        // Signal the save callback. This will relead the calendar
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
      let error_message = $_('calendar.event.settings.save.error.required_fields', {
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

  export const show = (eventData, cb) => {
    // Anonymous (Async) functions always as first!!
    (async () => {
      // If ID is given, load existing data
      if (eventData.id) {
        loading = true;
        await fetchCalendarEvents(eventData.id, (data) => {
          // Use miliseconds
          data.dtstart *= 1000;
          data.dtend *= 1000;
          data.freq = data.freq ? data.freq : '_';
          $formData = data;
        });
        setFields($formData);
        repeat = $formData.freq !== '_';
        // Loading done
        loading = false;
      }
    })();

    if (eventData.mode) {
        mode = eventData.mode;
    } else {
        mode = 'reminder';
    }

    repeat = false;

    // Reset form validation
    reset();
    validated = false;
    let now = Date.now();
    $formData = {
      dtstart: eventData.start ? Date.parse(eventData.start) : now,
      dtend:   eventData.end   ? Date.parse(eventData.end)   : now + 86400000,
      description: '',
      freq: '_',
      repeatend: 2,
      ...eventData
    };
    setFields($formData);

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
    <i class="fas fa-calendar-alt mr-2"></i>
    {$_('calendar.event.settings.title', { default: 'Event' })}
    <Helper />
  </svelte:fragment>

  <form class="needs-validation" class:was-validated="{validated}" use:form bind:this="{editForm}">
    <input type="hidden" name="id" disabled="{$formData.id && $formData.id !== '' ? null : true}" />
    <input type="hidden" name="mode" value="{mode}"/>
    <input type="hidden" name="repeatend" value="2" disabled={'reminder' !== mode}/>

    <div class="row">
      <div class="col-12 col-sm-12 col-md-9 col-lg-9">
        <Field
          type="text"
          name="summary"
          required="{true}"
          label="{$_('calendar.event.settings.summary.label', { default: 'Enter a name' })}"
          help="{$_('calendar.event.settings.summary.help', { default: 'Enter a name.' })}"
          invalid="{$_('calendar.event.settings.summary.invalid', { default: 'The name cannot be empty.' })}" />
        <WysiwygArea
          name="description"
          value="{$formData.description}"
          required="{false}"
          label="{$_('calendar.event.settings.description.label', { default: 'Enter a description' })}"
          help="{$_('calendar.event.settings.description.help', { default: 'Enter some information about this event.' })}" />
      </div>
      <div class="col-12 col-sm-12 col-md-3 col-lg-3">
        <FormGroup
          id="dtstart"
          required="{true}"
          horizontal="{false}"
          label="{$_('calendar.event.settings.date.label', { default: 'Date' })}"
          help="{$_('calendar.event.settings.date.help', { default: 'The date or period for this event.' })}">
          <input type="hidden" id="dtstart" name="dtstart" />
          <input type="hidden" id="dtend" name="dtend" />
          <p class="p-1 pt-2 mb-0">
            {$date($formData.dtstart, { format: 'medium' })}
            {#if $formData.dtend - $formData.dtstart > 24 * 3600000}
              - {$date($formData.dtend - 24 * 3600000, { format: 'medium' })}
            {/if}
          </p>
        </FormGroup>

        <Select
          name="freq"
          value="{$formData.freq}"
          options="{event_periods}"
          on:change="{(value) => {
            repeat = value.detail !== '_';
          }}"
          label="{mode === 'repeat'
            ? $_('calendar.event.settings.repeat.label', { default: 'Repeat every' })
            : $_('calendar.event.settings.remind.label', { default: 'Remind in' })}"
          help="{$_('calendar.event.settings.repeat.help', { default: 'Select a repeat period and an amount.' })}"
          invalid="{$_('calendar.event.settings.repeat.invalid', { default: 'Please enter a valid repeat period amount.' })}">
          <input
            type="number"
            class="form-control mt-2"
            name="interval"
            required="{repeat}"
            disabled="{!repeat}"
            placeholder="{$_('calendar.event.settings.repeat_amount.label', { default: 'Select amount' })}" />
        </Select>
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
