<script>
  import { dayjs } from 'svelte-time';
  import duration from 'dayjs/esm/plugin/duration';
  dayjs.extend(duration);
  import { onDestroy, onMount, getContext } from 'svelte';
  import { _ } from 'svelte-i18n';
  import { PageHeader } from 'svelte-adminlte';
  import tippy from 'sveltejs-tippy';
  import { followCursor } from 'tippy.js';

  import { locale } from '../locale/i18n';
  import { setCustomPageTitle, customPageTitleUsed } from '../stores/page-title';
  import { isAuthenticated } from '../stores/authentication';
  import { getCustomConfig } from '../config';
  import { ApiUrl } from '../constants/urls';
  import { fetchCalendarEvents, updateCalendarEvent, deleteCalendarEvent, downloadCalendar } from '../providers/api';
  import { successNotification, errorNotification } from '../providers/notification-provider';

  import Card from '../user-controls/Card.svelte';
  import LoginLink from '../components/common/LoginLink.svelte';
  import EventModel from '../modals/EventFormModal.svelte';

  let calendar;
  let loading = true;
  let showModal;

  let downloading = false;

  const settings = getCustomConfig();

  const { confirmModal } = getContext('confirm');

  const loadData = () => {
    calendar.refetchEvents();
  };

  const download_calendar = async () => {
    downloading = true;

    const filename = 'terrariumpi_calendar.ics';
    let ical = '';
    await downloadCalendar((data) => (ical = data));

    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(new Blob([ical]));
    link.download = filename;
    link.click();

    downloading = false;
  };

  const deleteCalendarEventCall = (event) => {
    event.stopPropagation();
    let data = JSON.parse(event.currentTarget.dataset.calendar);
    confirmModal(
      $_('calendar.event.delete.confirm.message', {
        default: "Are you sure you want to delete the event ''{name}''?",
        values: { name: data.name },
      }),
      async () => {
        try {
          await deleteCalendarEvent(data.id);
          successNotification(
            $_('calendar.event.delete.ok.message', { default: "The event ''{name}'' is deleted.", values: { name: button.name } }),
            $_('notification.delete.ok.title', { default: 'OK' })
          );
          loadData();
        } catch (e) {
          errorNotification(
            $_('calendar.event.delete.error.message', {
              default: "The event ''{name}'' could not be deleted!\nError: {error}",
              values: { name: button.name, error: e.message },
            }),
            $_('notification.delete.error.title', { default: 'ERROR' })
          );
        }
      }
    );
  };

  const editCalendarEvent = (eventData) => {
    showModal(eventData);
  };

  onMount(() => {
    setCustomPageTitle($_('calendar.title', { default: 'Calendar' }));

    let deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.style = 'display:block; background-color: transparent; border: 0px; position: absolute; right:0px; top: 0px; z-index: 999';
    deleteButton.innerHTML = '<i class="fas fa-trash-alt text-danger">';
    deleteButton.onclick = deleteCalendarEventCall;

    // We use the AdminLTE compiled calendar version which has better theming..
    calendar = new FullCalendar.Calendar(document.getElementById('calendar'), {
      initialView: 'dayGridMonth',
      locale: $locale.substring(0, 2),
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay',
      },
      themeSystem: 'bootstrap',
      events: {
        url: `${ApiUrl}/api/calendar/`,
      },

      droppable: false, // this allows things to be dropped onto the calendar !!!
      selectable: false,
      editable: false,

      loading: function (loading_state) {
        loading = loading_state;
      },

      eventMouseEnter: function (data) {
        if ($isAuthenticated) {
          deleteButton.setAttribute('data-calendar', JSON.stringify({ name: data.event.title, id: data.event.id }));
          data.el.appendChild(deleteButton);
        }
      },

      eventMouseLeave: function (data) {
        deleteButton.remove();
      },

      eventDidMount: function (data) {
        let end = data.event.end || data.event.start + 24 * 3600;
        tippy(data.el, {
          allowHTML: true,
          arrow: true,
          followCursor: 'horizontal',
          plugins: [followCursor],
          content:
            '<h6 style="font-weight: bold">' +
            data.event.title +
            '</h6>' +
            data.event.extendedProps.description +
            '<strong>' +
            $_('calendar.event.duration', { default: 'Duration' }) +
            ':' +
            '</strong> ' +
            dayjs.duration(end - data.event.start).humanize(),
        });
      },

      select: function (data) {
        if (!$isAuthenticated) {
          calendar.unselect();
        } else {
          // Open modal for adding event
          data.mode = 'repeat';
          editCalendarEvent(data);
        }
      },
      eventClick: function (data) {
        if ($isAuthenticated) {
          // Open modal for adding event
          data = {
            'id' : data.event.id,
            'mode' : 'repeat'
          }
          editCalendarEvent(data);
        }
      },

      eventDrop: function (data) {
        let move = data.delta.days * (24 * 3600) + data.delta.months * (30 * 24 * 3600);
        if ($isAuthenticated && move !== 0) {
          (async () => {
            let item = null;
            await fetchCalendarEvents(data.event.id, (data) => (item = data));
            item.dtstart += move;
            item.dtend += move;

            if (item) {
              try {
                await updateCalendarEvent(item);
                successNotification(
                  $_('calendar.event.settings.update.ok.message', {
                    default: "The event ''{name}'' is updated.",
                    values: { name: item.summary },
                  }),
                  $_('notification.delete.ok.title', { default: 'OK' })
                );
                loadData();
              } catch (e) {
                errorNotification(
                  $_('calendar.event.settings.update.error.message', {
                    default: "The event ''{name}'' could not be updated!\nError: {error}",
                    values: { name: item.summary, error: e.message },
                  }),
                  $_('notification.delete.error.title', { default: 'ERROR' })
                );
              }
            }
          })();
        } else {
          data.revert();
        }
      },

      eventResize: function (data) {
        let moveStart = data.startDelta.days * (24 * 3600) + data.startDelta.months * (30 * 24 * 3600);
        let moveEnd = data.endDelta.days * (24 * 3600) + data.endDelta.months * (30 * 24 * 3600);
        if ($isAuthenticated && (moveStart !== 0 || moveEnd !== 0)) {
          (async () => {
            let item = null;
            await fetchCalendarEvents(data.event.id, (data) => (item = data));
            item.dtstart += moveStart;
            item.dtend += moveEnd;

            if (item) {
              try {
                await updateCalendarEvent(item);
                successNotification(
                  $_('calendar.event.settings.update.ok.message', {
                    default: "The event ''{name}'' is updated.",
                    values: { name: item.summary },
                  }),
                  $_('notification.delete.ok.title', { default: 'OK' })
                );
                loadData();
              } catch (e) {
                errorNotification(
                  $_('calendar.event.settings.update.error.message', {
                    default: "The event ''{name}'' could not be updated!\nError: {error}",
                    values: { name: item.summary, error: e.message },
                  }),
                  $_('notification.delete.error.title', { default: 'ERROR' })
                );
              }
            }
          })();
        } else {
          data.revert();
        }
      },
    });

    calendar.render();
  });

  onDestroy(() => {
    calendar.destroy();
    customPageTitleUsed.set(false);
  });

  $: {
    if (calendar) {
      calendar.setOption('selectable', $isAuthenticated);
      calendar.setOption('editable', $isAuthenticated);
      calendar.setOption('eventResizableFromStart', $isAuthenticated);
    }
  }
</script>

<PageHeader>
  {$_('calendar.title', { default: 'Calendar' })}
  <svelte:fragment slot="breadcrumbs">
    {#if $isAuthenticated}
      <li class="breadcrumb-item">
        <a
          href="{'#'}"
          class="mt-1"
          target="_blank"
          rel="noopener noreferrer"
          title="{$_('calendar.actions.download', { default: 'Download iCal' })}"
          on:click|preventDefault="{download_calendar}">
          <i class="fas" class:fa-download="{!downloading}" class:fa-spinner="{downloading}" class:fa-spin="{downloading}"></i>
          {$_('calendar.actions.download', { default: 'Download iCal' })}
        </a>
      </li>
    {:else}
      <LoginLink />
    {/if}
  </svelte:fragment>
</PageHeader>
<div class="container-fluid">
  <div class="row">
    <div class="col-12">
      <Card loading="{loading}" noTools="{true}">
        <div id="calendar"></div>
      </Card>
    </div>
  </div>
</div>
{#if $isAuthenticated}
  <EventModel bind:show="{showModal}" on:save="{loadData}" />
{/if}

<style>
  @import '../../node_modules/admin-lte/plugins/fullcalendar/main.min.css';
</style>
