<script>
  import { onMount, onDestroy } from 'svelte';
  import { PageHeader } from 'svelte-adminlte';
  import { _ } from 'svelte-i18n';

  import { setCustomPageTitle, customPageTitleUsed } from '../stores/page-title';
  import { getCustomConfig } from '../config';

  import Card from '../user-controls/Card.svelte';

  let settings = getCustomConfig();

  onMount(() => {
    setCustomPageTitle($_('about.title', { default: 'About' }));
  });

  onDestroy(() => {
    customPageTitleUsed.set(false);
  });
</script>

<PageHeader>
  {$_('about.title', { default: 'About' })}
</PageHeader>
<div class="container-fluid">
  <div class="row">
    <div class="col">
      <Card loading="{false}" noPadding="{false}">
        <svelte:fragment slot="header">
          <i class="fas fa-info mr-2"></i>TerrariumPI v {settings.version}
        </svelte:fragment>
        <img src="/img/terrariumpi.jpg" class="img-thumbnail float-right" alt="TerariumPI Logo version {settings.version}" />
        <p>
          TerrariumPI is started back in 2015 in order to keep my <a
            href="https://en.wikipedia.org/wiki/Madagascar_day_gecko"
            target="_blank"
            rel="noopener noreferrer">Madagaskar day gecko</a> happy. This piece of software is started as a home automation for reptiles, but
          now it can be used for indoor plants growing and paludariums.
        </p>
        <p>
          This software is written in Python3 and uses the <a href="https://adminlte.io/" target="_blank" rel="noopener noreferrer"
            >AdminLTE admin web interface</a
          >. To make the GUI reactive we use <a href="https://svelte.dev" target="_blank" rel="noopener noreferrer">Svelte</a>.
        </p>
        <p>
          For documentation about how to install and set it up, see <a
            href="https://theyosh.github.io/TerrariumPI"
            target="_blank"
            rel="noopener noreferrer">https://theyosh.github.io/TerrariumPI</a
          >.
        </p>
        <p>
          For bugs and feature requests please open a <a
            href="https://github.com/theyosh/TerrariumPI/issues"
            target="_blank"
            rel="noopener noreferrer">Github issue</a
          >. <img alt="GitHub issues" src="https://img.shields.io/github/issues-raw/theyosh/terrariumpi" /> /
          <img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed-raw/theyosh/terrariumpi?color=00ff" />
        </p>
        <p>
          And there is a Matrix channel where you can try to ask questions and see if somebody can help you there: <a
            href="https://matrix.to/#/#terrariumpi:theyosh.nl"
            target="_blank"
            rel="noopener noreferrer">https://matrix.to/#/#terrariumpi:theyosh.nl</a
          >.
        </p>
        <p>
          Finally it would be nice when you use this software, to post some pictures of your setup at this Github issue: '<a
            href="https://github.com/theyosh/TerrariumPI/issues/210"
            target="_blank"
            rel="noopener noreferrer">Pictures of running TerrariumPI system #210</a
          >'
        </p>
        <p>API Documentation: <a href="api/redoc/" target="_blank">ReDoc</a> / <a href="api/swagger/" target="_blank">Swagger</a></p>
        <p><br />&copy; Copyright 2015 - 2023<br /><a href="https://theyosh.nl" target="_blank" rel="noopener noreferrer">TheYOSH</a></p>
      </Card>
    </div>
  </div>
</div>
