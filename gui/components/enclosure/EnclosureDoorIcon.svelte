<script>
  import { doors } from '../../stores/terrariumpi';
  export let enclosure_id;
</script>

{#if !enclosure_id || !$doors.enclosures[enclosure_id] || ($doors.enclosures[enclosure_id] && $doors.enclosures[enclosure_id].closed)}
  <i class="fas fa-lock"></i>
{:else}
  <i class="fas fa-lock-open text-danger"></i>
{/if}
