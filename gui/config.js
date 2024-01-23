import { get } from 'svelte/store';
import { Config } from '@keenmate/svelte-adminlte';
import { isAuthenticated } from './stores/authentication';
import { default as currentUserStore } from './stores/current-user';

const custom = {
  ContactEmail: 'tp@theyosh.nl',
  logged_in: false,
  docker: false,
};

export const getCustomConfig = (extra) => {
  extra = extra || {};
  const settings = {
    ...custom,
    ...window.terrariumPI,
    ...get(Config),
    ...extra,
  };
  Config.set(settings);

  if (settings.logged_in && settings.username) {
    isAuthenticated.set(true);
    currentUserStore.set(settings.username);
  }

  return get(Config);
};
