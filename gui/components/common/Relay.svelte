<script>
  import { onMount, getContext } from 'svelte';

  import { isAuthenticated } from '../../stores/authentication';
  import { relays } from '../../stores/terrariumpi';
  import { get_template_color } from '../../helpers/color-helpers';
  import { roundToPrecision } from '../../helpers/number-helpers';

  export let relay;

  const { toggleAction } = getContext('relayActions');

  let loaded = false;
  let dimmer;
  onMount(() => {
    if (relay.dimmer) {
      dimmer = jQuery(`input#${relay.id}`);
      dimmer.knob({
        format: function (value) {
          return roundToPrecision(value) + '%';
        },
        fgColor: get_template_color('text-success', false, true),
        bgColor: get_template_color('text-secondary', false, true),
        release: function (event) {
          if ($isAuthenticated) {
            // Bug in knob. When trigger a change, the release is fired.
            // So we check if the data value 'update' is 1 if the change should be fired to the backend
            if (1 == dimmer.data('update')) {
              let old_value = this.val();
              let value = Math.round(event);
              if (old_value != value) {
                toggleAction(relay, value);
              }
            }
          }
        },
      });
      dimmer
        .data('update', 1)
        .prop('readonly', true)
        .siblings('canvas')
        .addClass('btn btn-default m-2 p-2' + (!$isAuthenticated ? ' disabled' : ''));
    }
    loaded = true;
  });

  $: {
    if (loaded && $relays[relay.id].changed) {
      if (relay.dimmer) {
        if (parseInt(dimmer.val()) != $relays[relay.id].value) {
          dimmer.data('update', 0);
          dimmer.val($relays[relay.id].value);

          setTimeout(() => {
            dimmer.trigger('change');
            dimmer.data('update', 1);
          }, 0.1 * 1000);
        }
      }
      $relays[relay.id].changed = false;
    }
  }

  $: jQuery(`div.${relay.id} canvas`).toggleClass('disabled', !$isAuthenticated);
</script>

{#if relay.dimmer}
  <div class="dimmer">
    <input
      type="text"
      id="{relay.id}"
      class="dial"
      class:disabled="{!$isAuthenticated}"
      value="{relay.value}"
      disabled="{!$isAuthenticated}"
      data-width="165"
      data-height="165"
      data-min="0"
      data-max="100"
      data-angleArc="290"
      data-angleOffset="35" />
    <span
      style="position: absolute; top: 0px; left: 0px; height: 100%; width:100%; z-index:99"
      class:disabled="{!$isAuthenticated}"
      class:d-none="{$isAuthenticated}"></span>
  </div>
{:else}
  <button
    type="button"
    id="{relay.id}"
    class="btn btn-default mt-2 mb-2 text-secondary"
    disabled="{!$isAuthenticated}"
    on:click="{() => {
      toggleAction(relay);
    }}">
    <i class="fas fa-power-off" class:text-success="{$relays[relay.id].value > 0}" style="font-size: 9rem;"></i>
  </button>
{/if}

<style>
  .dimmer {
    position: relative;
  }
  input.dial {
    z-index: 30;
    left: 0px;
    margin: 33% 30% !important;
  }

  input.dial.disabled {
    cursor: not-allowed;
  }
</style>
