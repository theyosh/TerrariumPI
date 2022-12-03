<script>
  import { _ } from 'svelte-i18n';

  import { showLogin } from '../../stores/authentication';
</script>

<a href="/login/" class="{$$props.class}" title="{$_('general.login.title')}" on:click|preventDefault="{() => showLogin()}">
  <slot>
    <i class="fas fa-key mr-2"></i>{$_('general.login.title')}
  </slot>
</a>
