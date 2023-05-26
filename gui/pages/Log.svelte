<script>
  import { _ } from 'svelte-i18n';
  import { onMount, onDestroy } from 'svelte';
  import { PageHeader, BreadcrumbItem } from 'svelte-adminlte';
  import { date, time } from 'svelte-i18n';

  import { setCustomPageTitle, customPageTitleUsed } from '../stores/page-title';
  import { last_log_line } from '../stores/terrariumpi';
  import { fetchLoglines } from '../providers/api';
  import { isAuthenticated } from '../stores/authentication';

  let text_filter,
    error_filter,
    warning_filter = null;
  let logdata,
    filtered_logdata = '';
  let last_change = new Date();
  let lines_counter = 0;
  let downloading = false;

  const show_log_lines = (new_line, text_filter, error_filter, warning_filter) => {
    if (!logdata || logdata === undefined || logdata === '') {
      return;
    }

    if (new_line) {
      logdata = new_line + '\n' + logdata;
      last_log_line.set('');
    }

    text_filter = text_filter || '';

    let filters = [];
    if (error_filter) {
      filters.push('ERROR');
    }
    if (warning_filter) {
      filters.push('WARNING');
    }

    if (text_filter !== '' || filters.length > 0) {
      if (text_filter !== '' && filters.length > 0) {
        text_filter =
          '(.*' +
          text_filter +
          '.*\\s+-\\s+(' +
          filters.join('|') +
          ')\\s+-\\s+' +
          ')|(.*\\s+-\\s+(' +
          filters.join('|') +
          ')\\s+-\\s+.*' +
          text_filter +
          '.*)';
      } else if (text_filter === '' || filters.length > 0) {
        text_filter = '\\s+-\\s+(' + filters.join('|') + ')\\s+-';
      }

      text_filter = new RegExp('^.*' + text_filter + '.*', 'img');
      filtered_logdata = logdata.match(text_filter);

      if (filtered_logdata !== null) {
        filtered_logdata = filtered_logdata.join('\n').trim();
      } else {
        filtered_logdata = '';
      }
    } else {
      text_filter = false;
      filtered_logdata = logdata;
    }

    lines_counter = (filtered_logdata.match(/\n/g) || []).length;
    lines_counter = lines_counter > 0 ? lines_counter++ : lines_counter; // Add extra lastline if there are more then 0 lines
    last_change = new Date();
  };

  const download_logfile = async () => {
    downloading = true;

    const filename = 'terrariumpi_logfile.txt';
    let loglines = '';
    await fetchLoglines((data) => (loglines = data));

    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(new Blob([loglines]));
    link.download = filename;
    link.click();

    downloading = false;
  };

  onMount(() => {
    setCustomPageTitle($_('system.log.title', { default: 'System logging' }));
    fetchLoglines((data) => (logdata = data.split('\n').reverse().join('\n').trim()), true);
  });

  onDestroy(() => {
    customPageTitleUsed.set(false);
  });

  $: show_log_lines($last_log_line, text_filter, error_filter, warning_filter);
</script>

<PageHeader>
  {$_('system.log.title', { default: 'System logging' })}

  <svelte:fragment slot="breadcrumbs">
    {#if $isAuthenticated}
      <BreadcrumbItem>
        <a
          href="{'#'}"
          class="mt-1"
          target="_blank"
          rel="noopener noreferrer"
          title="{$_('system.log.download.title', { default: 'Download log file' })}"
          on:click|preventDefault="{download_logfile}">
          <i class="fas" class:fa-download="{!downloading}" class:fa-spinner="{downloading}" class:fa-spin="{downloading}"></i>
          {$_('system.log.download.title', { default: 'Download log file' })}
        </a>
      </BreadcrumbItem>
    {/if}
  </svelte:fragment>
</PageHeader>
<div class="container-fluid">
  <div class="row" style="height: 85vh !important">
    <div class="col-md-12">
      <div class="card logging h-100">
        <div class="card-header">
          <h3 class="card-title mr-1">
            <i class="fas fa-file-alt mr-2"></i>{$_('system.log.title')}
            <small class="ml-1 mr-2">{$_('system.log.lines', { default: '{lines} lines', values: { lines: lines_counter } })}</small>
            <small class="mr-2">{$date(last_change, { format: 'long' })} {$time(last_change, { format: 'short' })}</small>
          </h3>
          <div class="card-tools form-inline" style="flex-flow: nowrap">
            <label for="filerfield" class="form-check-label mr-4">{$_('system.log.filters.title', { default: 'Filters' })}:</label>
            <div class="input-group mr-3">
              <div class="form-group">
                <input
                  id="filerfield"
                  type="text"
                  class="form-control form-control-sm"
                  placeholder="{$_('system.log.filters.search', { default: 'Enter search terms' })}"
                  bind:value="{text_filter}" />
                {#if text_filter}
                  <button type="button" class="btn btn-tool" on:click="{() => (text_filter = null)}" style="margin-left: -30px">
                    <i class="form-control-clear fas fa-times"></i>
                  </button>
                {/if}
              </div>
            </div>
            <div class="form-check form-check-inline">
              <input class="form-check-input" type="checkbox" value="error" bind:checked="{error_filter}" />
              <label class="form-check-label" for="error_filter">{$_('system.log.filters.errors', { default: 'errors' })}</label>
            </div>
            <div class="form-check form-check-inline">
              <input class="form-check-input" type="checkbox" value="warning" bind:checked="{warning_filter}" />
              <label class="form-check-label" for="warning_filter">{$_('system.log.filters.warnings', { default: 'warnings' })}</label>
            </div>
          </div>
        </div>
        <div class="card-body">
          <textarea
            class="form-control text-monospace h-100"
            placeholder="{$_('system.log.loading', { default: 'Loading data' })}"
            readonly="readonly"
            bind:value="{filtered_logdata}"></textarea>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  textarea {
    font-size: 0.8rem;
  }
</style>
