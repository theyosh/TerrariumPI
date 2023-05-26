
import websocketStore from "svelte-websocket-store";
import { get } from "svelte/store";
import { _ } from 'svelte-i18n';

import {
  isDay, lastUpdate, uptime, systemLoad, systemCPUTemp, systemMemory, systemDisk, isOnline,

  currentPower,
  maxPower,
  totalPower,
  totalPowerCosts,
  totalPowerDuration,

  currentWater,
  maxWater,
  totalWater,
  totalWaterCosts,
  totalWaterDuration,

  updateSensor,
  updateButton,
  updateRelay,

  last_log_line
} from "../stores/terrariumpi";
import { isAuthenticated } from "../stores/authentication";
import { WebsocketUrl } from "../constants/urls";
import { fireworks, christmas } from "../constants/easter-eggs";
import { animate_footer_badge, animateHourglass } from "../helpers/animation-helpers";
import { errorNotification, successNotification } from "../providers/notification-provider";

export const websocket = websocketStore(`${WebsocketUrl}`, {});

const $_ = get(_);

let offlineCounter = null;

const _setOnline = () => {
  clearTimeout(offlineCounter);

  let current_state = get(isOnline);
  if (current_state.status !== true) {
    current_state.last_action = new Date();
    current_state.status = true;
    isOnline.set(current_state);
    successNotification($_('notification.online.message'), $_('notification.online.title'));
  }

  offlineCounter = setTimeout(() => {
    let current_state = get(isOnline);
    if (current_state.status !== false) {
      current_state.last_action = new Date();
      current_state.status = false;
      isOnline.set(current_state);
      errorNotification($_('notification.offline.message'), $_('notification.offline.title'));
      _reConnect();
    }
  }, 60 * 1000);
};

const _reConnect = () => {
  // TODO: Start a reconnect trigger......???
  try {
    websocket.set({ type: 'client_init', reconnect: true });
  } catch (e) {
    setTimeout(() => { _reConnect(); }, 30 * 1000);
  }
};

websocket.subscribe(message => {
  if (message.type === undefined) return;

  // let data = null
  let onlineUpdate = true;

  switch (message.type) {

    case 'systemstats':
      isDay.set(message.data.is_day);
      uptime.set(message.data.uptime);
      lastUpdate.set(new Date());
      systemLoad.set([message.data.load.percentage[0], message.data.load.percentage[1], message.data.load.percentage[2]]);
      systemCPUTemp.set(message.data.cpu_temperature);
      systemMemory.set([message.data.memory.used, message.data.memory.total]);
      systemDisk.set([message.data.storage.used, message.data.storage.total]);
      animateHourglass();
      // Some easter eggs.... :P
      fireworks();
      christmas();
      break;

    case 'power_usage_water_flow':
      currentPower.set(message.data.power.current);
      maxPower.set(message.data.power.max);
      totalPower.set(message.data.power.total);
      totalPowerCosts.set(message.data.power.costs);
      totalPowerDuration.set(message.data.power.duration);

      currentWater.set(message.data.flow.current);
      maxWater.set(message.data.flow.max);
      totalWater.set(message.data.flow.total);
      totalWaterCosts.set(message.data.flow.costs);
      totalWaterDuration.set(message.data.flow.duration);
      break;

    case 'sensor':
      updateSensor(message.data);
      break;

    case 'relay':
      updateRelay(message.data);
      break;

    case 'button':
      updateButton(message.data);
      break;

    case 'logline':
      if (get(isAuthenticated)) {
        last_log_line.set(message.data);
      }

      if (message.data.indexOf('WARNING') !== -1) {
        animate_footer_badge('warning');
      } else if (message.data.indexOf('ERROR') !== -1) {
        animate_footer_badge('danger');
      }
      animate_footer_badge();
      break;

    case 'softwareupdate':
      successNotification(message.data.message, message.data.title, { closeButton: true, timeOut: 0, extendedTimeOut: 0 });
      break;

    default:
      // eslint-disable-line no-console
      // console.log('Websocket messages left', message.type, message)
      onlineUpdate = false;
      break;
  }

  if (onlineUpdate) {
    _setOnline();
  }
});
