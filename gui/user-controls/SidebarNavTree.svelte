<script>
  export let href = '#';
  export let icon;
</script>

<li class="nav-item">
  <a href="{href}" class="nav-link">
    {#if icon}
      <i class="nav-icon {icon}"></i>
    {/if}
    <p>
      <slot />
      <i class="right fas fa-angle-left icon"></i>
    </p>
  </a>
  <ul class="nav nav-treeview margin">
    <slot name="children" />
  </ul>
</li>
<!--
<style lang="sass">
	.sidebar-collapsed .icon
		display: none
</style>
 -->
