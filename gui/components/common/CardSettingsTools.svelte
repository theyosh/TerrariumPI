<script>
  import { isAuthenticated } from '../../stores/authentication';
  import LoginLink from './LoginLink.svelte';
</script>

<div class="btn-group" class:d-none="{$isAuthenticated && $$slots.default === undefined}">
  <button type="button" class="btn btn-tool dropdown-toggle" data-toggle="dropdown">
    <i class="fas fa-wrench"></i>
  </button>
  <div class="dropdown-menu dropdown-menu-right" role="menu">
    {#if $isAuthenticated}
      <slot />
    {:else}
      <LoginLink class="dropdown-item" />
    {/if}
  </div>
</div>
