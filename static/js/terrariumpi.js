var globals = { websocket : null,
                connection : 'ws://' + location.host + '/live',
                gauges : [],
                websocket_timer : null,
                updatetimer : null,
                online_timer: null};

 $(document).ready(function() {
  websocket_init(false);

  // Bind to menu links in order to load Ajax calls
  $('#sidebar-menu a').on('click',load_page);

  // NProgress bar animation during Ajax calls
  $(document).on({
    ajaxStart: function() { NProgress.start();},
    ajaxComplete: function() { NProgress.done(); }
  });

  setInterval(function(){
    notification_timestamps();
  },30 * 1000);
});

function websocket_init(reconnect) {
  websocket_connect();

  globals.websocket.onopen = function(evt) {
    websocket_message({ 'type': 'client_init', 'reconnect' : reconnect});
    update_online_messages(true);
  };

  globals.websocket.onmessage = function(evt) {
    online_updater();

    var data = JSON.parse(evt.data);
    console.log(new Date(), data);

    switch(data.type) {
      case 'dashboard_uptime':
        update_dashboard_uptime(data.data);
        break;

      case 'dashboard_power_usage':
        update_dashboard_power_usage(data.data);
        break;

      case 'dashboard_water_flow':
        update_dashboard_water_flow(data.data);
        break;


      case 'dashboard_weather':
        update_dashboard_weather(data.data);
        break;

      case 'dashboard_switches':
        update_dashboard_power_switches(data.data);
        break;

      case 'power_usage_water_flow':
        update_dashboard_tile('total_power', data.data.total_power.toFixed(2));
        update_dashboard_tile('total_water', data.data.total_water.toFixed(2));
        break;

      case 'history_graph':
        $.each(data.data,function(index,graph){
          history_graph(graph.id !== undefined ? sensor.id : index , graph.summary);
        });
        break;

      case 'sensor_gauge':
        $.each(data.data,function(index,sensor){
          sensor_gauge(sensor.id !== undefined ? sensor.id : index , sensor);
        });
        break;


      case 'door_indicator':
        update_door_indicator(data.data);
        break;
    }
  };

  globals.websocket.onclose = function(evt) {
    is_offline();
    update_online_messages(false);
    clearInterval(globals.websocket_timer);
    globals.websocket_timer = setInterval(function(){
      websocket_init(true);
    }, 10 * 1000);
  };
}

function websocket_connect() {
  try {
    clearInterval(globals.websocket_timer);
    globals.websocket = null;
    globals.websocket = new WebSocket(globals.connection);
  } catch(error) {
    console.log('error', error);
  }
}

function websocket_message(message) {
  globals.websocket.send(JSON.stringify(message));
}

function menu_click(url) {
  var menu_item = $('a[href="' + url + '"]');
  if (menu_item.length == 1) {
    menu_item.parent().parent().parent().find('a:first').click();
    menu_item.click();
    return false;
  }
}

function load_page(url) {
  if (typeof url != 'string') {
    url = this.href;
  }
  if (url === '') return false;

  $.get( url, function( data ) {
    $( "#maincontent" ).html( data );
    reload_reload_theme();
    process_form();
  });
  return false;
}

function process_form(){
  $('form').each(function(){
    $(this).on('submit',function(){
      var form = $(this);
      $.ajax({
        method: form.attr('method'),
        url: form.attr('action'),
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(prepare_form_data(form))
      }).done(function( response ) {
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

function prepare_form_data(form){
  var formdata = [];

  var form_type = form.attr('action').split('/').pop();
  var re = /sensor_(\d+)_(.*)/i;
  var objectdata = {};
  var previd = -1;

  if (form_type === 'weather' || form_type === 'environment') {
    formdata = {};
  }

  try {
    form.find('input:not([disabled="disabled"]),select:not([disabled="disabled"])').each(function(){
      var field_name = $(this).attr('name');
      var field_value = $(this).val();

      switch(form_type) {
        case 'weather':
          formdata[field_name] = field_value;
          break;

        case 'sensors':
        case 'switches':
        case 'environment':
          if (form_type === 'switches') {
            re = /switch_(\d+)_(.*)/i;
          } else if (form_type === 'environment') {
            re = /(lights|humidity|heater)_(.*)/i;
          }
          if ((matches = re.exec(field_name)) !== null) {
            if (matches.index === re.lastIndex) {
                re.lastIndex++;
            }
            if (matches.length == 3) {
              if (previd != matches[1]) {
                if (Object.keys(objectdata).length > 1){
                  formdata[(form_type == 'switches' ? (previd * 1) -1 : previd)] = $.extend(true, {}, objectdata);
                }
                // New tiem
                objectdata = {};
                previd = matches[1];
              }
              if (matches[2] === 'on' || matches[2] === 'off') {
                field_value = moment(field_value,'LT').unix();
              }
              objectdata[matches[2]] = field_value;
            }
          }
          break;
      }
    });
    if (form_type === 'sensors' || form_type === 'switches' || form_type === 'environment') {
      formdata[(form_type == 'switches' ? (previd * 1) -1 : previd)] = $.extend(true, {}, objectdata);
    }

    console.log('Prepare form data: ', formdata);
  } catch(error) {
    console.log(error);
    return false;
  }
  return formdata;
}

function update_dashboard_tile(tile,text) {
  var div = $('div.tile_count #' + tile + ' div.count');
  if (div.length == 1 && div.text() != text) {
    div.text(text);
    var oldColor = div.css('color');
    div.addClass('green');
    div.animate({ color: jQuery.Color(oldColor) }, 1000, function() {
      $(this).removeClass('green').css('color','');
    });
  }
}

function update_dashboard_uptime(data) {
  update_dashboard_tile('uptime',format_uptime(data.uptime));
  $("#uptime .progress-bar-success").css('height', (data.load[0] * 100) + '%');
  $("#uptime .progress-bar-warning").css('height', (data.load[1] * 100) + '%');
  $("#uptime .progress-bar-danger").css('height', (data.load[2] * 100) + '%');
}

function update_dashboard_power_usage(data){
  update_dashboard_tile('power_wattage',data.current + '/' + data.max);
  var percentage = (data.max > 0 ? (data.current / data.max) * 100 : 0);
  $("#power_wattage .progress-bar-success").css('height', percentage + '%');
}

function update_dashboard_water_flow(data){
  update_dashboard_tile('water_flow',data.current + '/' + data.max);
  var percentage = (data.max > 0 ? (data.current / data.max) * 100 : 0);
  $("#water_flow .progress-bar-info").css('height', percentage + '%');
}

function update_dashboard_weather(data) {
  var icons = new Skycons({
      "color": "#73879C"
  });

  if ($('div#weather_today').length == 1) {


    $('div#weather_today .temperature').html(moment(data.hour_forecast[0].from * 1000).format('[<b>]dddd[</b>,] LT') + ' <span> in <b>' + data.temperature + '</b></span>');
    $('div#weather_today .weather-text h2').html(data.city.city + '<br><i>' + data.hour_forecast[0].weather + '</i>');

    $('div#weather_today .sunrise').text(moment(data.sun.rise * 1000).format('LT')).parent().css('fontWeight',(data.day ? 'bold' : 'normal'));
    $('div#weather_today .sunset').text(moment(data.sun.set * 1000).format('LT')).parent().css('fontWeight',(data.day ? 'normal' : 'bold'));

    $('div#weather_today .degrees').text(data.hour_forecast[0].temperature);
    icons.set($('div#weather_today canvas').attr('id'), data.hour_forecast[0].icon);

    var week_forecast_divs = $('div#weather_today div.row.weather-days div.daily-weather');
    // Set timestamp to tomorrow at 13 hours. That is the first week forecast we take
    var timestamp = Math.round(new Date(Date.now()).setHours(13) / 1000) + (24 * 60 * 60);
    var day_counter = 0;
    $.each(data.week_forecast, function(index,value) {
      if ( value.from - timestamp >= 3600 && day_counter < week_forecast_divs.length) {
        $(week_forecast_divs[day_counter]).find('.day').text(moment(value.from * 1000).format('ddd'));
        $(week_forecast_divs[day_counter]).find('.degrees').text(value.temperature);
        $(week_forecast_divs[day_counter]).find('h5').html(value.wind_speed.toFixed(1) + ' <i>' + (data.windspeed === 'ms' ? 'm/s' : 'Km/h') + '</i>');
        icons.set($(week_forecast_divs[day_counter]).find('canvas').attr('id'), value.icon);
        day_counter++;
        timestamp += (24 * 60 * 60);
      }
    });
    icons.play();

  }
}

function update_dashboard_power_switches(data) {
  $.each(data.switches,function(index,value){
    var power_switch = $('div#pw' + value.nr + '.power-switch');
    if (power_switch.length == 1) {
      // Set current state to div for toggleing
      power_switch.attr('data-state',value.state ? 1 : 0);

      power_switch.find('h2.title').text(value.name);
      power_switch.find('h5').html(value.power_wattage + ' <i>W</i>' + (value.water_flow > 0 ? '<br />' + value.water_flow + '<i>l/s</i>' : ''));
      power_switch.find('span').removeClass('blue green').addClass((value.state ? 'green' : 'blue'));

      // Check if the click trigger already has been set
      if (!Boolean(power_switch.attr('data-loaded'))) {
        // If not, set a click trigger to toggle the power switch
        power_switch.on('click',function(){
          var power_switch = $(this);
          websocket_message({'type':'toggle_switch', 'data' : {'nr': power_switch.attr('id').substr(2)*1,
                                                               'state' : !Boolean(power_switch.attr('data-state')*1)}});
        });
        // Set the data value to 1 so next round, this click action is not bind again and again
        power_switch.attr('data-loaded',1);
      }
    }
  });
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

  globals.online_timer = setTimeout(function(){
    is_offline();
  }, 120 * 1000);
}

function update_door_messages(online) {
  var title = (online ? 'Open' : 'Close');
  var message = (online ? 'Door has been opend!' : 'Door is closed');
  var icon = (online ? 'fa-lock' : 'fa-unlock');
  var color = (online ? 'green' : 'red');
  add_notification_message('door_messages',title,message,icon,color);
}

function update_online_messages(online) {
  var title = (online ? 'Online' : 'Offline');
  var message = (online ? 'Connection restored!' : 'Connection lost!');
  var icon = (online ? 'fa-check-circle-o' : 'fa-exclamation-triangle');
  var color = (online ? 'green' : 'red');
  add_notification_message('online_messages',title,message,icon,color);
}

function add_notification_message(type,title,message,icon,color) {
  var menu = $('ul#' + type);

  var notification = $('<a>').on('click',function(){
    close_notification_message(this);
  });
  notification.append($('<span>').addClass('image').append($('<img>').attr({'src':$('a.user-profile img').attr('src'),'alt':'Profile image'})));
  notification.append($('<span>').append($('<span>').text(title)).append($('<span>').addClass('time notification_timestamp').attr('timestamp',(new Date()).getTime()).text('...')));
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
    var duration = moment.duration( (now - timestamp) * -1);
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
          $BOX_CONTENT.slideToggle(200, function(){
              $BOX_PANEL.removeAttr('style');
          });
      } else {
          $BOX_CONTENT.slideToggle(200);
          $BOX_PANEL.css('height', 'auto');
      }

      $ICON.toggleClass('fa-chevron-up fa-chevron-down');
  });

  $('.close-link').click(function () {
      var $BOX_PANEL = $(this).closest('.x_panel');

      $BOX_PANEL.remove();
  });
}

function reload_reload_theme() {

  // Panel toolbox
  load_panel_tool_box();

  // Tooltip
  //$(document).ready(function() {
      $('[data-toggle="tooltip"]').tooltip({
          container: 'body'
      });
  //});
  // /Tooltip

  // Switchery
  //$(document).ready(function() {
      if ($(".js-switch")[0]) {
          var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch'));
          elems.forEach(function (html) {
              var switchery = new Switchery(html, {
                  color: '#26B99A'
              });
          });
      }
  //});
  // /Switchery

  // iCheck
  //$(document).ready(function() {
      if ($("input.flat")[0]) {
          $(document).ready(function () {
              $('input.flat').iCheck({
                  checkboxClass: 'icheckbox_flat-green',
                  radioClass: 'iradio_flat-green'
              });
          });
      }
  //});
  // /iCheck
}

function sensor_gauge(name,data) {
  //console.log('Update gauge: ' + name, data);
  if ($('#sensor_' + name).length == 1) {
    // Update title
    if (data.type !== undefined && data.name !== undefined) {
      $('#sensor_' + name + ' span.title').text(data.type + ' sensor: ' + (data.name !== '' ? data.name : data.address));
    }
    // Update timestamp indicator
    $('#sensor_' + name + ' small.data_update').text(moment().format('LLL'));

    // Setup a new gauge if needed
    if (globals.gauges[name] === undefined) {
      var valid_area = data.alarm_max - data.alarm_min;
      var colors = [
                    [0.0, $.Color(get_theme_color('red')).toHexString()],
                    [ (data.alarm_min - (0)) / (data.max - data.min) , $.Color(get_theme_color('orange')).toHexString() ],
                    [ (data.alarm_min + (valid_area/2)) / (data.max - data.min) , $.Color(get_theme_color('green')).toHexString() ],
                    [ (data.alarm_max + (0)) / (data.max - data.min) , $.Color(get_theme_color('orange')).toHexString() ],
                    [1.0, $.Color(get_theme_color('red')).toHexString()]
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

    //console.log('Update gauge: ' + name + ' DONE!');
  }
}

function history_graph(name,data,type) {
  if (type === undefined){
    type = 'temperature';
  }
  switch(type) {
    case 'temperature':
    case 'humidity':
      graph_data = [data.current, data.alarm_min, data.alarm_max];
      show_splines = true;
      show_lines = false;
      fill = false;
      break;

    case 'switch':
      graph_data = [data.power_wattage, data.water_flow];
      show_splines = false;
      show_lines = true;
      fill = true;
      break;
  }


  //console.log('Update graph: ' + name);
  if ($('#history_graph_' + name).length == 1) {
    $('#history_graph_' + name).html('').removeClass('loading');
    $('div.history_graph#history_graph_' + name).css('height',$('div.history_graph#history_graph_' + name).parents('div.x_content').height() + 'px');

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
         tickSize: [90, "minute"],
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
    //console.log('Update graph: ' + name + ' DONE!');
  }
}
