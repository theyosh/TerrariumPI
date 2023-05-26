export const template_sensor_type_color = (type) => {
  switch (type) {
    case 'temperature':
    case 'heating':
      return 'text-danger';

    case 'humidity':
      return 'text-info';

    case 'cooling':
    case 'watertank':
      return 'text-primary';

    case 'moisture':
      return 'text-info';

    case 'distance':
      return 'fa-signal';

    case 'light':
    case 'lights':
    case 'main lights':
    case 'uvi':
    case 'uva':
    case 'uvb':
    case 'ldr':
      return 'text-warning';

    case 'ph':
      return 'fa-flask';

    case 'fertility':
    case 'conductivity':
      return 'text-success';

    case 'co2':
    case 'altitude':
      return 'text-secondary';

    case 'pressure':
      return 'fa-cloud-upload-alt';

    case 'magnetic':
      return 'fa-lock';

    case 'motion':
      return 'fa-walking';

    case 'audio':
      return 'text-success';
  }
};

export const template_sensor_type_icon = (type) => {
  switch (type) {
    case 'temperature':
      return 'fas fa-thermometer-half';

    case 'heating':
      return 'fas fa-fire';

    case 'cooling':
      return 'fas fa-fan';

    case 'humidity':
    case 'sensors':
      return 'fas fa-tint';

    case 'moisture':
      return 'fas fa-water';

    case 'distance':
      return 'fas fa-signal';

    case 'light':
    case 'lights':
    case 'main_lights':
    case 'ldr':
      return 'fas fa-lightbulb';

    case 'main lights':
      return 'fas fa-sun';

    case 'ph':
      return 'fas fa-flask';

    case 'uvi':
      return 'fas fa-sun';

    case 'uva':
      return 'fas fa-adjust';

    case 'uvb':
      return 'fas fa-adjust fa-rotate-180';

    case 'fertility':
    case 'conductivity':
      return 'fas fa-seedling';

    case 'co2':
      return 'fas fa-wind';

    case 'altitude':
      return 'fas fa-level-up-alt';

    case 'pressure':
      return 'fas fa-cloud-upload-alt';

    case 'magnetic':
      return 'fas fa-lock';

    case 'motion':
      return 'fas fa-walking';

    case 'watertank':
      return 'fas fa-faucet';

    case 'audio':
      return 'fas fa-headphones';

    case 'display':
      return 'fas fa-newspaper';

    case 'email':
      return 'fas fa-at';

    case 'mqtt':
      return 'fas fa-bullhorn';

    case 'pushover':
      return 'fab fa-pinterest';

    case 'telegram':
      return 'fab fa-telegram-plane';

    case 'traffic':
      return 'fas fa-traffic-light';

    case 'twitter':
      return 'fab fa-twitter';

    case 'buzzer':
      return 'fas fa-music';

    case 'webhook':
      return 'fas fa-cloud-upload-alt';

    case 'weather':
      return 'fas fa-cloud-sun';

    case 'timer':
      return 'fas fa-clock';

    case 'disabled':
      return 'fas fa-ban';

    case 'weather_inverse':
      return 'fas fa-cloud-moon';

    case 'remote':
      return 'fas fa-wifi';
  }
};

export const get_weather_icon = (weather_type, is_day) => {
  // https://openweathermap.org/weather-conditions
  let day_icon = (is_day ? 'sun' : 'moon');
  weather_type = weather_type.slice(0, -1);

  let weather_icons = {
    '01': day_icon,
    '02': 'cloud_' + day_icon,
    '03': 'cloud',
    '04': 'cloud_' + day_icon,
    '09': 'cloud_rain_' + day_icon,
    '10': 'cloud_drizzle_' + day_icon,
    '11': 'cloud_lightning_' + day_icon,
    '13': 'cloud_snow_alt_' + day_icon,
    '50': 'cloud_fog_' + day_icon,
  };

  return 'img/weather_icons/' + 'climacon-' + weather_icons[weather_type] + '.svg';
};

export const setFavicon = (url) => {
  const headTitle = document.querySelector('head');
  const setFavicon = document.createElement('link');
  setFavicon.setAttribute('rel', 'shortcut icon');
  setFavicon.setAttribute('type', 'image/x-icon');
  setFavicon.setAttribute('href', url);
  headTitle.appendChild(setFavicon);
};