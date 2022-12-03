<script>
  import { doors } from '../../stores/terrariumpi';
  export let door_id;
</script>

{#if !door_id || !$doors.doors[door_id] || ($doors.doors[door_id] && $doors.doors[door_id].closed)}
  <i class="fas fa-lock text-success"></i>
{:else}
  <i class="fas fa-lock-open text-danger"></i>
{/if}
