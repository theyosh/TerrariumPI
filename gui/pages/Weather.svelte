<script>
  import { onMount, onDestroy } from 'svelte';
  import { Line } from 'svelte-chartjs';
  import { Chart as ChartJS, Title, Tooltip, Legend, TimeScale, LinearScale, PointElement, LineElement } from 'chart.js';
  ChartJS.register(Title, Tooltip, Legend, TimeScale, LinearScale, PointElement, LineElement);
  import 'chartjs-adapter-dayjs-3';
  import { _ } from 'svelte-i18n';
  import { PageHeader, BreadcrumbItem } from 'svelte-adminlte';
  import { date, time } from 'svelte-i18n';

  import { setCustomPageTitle, customPageTitleUsed } from '../stores/page-title';
  import { roundToPrecision } from '../helpers/number-helpers';
  import { get_weather_icon } from '../helpers/icon-helpers';
  import { isAuthenticated } from '../stores/authentication';
  import { fetchWeatherData, fetchWeatherForecast } from '../providers/api';
  import { graphDefaultOpts, graphTypes } from '../constants/graph';
  import { get_template_color } from '../helpers/color-helpers';
  import { isDay } from '../stores/terrariumpi';

  import Card from '../user-controls/Card.svelte';
  import LoginLink from '../components/common/LoginLink.svelte';
  import WeatherSettings from '../modals/WeatherFormModal.svelte';

  let weatherData = {};
  let graphData = [];
  let loading_current = true;
  let loading_forecast = true;
  let showModal;

  let graphOpts = { ...graphDefaultOpts };

  const loadData = () => {
    loadCurrentData(true);
    loadForecastData(true);
  };

  const fixCardHeight = () => {
    let cards = document.querySelectorAll('div.card div.card-body');
    cards[1].style.height = cards[0].clientHeight + 'px';
  };

  const loadCurrentData = async (loading) => {
    loading = loading || false;
    loading_current = loading === true;

    if (loading === true) {
      await fetchWeatherData((data) => (weatherData = data));
    } else {
      fetchWeatherData((data) => (weatherData = data));
    }
    loading_current = false;
  };

  const loadForecastData = async (loading) => {
    loading = loading || false;
    loading_forecast = loading === true;

    let new_data;
    await fetchWeatherForecast((data) => {
      new_data = data.map((point) => {
        point.timestamp *= 1000;
        return point;
      });
    });

    if (loading === true) {
      graphData = {
        labels: null,
        datasets: [
          {
            label: $_('general.temperature', { default: 'Temperature' }),
            graphType: 'temperature',
            lineTension: 0.5,
            data: new_data,
            parsing: {
              xAxisKey: 'timestamp',
              yAxisKey: 'temperature',
            },
            yAxisID: 'y',
            fill: false,
            borderColor: graphTypes['value'].colors.line,
            backgroundColor: graphTypes['value'].colors.background,
          },
          {
            label: $_('general.humidity', { default: 'Humdity' }),
            graphType: 'humidity',
            lineTension: 0.5,
            data: new_data,
            parsing: {
              xAxisKey: 'timestamp',
              yAxisKey: 'humidity',
            },
            yAxisID: 'y2',
            fill: false,
            borderColor: get_template_color('text-primary'),
            backgroundColor: get_template_color('text-primary', 0.7),
          },
        ],
      };
    } else {
      graphOpts.animation = { duration: 0 };
      graphData.datasets[0].data = new_data;
      graphData.datasets[1].data = new_data;
      graphData.labels = new_data.map((point) => {
        return point.timestamp;
      });
    }

    fixCardHeight();
    setTimeout(() => {
      fixCardHeight();
    }, 0.25);

    loading_forecast = false;
  };

  onMount(() => {
    (async () => {
      // Get initial data
      await loadCurrentData(true);
      loadForecastData(true);
    })();

    graphOpts.scales.x.time.unit = 'hour';
    graphOpts.scales.x.time.displayFormats.hour = 'dd LT';
    graphOpts.scales.y2.display = true;
    graphOpts.scales.y.min = null;
    graphOpts.scales.y2.min = null;

    setCustomPageTitle($_('weather.title', { default: 'Weather' }));

    // Reload every 15 minutes
    const intervalCurrent = setInterval(async () => {
      loadCurrentData(false);
    }, 15 * 60 * 1000);

    // Reload every 60 minutes
    const intervalForecast = setInterval(async () => {
      loadForecastData(false);
    }, 60 * 60 * 1000);

    //If a function is returned from onMount, it will be called when the component is unmounted.
    return () => {
      clearInterval(intervalCurrent);
      clearInterval(intervalForecast);
    };
  });

  onDestroy(() => {
    customPageTitleUsed.set(false);
  });
</script>

<PageHeader>
  {$_('weather.title', { default: 'Weather' })}

  <svelte:fragment slot="breadcrumbs">
    <BreadcrumbItem>
      {#if $isAuthenticated}
        <a href="{'#'}" on:click|preventDefault="{() => showModal()}">
          <i class="fas fa-wrench pt-1 mr-1"></i>{$_('general.settings.title', { default: 'Settings' })}
        </a>
      {:else}
        <LoginLink />
      {/if}
    </BreadcrumbItem>
    {#if weatherData.location}
      <BreadcrumbItem>
        <a href="{weatherData.credits.url}" target="_blank" rel="noopener noreferrer">{weatherData.credits.text}</a>
      </BreadcrumbItem>
    {/if}
  </svelte:fragment>
</PageHeader>

<div class="container-fluid">
  <div class="row">
    <div class="col-12 col-sm-12 col-md-5">
      <Card loading="{loading_current}" removeParent="{true}" class="current">
        <svelte:fragment slot="header">
          <i class="fas mr-2" class:fa-cloud-sun="{$isDay}" class:fa-cloud-moon="{!$isDay}"></i>{$_('weather.current', {
            default: 'Current',
          })}
        </svelte:fragment>
        {#if !loading_current && !weatherData.location}
          <div class="row">
            <div class="col text-center">
              <h1 class="m4">{$_('weather.no_data', { default: 'No weather data available'})}</h1>
            </div>
          </div>
        {:else if !loading_current && weatherData.location}
          <div class="row">
            <div class="col-9">
              <strong>{$date(new Date(weatherData.forecast[0].timestamp * 1000), { format: 'full' })}</strong>
            </div>
            <div class="col-3 text-right">
              <i class="fas fa-location-arrow" style="transform: rotate({weatherData.forecast[0].wind.direction + 135}deg)"></i>
              <span class="text-nowrap">{roundToPrecision(weatherData.forecast[0].wind.speed)} {weatherData.indicators.wind}</span>
            </div>
          </div>
          <div class="row">
            <div
              class="col-3 weather-icon"
              style="background: url({get_weather_icon(weatherData.forecast[0].weather.icon, weatherData.is_day)}) no-repeat center"
              title="{weatherData.forecast[0].weather.description}">
            </div>
            <div class="col-7">
              <h3>{weatherData.location.city}</h3>
              <h4>{weatherData.forecast[0].weather.description}</h4>
            </div>
            <div class="pl-0 col-2 text-right text-nowrap">
              <i class="fas fa-sun"></i>
              {$time(new Date(weatherData.sun.rise * 1000), { format: 'short' })}<br />
              <i class="fas fa-moon"></i>
              {$time(new Date(weatherData.sun.set * 1000), { format: 'short' })}
              <h5 class="mt-4">{roundToPrecision(weatherData.forecast[0].temp)} {weatherData.indicators.temperature}</h5>
            </div>
          </div>
          <div class="row">
            {#each weatherData.forecast.slice(1, 7) as day, counter}
              <div class="col pr-0" class:d-none="{counter === 5}" class:d-sm-inline="{counter === 5}">
                <div class="description-block">
                  <h5 class="description-header">{$date(new Date(day.timestamp * 1000), { weekday: 'short' })}</h5>
                  <span class="description-text">{roundToPrecision(day.temp)} {weatherData.indicators.temperature}</span>
                  <img
                    class="weather-icon"
                    src="{get_weather_icon(day.weather.icon, weatherData.is_day)}"
                    alt="{day.weather.description}"
                    title="{day.weather.description}" />
                  <i class="fas fa-location-arrow" style="transform: rotate({day.wind.direction + 135}deg)"></i><br />
                  <span class="text-nowrap">{roundToPrecision(day.wind.speed, 1)} {weatherData.indicators.wind}</span>
                </div>
              </div>
            {/each}
          </div>
        {/if}
      </Card>
    </div>
    <div class="col col-md-7">
      <Card loading="{loading_forecast}" class="forecast">
        <svelte:fragment slot="header">
          <i class="fas mr-2" class:fa-cloud-sun="{$isDay}" class:fa-cloud-moon="{!$isDay}"></i>
          {$_('weather.forecast', { default: 'Forecast'})}
        </svelte:fragment>
        {#if !loading_forecast}
          {#if graphData.datasets[0].data.length > 0}
            <Line data="{graphData}" options="{graphOpts}" />
          {:else}
            <div class="row">
              <div class="col text-center">
                <h1 class="m4">{$_('weather.no_data', { default: 'No weather data available'})}</h1>
              </div>
            </div>
          {/if}
        {/if}
      </Card>
    </div>
  </div>
</div>

{#if $isAuthenticated}
  <WeatherSettings bind:show="{showModal}" on:save="{loadData}" />
{/if}
