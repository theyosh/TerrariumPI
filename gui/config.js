import { getConfig, setConfig } from 'svelte-adminlte/src/config.js';
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
    ...getConfig(),
    ...extra
  };
  setConfig(settings);

  if (settings.logged_in && settings.username) {
    isAuthenticated.set(true);
    currentUserStore.set(settings.username);
  }

  return getConfig();
};