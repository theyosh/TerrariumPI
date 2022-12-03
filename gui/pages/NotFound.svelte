<script>
  import { onMount, onDestroy } from 'svelte';
  import { PageHeader } from 'svelte-adminlte';
  import { _ } from 'svelte-i18n';

  import { setCustomPageTitle, customPageTitleUsed } from '../stores/page-title';

  onMount(() => {
    setCustomPageTitle('404 ' + $_('not-found.title', { default: 'Page not found' }));
  });

  onDestroy(() => {
    customPageTitleUsed.set(false);
  });
</script>

<PageHeader>
  404 {$_('not-found.title', { default: 'Page not found' })}
</PageHeader>

<div class="container-fluid">
  <div class="row">
    <div class="col-12 text-center pt-5">
      <div class="error-page">
        <h2 class="headline text-warning">404</h2>
        <div class="error-content">
          <h3><i class="fas fa-exclamation-triangle text-warning"></i> Oops! Page not found.</h3>
          <p>We could not find the page you were looking for. Meanwhile, you may <a href="/">return to dashboard</a>.</p>
        </div>
      </div>
    </div>
  </div>
</div>
