<script>
  import { Modal } from 'svelte-adminlte';
  import { onMount, getContext } from 'svelte';
  import { _ } from 'svelte-i18n';
  import { createForm } from 'felte';

  import { errorNotification } from '../providers/notification-provider';
  import { updateSensor } from '../stores/terrariumpi';
  import { fetchSensors } from '../providers/api';
  import { formToJSON } from '../helpers/form-helpers';

  import Helper from '../components/form/Helper.svelte';
  import Select from '../components/form/Select.svelte';

  let modal;
  let editForm;

  let validated = false;
  let sensors = [];
  let selected = [];

  let edit = false;

  const { setMarker, deleteMarker } = getContext('webcamMarker');

  const _processForm = async (values, context) => {
    validated = true;
    if (context.form.checkValidity()) {
      values = formToJSON(editForm);
      setMarker(values);
      hide();
    } else {
      errorNotification('Error saving markers', 'ERROR');
    }
  };

  const { form, isSubmitting, createSubmitHandler } = createForm({
    onSubmit: _processForm,
  });

  const formSubmit = createSubmitHandler({
    onSubmit: _processForm,
  });

  export const show = (marker) => {
    edit = marker ? true : false;
    selected = edit ? marker.target.options.sensors : [];
    editForm.elements['markerid'].value = edit ? marker.target._leaflet_id : '';

    fetchSensors(false, (data) => {
      sensors = data.map((item) => {
        updateSensor(item);
        return { value: item.id, text: item.name };
      });
    });

    validated = false;
    modal.show();
  };

  export const hide = () => {
    modal.hide();
  };

  onMount(() => {
    editForm.setAttribute('novalidate', 'novalidate');
  });
</script>

<Modal bind:this="{modal}">
  <svelte:fragment slot="header">
    <i class="fas fa-marker mr-2"></i>
    {$_('webcams.markers.settings.title', { default: 'Sensors' })}
    <Helper />
  </svelte:fragment>

  <form class="form-horizontal needs-validation" class:was-validated="{validated}" use:form bind:this="{editForm}">
    <input type="hidden" name="markerid" disabled="{!edit}" value="" />

    <Select
      name="sensors"
      value="{selected}"
      multiple="{true}"
      required="{true}"
      options="{sensors}"
      label="{$_('webcams.markers.settings.doors.label', { default: 'Sensors' })}"
      help="{$_('webcams.markers.settings.doors.help', { default: 'Select the senors you want to show.' })}"
      invalid="{$_('webcams.markers.settings.doors.invalid', { default: 'Make a choice.' })}" />

    <!-- We need this nasty hack to make submit with enter key to work -->
    <button type="submit" style="display:none"> </button>
  </form>

  <svelte:fragment slot="actions">
    <div class="d-flex justify-content-between w-100">
      <button type="button" class="btn btn-default" on:click="{hide}">
        {$_('modal.general.close', { default: 'Close ' })}
      </button>

      {#if edit}
        <button type="button" class="btn btn-danger mr-5" on:click="{() => deleteMarker(editForm.elements['markerid'].value)}">
          {$_('webcams.markers.settings.delete', { default: 'Delete' })}
        </button>
      {/if}

      <button type="button" class="btn btn-primary ml-3" disabled="{$isSubmitting}" on:click="{formSubmit}">
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" class:d-none="{!$isSubmitting}"></span>
        {$_('modal.general.save', { default: 'Save' })}
      </button>
    </div>
  </svelte:fragment>
</Modal>
