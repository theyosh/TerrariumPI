## Leaflet.fullscreen
A HTML5 fullscreen plugin for Leaflet.

### Usage

To provide a button for toggling fullscreen on and off:

``` js
// Create a new map with a fullscreen button:
var map = new L.Map('map', {
    fullscreenControl: true,
    // OR
    fullscreenControl: {
        pseudoFullscreen: false // if true, fullscreen to page width and height
    }
});

// or, add to an existing map:
map.addControl(new L.Control.Fullscreen());
```

The plugin also adds several methods to `L.Map` which are always available, even if you choose not to use the fullscreen button:

``` js
map.isFullscreen() // Is the map fullscreen?
map.toggleFullscreen() // Either go fullscreen, or cancel the existing fullscreen.

// `fullscreenchange` Event that's fired when entering or exiting fullscreen.
map.on('fullscreenchange', function () {
    if (map.isFullscreen()) {
        console.log('entered fullscreen');
    } else {
        console.log('exited fullscreen');
    }
});
```

### Localization

To change fullscreen control text:

``` js
map.addControl(new L.Control.Fullscreen({
    title: {
        'false': 'View Fullscreen',
        'true': 'Exit Fullscreen'
    }
}));
```

### Including via CDN

Leaflet.fullscreen is [available through the Mapbox Plugin CDN](https://www.mapbox.com/mapbox.js/plugins/#leaflet-fullscreen) - just copy this include:

```html
<script src='https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/Leaflet.fullscreen.min.js'></script>
<link href='https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/leaflet.fullscreen.css' rel='stylesheet' />
```

### Building

    npm install && make

__ProTip__ You may want to install `watch` so you can run `watch make`
without needing to execute make on every change.

### Supported Leaflet Versions

Leaflet 1.0 and later is supported. Earlier versions may work, but are not tested.
