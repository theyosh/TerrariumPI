<script>
  import { onMount, onDestroy, getContext } from 'svelte';
  import { PageHeader } from 'svelte-adminlte';
  import { _ } from 'svelte-i18n';

  import { setCustomPageTitle, customPageTitleUsed } from '../stores/page-title';
  import {
    fetchNotificationServices,
    deleteNotificationService,
    fetchNotificationMessages,
    deleteNotificationMessage,
  } from '../providers/api';
  import { successNotification, errorNotification } from '../providers/notification-provider';
  import { template_sensor_type_icon } from '../helpers/icon-helpers';
  import { isDarkInterface } from '../stores/terrariumpi';
  import { nl2br } from '../helpers/string-helpers';

  import Card from '../user-controls/Card.svelte';
  import CardSettingsTools from '../components/common/CardSettingsTools.svelte';

  let services_loading = false;
  let services = [];

  let messages_loading = false;
  let messages = [];

  const { confirmModal } = getContext('confirm');
  const { editService, editMessage } = getContext('modals');

  const deleteServiceAction = (service) => {
    confirmModal(
      $_('services.delete.confirm.message', {
        default: "Are you sure you want to delete the service ''{name}''?",
        values: { name: service.name },
      }),
      async () => {
        try {
          await deleteNotificationService(service.id);
          successNotification(
            $_('services.delete.ok.message', { default: "The service ''{name}'' is deleted.", values: { name: service.name } }),
            $_('notification.delete.ok.title', { default: 'OK' })
          );
          loadServices();
        } catch (e) {
          errorNotification(
            $_('services.delete.error.message', {
              default: "The service ''{name}'' could not be deleted!\nError: {error}",
              values: { name: service.name, error: e.message },
            }),
            $_('notification.delete.error.title', { default: 'ERROR' })
          );
        }
      }
    );
  };

  const deleteMessageAction = (message) => {
    confirmModal(
      $_('messages.delete.confirm.message', {
        default: "Are you sure you want to delete the message ''{name}''?",
        values: { name: message.title },
      }),
      async () => {
        try {
          await deleteNotificationMessage(message.id);
          successNotification(
            $_('messages.delete.ok.message', { default: "The message ''{name}'' is deleted.", values: { name: message.title } }),
            $_('notification.delete.ok.title', { default: 'OK' })
          );
          loadMessages();
        } catch (e) {
          errorNotification(
            $_('messages.delete.error.message', {
              default: "The message ''{name}'' could not be deleted!\nError: {error}",
              values: { name: message.title, error: e.message },
            }),
            $_('notification.delete.error.title', { default: 'ERROR' })
          );
        }
      }
    );
  };

  const loadServices = async () => {
    services_loading = true;
    await fetchNotificationServices(null, (data) => (services = data));
    services_loading = false;
  };

  const loadMessages = async () => {
    messages_loading = true;
    await fetchNotificationMessages(null, (data) => (messages = data));
    messages_loading = false;
  };

  onMount(() => {
    loadServices();
    loadMessages();
    setCustomPageTitle($_('system.notifications.title', { default: 'Notifications' }));
  });

  onDestroy(() => {
    customPageTitleUsed.set(false);
  });
</script>

<PageHeader>
  {$_('system.notifications.title', { default: 'Notifications' })}
</PageHeader>
<div class="container-fluid">
  <div class="row">
    <div class="col">
      <Card loading="{services_loading}">
        <svelte:fragment slot="header">
          <i class="fas fa-bell mr-2"></i>{$_('services.title', { default: 'Notification services' })}
        </svelte:fragment>

        <svelte:fragment slot="tools">
          <CardSettingsTools>
            <button class="dropdown-item" on:click="{() => editService()}">
              <i class="fas fa-plus mr-2"></i>{$_('services.add', { default: 'Add service' })}
            </button>
          </CardSettingsTools>
        </svelte:fragment>

        {#if services.length > 0}
          <div class="row">
            <!-- Sort based on translated names -->
            {#each services.sort((a, b) => a.name.localeCompare(b.name)) as service}
              <div class="col-2">
                <div class="info-box">
                  <a
                    href="{'#'}"
                    class="info-box-icon"
                    title="{$_('services.actions.edit', { default: 'Edit service' })}"
                    class:bg-info="{service.enabled}"
                    class:bg-gray="{!service.enabled}"
                    on:click|preventDefault="{() => editService(service)}">
                    <i class="{template_sensor_type_icon(service.type)}"></i>
                  </a>
                  <div class="info-box-content">
                    <span class="info-box-text">{service.name}</span>
                    <span class="info-box-number"
                      >{$_('services.ratelimit', {
                        default: '{number, plural, =0 {Unlimited messages} other {Max # per minute}}',
                        values: { number: service.rate_limit },
                      })}</span>
                    <span class="info-box-text"
                      >{$_('services.enabled', { default: 'Enabled' })}:
                      <i class="fas" class:fa-check="{service.enabled}" class:fa-times="{!service.enabled}"> </i></span>
                    <button
                      class="btn btn-small text-danger"
                      title="{$_('services.actions.delete', { default: 'Delete service' })}"
                      on:click="{() => deleteServiceAction(service)}">
                      <i class="fas fa-trash-alt"></i>
                    </button>
                  </div>
                </div>
              </div>
            {/each}
          </div>
        {/if}
      </Card>
    </div>
  </div>

  <div class="row">
    <div class="col">
      <Card loading="{messages_loading}">
        <svelte:fragment slot="header">
          <i class="fas fa-envelope-open-text mr-2"></i>{$_('messages.title', { default: 'Notification messages' })}
        </svelte:fragment>

        <svelte:fragment slot="tools">
          <CardSettingsTools>
            <button class="dropdown-item" on:click="{() => editMessage()}">
              <i class="fas fa-plus mr-2"></i>{$_('messages.add', { default: 'Add message' })}
            </button>
          </CardSettingsTools>
        </svelte:fragment>

        {#if messages.length > 0}
          <div class="row">
            <table class="table">
              <thead>
                <tr>
                  <th>{$_('messages.table.type', { default: 'Type' })}</th>
                  <th>{$_('messages.table.subject', { default: 'Subject' })}</th>
                  <th>{$_('messages.table.message', { default: 'Message' })}</th>
                  <th style="white-space: nowrap;">{$_('messages.table.rate_limit', { default: 'Rate limit' })}</th>
                  <th>{$_('messages.table.enabled', { default: 'Enabled' })}</th>
                  <th>{$_('messages.table.services', { default: 'Services' })}</th>
                  <th>{$_('messages.table.actions', { default: 'Actions' })}</th>
                </tr>
              </thead>
              <tbody>
                <!-- Sort based on translated names -->
                {#each messages.sort((a, b) => a.title.localeCompare(b.title)) as message}
                  <tr>
                    <td>{message.type}</td>
                    <td>{message.title}</td>
                    <td>{@html nl2br(message.message)}</td>
                    <td
                      >{$_('messages.ratelimit', {
                        default: '{number, plural, =0 {Unlimited messages} other {Max # per minute}}',
                        values: { number: message.rate_limit },
                      })}</td>
                    <td><i class="fas" class:fa-check="{message.enabled}" class:fa-times="{!message.enabled}"> </i></td>
                    <td>
                      {#each message.services as message_service}
                        <i class="{template_sensor_type_icon(message_service.type)}" class:text-info="{message_service.enabled}"></i>&nbsp;
                      {/each}
                    </td>
                    <td class="text-nowrap">
                      <button
                        class="btn btn-sm"
                        title="{$_('messages.actions.edit', { default: 'Edit message' })}"
                        class:btn-light="{!$isDarkInterface}"
                        class:btn-dark="{$isDarkInterface}"
                        on:click="{() => editMessage(message)}">
                        <i class="fas fa-wrench"></i>
                      </button>
                      <button
                        class="btn btn-sm"
                        title="{$_('messages.actions.delete', { default: 'Delete message' })}"
                        class:btn-light="{!$isDarkInterface}"
                        class:btn-dark="{$isDarkInterface}"
                        on:click="{() => deleteMessageAction(message)}">
                        <i class="fas fa-trash-alt text-danger"></i>
                      </button>
                    </td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        {/if}
      </Card>
    </div>
  </div>
</div>

<style>
  div.info-box:hover div.info-box-content button.text-danger {
    display: block !important;
  }

  .info-box-content {
    line-height: 120% !important;
  }

  button.text-danger {
    position: absolute;
    top: 0px;
    right: 0px;
    display: none;
  }
</style>
