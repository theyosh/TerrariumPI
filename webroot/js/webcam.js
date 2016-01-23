function loadWebcams() {
  jQuery.ajax({
    url: '/webcam/list',
    dataType: 'json'
  }).done(function(result) {
    var counter = 0;
    jQuery.each(result.value, function() {
      new Webcam(this.id,
        this.name,
        this.max_zoom,
        this.url,
        this.archive,
        this.rotation,
        this.height,
        this.width,
        30);
    });
  });
}

function addWebCamForm() {
  var fields = [];
  fields.push({
    'name': 'id',
    'type': 'text',
    'value': '{new}',
    'label': 'ID',
    'help': 'Enter the md5 hash of the webcam address',
    'readonly': true
  });
  fields.push({
    'name': 'name',
    'type': 'text',
    'value': '',
    'label': 'Name',
    'help': 'Enter a name of this webcam'
  });
  fields.push({
    'name': 'url',
    'type': 'text',
    'value': '',
    'label': 'URL',
    'help': 'Enter the full url this webcam'
  });
  fields.push({
    'name': 'archiving',
    'type': 'dropdown',
    'values': new Array({
      'name': 'No archiving',
      'value': 0
    }, {
      'name': '1 minute',
      'value': 60
    }, {
      'name': '15 minutes',
      'value': 15 * 60
    }, {
      'name': '1 hour',
      'value': 60 * 60
    }),
    'label': 'Set archiving time',
    'help': 'Enabled web cam images archiving'
  });
  fields.push({
    'name': 'rotation',
    'type': 'dropdown',
    'values': new Array({
      'name': 'No rotation',
      'value': 0
    }, {
      'name': '90 degrees',
      'value': 90
    }, {
      'name': '180 degress',
      'value': 180
    }, {
      'name': '270 degress',
      'value': 270
    }),
    'label': 'Set the image rotation',
    'help': 'Set the image rotation'
  });
  showEditForm('Add new webcam', fields, '/webcam/add', 'loadWebcams()');
}

function Webcam(id, name, max_zoom, url, archive, rotation, height, width, timeout) {
  this._id = id;
  this._name = name;
  this._max_zoom = max_zoom;
  this._url = url;
  this._archive = archive;
  this._rotation = rotation;
  this._height = height;
  this._width = width;
  this._timeout = timeout;

  this._webcamCanvas = jQuery('<div>').addClass('webcam').attr({
    'id': this._id
  });
  this._canvasEdit = jQuery('<span>').addClass('icon options edit').attr('title', 'Options (logged in)').css({
    'float': 'right',
    'display': 'none'
  });

  var me = this;
  this._canvasEdit.bind('click', {
    action: '/webcam/' + this._id + '/set'
  }, function(event) {
    var fields = [];
    fields.push({
      'name': 'id',
      'type': 'text',
      'value': me._id,
      'label': 'ID',
      'help': 'Enter the md5 hash of the webcam address',
      'readonly': true
    });
    fields.push({
      'name': 'name',
      'type': 'text',
      'value': me._name,
      'label': 'Name',
      'help': 'Enter a name of this webcam'
    });
    fields.push({
      'name': 'url',
      'type': 'text',
      'value': me._url,
      'label': 'URL',
      'help': 'Enter the full url this webcam'
    });
    fields.push({
      'name': 'archiving',
      'type': 'dropdown',
      'values': new Array({
        'name': 'No archiving',
        'value': 0
      }, {
        'name': '1 minute',
        'value': 60
      }, {
        'name': '15 minutes',
        'value': 15 * 60
      }, {
        'name': '1 hour',
        'value': 60 * 60
      }),
      'label': 'Set archiving time',
      'help': 'Enabled web cam images archiving'
    });
    fields.push({
      'name': 'rotation',
      'type': 'dropdown',
      'values': new Array({
        'name': 'No rotation',
        'value': 0
      }, {
        'name': '90 degrees',
        'value': 90
      }, {
        'name': '180 degress',
        'value': 180
      }, {
        'name': '270 degress',
        'value': 270
      }),
      'label': 'Set the image rotation',
      'help': 'Set the image rotation'
    });
    showEditForm('Webcam settings ' + me._name, fields, event.data.action);
  });

  jQuery('.webcams').append(this._webcamCanvas);
  this._webcamLayer = function() {
    return L.tileLayer('webcam/' + this._id + '_tile_{z}_{x}_{y}.jpg?time=' + (new Date()).valueOf(), {
      minZoom: 0,
      maxZoom: this._max_zoom + 1,
      maxNativeZoom: this._max_zoom,
      attribution: this._name + ' | Last update: ' + moment().format("DD-MM-YYYY@HH:mm:ss"),
      tms: false,
      noWrap: true,
      unloadInvisibleTiles: false,
    });
  }

  this._map = L.map(this._id, {
    fullscreenControl: true
  }).setView([0, 0], 0);
  this._loadingControl = L.Control.loading({
    separate: true
  });
  this._map.addControl(this._loadingControl);
  this._newlayer = this._layer = this._webcamLayer();
  this._map.addLayer(this._layer);

  this._webcamCanvas.hover(
    function() {
      if (loggedin) me._canvasEdit.fadeIn();
    },
    function() {
      if (loggedin) me._canvasEdit.fadeOut();
    }
  );
  this._webcamCanvas.append(this._canvasEdit);

  this.update = function() {
    var me = this;
    this._newlayer = this._webcamLayer();
    this._newlayer.on('load', function(e) {
      me._newlayer.bringToFront()
      me._map.removeLayer(me._layer);
      me._newlayer.off('load'); // Remove the load event due to reloading of the layer when moving around....
      me._layer = me._newlayer;
    });
    this._last_update = new Date();
    this._map.addLayer(this._newlayer);
  }

  var me = this;
  setInterval(function() {
    me.update();
  }, this._timeout * 1000);
}