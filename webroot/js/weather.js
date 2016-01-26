var weatherMaxStars = 10;
var weatherTimerTimeOut = 60; // In seconds

function loadWeather() {
  loadWeatherLandScape();
  updateWeather();
}

function loadWeatherLandScape() {
  var starssky = jQuery('<div>').addClass('sky');
  starssky.append(jQuery('<div>').addClass('stars'));
  starssky.append(jQuery('<div>').addClass('twinkling'));
  starssky.append(jQuery('<div>').addClass('test'));

  var div = jQuery('<div>').addClass('landscape').addClass('night')
    .append(jQuery('<div>').addClass('header'))
    .append(jQuery('<div>').addClass('horizon')
      .append(jQuery('<div>').addClass('orb')
        .append(jQuery('<span>'))))
    .append(jQuery('<div>').addClass('rise')
      .append(jQuery('<span>').addClass('date').text('rise'))
      .append(jQuery('<div>').addClass('arrow')))
    .append(jQuery('<div>').addClass('set')
      .append(jQuery('<span>').addClass('date').text('set'))
      .append(jQuery('<div>').addClass('arrow')));

  jQuery('#weather').append(div);

  for (var i = 0; i < weatherMaxStars; i++) new Star();

  jQuery('.landscape .horizon .orb span').jqxTooltip({
    trigger: 'click',
    content: '<b>Loading...</b>',
    showArrow: true,
    showDelay: 5000,
    position: 'bottom',
    name: 'sensorInfo'
  }).bind('opening', function(event) {
    var content = jQuery('<div>').addClass('tooltipContent');
    if (loggedin) {
      content.append(jQuery('<span>').addClass('icon options edit').attr('title', 'Options (logged in)').bind('click', function(event) {
        jQuery.ajax({
          url: '/weather/all',
          dataType: 'json'
        }).done(function(result) {
          var fields = [];
          fields.push({
            'name': 'xmlsource',
            'type': 'text',
            'value': result.value.xmlsource,
            'label': 'XML Url',
            'help': 'Enter the full XML url from yo.nr'
          });
          showEditForm('Weather xml url', fields, '/weather/set', 'updateWeather()');
        }).fail(function() {});
      }));
    }
    var contents = this.title.split("\n");
    for (var i = 0; i < contents.length; i++) {
      if (i == 0) {
        content.append('<strong>' + contents[i] + '</strong><br />');
      } else {
        content.append(contents[i] + '<br />');
      }
    }
    jQuery(this).jqxTooltip({
      content: content
    })
  });
}

function updateWeather(runonce) {
  runonce = runonce || false
  jQuery.ajax({
    url: '/weather/all',
    dataType: 'json'
  }).done(function(result) {
    // Update the credits

    var credits = jQuery('.landscape .header');
    credits.html('');
    credits.append('<a href="http://maps.google.com/maps?q=' + result.value.location.lat + ',' + result.value.location.long + '&z=10" title="Location: ' + result.value.city + ' (' + result.value.country + ')" target="_blank" style="float:left"><strong>Location:</strong> ' + result.value.city + ' (' + result.value.country + ')</a>');
    credits.append('<a href="' + result.value.credits.link + '" title="' + result.value.credits.text + '" target="_blank" style="float:right">' + result.value.credits.text + '</a>');

    // Update times and day vs night
    var now = new Date(result.value.locationtime * 1000);
    var rise = new Date(result.value.sunrise * 1000);
    var set = new Date(result.value.sunset * 1000);
    var isDay = (result.value.day == 1 || result.value.day == true);

    if (!isDay) {
      rise = new Date(result.value.sunset * 1000);
      set = new Date(result.value.sunrise * 1000);
      set.setDate(set.getDate() + 1);

      if (!(rise < now && now < set)) {
        rise.setDate(rise.getDate() - 1);
        set.setDate(set.getDate() - 1);
      }
    }

    // Update the set and rise times and day vs night
    jQuery('.landscape').removeClass('day night').addClass((isDay ? 'day' : 'night'));
    jQuery('.landscape .rise .date').text(moment(rise).format('HH:mm:ss')).attr({
      'title': (isDay ? 'Sun' : 'Moon') + ' rises at ' + moment(rise).format('dddd, MMMM D YYYY, HH:mm:ss')
    });
    jQuery('.landscape .set .date').text(moment(set).format('HH:mm:ss')).attr({
      'title': (isDay ? 'Sun' : 'Moon') + ' sets at ' + moment(set).format('dddd, MMMM D YYYY, HH:mm:ss')
    });

    // Position the orb (sun or moon)
    var distanceDone = now - rise;
    var distance = Math.abs(set - rise);
    var leftPercentage = topPercentage = Math.round((distanceDone / distance) * 100);
    topPercentage = 100 - (topPercentage * 2);
    if (leftPercentage > 50) topPercentage *= -1;
    jQuery('.landscape .horizon span').attr('title', 'Local time: ' + moment().format('HH:mm:ss') + "\n" +
        'Total time: ' + timeFormat(distance) + "\n" +
        'Time done: ' + timeFormat(Math.round(distanceDone / 1000) * 1000) + "\n" +
        'Time left: ' + timeFormat(Math.round((distance - distanceDone) / 1000) * 1000) + "\n" +
        'Position: ' + leftPercentage + '%' + "\n" +
        'Last update: ' + moment().format("dddd D MMMM YYYY, HH:mm:ss"))
      .animate({
        'left': leftPercentage + '%',
        'top': topPercentage + '%'
      }, 1000);

    // Update the weather temperature
    var id = ('weather_' + result.value.city).toLowerCase();
    if (sensorList[id] == undefined) {
      sensorList[id] = new TemperatureSensor(id,
        'Weather in city: ' + result.value.city, {
          min: result.value.temperature.minlimit,
          max: result.value.temperature.maxlimit
        }, {
          min: result.value.temperature.min,
          max: result.value.temperature.max,
          current: result.value.temperature.current
        },
        result.value.temperature.alarm,
        result.value.temperature.alarm_enabled,
        result.value.temperature.logging_enabled,
        result.value.temperature.indicator
      );
    } else {
      var data = {};
      data.name = 'Weather in city: ' + result.value.city;
      data.current = result.value.temperature.current;
      data.min = result.value.temperature.min;
      data.max = result.value.temperature.max;
      data.minlimit = result.value.temperature.minlimit;
      data.maxlimit = result.value.temperature.maxlimit;
      data.alarm = result.value.temperature.alarm;
      data.alarm_enabled = result.value.temperature.alarm_enabled;
      data.logging_enabled = result.value.temperature.logging_enabled;
      data.indicator = result.value.temperature.indicator;

      sensorList[id].update(data);
    }
  }).fail(function(result) {

  });
  if (!runonce) setTimeout(function() {
    updateWeather()
  }, weatherTimerTimeOut * 1000);
}

function Star() {
  this._type = (Math.round(Math.random() + 1) == 1 ? 'small' : 'big');
  this._timeout = (Math.round(Math.random() * 10) + 30) * 1000;
  this._speed = (Math.round(Math.random() * 2) + 2) * 1000;

  this._canvas = jQuery('<div>').addClass('star').addClass(this._type);
  this._canvas.css({
    'top': Math.floor((Math.random() * 7) + 1) + '%',
    'left': Math.floor((Math.random() * 90) + 1) + '%'
  });

  this.draw = function() {
    jQuery('.landscape').append(this._canvas);
  }

  this.animate = function() {
    if (this._canvas.is(':visible')) {
      this._canvas.animate({
        'background-size': '100%'
      }, this._speed).animate({
        'background-size': '70%'
      }, this._speed);
    }
  }

  this.draw();
  var me = this;
  setInterval(function() {
    me.animate();
  }, this._timeout);
}
