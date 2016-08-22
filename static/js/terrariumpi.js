var globals = {
  websocket: null,
  connection: 'ws' + (location.protocol == 'https:' ? 's' : '') + '://' + location.host + '/live',
  gauges: [],
  webcams: [],
  websocket_timer: null,
  updatetimer: null,
  online_timer: null
};
$(document).ready(function() {
  $('#system_time').text(moment().format('LLLL'));
  websocket_init(false);
  // Bind to menu links in order to load Ajax calls
  $('#sidebar-menu a').on('click', load_page);
  // NProgress bar animation during Ajax calls
  $(document).on({
    ajaxStart: function() {
      NProgress.start();
    },
    ajaxComplete: function() {
      NProgress.done();
    }
  });

  setInterval(function() {
    notification_timestamps();
    updateWebcams();
    $('#system_time').text(moment().format('LLLL'));
  }, 30 * 1000);

  load_page('dashboard.html');
});

function websocket_init(reconnect) {
  websocket_connect();
  globals.websocket.onopen = function(evt) {
    websocket_message({
      'type': 'client_init',
      'reconnect': reconnect
    });
    update_online_messages(true);
  };
  globals.websocket.onmessage = function(evt) {
    online_updater();
    var data = JSON.parse(evt.data);
    console.log(new Date(), data);
    switch (data.type) {
      case 'uptime':
        update_dashboard_uptime(data.data);
        break;
      case 'power_usage_water_flow':
        update_dashboard_power_usage(data.data.power);
        update_dashboard_water_flow(data.data.water);
        break;
      /*
      case 'dashboard_water_flow':
        update_dashboard_water_flow(data.data);
        break;
        */

      case 'environment':
        $.each(['heater', 'sprayer', 'light'], function(index, value) {
          update_dashboard_environment(value, data.data[value]);
        });
        break;
      case 'sensor_gauge':
        $.each(data.data, function(index, sensor) {
          sensor_gauge(sensor.id !== undefined ? sensor.id : index, sensor);
        });
        break;
      case 'power_switches':
        $.each(data.data, function(index, value) {
          update_power_switch(value.id, value);
        });
        break;
      case 'door_indicator':
        update_door_indicator(data.data);
        break;
      case 'update_weather':
        update_weather(data.data);
        break;
    }
  };
  globals.websocket.onclose = function(evt) {
    is_offline();
    update_online_messages(false);
    clearInterval(globals.websocket_timer);
    globals.websocket_timer = setInterval(function() {
      websocket_init(true);
    }, 10 * 1000);
  };
}

function websocket_connect() {
  try {
    clearInterval(globals.websocket_timer);
    globals.websocket = null;
    globals.websocket = new WebSocket(globals.connection);
  } catch (error) {
    console.log('error', error);
  }
}

function websocket_message(message) {
  try {
    globals.websocket.send(JSON.stringify(message));
  } catch (error) {
    console.log('error', error);
  }
}

function menu_click(url) {
  // Find the menu item that should be loaded
  var menu_item = $('a[href="' + url + '"]');
  // Exists?
  if (menu_item.length == 1) {
    // Get the parent menu item
    var parent_menu = menu_item.parent('li').parents('li');
    // If the parent menu is active, we are al ready on the right parent menu
    if (parent_menu.hasClass('active')) {
      // Parent menu is the same, so clear all active submenu's
      parent_menu.find('.child_menu li').removeClass('active');
    } else {
      // Open parent menu
      parent_menu.find('a:first').click();
    }
    // Trigger the click on the sub menu item
    menu_item.click();
  }
  // Make sure that the browser will not fire it's url loading event
  return false;
}

function load_page(url) {
  // If no url given, use the event trigger a href attribute
  if (typeof url != 'string') {
    url = this.href;
  }
  // Only process with some input
  if (url !== '') {
    // Get the menu url so that jQuery can match
    var menu_url = url.replace('http://' + location.host + '/', '');
    // Reset the main content height
    $("#maincontent").height(0);
    // Load the data through AJAX
    $.get(url, function(data) {
      // Clear all submenu's that are not clicked
      $('.child_menu a[href!="' + menu_url + '"]').parent().removeClass('active');
      $('.child_menu a[href="' + menu_url + '"]').parent().addClass('active');
      // Put the content on the page
      $("#maincontent").html(data);
      // Reload some theme settings per page
      reload_reload_theme();
    });
  }
  // Make sure the browser will not fire it's url loading event
  return false;
}

function process_form() {
  $('form').each(function() {
    $(this).on('submit', function() {
      var form = $(this);
      $.ajax({
        method: form.attr('method'),
        url: form.attr('action'),
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(prepare_form_data(form))
      }).done(function(response) {
        if (response.ok) {
          new PNotify({
            title: "Data saved",
            type: "success",
            text: "Your changes are saved",
            nonblock: {
              nonblock: true
            },
            delay: 1000,
            mouse_reset: false,
            addclass: 'dark',
            styling: 'bootstrap3',
            hide: true,
          });
        }
      });
      return false;
    });
  });
}

function prepare_form_data(form) {
  var formdata = [];
  var form_type = form.attr('action').split('/').pop();
  var re = /(sensor|switch|webcam|light|sprayer|heater)(_\d+)?_(.*)/i;
  var objectdata = {};
  var prev_nr = -1;
  if (form_type === 'weather' || form_type === 'environment' || form_type === 'system') {
    formdata = {};
  }
  try {
    form.find('div:visible input:not([disabled="disabled"]),div:visible select:not([disabled="disabled"])').each(function() {
      var field_name = $(this).attr('name');
      var field_value = $(this).val();
      switch (form_type) {
        case 'weather':
        case 'system':
          formdata[field_name] = field_value;
          break;
        case 'sensors':
        case 'switches':
        case 'environment':
        case 'webcams':
          if ((matches = re.exec(field_name)) !== null) {
            if (matches.index === re.lastIndex) {
              re.lastIndex++;
            }
            if (matches.length >= 3) {
              if (matches[2] === undefined) {
                current_nr = matches[1];
              } else {
                current_nr = matches[2].substr(1) * 1;
              }
              if (prev_nr != current_nr) {
                if (Object.keys(objectdata).length > 1) {
                  formdata[prev_nr] = $.extend(true, {}, objectdata);
                }
                // New item
                objectdata = {};
                prev_nr = current_nr;
              }
              if (matches[3] === 'on' || matches[3] === 'off') {
                field_value = moment(field_value, 'LT').unix();
              }
              objectdata[matches[3]] = field_value;
            }
          }
          break;
      }
    });
    if (Object.keys(objectdata).length > 1) {
      formdata[prev_nr] = $.extend(true, {}, objectdata);
    }
  } catch (error) {
    console.log(error);
    return false;
  }
  return formdata;
}

function update_dashboard_tile(tile, text) {
  var div = $('div.tile_count #' + tile + ' div.count');
  if (div.length == 1 && div.text() != text) {
    div.text(text);
    var oldColor = div.css('color');
    div.addClass('green');
    div.animate({
      color: oldColor
    }, 1000, function() {
      $(this).removeClass('green').css('color', '');
    });
  }
}

function update_dashboard_uptime(data) {
  update_dashboard_tile('uptime', format_uptime(data.uptime));
  $("#uptime .progress-bar-success").css('height', (data.load[0] * 100) + '%');
  $("#uptime .progress-bar-warning").css('height', (data.load[1] * 100) + '%');
  $("#uptime .progress-bar-danger").css('height', (data.load[2] * 100) + '%');
}

function update_dashboard_power_usage(data) {
  update_dashboard_tile('power_wattage', data.current + '/' + data.max);
  var percentage = (data.max > 0 ? (data.current / data.max) * 100 : 0);
  $("#power_wattage .progress-bar-success").css('height', percentage + '%');
  data.total /= 1000;
  update_dashboard_tile('total_power', data.total.toFixed(2));
}

function update_dashboard_water_flow(data) {
  update_dashboard_tile('water_flow', data.current + '/' + data.max);
  var percentage = (data.max > 0 ? (data.current / data.max) * 100 : 0);
  $("#water_flow .progress-bar-info").css('height', percentage + '%');
  update_dashboard_tile('total_water', data.total.toFixed(2));
}

function update_weather(data) {
  var icons = new Skycons({
    "color": "#73879C"
  });
  var weather_current = $('div#weather_today');
  if (weather_current.length == 1) {
    weather_current.find('.status').html(moment(data.hour_forecast[0].from * 1000).format('[<b>]dddd[</b>,] LT') + ' <span> in <b>' + data.temperature + '</b></span>');
    weather_current.find('h2').html(data.city.city + '<br><i>' + data.hour_forecast[0].weather + '</i>');
    weather_current.find('.sunrise').text(moment(data.sun.rise * 1000).format('LT')).parent().css('fontWeight', (data.day ? 'bold' : 'normal'));
    weather_current.find('.sunset').text(moment(data.sun.set * 1000).format('LT')).parent().css('fontWeight', (data.day ? 'normal' : 'bold'));
    weather_current.find('.degrees').text(data.hour_forecast[0].temperature);
    icons.set(weather_current.find('canvas').attr('id'), data.hour_forecast[0].icon);
    var week_forecast_divs = weather_current.find('div.row.weather-days div.daily-weather');
    // Set timestamp to tomorrow at 13 hours. That is the first week forecast we take
    var timestamp = Math.round(new Date(Date.now()).setHours(13) / 1000) + (24 * 60 * 60);
    var day_counter = 0;
    var graphdata = [];
    $.each(data.week_forecast, function(index, value) {
      graphdata.push([(value.to - ((value.to - value.from) / 2)) * 1000, value.temperature]);
      if (value.from - timestamp >= 3600 && day_counter < week_forecast_divs.length) {
        $(week_forecast_divs[day_counter]).find('.day').text(moment(value.from * 1000).format('ddd'));
        $(week_forecast_divs[day_counter]).find('.degrees').text(value.temperature);
        $(week_forecast_divs[day_counter]).find('h5').html(value.wind_speed.toFixed(1) + ' <i>' + (data.windspeed === 'ms' ? 'm/s' : 'Km/h') + '</i>');
        icons.set($(week_forecast_divs[day_counter]).find('canvas').attr('id'), value.icon);
        day_counter++;
        timestamp += (24 * 60 * 60);
      }
    });
    icons.play();
    history_graph('weather_week', graphdata, 'weather');
    graphdata = [];
    $.each(data.hour_forecast, function(index, value) {
      graphdata.push([(value.to - ((value.to - value.from) / 2)) * 1000, value.temperature]);
    });
    history_graph('weather_day', graphdata, 'weather');
  }
}

function update_dashboard_environment(name, value) {
  var systempart = $('div.environment_' + name);
  var enabledColor = '';
  switch (name) {
    case 'light':
      enabledColor = 'orange';
      systempart.find('h4 small').text('modus: ' + value.modus);
      systempart.find('.on').text(moment(value.on * 1000).format('LT'));
      systempart.find('.off').text(moment(value.off * 1000).format('LT'));
      systempart.find('.duration').text(moment.duration(Math.abs(value.off - value.on) * 1000).humanize());
      break;
    case 'sprayer':
      enabledColor = 'blue';
      systempart.find('.current').text(value.current.toFixed(3) + '%');
      systempart.find('.alarm_min').text(value.alarm_min + '%');
      systempart.find('span.glyphicon-warning-sign').toggle(value.alarm);
      break;
    case 'heater':
      enabledColor = 'red';
      systempart.find('h4 small').text('modus: ' + value.modus);
      systempart.find('.current').text(value.current.toFixed(3) + 'C');
      systempart.find('.alarm_min').text(value.alarm_min + 'C');
      systempart.find('.alarm_max').text(value.alarm_max + 'C');
      systempart.find('span.glyphicon-warning-sign').toggle(value.alarm);
      break;
  }
  systempart.find('h4').removeClass('orange blue red').addClass(value.enabled ? enabledColor : '').attr('title', value.enabled ? 'enabled' : 'disabled');
  systempart.find('.state i').removeClass('red green').addClass(value.state == 'on' ? 'green' : 'red').attr('title', value.state);
}

function format_uptime(uptime) {
  uptime = moment.duration(uptime * 1000);
  var uptime_duration = '';
  uptime_duration += uptime.days() + 'D';
  uptime_duration += (uptime.hours() < 10 ? '0' : '') + uptime.hours() + 'H';
  uptime_duration += (uptime.minutes() < 10 ? '0' : '') + uptime.minutes() + 'M';
  uptime_duration += (uptime.seconds() < 10 ? '0' : '') + uptime.seconds() + 'S';
  return uptime_duration;
}

function online_updater() {
  clearTimeout(globals.online_timer);
  is_online();
  globals.online_timer = setTimeout(function() {
    is_offline();
  }, 120 * 1000);
}

function update_door_messages(online) {
  var title = (online ? 'Open' : 'Close');
  var message = (online ? 'Door has been opend!' : 'Door is closed');
  var icon = (online ? 'fa-lock' : 'fa-unlock');
  var color = (online ? 'green' : 'red');
  add_notification_message('door_messages', title, message, icon, color);
}

function update_online_messages(online) {
  var title = (online ? 'Online' : 'Offline');
  var message = (online ? 'Connection restored!' : 'Connection lost!');
  var icon = (online ? 'fa-check-circle-o' : 'fa-exclamation-triangle');
  var color = (online ? 'green' : 'red');
  add_notification_message('online_messages', title, message, icon, color);
}

function add_notification_message(type, title, message, icon, color) {
  var menu = $('ul#' + type);
  if (menu.find('li:first a span.message').text() == message) {
    // Skip duplicate messages
    return;
  }
  var notification = $('<a>').on('click', function() {
    close_notification_message(this);
  });
  notification.append($('<span>').addClass('image').append($('<img>').attr({
    'src': $('div.profile_pic img').attr('src'),
    'alt': 'Profile image'
  })));
  notification.append($('<span>').append($('<span>').text(title)).append($('<span>').addClass('time notification_timestamp').attr('timestamp', (new Date()).getTime()).text('...')));
  notification.append($('<span>').addClass('message').text(message).append($('<span>').addClass('pull-right').html('<i class="fa ' + icon + ' ' + color + '"></i>')));
  // Remove no messages line
  menu.find('li.no_message').hide();
  // Add new message on top
  menu.prepend($('<li>').addClass('notification').append(notification));
  // Only allow 5 messages, more will be removed
  menu.find('li.notification:gt(4)').remove();
  // Update the notifcation time
  notification_timestamps();
}

function close_notification_message(notification) {
  notification = $(notification).parent();
  var menu = notification.parent('ul');
  notification.remove();
  if (menu.find('li.notification').length === 0) {
    menu.find('li.no_message').show();
  } else {
    menu.find('li.no_message').hide();
  }
}

function notification_timestamps() {
  var now = (new Date()).getTime();
  $('span.notification_timestamp').each(function() {
    var timestamp = $(this).attr('timestamp') * 1;
    var duration = moment.duration((now - timestamp) * -1);
    $(this).text(duration.humanize(true));
  });
}

function is_online() {
  var online_indicator = $('a#online_indicator');
  online_indicator.find('span').text('Online');
  online_indicator.find('i.fa').removeClass('fa-check-circle-o fa-exclamation-triangle red green').addClass('fa-check-circle-o green');
}

function is_offline() {
  var online_indicator = $('a#online_indicator');
  online_indicator.find('span').text('Offline');
  online_indicator.find('i.fa').removeClass('fa-check-circle-o fa-exclamation-triangle red green').addClass('fa-exclamation-triangle red');
}

function update_door_indicator(status) {
  if (status == 'open') {
    door_open();
  } else {
    door_closed();
  }
}

function door_open() {
  var online_indicator = $('a#door_indicator');
  online_indicator.find('span').text('Door open');
  online_indicator.find('i.fa').removeClass('fa-lock fa-unlock red green').addClass('fa-unlock red');
}

function door_closed() {
  var online_indicator = $('a#door_indicator');
  online_indicator.find('span').text('Door closed');
  online_indicator.find('i.fa').removeClass('fa-lock fa-unlock red green').addClass('fa-lock green');
}

function get_theme_color(color) {
  if (color == 'orange') return '#f0ad4e';
  return $('<div>').addClass(color).css('color');
}

function load_panel_tool_box() {
  $('.collapse-link').on('click', function() {
    var $BOX_PANEL = $(this).closest('.x_panel'),
      $ICON = $(this).find('i'),
      $BOX_CONTENT = $BOX_PANEL.find('.x_content');
    // fix for some div with hardcoded fix class
    if ($BOX_PANEL.attr('style')) {
      $BOX_CONTENT.slideToggle(200, function() {
        $BOX_PANEL.removeAttr('style');
      });
    } else {
      $BOX_CONTENT.slideToggle(200);
      $BOX_PANEL.css('height', 'auto');
    }
    $ICON.toggleClass('fa-chevron-up fa-chevron-down');
  });
  $('.close-link').click(function() {
    var $BOX_PANEL = $(this).closest('.x_panel');
    $BOX_PANEL.remove();
  });
}

function reload_reload_theme() {
  // Panel toolbox
  load_panel_tool_box();
  // Tooltip
  $('[data-toggle="tooltip"]').tooltip({
    container: 'body'
  });
  process_form();
}

function sensor_gauge(name, data) {
  if ($('#sensor_' + name).length == 1) {
    // Update title
    if (data.type !== undefined && data.name !== undefined) {
      $('#sensor_' + name + ' span.title').text(data.type + ' sensor: ' + (data.name !== '' ? data.name : data.address));
    }
    // Update timestamp indicator
    $('#sensor_' + name + ' small').text(moment().format('LLL'));
    // Setup a new gauge if needed
    if (globals.gauges[name] === undefined) {
      var valid_area = data.alarm_max - data.alarm_min;
      var colors = [
        [0.0, '#E74C3C'],
        [(data.alarm_min - (0)) / (data.max - data.min), '#f0ad4e'],
        [(data.alarm_min + (valid_area / 2)) / (data.max - data.min), '#1ABB9C'],
        [(data.alarm_max + (0)) / (data.max - data.min), '#f0ad4e'],
        [1.0, '#E74C3C']
      ];
      var opts = {
        animationSpeed: 32,
        lines: 12,
        angle: 0,
        lineWidth: 0.4,
        pointer: {
          length: 0.75,
          strokeWidth: 0.042,
          color: '#1D212A'
        },
        limitMax: 'false',
        strokeColor: '#F0F3F3',
        generateGradient: true,
        minValue: data.min,
        maxValue: data.max,
        percentColors: colors,
      };
      globals.gauges[name] = new Gauge(document.getElementById('gauge_canvas_' + name)).setOptions(opts);
      globals.gauges[name].setTextField(document.getElementById('gauge_text_' + name));
    }
    // Update values
    globals.gauges[name].minValue = data.min;
    globals.gauges[name].maxValue = data.max;
    globals.gauges[name].set(data.current);
    $('div#sensor_' + name + ' .x_title h2 .badge').toggle(data.alarm);
  }
}

function history_graph(name, data, type) {
  if (type === undefined) {
    type = 'temperature';
  }
  var graph_data = [];
  var show_splines = true;
  var fill = false;
  var show_lines = false;
  switch (type) {
    case 'temperature':
    case 'humidity':
      graph_data = [{
        label: 'Current',
        data: data.current
      }, {
        label: 'Alarm min',
        data: data.alarm_min
      }, {
        label: 'Alarm max',
        data: data.alarm_max
      }];
      break;
    case 'weather':
    case 'system_temperature':
      graph_data = [{
        label: 'Temperature',
        data: data
      }];
      break;
    case 'system_uptime':
      graph_data = [{
        label: 'Uptime',
        data: data
      }];
      break;
    case 'system_load':
      graph_data = [{
        label: 'Load',
        data: data.load1
      }, {
        label: 'Load5',
        data: data.load5
      }, {
        label: 'Load15',
        data: data.load15
      }];
      break;
    case 'system_memory':
      graph_data = [{
        label: 'Used',
        data: data.used
      }, {
        label: 'Free',
        data: data.free
      }, {
        label: 'Total',
        data: data.total
      }];
      break;
    case 'switch':
      graph_data = [data.power_wattage, data.water_flow];
      graph_data = [{
        label: 'Power usage',
        data: data.power_wattage
      }, {
        label: 'Water flow',
        data: data.water_flow
      }];
      show_splines = false;
      show_lines = true;
      fill = true;
      break;
  }
  var tickSize = 60;
  var total_data_duration = (graph_data[0].data[graph_data[0].data.length - 1][0] - graph_data[0].data[0][0]) / 3600000;
  if (total_data_duration > 120) {
    tickSize = 360;
  } else if (total_data_duration > 120) {
    tickSize = 240;
  } else if (total_data_duration > 48) {
    tickSize = 180;
  } else if (total_data_duration > 24) {
    tickSize = 120;
  }
  if ($('#history_graph_' + name).length == 1) {
    $('#history_graph_' + name).html('').removeClass('loading');
    $.plot($('#history_graph_' + name), graph_data, {
      series: {
        splines: {
          show: show_splines,
          tension: 0.4,
          lineWidth: 2,
          fill: fill
        },
        lines: {
          show: show_lines,
          lineWidth: 2,
          fill: fill
        },
        shadowSize: 2
      },
      grid: {
        verticalLines: true,
        hoverable: true,
        clickable: true,
        tickColor: "#d5d5d5",
        borderWidth: 1,
        color: '#fff'
      },
      colors: ["rgba(38, 185, 154, 0.38)", "rgba(3, 88, 106, 0.38)", "rgba(3, 88, 106, 0.38)"],
      xaxis: {
        tickColor: "rgba(51, 51, 51, 0.06)",
        mode: "time",
        timezone: "browser",
        tickSize: [tickSize, "minute"],
        //tickLength: 10,
        axisLabel: "Date",
        axisLabelUseCanvas: true,
        axisLabelFontSizePixels: 12,
        axisLabelFontFamily: 'Verdana, Arial',
        axisLabelPadding: 0,
        //transform: function (v) { return -v; },
        //inverseTransform: function (v) { return -v; }
      },
      yaxis: {
        ticks: 8,
        tickColor: "rgba(51, 51, 51, 0.06)",
      },
      tooltip: true
    });
  }
}

function update_power_switch(id, data) {
  var power_switch = $('#switch_' + id);
  power_switch.find('h2 span.title').text('Switch ' + data.name);
  power_switch.find('h2 small.data_update').text(data.power_wattage + 'W' + (data.water_flow > 0 ? ', ' + data.water_flow + 'L/m' : ''));
  power_switch.find('span.glyphicon').removeClass('blue green').addClass((data.state ? 'green' : 'blue'));
}

function update_switch_history() {
  if ($('div.row.switch').length >= 0) {
    $.getJSON('/api/history/switches', function(data) {
      $.each(data.switches, function(index, powerswitch) {
        var graphdata = {
          power_wattage: [],
          water_flow: []
        };
        var state_chage = -1;
        $.each(powerswitch.state, function(counter, status) {
          if (!status[1]) {
            powerswitch.power_wattage[counter][1] = 0;
            powerswitch.water_flow[counter][1] = 0;
          }
          var copy = {};
          if (counter > 0 && state_chage != status[1]) {
            // Copy previous object to get the right status with current timestamp
            copy = $.extend(true, {}, powerswitch.power_wattage[counter - 1]);
            copy[0] = status[0];
            graphdata.power_wattage.push(copy);
            copy = $.extend(true, {}, powerswitch.water_flow[counter - 1]);
            copy[0] = status[0];
            graphdata.water_flow.push(copy);
            state_chage = status[1];
          }
          graphdata.power_wattage.push(powerswitch.power_wattage[counter]);
          graphdata.water_flow.push(powerswitch.water_flow[counter]);
          if (counter == powerswitch.state.length - 1) {
            // Add endpoint which is a copy of the last point, with current time
            copy = $.extend(true, {}, powerswitch.power_wattage[counter]);
            copy[0] = (new Date()).getTime();
            graphdata.power_wattage.push(copy);
            copy = $.extend(true, {}, powerswitch.water_flow[counter]);
            copy[0] = (new Date()).getTime();
            graphdata.water_flow.push(copy);
          }
        });
        history_graph(index, graphdata, 'switch');
      });
      clearTimeout(globals.updatetimer);
      globals.updatetimer = setTimeout(function() {
        update_switch_history();
      }, 1 * 60 * 1000);
    });
  }
}

function update_dashboard_history() {
  if ($('#sensor_temperature, #sensor_humidity').length >= 1) {
    $.getJSON('/api/history/sensors/average', function(data) {
      $.each(data.sensors, function(index, value) {
        history_graph(index, value);
      });
      clearTimeout(globals.updatetimer);
      globals.updatetimer = setTimeout(function() {
        update_dashboard_history();
      }, 1 * 60 * 1000)
    });
  }
}

function update_webcam_preview(name, url) {
  $('img#webcam_' + name + '_preview').attr('src', url);
}

function toggleSwitch(id) {
  id = id.split('_')[1];
  websocket_message({
    'type': 'toggle_switch',
    'data': {
      'id': id,
      'state': 'toggle'
    }
  });
}

function update_sensor_history(type) {
  if ($('div.row.sensor').length >= 1) {
    $.getJSON('/api/history/sensors/' + type, function(data) {
      $.each(data[type], function(index, sensor) {
        history_graph(index, sensor);
      });
      clearTimeout(globals['updatetimer']);
      globals['updatetimer'] = setTimeout(function() {
        update_sensor_history(type);
      }, 1 * 60 * 1000)
    });
  }
}

function updateWebcams() {
  if ($('.webcam').length > 0) {
    $.each(Object.keys(globals.webcams), function(index, webcamid) {
      globals.webcams[webcamid].eachLayer(function(layer) {
        layer.redraw();
      });
    });
  }
}

function initWebcam(webcamid, name, maxzoom) {
  if ($('div#webcam_' + webcamid).length == 1) {
    $('div#webcam_' + webcamid).parents('.x_panel').find('h2 small').text(name);
    if (globals.webcams[webcamid] === undefined) {
      globals.webcams[webcamid] = new L.Map('webcam_' + webcamid, {
        layers: [createWebcamLayer(webcamid, maxzoom)],
        fullscreenControl: true,
      }).setView([0, 0], 1);
      var loadingControl = L.Control.loading({
        separate: true
      });
      globals.webcams[webcamid].addControl(loadingControl);
    }
  }
}

function createWebcamLayer(webcamid, maxzoom) {
  return L.tileLayer('/static/webcam/{id}_tile_{z}_{x}_{y}.jpg?_{time}', {
    time: function() {
      return (new Date()).valueOf();
    },
    id: webcamid,
    noWrap: true,
    continuousWorld: false,
    maxNativeZoom: maxzoom,
    maxZoom: maxzoom + 1
  });
}
