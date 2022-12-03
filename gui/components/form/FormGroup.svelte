<script>
  import Label from './Label.svelte';

  export let id;
  export let label = null;
  export let required = null;

  export let help = null;
  export let invalid = null;

  export let horizontal = false;
</script>

<div class="form-group row">
  {#if label}
    <Label id="{id}" label="{label}" required="{required}" />
  {/if}
  <div class="col {$$props.class || ''}" class:col-12="{!horizontal}">
    <slot />
    {#if help}
      <small class="text-muted d-none">{@html help}</small>
    {/if}
    {#if invalid}
      <div class="invalid-feedback">{@html invalid}</div>
    {/if}
  </div>
</div>
