import { writable, get } from "svelte/store";
import { apiLogin } from "../providers/api";
import { websocket } from "../providers/websocket";
import { default as currentUserStore } from "./current-user";

export const isAuthenticated = writable(false);
export const loginModal = writable(null);
export const credentials = writable(null);

export const showLogin = () => {
  // Show modal
  get(loginModal).show();
};

export const doLogin = async (username, password) => {
  // Call to login API and check result
  const login = await apiLogin(username, password);
  if (login) {
    // Reconnect with auth cookie for logfile data
    currentUserStore.set(username);
    credentials.set({ username: username, password: password });
    try {
      websocket.set({ type: 'client_init', auth: window.btoa(username + ':' + password) });
      // TODO: Stupid timeout is needed in order to remove the login backdrop shadow div....
    } catch (e) {
      /* empty */
    }
    setTimeout(function () {
      isAuthenticated.set(true);
    }, 1000);
  }
  return login;
};

export const doLogout = () => {
  // Delete all cookies....
  document.cookie.split(';').forEach(function (c) {
    document.cookie = c.trim().split('=')[0] + '=;' + 'expires=Thu, 01 Jan 1970 00:00:00 UTC;';
  });

  websocket.set({ type: 'client_init', auth: '' });
  credentials.set({});
  currentUserStore.set(null);

  setTimeout(function () {
    isAuthenticated.set(false);
  }, 500);
};