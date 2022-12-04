import { get } from "svelte/store";

import { customPageTitleUsed, pageTitle } from "../stores/page-title";
import { getCustomConfig } from "../config";
import { template_sensor_type_icon } from "../helpers/icon-helpers";

import Home from "./Home.svelte";
import Dashboard from "./Dashboard.svelte";
import Weather from "./Weather.svelte";
import Calendar from "./Calendar.svelte";
import Sensors from "./Sensors.svelte";
import Relays from "./Relays.svelte";
import Buttons from "./Buttons.svelte";
import Webcams from "./Webcams.svelte";
import AudioFiles from "./Audiofiles.svelte";
import Playlists from "./Playlists.svelte";
import Enclosures from "./Enclosures.svelte";
import Status from "./Status.svelte";
import Settings from "./Settings.svelte";
import Log from "./Log.svelte";
import Notifications from "./Notifications.svelte";
import About from "./About.svelte";

import NotFound from "./NotFound.svelte";
import Error from "./Error.svelte";

const settings = getCustomConfig();

export const Pages = [
  {
    name: "Error",
    title: "error.title",
    url: "/error",
    breadcrumb: ["Error"],
    hide: true
  },
  {
    name: "Home",
    title: "home.menu.title",
    url: "/",
    breadcrumb: ["Route 1"],
    icon: "fas fa-home",
    hide: false,
    nesting: true,
    subroutes: [
      {
        name: "Dashboard",
        title: "dashboard.menu.title",
        url: "/dashboard/",
        breadcrumb: ["Home"],
        icon: "fas fa-th-list",
        hide: false
      },
      {
        name: "Weather",
        title: "weather.menu.title",
        url: "/weather/",
        breadcrumb: ["Home"],
        icon: "fas fa-cloud-sun",
        hide: false
      },
      {
        name: "Calendar",
        title: "calendar.menu.title",
        url: "/calendar/",
        breadcrumb: ["Home"],
        icon: "fas fa-calendar-alt",
        hide: false
      },
      {
        name: "allSensors",
        title: "sensors.all.menu.title",
        url: "/sensors/all/",
        breadcrumb: ["Home"],
        icon: "fas fa-tint",
        hide: settings.show_gauge_overview != 1
      },
    ]
  },
  {
    name: "Sensors",
    title: "sensors.menu.title",
    url: "/sensors/",
    breadcrumb: [],
    icon: "fas fa-tint",
    hide: false,
    nesting: true,
    subroutes: [...settings.available_sensor_types.map(sensor_type => {
      return {
        name: `sensors_${sensor_type}`,
        title: `sensors.${sensor_type}.menu.title`,
        url: `/sensors/${sensor_type}/`,
        breadcrumb: ["Home", "Sensors"],
        icon: 'fas ' + template_sensor_type_icon(sensor_type),
        hide: false
      };
    }), ...[{
      name: 'new_sensor',
      title: 'sensors.menu.new.title',
      url: 'new_sensor',
      breadcrumb: ["Home", "Sensors"],
      icon: 'fas fa-plus disabled',
      hide: false
    }, {
      name: 'scan_sensors',
      title: 'sensors.menu.scan.title',
      url: 'scan_sensors',
      breadcrumb: ["Home", "Sensors"],
      icon: 'fas fa-sync-alt disabled',
      hide: false
    }]
    ]
  },
  {
    name: "Relays",
    title: "relays.menu.title",
    url: "/relays/",
    breadcrumb: [],
    icon: "fas fa-bolt",
    hide: false,
    nesting: true,
    subroutes: [
      {
        name: 'relay_status',
        title: 'relays.menu.status.title',
        url: "/relays/",
        breadcrumb: ["Home", "Sensors"],
        icon: 'fas fa-power-off',
        hide: false
      },
      {
        name: 'new_relay',
        title: 'relays.menu.new.title',
        url: 'new_relay',
        breadcrumb: ["Home", "Sensors"],
        icon: 'fas fa-plus disabled',
        hide: false
      }, {
        name: 'scan_relays',
        title: 'relays.menu.scan.title',
        url: 'scan_relays',
        breadcrumb: ["Home", "Sensors"],
        icon: 'fas fa-sync-alt disabled',
        hide: false
      }
    ]
  },
  {
    name: "Buttons",
    title: "buttons.menu.title",
    url: "/buttons/",
    breadcrumb: [],
    icon: "fas fa-thumbtack",
    hide: false,
    nesting: true,
    subroutes: [
      {
        name: 'button_status',
        title: 'buttons.menu.status.title',
        url: "/buttons/",
        breadcrumb: ["Home", "Buttons"],
        icon: 'fas fa-list',
        hide: false
      },
      {
        name: 'new_button',
        title: 'buttons.menu.new.title',
        url: 'new_button',
        breadcrumb: ["Home", "Buttons"],
        icon: 'fas fa-plus disabled',
        hide: false
      }
    ]
  },
  {
    name: "Webcams",
    title: "webcams.menu.title",
    url: "/webcams/",
    breadcrumb: [],
    icon: "fas fa-video",
    hide: false,
    nesting: true,
    subroutes: [
      {
        name: 'webcam_status',
        title: 'webcams.menu.status.title',
        url: "/webcams/",
        breadcrumb: ["Home", "Webcams"],
        icon: 'fas fa-tv',
        hide: false
      },
      {
        name: 'new_webcam',
        title: 'webcams.menu.new.title',
        url: 'new_webcam',
        breadcrumb: ["Home", "Webcams"],
        icon: 'fas fa-plus disabled',
        hide: false
      }
    ]
  },
  {
    name: "Audio",
    title: "audio.menu.title",
    url: "/audio/",
    breadcrumb: [],
    icon: "fas fa-music",
    hide: false,
    nesting: true,
    subroutes: [
      {
        name: 'audio_files',
        title: 'audio.menu.files.title',
        url: "/audio/files/",
        breadcrumb: ["Home", "Audio"],
        icon: 'fas fa-file-audio',
        hide: false
      },
      {
        name: 'playlists',
        title: 'audio.menu.playlists.title',
        url: "/audio/playlists/",
        breadcrumb: ["Home", "Audio"],
        icon: 'fas fa-play',
        hide: false
      },
      {
        name: 'new_playlist',
        title: 'audio.menu.new_playlist.title',
        url: 'new_playlist',
        breadcrumb: ["Home", "Audio"],
        icon: 'fas fa-plus disabled',
        hide: false
      }
    ]
  },
  {
    name: "Enclosures",
    title: "enclosures.menu.title",
    url: "/enclosures/",
    breadcrumb: [],
    icon: "fas fa-globe",
    hide: false,
    nesting: true,
    subroutes: [
      {
        name: 'enclosures_list',
        title: 'enclosures.menu.list.title',
        url: "/enclosures/",
        breadcrumb: ["Home", "Enclosures"],
        icon: 'fas fa-building',
        hide: false
      },
      {
        name: 'new_enclosure',
        title: 'enclosures.menu.new_enclosure.title',
        url: 'new_enclosure',
        breadcrumb: ["Home", "Enclosures"],
        icon: 'fas fa-plus disabled',
        hide: false
      },
      {
        name: 'new_area',
        title: 'enclosures.menu.new_area.title',
        url: 'new_area',
        breadcrumb: ["Home", "Enclosures"],
        icon: 'fas fa-plus disabled',
        hide: false
      }
    ]
  },
  {
    name: "System",
    title: "system.menu.title",
    url: "/system/",
    breadcrumb: [],
    icon: "fas fa-cog",
    hide: false,
    nesting: true,
    subroutes: [
      {
        name: 'system_status',
        title: 'system.menu.status.title',
        url: "/system/status/",
        breadcrumb: ["Home", "System"],
        icon: 'fas fa-exclamation-triangle',
        hide: false
      },
      {
        name: 'system_notifications',
        title: 'system.menu.notifications.title',
        url: "/system/notifications/",
        breadcrumb: ["Home", "System"],
        icon: 'fas fa-bell disabled',
        hide: false
      },
      {
        name: 'system_settings',
        title: 'system.menu.settings.title',
        url: "/system/settings/",
        breadcrumb: ["Home", "System"],
        icon: 'fas fa-cogs disabled',
        hide: false
      },
      {
        name: 'system_log',
        title: 'system.menu.log.title',
        url: "/system/log/",
        breadcrumb: ["Home", "System"],
        icon: 'fas fa-file-alt disabled',
        hide: false
      },

      {
        name: 'system_restart',
        title: 'system.menu.restart.title',
        url: 'system_restart',
        breadcrumb: ["Home", "System"],
        icon: 'fas fa-sync-alt disabled',
        hide: false
      },
      {
        name: 'system_reboot',
        title: 'system.menu.reboot.title',
        url: 'system_reboot',
        breadcrumb: ["Home", "System"],
        icon: 'fas fa-sync-alt disabled',
        hide: false
      },
      {
        name: 'system_shutdown',
        title: 'system.menu.shutdown.title',
        url: 'system_shutdown',
        breadcrumb: ["Home", "System"],
        icon: 'fas fa-power-off disabled',
        hide: false
      }
    ]
  }
];

export const PageUrls = Pages.reduce((acc, x) => {
  acc[x.name] = x.url;
  if (x.subroutes) {
    // Recursive....
    acc = x.subroutes.reduce((bcc, y) => {
      bcc[y.name] = y.url;
      return bcc;
    }, acc);
  }
  return acc;
}, {});

export const fillParams = (pageUrl, params) => {
  return Object
    .keys(params)
    .reduce(
      (acc, key) => acc.replace(`:${key}`, params[key]),
      pageUrl
    );
};

export const pageUrlToRegex = (pageUrl) => {
  return "^" + pageUrl.replace(/\/:\w+(\??)/, "/?([\\w\\-d]+)$1") + "$";
};

export const getPage = (name) => {
  return Pages.find((o) => o.name === name);
};

export const onRouteLoaded = async (route) => {
  const page = Pages.find(x => x.url === route.route);

  if (!page || get(customPageTitleUsed))
    return;

  pageTitle.set(typeof page.title === "function"
    ? await page.title()
    : page.title
  );
};

export default {
  [PageUrls.Home]: Home,
  [PageUrls.Dashboard]: Dashboard,
  [PageUrls.Weather]: Weather,
  [PageUrls.Calendar]: Calendar,
  ['/sensors/all/']: Sensors,
  ['/sensors/:type/']: Sensors,
  [PageUrls.Relays]: Relays,
  [PageUrls.Buttons]: Buttons,
  [PageUrls.Webcams]: Webcams,
  [PageUrls.audio_files]: AudioFiles,
  [PageUrls.playlists]: Playlists,
  [PageUrls.Enclosures]: Enclosures,
  [PageUrls.system_status]: Status,
  [PageUrls.system_settings]: Settings,
  [PageUrls.system_log]: Log,
  [PageUrls.system_notifications]: Notifications,

  ['/about/']: About,

  [PageUrls.Error]: Error,
  // The catch-all route must always be last
  "*": NotFound
};
