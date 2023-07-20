import { get } from "svelte/store";

import { ApiUrl } from "../constants/urls";
import { credentials } from "../stores/authentication";

const apiHost = `${ApiUrl}/api`;

const headers = (extra_headers) => {
  let headers = {
    ...{
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest'
    }, ...extra_headers
  };

  const creds = get(credentials);
  if (creds) {
    headers['Authorization'] = 'Basic ' + window.btoa(creds.username + ":" + creds.password);
  }

  return headers;
};

export const apiLogin = async (username, password) => {
  return await fetch(`${ApiUrl}/login/`, {
    redirect: 'manual', // Only for dev??
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + window.btoa(username + ":" + password)
    }
  })
    .then(response => {
      if ([200, 302, 303, 307].indexOf(response.status) !== -1 || response.type === 'opaqueredirect') { // Redirect only for dev??
        return true;
      }
      return false;
    })
    .catch(() => {
      return false;
    });
};

const __processData = async (type, url, data, cb, extra_headers) => {

  extra_headers = extra_headers || {};
  let body = ['GET', 'HEAD'].indexOf(type) !== -1 ? null : data;
  let postheaders = headers(extra_headers);

  if (type === 'UPLOAD') {
    type = 'POST';
    // Make the upload fix there own Content type headers for multipart boundary
    delete (postheaders['Content-Type']);
  } else if (['PUT', 'POST'].indexOf(type) !== -1) {
    body = JSON.stringify(body);
  }

  let response = await fetch(url, {
    method: type,
    headers: postheaders,
    body: body,
  });

  if (response.status === 401) {
    throw new Error('Authentication required (401)');
  } else if (response.status === 404) {
    throw new Error('Requested data is not available (404)');
  }

  let result = await response.text();
  try {
    result = JSON.parse(result);
  } catch {
    // Not JSON content, so keep the text version
  }

  if (response.status === 500) {
    throw new Error(result.message);
  }

  if (cb) {
    data = result.data ? result.data : result;
    cb(data);
  }
};

// API Helpers
const _getData = async (url, cb, extra_headers) => {
  await __processData('GET', url, {}, cb, extra_headers);
};

const _postData = async (url, data, cb, extra_headers) => {
  await __processData('POST', url, data, cb, extra_headers);
};

const _updateData = async (url, data, cb, extra_headers) => {
  await __processData('PUT', url, data, cb, extra_headers);
};

const _deleteData = async (url, data, cb, extra_headers) => {
  await __processData('DELETE', url, data, cb, extra_headers);
};

const _uploadData = async (url, data, cb, extra_headers) => {
  await __processData('UPLOAD', url, data, cb, extra_headers);
};
// End API Helpers


// Upload helpers
export const uploadFile = async (file) => {
  let data = new FormData();
  data.append('file', file.files[0]);

  let filename = null;
  await _uploadData(`${ApiUrl}/media/upload/`, data, (result) => {
    filename = result.file;
  });

  return filename;
};
// End Upload helpers


// Weather API
export const fetchWeatherData = async (cb) => {
  await _getData(`${apiHost}/weather/`, cb);
};

export const fetchWeatherForecast = async (cb) => {
  await _getData(`${apiHost}/weather/forecast/`, cb);
};
// End Weather API


// Calendar API
export const fetchCalendarEvents = async (id, cb) => {
  let url = `${apiHost}/calendar/`;
  if (id) {
    url += `${id}/`;
  }
  await _getData(url, cb);
};

export const fetchUpcomingEvents = async (cb) => {
  await fetchCalendarEvents(false, cb);
};

export const addCalendarEvent = async (data, cb) => {
  await _postData(`${apiHost}/calendar/`, data, cb);
};

export const updateCalendarEvent = async (data, cb) => {
  if (data.id) {
    await _updateData(`${apiHost}/calendar/${data.id}/`, data, cb);
  } else {
    await addCalendarEvent(data, cb);
  }
};

export const deleteCalendarEvent = async (id, cb) => {
  await _deleteData(`${apiHost}/calendar/${id}/`, {}, cb);
};

export const downloadCalendar = async (cb) => {
  await _getData(`${apiHost}/calendar/download/`, cb);
};
// End Calendar API


// Sensors API
export const fetchSensorsHardware = async (cb) => {
  await _getData(`${apiHost}/sensors/hardware/`, cb);
};

export const scanSensors = async (cb) => {
  await _postData(`${apiHost}/sensors/scan/`, {}, cb);
};

export const fetchSensors = async (sensor_id, cb) => {
  let url = `${apiHost}/sensors/`;
  if (sensor_id) {
    url += `${sensor_id}/`;
  }
  await _getData(url, cb);
};

export const addSensor = async (data, cb) => {
  delete (data.id);
  await _postData(`${apiHost}/sensors/`, data, cb);
};

export const updateSensor = async (data, cb) => {
  if (data.id) {
    await _updateData(`${apiHost}/sensors/${data.id}/`, data, cb);
  } else {
    await addSensor(data, cb);
  }
};

export const deleteSensor = async (id, cb) => {
  await _deleteData(`${apiHost}/sensors/${id}/`, {}, cb);
};
// End Sensors API


// Relays API
export const fetchRelaysHardware = async (cb) => {
  await _getData(`${apiHost}/relays/hardware/`, cb);
};

export const scanRelays = async (cb) => {
  await _postData(`${apiHost}/relays/scan/`, {}, cb);
};

export const toggleRelay = async (relay_id, cb) => {
  await _postData(`${apiHost}/relays/${relay_id}/toggle/`, {}, cb);
};

export const dimRelay = async (relay_id, dim_value, cb) => {
  await _postData(`${apiHost}/relays/${relay_id}/${dim_value}/`, {}, cb);
};

export const manualRelay = async (relay_id, cb) => {
  await _postData(`${apiHost}/relays/${relay_id}/manual/`, {}, cb);
};

export const fetchRelays = async (id, cb) => {
  let url = `${apiHost}/relays/`;
  if (id) {
    url += `${id}/`;
  }
  await _getData(url, cb);
};

export const addRelay = async (data, cb) => {
  delete (data.id);
  await _postData(`${apiHost}/relays/`, data, cb);
};

export const updateRelay = async (data, cb) => {
  if (data.id) {
    await _updateData(`${apiHost}/relays/${data.id}/`, data, cb);
  } else {
    await addRelay(data, cb);
  }
};

export const deleteRelay = async (id, cb) => {
  await _deleteData(`${apiHost}/relays/${id}/`, {}, cb);
};
// End Relays API


// Buttons API
export const fetchButtonsHardware = async (cb) => {
  await _getData(`${apiHost}/buttons/hardware/`, cb);
};

export const fetchButtons = async (id, cb) => {
  let url = `${apiHost}/buttons/`;
  if (id) {
    url += `${id}/`;
  }
  await _getData(url, cb);
};

export const addButton = async (data, cb) => {
  delete (data.id);
  await _postData(`${apiHost}/buttons/`, data, cb);
};

export const updateButton = async (data, cb) => {
  if (data.id) {
    await _updateData(`${apiHost}/buttons/${data.id}/`, data, cb);
  } else {
    await addButton(data, cb);
  }
};

export const deleteButton = async (id, cb) => {
  await _deleteData(`${apiHost}/buttons/${id}/`, {}, cb);
};
// End Buttons API


// Webcam API
export const fetchWebcamsHardware = async (cb) => {
  await _getData(`${apiHost}/webcams/hardware/`, cb);
};

export const fetchWebcamArchive = async (webcam_id, year, month, day, cb) => {
  await _getData(`${apiHost}/webcams/${webcam_id}/archive/${year}/${month}/${day}/`, cb);
};

export const fetchWebcams = async (id, cb) => {
  let url = `${apiHost}/webcams/`;
  if (id) {
    url += `${id}/`;
  }
  await _getData(url, cb);
};

export const addWebcam = async (data, cb) => {
  delete (data.id);
  await _postData(`${apiHost}/webcams/`, data, cb);
};

export const updateWebcam = async (data, cb) => {
  if (data.id) {
    await _updateData(`${apiHost}/webcams/${data.id}/`, data, cb);
  } else {
    await addWebcam(data, cb);
  }
};

export const deleteWebcam = async (id, cb) => {
  await _deleteData(`${apiHost}/webcams/${id}/`, {}, cb);
};
// End Webcam API


// Audio API
export const fetchSoundcards = async (cb) => {
  await _getData(`${apiHost}/audio/hardware/`, cb);
};

export const fetchAudiofiles = async (cb) => {
  await _getData(`${apiHost}/audio/files/`, cb);
};

export const deleteAudioFile = async (file, cb) => {
  await _deleteData(`${apiHost}/audio/files/${file}/`, cb);
};

export const fetchPlaylists = async (id, cb) => {
  let url = `${apiHost}/playlists/`;
  if (id) {
    url += `${id}/`;
  }
  await _getData(url, cb);
};

export const addPlaylist = async (data, cb) => {
  delete (data.id);
  await _postData(`${apiHost}/playlists/`, data, cb);
};

export const updatePlaylist = async (data, cb) => {
  if (data.id) {
    await _updateData(`${apiHost}/playlists/${data.id}/`, data, cb);
  } else {
    await addPlaylist(data, cb);
  }
};

export const deletePlaylist = async (playlist, cb) => {
  await _deleteData(`${apiHost}/playlists/${playlist}/`, cb);
};
// End Audio API


// Enclosure API
export const fetchEnclosures = async (enclosure_id, cb) => {
  let url = `${apiHost}/enclosures/`;
  if (enclosure_id) {
    url += `${enclosure_id}/`;
  }

  // This callback will alter the start and end time for the enclosure areas which uses a timer mode.
  const fixTimerModeStartAndEndTimesCb = (data) => {
    data.forEach(enclosure => {
        enclosure.areas.forEach(area => {
            if (area.mode === 'timer') {
                ['day', 'night', 'low', 'high'].forEach(period => {
                    if (area.state[period]) {
                        let startTime = area.setup[period].begin.split(':');
                        let endTime = area.setup[period].end.split(':');

                        area.state[period].begin = new Date();
                        area.state[period].begin.setHours(startTime[0]);
                        area.state[period].begin.setMinutes(startTime[1]);
                        area.state[period].begin.setSeconds(0);

                        area.state[period].end = new Date();
                        area.state[period].end.setHours(endTime[0]);
                        area.state[period].end.setMinutes(endTime[1]);
                        area.state[period].end.setSeconds(0);

                        area.state[period].begin = area.state[period].begin.getTime() / 1000;
                        area.state[period].end = area.state[period].end.getTime() / 1000;
                    }
                });
            }
        });
    });

    cb(data);
  };

  await _getData(url, fixTimerModeStartAndEndTimesCb);
};

export const addEnclosure = async (data, cb) => {
  delete (data.id);
  await _postData(`${apiHost}/enclosures/`, data, cb);
};

export const updateEnclosure = async (data, cb) => {
  if (data.id) {
    await _updateData(`${apiHost}/enclosures/${data.id}/`, data, cb);
  } else {
    await addEnclosure(data, cb);
  }
};

export const deleteEnclosure = async (playlist, cb) => {
  await _deleteData(`${apiHost}/enclosures/${playlist}/`, cb);
};
// End Enclosure API


// Area API
export const fetchAreaTypes = async (cb) => {
  await _getData(`${apiHost}/areas/types/`, cb);
};

export const fetchAreas = async (area_id, cb) => {
  let url = `${apiHost}/areas/`;
  if (area_id) {
    url += `${area_id}/`;
  }
  await _getData(url, cb);
};

export const addArea = async (data, cb) => {
  delete (data.id);
  await _postData(`${apiHost}/areas/`, data, cb);
};

export const updateArea = async (data, cb) => {
  if (data.id) {
    await _updateData(`${apiHost}/areas/${data.id}/`, data, cb);
  } else {
    await addArea(data, cb);
  }
};

export const deleteArea = async (playlist, cb) => {
  await _deleteData(`${apiHost}/areas/${playlist}/`, cb);
};
// End Area API



export const fetchSystemstats = async (cb) => {
  await _getData(`${apiHost}/system_status/`, cb);
};

export const fetchSystemSettings = async (settingid, cb) => {
  let url = `${apiHost}/settings/${(settingid ? settingid + "/" : '')}`;
  await _getData(url, cb);
};

export const updateSystemSettings = async (data, cb) => {
  let url = `${apiHost}/settings/`;
  if (Object.keys(data).length === 1) {
    let key = Object.keys(data)[0];
    url += key + '/';
    data = { value: data[key] };
  }
  await _updateData(url, data, cb);
};

export const systemRestart = async (cb) => {
  await _postData(`${apiHost}/restart/`, {}, cb);
};

export const systemReboot = async (cb) => {
  await _postData(`${apiHost}/reboot/`, {}, cb);
};

export const systemShutdown = async (cb) => {
  await _postData(`${apiHost}/shutdown/`, {}, cb);
};

export const fetchLoglines = async (cb, preview) => {
  preview = preview || false;
  let range_request = preview ? { 'Range': 'bytes=-102300' } : {};
  await _getData(`${apiHost}/logfile/download/`, cb, range_request);
};

export const fetchGraphData = async (type, id, period, cb) => {
  period = period || 'day';
  await _getData(`${apiHost}/${type}/${id}/history/${period}/`, cb);
};

export const fetchExportData = async (type, id, period, cb) => {
  period = period || 'day';
  await _getData(`${apiHost}/${type}/${id}/export/${period}/`, cb);
};


// Notification services API
export const fetchDisplayTypes = async (cb) => {
  await _getData(`${apiHost}/displays/hardware/`, cb);
};

export const fetchNotificationServiceTypes = async (cb) => {
  await _getData(`${apiHost}/notification/services/types/`, cb);
};

export const fetchNotificationServices = async (service_id, cb) => {
  let url = `${apiHost}/notification/services/`;
  if (service_id) {
    url += `${service_id}/`;
  }
  await _getData(url, cb);
};

export const addNotificationService = async (data, cb) => {
  delete (data.id);
  await _postData(`${apiHost}/notification/services/`, data, cb);
};

export const updateNotificationService = async (data, cb) => {
  if (data.id) {
    await _updateData(`${apiHost}/notification/services/${data.id}/`, data, cb);
  } else {
    await addNotificationService(data, cb);
  }
};

export const deleteNotificationService = async (service_id, cb) => {
  await _deleteData(`${apiHost}/notification/services/${service_id}/`, cb);
};
// End notification services API


// Notification messages API
export const fetchNotificationMessageTypes = async (cb) => {
  await _getData(`${apiHost}/notification/messages/types/`, cb);
};

export const fetchNotificationMessages = async (message_id, cb) => {
  let url = `${apiHost}/notification/messages/`;
  if (message_id) {
    url += `${message_id}/`;
  }
  await _getData(url, cb);
};

export const addNotificationMessage = async (data, cb) => {
  delete (data.id);
  await _postData(`${apiHost}/notification/messages/`, data, cb);
};

export const updateNotificationMessage = async (data, cb) => {
  if (data.id) {
    await _updateData(`${apiHost}/notification/messages/${data.id}/`, data, cb);
  } else {
    await addNotificationMessage(data, cb);
  }
};

export const deleteNotificationMessage = async (message_id, cb) => {
  await _deleteData(`${apiHost}/notification/messages/${message_id}/`, cb);
};
// End notification messages API