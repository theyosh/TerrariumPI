<script>
  import { onMount } from 'svelte';

  import { buttons } from '../../stores/terrariumpi';

  export let button;

  // Set the initial relay value
  $buttons[button.id] = {
    value: button.value,
    error: button.error,
    last_update: new Date(),
    changed: true,
  };

  onMount(() => {
    $buttons[button.id].last_update = new Date();
  });
</script>

<h1 class="pt-3 button">
  <i
    class="fas text-secondary"
    class:fa-lock="{button.hardware === 'magnetic' && $buttons[button.id].value}"
    class:fa-lock-open="{button.hardware === 'magnetic' && !$buttons[button.id].value}"
    class:fa-lightbulb="{button.hardware === 'ldr'}"
    class:fa-walking="{button.hardware === 'motion'}"
    class:fa-wifi="{button.hardware === 'remote'}"
    class:text-success="{$buttons[button.id].value}"
    id="{button.id}"
    class:text-danger="{button.hardware === 'magnetic' && !$buttons[button.id].value}"></i>
</h1>

<style>
  h1.button {
    font-size: 8rem;
  }
</style>
