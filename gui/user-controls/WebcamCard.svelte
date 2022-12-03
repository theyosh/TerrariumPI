<script>
  import { setContext, getContext } from 'svelte';
  import { _ } from 'svelte-i18n';

  import Card from '../user-controls/Card.svelte';
  import Webcam from '../components/common/Webcam.svelte';
  import CardSettingsTools from '../components/common/CardSettingsTools.svelte';

  export let webcam;

  const { editWebcam } = getContext('modals');
  const { deleteAction, ignoreAction } = getContext('webcamActions');

  let loading = true;
  function setLoading(state) {
    loading = state;
  }

  setContext('loading', {
    setLoading,
  });
</script>

{#if webcam}
  <Card loading="{loading}" noPadding="{false}" removeParent="{true}" class="{webcam.id} {$$props.class ? $$props.class : ''}">
    <svelte:fragment slot="header">
      <i class="fas fa-fw fa-video mr-2"></i>{webcam.name}
      <small class="ml-2 text-muted">{$_('gauge.last_update', { default: 'Last update' })}: <span></span></small>
    </svelte:fragment>

    <svelte:fragment slot="tools">
      <CardSettingsTools>
        <button
          class="dropdown-item"
          title="{$_('webcams.actions.ignore', { default: 'Ignore webcam' })}"
          on:click="{() => ignoreAction(webcam)}">
          <i class="fas fa-ban mr-2"></i>{$_('webcams.actions.ignore', { default: 'Ignore webcam' })}
        </button>

        <button
          class="dropdown-item"
          title="{$_('webcams.actions.settings', { default: 'Edit webcam' })}"
          on:click="{() => editWebcam(webcam)}">
          <i class="fas fa-wrench mr-2"></i>{$_('webcams.actions.settings', { default: 'Edit webcam' })}
        </button>

        <button
          class="dropdown-item text-danger"
          title="{$_('webcams.actions.delete', { default: 'Delete webcam' })}"
          on:click="{() => deleteAction(webcam)}">
          <i class="fas fa-trash-alt mr-2"></i>{$_('webcams.actions.delete', { default: 'Delete webcam' })}
        </button>
      </CardSettingsTools>
    </svelte:fragment>

    <div class="row" style="min-height: 380px">
      <div class="col-12">
        <Webcam webcam="{webcam}" />
      </div>
    </div>
  </Card>
{/if}
