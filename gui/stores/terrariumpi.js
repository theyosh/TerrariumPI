import { writable, get, derived } from "svelte/store";
import { _ } from "svelte-i18n";
import { successNotification } from "../providers/notification-provider";
import { getCustomConfig } from "../config";

export const dynamic_settings = writable({});

export const upcomingCalendarItems = writable([]);
export const isDay = writable(true);
export const lastUpdate = writable(new Date());
export const isOnline = writable({ status: null, last_action: null });

// Dashboard info boxes
export const uptime = writable(0);

export const systemLoad = writable([0, 0, 0]);
export const systemCPUTemp = writable(0);
export const systemMemory = writable([0, 0, 0]);
export const systemDisk = writable([0, 0, 0]);

export const currentPower = writable(0);
export const maxPower = writable(0);
export const currentWater = writable(0);
export const maxWater = writable(0);
export const totalPower = writable(0);
export const totalPowerCosts = writable(0);
export const totalPowerDuration = writable(0);
export const totalWater = writable(0);
export const totalWaterCosts = writable(0);
export const totalWaterDuration = writable(0);

export const sensors = writable({});
export const relays = writable({});
export const buttons = writable({});
export const graphs = writable({});

export const last_log_line = writable('');

const $_ = get(_);

export const updateButton = (button) => {
  if (!button) return;

  let loaded_buttons = get(buttons);
  let old_state = loaded_buttons[button.id] ? loaded_buttons[button.id].value : null;

  loaded_buttons[button.id] = { ...loaded_buttons[button.id], ...button };

  if (old_state !== button.value) {
    loaded_buttons[button.id].last_update = new Date();
  }

  // Add door property if it has an connected enclosure
  loaded_buttons[button.id].door = button.enclosure !== null;
  if (loaded_buttons[button.id].door) {
    let inverse = button.hardware === 'remote' && button.calibration?.inverse === 'on';
    loaded_buttons[button.id].closed = button.value === (inverse ? 0 : 1);

    if ((old_state !== null || button.value === (inverse ? 1 : 0)) && old_state !== button.value) {
      // Door notification
      successNotification(
        $_(loaded_buttons[button.id].closed ? 'notification.door.status.closed' : 'notification.door.status.opened', { values: { name: loaded_buttons[button.id].name } }),
        $_('notification.door.status.title')
      );
    }
  }

  buttons.set(loaded_buttons);
};

export const updateRelay = (relay) => {
  if (!relay) return;

  let loaded_relays = get(relays);
  let old_state = loaded_relays[relay.id] ? loaded_relays[relay.id].value : null;

  loaded_relays[relay.id] = { ...loaded_relays[relay.id], ...relay };

  loaded_relays[relay.id].changed = old_state !== relay.value;
  loaded_relays[relay.id].last_update = new Date();

  relays.set(loaded_relays);
};

export const doors = derived(
  buttons,
  ($buttons) => {
    let doors = {};
    let enclosures = {};
    Object.keys($buttons).filter(button_id => $buttons[button_id].door).map(button_id => {
      if (!enclosures[$buttons[button_id].enclosure]) {
        enclosures[$buttons[button_id].enclosure] = { closed: true };
      }
      enclosures[$buttons[button_id].enclosure].closed = enclosures[$buttons[button_id].enclosure].closed && $buttons[button_id].closed;
      doors[button_id] = $buttons[button_id];
    });
    return { closed: Object.values(doors).every(door => door.closed), doors: doors, enclosures: enclosures };
  }
);

export const isDarkInterface = derived(
  isDay,
  ($isDay) => {
    const settings = getCustomConfig();
    const isDark = settings.auto_dark_mode && !$isDay;
    return isDark;
  }
);

export const updateSensor = (gauge) => {
  if (!gauge) return;

  let loaded_gauges = get(sensors);

  loaded_gauges[gauge.id] = { ...loaded_gauges[gauge.id], ...gauge };

  loaded_gauges[gauge.id].measure_min = !loaded_gauges[gauge.id].measure_min ? loaded_gauges[gauge.id].value : Math.min(loaded_gauges[gauge.id].measure_min, loaded_gauges[gauge.id].value);
  loaded_gauges[gauge.id].measure_max = !loaded_gauges[gauge.id].measure_max ? loaded_gauges[gauge.id].value : Math.max(loaded_gauges[gauge.id].measure_max, loaded_gauges[gauge.id].value);

  loaded_gauges[gauge.id].alarm = loaded_gauges[gauge.id].value < loaded_gauges[gauge.id].alarm_min || loaded_gauges[gauge.id].value > loaded_gauges[gauge.id].alarm_max;

  loaded_gauges[gauge.id].changed = true;
  loaded_gauges[gauge.id].last_update = new Date();

  sensors.set(loaded_gauges);
};

systemLoad.subscribe(store => {
  let known_gauges = get(sensors);
  if (known_gauges['system_load']) {
    known_gauges.system_load.value = store[0];
    known_gauges.system_load.changed = true;
    sensors.set(known_gauges);
  }
});

systemCPUTemp.subscribe(store => {
  let known_gauges = get(sensors);
  if (known_gauges['cpu_temp']) {
    known_gauges.cpu_temp.value = store;
    known_gauges.cpu_temp.changed = true;
    sensors.set(known_gauges);
  }
});

systemMemory.subscribe(store => {
  let known_gauges = get(sensors);
  if (known_gauges['memory']) {
    known_gauges.memory.value = store[0];
    known_gauges.memory.changed = true;
    sensors.set(known_gauges);
  }
});

systemDisk.subscribe(store => {
  let known_gauges = get(sensors);
  if (known_gauges['disk']) {
    known_gauges.disk.value = store[0];
    known_gauges.disk.changed = true;
    sensors.set(known_gauges);
  }
});