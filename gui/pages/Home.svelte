<script>
  import { PageHeader } from 'svelte-adminlte';
  import { _ } from 'svelte-i18n';
  import { onMount, onDestroy } from 'svelte';

  import { setCustomPageTitle, customPageTitleUsed } from '../stores/page-title';

  onMount(() => {
    setCustomPageTitle($_('home.title', { default: 'Home' }));
    // Redirect to dashboard
    location.href = '/#/dashboard/';
  });

  onDestroy(() => {
    customPageTitleUsed.set(false);
  });
</script>

<PageHeader>
  {$_('home.title', { default: 'Home' })}
</PageHeader>
