var systemTimerTimeOut = 30; // In seconds

function loadSystem() {
  loadSystemDashboard();
  updateSystem();
}

function loadSystemDashboard() {
  var table = jQuery('<table>');
  // Dashboard title row
  table.append(jQuery('<tr>').append(jQuery('<td>').append(jQuery('<span>').addClass('icon about pointer').attr('title', 'About')))
    .append(jQuery('<td>').attr({
      'colspan': 2
    }).append(jQuery('<h1>').text('System')))
    .append(jQuery('<td>').append(jQuery('<span>').addClass('updater')))
  );
  // Last update row
  table.append(jQuery('<tr>').append(jQuery('<td>').attr({
    'colspan': 4,
    'id': 'system_update'
  }).text('updating...')));
  table.append(jQuery('<tr>').append(jQuery('<td>').attr({
    'colspan': 4,
    'id': 'system_uptime'
  }).text('updating...')));

  table.append(jQuery('<tr>').append(jQuery('<td>').text('Engine').append(jQuery('<span>').addClass('icon engine inactive enabled')))
    .append(jQuery('<td>').text('Environment').append(jQuery('<span>').addClass('icon environment inactive enabled')))
    .append(jQuery('<td>').text('Collector').append(jQuery('<span>').addClass('icon collector inactive enabled')))
    .append(jQuery('<td>').text('Webserver').append(jQuery('<span>').addClass('icon webserver inactive enabled')))
  );

  table.append(jQuery('<tr>').append(jQuery('<td>').text('Twitter').append(jQuery('<span>').addClass('icon twitter inactive enabled')))
    .append(jQuery('<td>').text('SMS').append(jQuery('<span>').addClass('icon inactive enabled')))
    .append(jQuery('<td>').text('WebCam').append(jQuery('<span>').addClass('icon addwebcam inactive')))
    .append(jQuery('<td>').text('Loglevel').append(jQuery('<span>').addClass('icon loglevel inactive enabled')))
  );

  table.append(jQuery('<tr>').append(jQuery('<td>').append(jQuery('<div>').attr({
      'id': 'gauge_memory'
    }).css({
      'width': '5.5em',
      'height': '5.5em'
    })))
    .append(jQuery('<td>').append(jQuery('<div>').attr({
      'id': 'gauge_cpuspeed'
    }).css({
      'width': '5.5em',
      'height': '5.5em'
    })))
    .append(jQuery('<td>').append(jQuery('<div>').attr({
      'id': 'gauge_cpuload'
    }).css({
      'width': '5.5em',
      'height': '5.5em'
    })))
    .append(jQuery('<td>').append(jQuery('<div>').attr({
      'id': 'gauge_cputemp'
    }).css({
      'width': '5.5em',
      'height': '5.5em'
    })))
  );

  table.append(jQuery('<tr>').append(jQuery('<td>').append(jQuery('<div>').attr({
      'id': 'gauge_wattage'
    }).css({
      'width': '5.5em',
      'height': '5.5em'
    })))
    .append(jQuery('<td>').append(jQuery('<div>').attr({
      'id': 'gauge_waterflow'
    }).css({
      'width': '5.5em',
      'height': '5.5em'
    })))
  );

  jQuery('#system').append(table);
  jQuery('#system span.icon.about').bind('click', function() {
    showAboutWindow();
  });
  jQuery('div#gauge_wattage').addClass('pointer').bind('click', function() {
    showPowerHistoryGraph('system_wattage', 'Power usage', 'wattage');
  });
}

var gauges = ['memory', 'cpuload', 'cputemp', 'cpuspeed', 'wattage', 'waterflow'];

function updateSystemGauges(name, value, max) {
  var basic_settings = {
    id: "gauge",
    value: 50,
    min: 0,
    max: 100,
    title: "title",
    titleFontColor: "black",
    valueFontColor: "black",
    levelColorsGradient: true,
    gaugeWidthScale: 0.5,
    decimals: 2,
    valueMinFontSize: 10,
    symbol: '%'
  }

  basic_settings.id = 'gauge_' + name;
  basic_settings.title = name;
  basic_settings.value = value;

  if (max != undefined) {
    basic_settings.max = max;
  }

  if (gauges[name] == undefined) {
    switch (name) {
      case 'memory':

        break;
      case 'cpuload':

        break;
      case 'cputemp':
        basic_settings.min = 35;
        basic_settings.max = 80;
        basic_settings.symbol = 'C';
        break;
      case 'cpuspeed':
        basic_settings.min = 600000000;
        basic_settings.max = 1000000000;
        basic_settings.humanFriendly = true;
        basic_settings.symbol = 'hz';
        break;
      case 'wattage':
        basic_settings.symbol = 'W';
        basic_settings.decimals = 0;
        break;
    }
    gauges[name] = new JustGage(basic_settings);
  } else {
    if (max != undefined) {
      gauges[name].refresh(value, max);
    } else {
      gauges[name].refresh(value);
    }
  }
}

function updateSystemIcon(name, status, message) {

  var icon = jQuery('#system .' + name);
  icon.removeClass('inactive enabled on error');

  switch (status) {
    case 'on':
      icon.addClass('enabled on');
      break;
    case 'off':
    case 'error':
      icon.addClass('enabled error');
      break;
    case 'inactive':
      icon.addClass('enabled on inactive');
      break;
    default:
      icon.addClass('enabled on inactive');
      break;
  }
  icon.attr('title', message);
}

function updateSystem() {
  jQuery.ajax({
    url: '/system/all/online',
    dataType: 'json'
  }).done(function(result) {
    updater('system');

    for (var prop in result.value) {
      if (result.value.hasOwnProperty(prop)) {
        if (prop == 'wattage' || prop == 'waterflow') {
          updateSystemGauges(prop, result.value[prop].current, result.value[prop].max);
        } else if (jQuery.inArray(prop, gauges) != -1) {
          updateSystemGauges(prop, result.value[prop]);
        } else if (prop == 'uptime') {
          jQuery('#system #system_uptime').html('Running for <strong>' + moment.duration(result.value[prop], 'seconds').humanize() + '</strong>');
        } else {
          updateSystemIcon(prop, (result.value[prop] ? 'on' : 'off'), (result.value[prop] ? 'OK!' : 'Error!'));
        }
      }
    }
    jQuery('#system #system_update').html('Last update:<br />' + moment().format("dddd D MMMM YYYY, HH:mm:ss"));
  }).fail(function(result) {
    updateSystemIcon('webserver', 'error', 'Offline!!!');
    jQuery('#system .icon:not(.error):not(.about)').addClass('inactive');
  });
  setTimeout(function() {
    updateSystem()
  }, systemTimerTimeOut * 1000);
}