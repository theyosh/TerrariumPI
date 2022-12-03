<script>
  import { _ } from 'svelte-i18n';
  import { getContext } from 'svelte';

  import { isAuthenticated, doLogout } from '../../stores/authentication';
  import { default as currentUserStore } from '../../stores/current-user';
  import { getCustomConfig } from '../../config';
  import { ApiUrl } from '../../constants/urls';
  import LoginLink from '../common/LoginLink.svelte';

  let settings = getCustomConfig();
  const { confirmModal } = getContext('confirm');
</script>

<a href="/" class="brand-link">
  <img src="img/AdminLTELogo.png" alt="AdminLTE Logo" class="brand-image img-circle elevation-3" style="opacity: .8" />
  <span class="brand-text font-weight-light">{settings.name}</span>
</a>
<div class="user-panel mt-3 pb-3 mb-3 d-flex">
  <div class="image pt-2 pl-1">
    <img src="img/christmas_hat.png" class="christmashat d-none" title="!! Merry Christmas !!" alt="!! Merry Christmas !!" />
    <img src="{ApiUrl}/{settings.profile}" class="img-circle elevation-2 img-thumbnail" alt="Profile" />
  </div>
  <div class="info">
    {#if $isAuthenticated}
      <a
        href="/logout/"
        title="{$_('general.logout.title')}"
        on:click|preventDefault="{() => confirmModal($_('modal.confirm.system.logout'), () => doLogout())}">
        {$_('userpanel.logout.text1', { values: { name: $currentUserStore } })}
        <br />
        {$_('userpanel.logout.text2')}
      </a>
    {:else}
      <LoginLink>
        {$_('userpanel.login.text1')}
        <br />
        {$_('userpanel.login.text2')}
      </LoginLink>
    {/if}
  </div>
</div>

<style>
  div.user-panel {
    overflow: visible;
  }
  div.image img.img-thumbnail {
    width: 3rem;
    max-width: none;
  }
  div.image img.christmashat {
    position: absolute;
    z-index: 1039;
    width: 3rem;
    left: 1rem;
    top: -1rem;
  }
</style>
