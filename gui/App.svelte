<script context="module">
  import { locale } from './locale/i18n';

  import { dayjs } from 'svelte-time';
  import duration from 'dayjs/esm/plugin/duration';
  dayjs.extend(duration);

  // Import Dayjs locales
  import 'dayjs/locale/de';
  import 'dayjs/locale/de-at';
  import 'dayjs/locale/en';
  import 'dayjs/locale/en-gb';
  import 'dayjs/locale/es';
  import 'dayjs/locale/fr';
  import 'dayjs/locale/it';
  import 'dayjs/locale/ja';
  import 'dayjs/locale/nb';
  import 'dayjs/locale/nl';
  import 'dayjs/locale/pl';
  import 'dayjs/locale/pt';

  // Reload when language changes.....?
  locale.subscribe((x) => {
    dayjs.locale(x);
  });
</script>

<script>
  import { onDestroy, onMount, setContext } from 'svelte';
  import { fade } from 'svelte/transition';
  import { get } from 'svelte/store';
  import Router from 'svelte-spa-router';
  import { _, date, time } from 'svelte-i18n';
  import {
    TopNavigation,
    Sidebar,
    SidebarNavItem,
    Dropdown,
    DropdownItem,
    DropdownButton,
    DropdownMenu,
    DropdownDivider,
  } from 'svelte-adminlte';

  import RoutePages, { onRouteLoaded, Pages, PageUrls } from './pages';
  import { listenPageTitleChanged, customPageTitleUsed } from './stores/page-title';
  import { isDay, lastUpdate, isOnline, doors, isDarkInterface } from './stores/terrariumpi';
  import { animate_footer_badge } from './helpers/animation-helpers';
  import { websocket } from './providers/websocket';
  import { fetchUpcomingEvents, scanSensors, scanRelays, systemRestart, systemReboot, systemShutdown } from './providers/api';
  import { isAuthenticated, loginModal } from './stores/authentication';

  import SidebarNavTree from './user-controls/SidebarNavTree.svelte';
  import { updateSiteBar, toggleSidebarAdminActions } from './helpers/sidebar';
  import { setFavicon } from './helpers/icon-helpers';
  import Time from 'svelte-time';
  import { ApiUrl } from './constants/urls';

  import { getCustomConfig } from './config';
  import { default as UserPanel } from './components/common/UserPanel.svelte';
  import { template_sensor_type_icon } from './helpers/icon-helpers';
  import { autoDarkmode } from './helpers/color-helpers';

  import ConfirmModal from './modals/ConfirmModal.svelte';
  import LoginModal from './modals/LoginFormModal.svelte';
  import ButtonFormModal from './modals/ButtonFormModal.svelte';
  import RelayFormModal from './modals/RelayFormModal.svelte';
  import SensorFormModal from './modals/SensorFormModal.svelte';
  import WebcamFormModal from './modals/WebcamFormModal.svelte';
  import EnclosureFormModal from './modals/EnclosureFormModal.svelte';
  import PlaylistFormModal from './modals/PlaylistFormModal.svelte';
  import AreaModal from './modals/AreaFormModal.svelte';

  import ServiceModal from './modals/ServiceModal.svelte';
  import MessageModal from './modals/MessageModal.svelte';

  import { successNotification } from './providers/notification-provider';

  let localeLanguage = '';
  let settings = getCustomConfig();
  let pageTitleSubscription;
  let localeSubscription;
  let upcomingEvents = [];

  let modalConfirm;
  let showConfirm;
  let hideConfirm;
  let confirmMessage = '';
  let confirmCallback;

  let editModal;
  let editModelContent;

  $isDay = !settings.is_night;
  $isAuthenticated = settings.logged_in;

  const sensor_submenu_sorting = (data) => {
    data.forEach((menu) => {
      if (menu.name === 'Sensors') {
        let light_submenu = menu.subroutes
          .filter((submenu) => {
            return ['sensors_light', 'sensors_uva', 'sensors_uvb', 'sensors_uvi'].indexOf(submenu.name) !== -1;
          })
          .sort((a, b) => $_(`${a.title}`).localeCompare($_(`${b.title}`)));

        if (light_submenu.length > 0) {
          let other_menu = menu.subroutes.filter((submenu) => {
            return ['sensors_light', 'sensors_uva', 'sensors_uvb', 'sensors_uvi'].indexOf(submenu.name) === -1;
          });
          menu.subroutes = [
            {
              name: 'sensors_light',
              title: 'sensors.light.menu.title',
              url: '',
              breadcrumb: ['Home', 'Sensors'],
              icon: 'fas ' + template_sensor_type_icon('light'),
              hide: false,
              subroutes: light_submenu,
            },
            ...other_menu,
          ];
        }
        menu.subroutes = [
          ...menu.subroutes.slice(0, -2).sort((a, b) => $_(`${a.title}`).localeCompare($_(`${b.title}`))),
          ...menu.subroutes.slice(-2),
        ];
      }
    });
  };

  const confirmModal = (message, callback) => {
    confirmMessage = message;
    confirmCallback = callback;
    modalConfirm.show();
  };

  setContext('confirm', {
    confirmModal,
  });

  setContext('modals', {
    editArea: (item, cb) => newModal('new_area', item, cb),
    editButton: (item, cb) => newModal('new_button', item, cb),
    editEnclosure: (item, cb) => newModal('new_enclosure', item, cb),
    editPlaylist: (item, cb) => newModal('new_playlist', item, cb),
    editRelay: (item, cb) => newModal('new_relay', item, cb),
    editSensor: (item, cb) => newModal('new_sensor', item, cb),
    editWebcam: (item, cb) => newModal('new_webcam', item, cb),
    editService: (item, cb) => newModal('new_service', item, cb),
    editMessage: (item, cb) => newModal('new_message', item, cb),
  });

  const newModal = (type, item, cb) => {
    editModelContent = null;

    switch (type) {
      case 'new_area':
        editModelContent = AreaModal;
        break;

      case 'new_button':
        editModelContent = ButtonFormModal;
        break;

      case 'new_enclosure':
        editModelContent = EnclosureFormModal;
        break;

      case 'new_playlist':
        editModelContent = PlaylistFormModal;
        break;

      case 'new_relay':
        editModelContent = RelayFormModal;
        break;

      case 'new_sensor':
        editModelContent = SensorFormModal;
        break;

      case 'new_webcam':
        editModelContent = WebcamFormModal;
        break;

      case 'new_service':
        editModelContent = ServiceModal;
        break;

      case 'new_message':
        editModelContent = MessageModal;
        break;
    }

    if (editModelContent) {
      setTimeout(() => {
        editModal.show(item ? item.id : null, cb);
      }, 150);
    }
  };

  const confirmAction = async () => {
    try {
      await confirmCallback();
      confirmCallback = null;
    } catch {}
    hideConfirm();
  };

  const menuAction = async (action) => {
    let title = null;
    let message = null;

    switch (action) {
      case 'scan_sensors':
        await scanSensors((data) => (message = data.message));
        title = $_('notification.scanning.ok.title');
        break;
      case 'scan_relays':
        await scanRelays((data) => (message = data.message));
        title = $_('notification.scanning.ok.title');
        break;
      case 'system_restart':
        await systemRestart((data) => (message = data.message));
        title = $_('notification.restart.ok.title');
        break;
      case 'system_reboot':
        await systemReboot((data) => (message = data.message));
        title = $_('notification.reboot.ok.title');
        break;
      case 'system_shutdown':
        await systemShutdown((data) => (message = data.message));
        title = $_('notification.shutdown.ok.title');
        break;
    }
    successNotification(message, title);

    title = null;
    message = null;
  };

  const confirmModalWindow = (type) => {
    let message = '';

    switch (type) {
      case 'scan_sensors':
        message = $_('modal.confirm.sensors.scan');
        break;
      case 'scan_relays':
        message = $_('modal.confirm.relays.scan');
        break;
      case 'system_restart':
        message = $_('modal.confirm.system.restart');
        break;
      case 'system_reboot':
        message = $_('modal.confirm.system.reboot');
        break;
      case 'system_shutdown':
        message = $_('modal.confirm.system.shutdown');
        break;
    }

    confirmModal(message, () => menuAction(type));
  };

  // Update sensor sub menu sorting
  sensor_submenu_sorting(Pages);

  // Auto 'magical' set/remove darkmode ONLY when isDay changed
  $: autoDarkmode($isDarkInterface);

  // Update disabled and enabled menu features
  $: toggleSidebarAdminActions($isAuthenticated);

  onMount(() => {
    try {
      $websocket = { type: 'client_init' };
    } catch (e) {
      console.log('Websocket reconnecting ex', e);
    }

    // Get initial data
    fetchUpcomingEvents((data) => {
      upcomingEvents = data;
    });

    /* GUI Hacks */
    setFavicon(ApiUrl + '/' + settings.favicon);
    document.querySelector('nav.main-header').classList.add('text-sm');
    document.querySelector('aside.main-sidebar').prepend(document.querySelector('a.brand-link'));
    document.querySelector('div.sidebar').prepend(document.querySelector('div.user-panel'));

    const sidebar = jQuery('div.sidebar nav.mt-2 ul.nav-sidebar');
    sidebar.addClass('nav-child-indent nav-flat');
    sidebar.find('i.disabled').removeClass('disabled').parent().parent().addClass('disabled');
    sidebar.find('i.fa-sync-alt').slice(2, 3).parent().addClass('text-info');
    sidebar.find('i.fa-sync-alt').last().parent().addClass('text-warning');
    sidebar.find('i.fa-power-off:last').parent().addClass('text-danger');

    localeSubscription = locale.subscribe((x) => (localeLanguage = x));
    pageTitleSubscription = listenPageTitleChanged();

    toggleSidebarAdminActions($isAuthenticated);

    // Reload every 15 minutes
    const interval = setInterval(() => {
      fetchUpcomingEvents((data) => {
        upcomingEvents = data;
      });
      animate_footer_badge();
    }, 15 * 60 * 1000);

    //If a function is returned from onMount, it will be called when the component is unmounted.
    return () => {
      clearInterval(interval);
    };
  });

  onDestroy(() => {
    if (localeSubscription) localeSubscription();
    if (pageTitleSubscription) pageTitleSubscription();
  });

  function routeLoaded({ detail: route }) {
    if (get(customPageTitleUsed)) return;

    return onRouteLoaded(route);
  }
</script>

<div class="wrapper">
  <TopNavigation>
    <svelte:fragment slot="right">
      <Dropdown>
        <DropdownButton data-widget="fullscreen">
          <i class="fas fa-expand-arrows-alt"></i>
        </DropdownButton>
      </Dropdown>
      <Dropdown>
        <DropdownButton>
          <i class="fas fa-calendar-alt"></i>
          <span class="badge badge-primary navbar-badge">{upcomingEvents.length > 0 ? upcomingEvents.length : ''}</span>
        </DropdownButton>
        <DropdownMenu right="{true}" large="{true}">
          <DropdownItem disabled="{true}" style="text-align:center; font-weight: bold"
            >{$_('topbar.upcoming_events', { values: { number: upcomingEvents.length } })}</DropdownItem>
          <DropdownDivider />
          {#each upcomingEvents as event}
            <DropdownItem href="#{PageUrls.Calendar}">
              <i class="fas fa-calendar-alt mr-2"></i>{event.title}
              <span class="float-right text-muted text-sm"><Time relative timestamp="{event.start}" /></span>
            </DropdownItem>
          {/each}
          <DropdownDivider />
          <DropdownItem href="#{PageUrls.Calendar}" style="text-align:center;">{$_('calendar.title')}</DropdownItem>
        </DropdownMenu>
      </Dropdown>
      <Dropdown>
        <DropdownButton>
          <i
            class="fas"
            class:fa-lock="{$doors.closed === null || $doors.closed === true}"
            class:fa-lock-open="{$doors.closed === false}"
            class:text-danger="{$doors.closed === false}"></i>
        </DropdownButton>
        <DropdownMenu right="{true}" large="{true}">
          <DropdownItem disabled="{true}" style="text-align:center; font-weight: bold">{$_('topbar.door_status')}</DropdownItem>
          <DropdownDivider />
          {#each Object.keys($doors.doors) as doorid}
            <DropdownItem disabled="{true}">
              <i
                class="fas"
                class:fa-lock="{$doors.doors[doorid].closed === true}"
                class:fa-lock-open="{$doors.doors[doorid].closed === false}"
                class:text-danger="{$doors.doors[doorid].closed === false}"></i>
              <span class="ml-1">
                {$doors.doors[doorid].name}
              </span>
              <span class="float-right text-muted text-sm">
                <Time live relative timestamp="{$doors.doors[doorid].last_update}" />
              </span>
            </DropdownItem>
          {/each}
        </DropdownMenu>
      </Dropdown>
      <Dropdown>
        <DropdownButton>
          <i class="fas fa-check-circle" class:text-success="{$isOnline.status === true}" class:text-danger="{$isOnline.status === false}"
          ></i>
        </DropdownButton>
        <DropdownMenu right="{true}" large="{true}">
          <DropdownItem disabled="{true}" style="text-align:center; font-weight: bold">{$_('topbar.current_status')}</DropdownItem>
          <DropdownDivider />
          <DropdownItem disabled="{true}">
            <i class="fas fa-check-circle" class:text-success="{$isOnline.status === true}" class:text-danger="{$isOnline.status === false}"
            ></i>
            {#if $isOnline.status !== null}
              <span class="ml-1">
                {$date($isOnline.last_action, { month: 'numeric', day: 'numeric' })}
                {$time($isOnline.last_action, { format: 'short' })}
              </span>
              <span class="float-right text-muted text-sm">
                <Time live relative timestamp="{$isOnline.last_action}" />
              </span>
            {/if}
          </DropdownItem>
        </DropdownMenu>
      </Dropdown>
      <span class="nav-link text-nowrap ml-1 pl-0 pr-0 ">
        <span class="fa-stack fa-1x mr-3">
          {#if $isDay}
            <i class="fas fa-sun mr-1 fa-stack-1x" transition:fade></i>
          {:else}
            <i class="fas fa-moon mr-1 fa-stack-1x" transition:fade></i>
          {/if}
        </span>
        <span class="d-none d-sm-inline">{$date($lastUpdate, { format: 'full' })}, {$time($lastUpdate, { format: 'short' })}</span>
        <span class="d-inline d-sm-none">{$date($lastUpdate, { format: 'medium' })}, {$time($lastUpdate, { format: 'short' })}</span>
      </span>
    </svelte:fragment>
  </TopNavigation>
  <Sidebar>
    <UserPanel />
    {#each Pages as page}
      {#if !page.hide}
        {#if page.subroutes && page.subroutes.length > 0}
          <SidebarNavTree icon="{page.icon}" href="#{page.url}">
            {$_(page.title)}
            <svelte:fragment slot="children">
              {#each page.subroutes as sub}
                {#if !sub.hide}
                  {#if ['scan_sensors', 'scan_relays', 'system_restart', 'system_reboot', 'system_shutdown'].indexOf(sub.url) != -1}
                    <li class="nav-item">
                      <a
                        href="{'#'}"
                        class="nav-link"
                        title="{$_(sub.title)}"
                        on:click|preventDefault="{() => confirmModalWindow(`${sub.url}`)}">
                        <i class="nav-icon fas {sub.icon}"></i>
                        <p>{$_(sub.title)}</p>
                      </a>
                    </li>
                  {:else if ['new_button', 'new_relay', 'new_sensor', 'new_webcam', 'new_playlist', 'new_enclosure', 'new_area'].indexOf(sub.url) != -1}
                    <li class="nav-item">
                      <a href="{'#'}" class="nav-link" title="{$_(sub.title)}" on:click|preventDefault="{() => newModal(`${sub.url}`)}">
                        <i class="nav-icon fas {sub.icon}"></i>
                        <p>{$_(sub.title)}</p>
                      </a>
                    </li>
                  {:else if sub.subroutes && sub.subroutes.length > 0}
                    <SidebarNavTree icon="{sub.icon}" href="#{sub.url}">
                      {$_(sub.title)}
                      <svelte:fragment slot="children">
                        {#each sub.subroutes as subsub}
                          {#if !subsub.hide}
                            <SidebarNavItem icon="{subsub.icon}" href="#{subsub.url}">
                              <p>{$_(subsub.title)}</p>
                            </SidebarNavItem>
                          {/if}
                        {/each}
                      </svelte:fragment>
                    </SidebarNavTree>
                  {:else}
                    <SidebarNavItem icon="{sub.icon}" href="#{sub.url}">
                      <p>{$_(sub.title)}</p>
                    </SidebarNavItem>
                  {/if}
                {/if}
              {/each}
            </svelte:fragment>
          </SidebarNavTree>
        {:else}
          <SidebarNavItem icon="{page.icon}" href="#{page.url}" title="{$_(page.title)}">
            <p>{$_(page.title)}</p>
          </SidebarNavItem>
        {/if}
      {/if}
    {/each}

    <li class="nav-header">&nbsp;</li>
    <li class="nav-item">
      <a href="#/about/" class="nav-link" title="{$_('about.title', { default: 'About' })}">
        <i class="fas fa-info nav-icon"></i>
        <p>{$_('about.title', { default: 'About' })}</p>
      </a>
    </li>
  </Sidebar>

  <div class="content-wrapper">
    <div class="content">
      <Router routes="{RoutePages}" on:routeLoaded="{routeLoaded}" on:routeLoaded="{updateSiteBar}" />
    </div>
  </div>
  <footer class="main-footer p-2 text-sm">
    &copy; 2015 - 2022 <a target="_blank" rel="noopener noreferrer" href="https://theyosh.nl">TheYOSH</a>
    <!-- Credits to the original builders. The least I can do -->
    <small>
      using <a target="_blank" rel="noopener noreferrer" href="https://adminlte.io">AdminLTE</a>,
      <a target="_blank" rel="noopener noreferrer" href="https://svelte.dev">Svelte</a>
      and
      <a target="_blank" rel="noopener noreferrer" href="https://github.com/KeenMate/rollup-svelte-adminlte-template">KeenMate template</a>
    </small>
    <div class="float-right d-sm-inline-block">
      <small class="badge badge-success opacity-1" title="{$_('footer.current_activity')}">&nbsp;&nbsp;</small>
      <small class="badge badge-warning opacity-1 ml-1" title="{$_('footer.warning_messages')}">&nbsp;&nbsp;</small>
      <small class="badge badge-danger  opacity-1 ml-1" title="{$_('footer.error_messages')}">&nbsp;&nbsp;</small>
      <span class="d-none d-sm-inline"
        >&nbsp;&nbsp; {settings.name}
        {settings.version} - <small>{settings.device}</small> -
        {#if $isAuthenticated}
          <a
            href="https://github.com/theyosh/TerrariumPI/commit/{settings.gitversion}"
            target="_blank"
            rel="noopener noreferrer"
            title="Git commit">{settings.gitversion.substring(0, 8)}</a> -
        {/if}
      </span>
      <small>
        <a href="https://github.com/theyosh/TerrariumPI" target="_blank" rel="noopener noreferrer" title="Download TerrariumPI on Github"
          >Terrarium home automation</a>
      </small>
    </div>
  </footer>
</div>

{#if $isAuthenticated}
  <svelte:component this="{editModelContent}" bind:this="{editModal}" />

  <ConfirmModal
    bind:show="{showConfirm}"
    bind:hide="{hideConfirm}"
    confirmMessage="{confirmMessage}"
    on:confirm="{confirmAction}"
    bind:this="{modalConfirm}" />
{:else}
  <LoginModal bind:this="{$loginModal}" />
{/if}

<style>
  .fa-stack {
    width: auto;
    top: -0.2rem;
    left: 0rem;
  }
</style>
