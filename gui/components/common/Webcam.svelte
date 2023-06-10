<script>
  import { onMount, onDestroy, getContext } from 'svelte';
  import { date, time, _ } from 'svelte-i18n';
  import { LeafletMap, TileLayer, Marker, Tooltip, DivIcon } from 'svelte-leafletjs';
  import 'leaflet/dist/leaflet.css';

  import { Fancybox } from '@fancyapps/ui';
  import '@fancyapps/ui/dist/fancybox/fancybox.css';

  import { sensors, updateSensor } from '../../stores/terrariumpi';
  import { fetchSensors, fetchWebcamArchive } from '../../providers/api';
  import { getCustomConfig } from '../../config';
  import { roundToPrecision } from '../../helpers/number-helpers';
  import { ApiUrl } from '../../constants/urls';
  import { fancyAppsLanguage } from '../../constants/ui';
  import { errorNotification } from '../../providers/notification-provider';
  import LoadingModal from '../../modals/LoadingModal.svelte';

  import L from 'leaflet';
  import 'leaflet-fullscreen';

  import hls from 'hls.js';

  export let webcam;
  export let edit = false;

  export const getWebcamMap = () => {
    return map.getMap();
  };

  export const getIconOptions = () => {
    return iconOptions;
  };

  const { setLoading } = getContext('loading');

  let updateMarkers = () => {};
  let showMarkerModal = () => {};

  if (edit) {
    try {
      let { showModal, markerLocations } = getContext('webcamMarker');
      updateMarkers = markerLocations;
      showMarkerModal = showModal;
    } catch (e) {
      console.log('No context available....', e);
    }
  }

  const settings = getCustomConfig();
  const max_zoom = Math.log2(Math.pow(2, Math.ceil(Math.log2(Math.max(webcam.width, webcam.height)))) / 256);

  const mapOptions = {
    center: [0, 0],
    zoom: 1,
    fullscreenControl: true,
  };

  export const iconOptions = {
    iconUrl: 'img/marker-icon-2x.png',
    shadowUrl: 'img/marker-shadow.png',
    iconSize: [25, 41],
    shadowSize: [45, 41],
  };

  export const toolTipOptions = {
    permanent: true,
    direction: 'auto',
    opacity: 0.5,
  };

  export const popUpOptions = {
    autoClose: false,
    closeOnEscapeKey: false,
    closeOnClick: false,
    closeButton: false,
  };

  export const markerOptions = {
    draggable: edit,
  };

  const tileUrl = `${ApiUrl}/webcam/{id}/tiles/tile_{z}_{x}_{y}.jpg?_{time}`;

  const tileLayerOptions = {
    time: function () {
      return new Date().valueOf();
    },
    id: webcam.id,
    noWrap: true,
    continuousWorld: false,
    minZoom: 0,
    maxZoom: max_zoom + 1,
    maxNativeZoom: max_zoom,
  };

  const generatePulsatingMarker = (radius, color) => {
    const cssStyle = `
      width: ${radius}px;
      height: ${radius}px;
      margin-left: -${radius / 4}px;
      margin-top: -${radius / 4}px;
      left: 5px;
      top: 0px;
      color: ${color};
      box-shadow: 0 0 0 ${color};
    `;
    return L.divIcon({
      html: `<span style="${cssStyle}" class="pulse"/>`,
      // empty class name to prevent the default leaflet-div-icon to apply
      className: '',
    });
  };

  const pulsateMarkers = () => {
    let pulse_markers = document.querySelectorAll('.pulse');
    pulse_markers.forEach((item) => {
      item.classList.remove('pulse');
    });

    setTimeout(() => {
      pulse_markers.forEach((item) => {
        item.classList.add('pulse');
      });
    }, 10);
  };

  const pulsatingIcon = generatePulsatingMarker(25, 'red');

  let tileLayer;
  let map;
  let videoplayer;
  let hlsplayer;

  const ExtraWebcamControls = L.Control.extend({
    options: {
      position: 'topleft',
      archive: true,
    },
    initialize: function (options) {
      // constructor
      L.Util.setOptions(this, options);
    },
    onAdd: function (map) {
      const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');

      const raw_image = L.DomUtil.create('a', 'leaflet-bar-part', container);
      raw_image.href = `${ApiUrl}/webcam/${webcam.id}/${webcam.id}_raw.jpg`;
      raw_image.title = $_('webcams.controls.save_raw_image', { default: 'Save RAW image' });
      raw_image.target = '_blank';
      L.DomUtil.create('i', 'fas fa-camera', raw_image);

      if (!edit && webcam.archive.state !== 'disabled') {
        const archive_link = L.DomUtil.create('a', 'leaflet-bar-part', container);
        archive_link.href = '#';
        archive_link.title = $_('webcams.controls.archive', { default: 'Archive' });
        L.DomEvent.on(
          archive_link,
          'click',
          (e) => {
            e.stopPropagation();
            e.preventDefault();
            webcamArchive();
          },
          this
        );
        L.DomUtil.create('i', 'fas fa-archive', archive_link);
      }

      if (webcam.markers.length > 0) {
        const markers_link = L.DomUtil.create('a', 'leaflet-bar-part', container);
        markers_link.href = '#';
        markers_link.title = $_('webcams.controls.show_markers', { default: 'Show markers' });
        L.DomEvent.on(
          markers_link,
          'click',
          (e) => {
            e.stopPropagation();
            e.preventDefault();
            map._panes.shadowPane.classList.toggle('d-none');
            map._panes.markerPane.classList.toggle('d-none');
            map._panes.tooltipPane.classList.toggle('d-none');
          },
          this
        );
        L.DomUtil.create('i', 'fas fa-info', markers_link);
      }

      if (edit) {
        const marker_drop = L.DomUtil.create('a', 'leaflet-bar-part', container);
        marker_drop.href = '#';
        marker_drop.title = $_('webcams.controls.new_marker', { default: 'Add marker' });
        L.DomEvent.on(
          marker_drop,
          'click',
          (e) => {
            e.stopPropagation();
            e.preventDefault();
            showMarkerModal();
          },
          this
        );
        L.DomUtil.create('i', 'fas fa-map-marker', marker_drop);
      }

      if (!edit && webcam.is_live) {
        const toggle_audio = L.DomUtil.create('a', 'leaflet-bar-part', container);
        toggle_audio.href = '#';
        toggle_audio.title = $_('webcams.controls.toggle_volume', { default: 'Toggle volume' });
        L.DomEvent.on(
          toggle_audio,
          'click',
          (e) => {
            e.stopPropagation();
            e.preventDefault();
            if (videoplayer) {
              videoplayer.muted = !videoplayer.muted;
              e.target.classList.remove('fa-volume-up');
              e.target.classList.remove('fa-volume-mute');
              e.target.classList.add(videoplayer.muted ? 'fa-volume-up' : 'fa-volume-mute');
            }
          },
          this
        );
        L.DomUtil.create('i', 'fas fa-volume-up', toggle_audio);
      }
      return container;
    },
  });

  if (webcam.markers && webcam.markers.length > 0) {
    let sensors_loaded = true;
    for (let x = 0; x < webcam.markers.length; x++) {
      sensors_loaded = sensors_loaded && webcam.markers[x].sensors.some((sensor_id) => $sensors[sensor_id] && $sensors[sensor_id].type);
      if (!sensors_loaded) {
        (async () => {
          fetchSensors(false, (data) => {
            data.forEach((sensor) => {
              updateSensor(sensor);
            });
          });
        })();
        break;
      }
    }
  }

  let webcamArchiveLoadingModal = null;
  const webcamArchive = () => {
    let image_archive = [];
    let counter = 0;

    async function loadImages(archive_date) {
      archive_date = archive_date || new Date();

      fetchWebcamArchive(
        webcam.id,
        archive_date.getFullYear(),
        (archive_date.getMonth() < 9 ? '0' : '') + (archive_date.getMonth() + 1),
        (archive_date.getDate() < 10 ? '0' : '') + archive_date.getDate(),

        (data) => {
          image_archive = [
            ...image_archive,
            ...data.archive_images.map((image) => {
              let image_date = new Date(image.slice(-14, -4) * 1000);
              return {
                src: `${ApiUrl}/${image.slice(1)}`,
                thumb: `${ApiUrl}/${image.slice(1)}`,
                type: 'image',
                caption: $date(image_date, { format: 'full' }) + ' ' + $time(image_date, { format: 'medium' }),
              };
            }),
          ];

          webcamArchiveLoadingModal.setMessage($_('webcams.archive.modal.loading.status', { default: 'Currently loaded {total} images ... ({percentage}%)', values: { total: image_archive.length, percentage: (counter/10)*100 } }));

          if (counter++ < 10) {
            loadImages(new Date(archive_date.getTime() - 24 * 60 * 60 * 1000));
          } else if (image_archive.length > 0) {
            new Fancybox(image_archive, {
                 l10n: fancyAppsLanguage(),
            });
            webcamArchiveLoadingModal.hide();
          } else {
            errorNotification($_('webcams.archive.no_images', { default: 'No archive images available' }));
          }
        }
      );
    }

    // Open loading modal
    webcamArchiveLoadingModal.setMessage($_('webcams.archive.modal.loading.title', { default: 'Starting loading webcam archive images ...' }));
    webcamArchiveLoadingModal.show();
    loadImages();
  };

  onMount(() => {
    map.getMap().addControl(new ExtraWebcamControls());

    if (webcam.is_live) {
      let hls_url = webcam.hardware.indexOf('remote') !== -1 ? webcam.address : `${ApiUrl}/webcam/${webcam.id}/stream.m3u8`;
      L.videoOverlay(
        hls_url,
        L.latLngBounds([
          [150, -180],
          [-150, 180],
        ]),
        {
          autoplay: true,
          muted: true,
          keepAspectRatio: true,
        }
      )
        .on('add', (event) => {
          videoplayer = event.sourceTarget._image;
          if (!videoplayer.canPlayType('application/vnd.apple.mpegurl')) {
            hlsplayer = new hls({ debug: false });
            hlsplayer.loadSource(hls_url);
            hlsplayer.attachMedia(videoplayer);
            hlsplayer.on(hls.Events.MANIFEST_PARSED, function () {
              videoplayer.play();
            });
          }
        })
        .addTo(map.getMap());
    }

    // Fix for class names starting with a number (based on UUID) https://stackoverflow.com/a/39004242
    const lastUpdate = document.querySelector(`div.card.${webcam.id} small span`.replace(/\.(\d)/gm, `\.\\3$1 `));
    lastUpdate.innerText = $date(new Date(), { format: 'long' }) + ' ' + $time(new Date(), { format: 'short' });

    let interval = null;
    interval = setInterval(() => {
      if (!webcam.is_live) {
        tileLayer.getTileLayer().redraw();
        pulsateMarkers();
      }
      lastUpdate.innerText = $date(new Date(), { format: 'long' }) + ' ' + $time(new Date(), { format: 'short' });
    }, 30 * 1000);

    setLoading(false);
    return () => {
      clearInterval(interval);
    };
  });

  onDestroy(() => {
    if (videoplayer) {
      videoplayer.pause();
      videoplayer.src = '';
      if (hlsplayer) {
        hlsplayer.destroy();
      }
    }
  });
</script>

<LeafletMap bind:this="{map}" options="{mapOptions}">
  {#if !webcam.is_live}
    <TileLayer bind:this="{tileLayer}" url="{tileUrl}" options="{tileLayerOptions}" />
  {/if}
  {#if webcam.markers.length > 0}
    {#each webcam.markers as marker}
      <Marker
        options="{{ ...markerOptions, ...{ sensors: marker.sensors } }}"
        latLng="{[marker.lat, marker.long]}"
        events="{['move', 'dblclick']}"
        on:move="{(e) => updateMarkers()}"
        on:dblclick="{(e) => showMarkerModal(e.detail)}">
        <DivIcon options="{pulsatingIcon.options}" />
        {#if !marker.sensors.some((sensor_id) => $sensors[sensor_id] && $sensors[sensor_id].type)}
          <Tooltip options="{{ ...toolTipOptions, ...{ direction: marker.long > 0 ? 'right' : 'left' } }}">
            <strong>Loading</strong>
          </Tooltip>
        {:else}
          <Tooltip options="{{ ...toolTipOptions, ...{ direction: marker.long > 0 ? 'right' : 'left' } }}">
            {#each marker.sensors as sensor_id, counter}
              {#if counter === 0}
                <strong>{$sensors[sensor_id].name}</strong>
              {/if}
              {#if $sensors[sensor_id]}
                {settings.units[$sensors[sensor_id].type].name.toLowerCase().slice(0, 4)}
                {roundToPrecision($sensors[sensor_id].value)}
                {settings.units[$sensors[sensor_id].type].value}<br />
              {/if}
            {/each}
          </Tooltip>
        {/if}
      </Marker>
    {/each}
  {/if}
</LeafletMap>

<svelte:options accessors/>
<LoadingModal bind:this="{webcamArchiveLoadingModal}" />

<style>
  strong {
    display: block;
    text-align: center;
  }
</style>
