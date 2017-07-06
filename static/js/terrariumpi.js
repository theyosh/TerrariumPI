'use strict';

var globals = {
  websocket: null,
  connection: 'ws' + (location.protocol == 'https:' ? 's' : '') + '://' + location.host + '/live',
  gauges: [],
  webcams: [],
  graphs: {},
  graph_cache: 5 * 60,
  websocket_timer: null,
  online_timer: null
};

/**
 * Resize function without multiple trigger
 * 
 * Usage:
 * $(window).smartresize(function(){  
 *     // code here
 * });
 */
(function($,sr){
    // debouncing function from John Hann
    // http://unscriptable.com/index.php/2009/03/20/debouncing-javascript-methods/
    var debounce = function (func, threshold, execAsap) {
      var timeout;

        return function debounced () {
            var obj = this, args = arguments;
            function delayed () {
                if (!execAsap)
                    func.apply(obj, args); 
                timeout = null; 
            }

            if (timeout)
                clearTimeout(timeout);
            else if (execAsap)
                func.apply(obj, args);

            timeout = setTimeout(delayed, threshold || 100); 
        };
    };

    // smartresize 
    jQuery.fn[sr] = function(fn){  return fn ? this.bind('resize', debounce(fn)) : this.trigger(sr); };

})(jQuery,'smartresize');

function websocket_init(reconnect) {
  websocket_connect();
  globals.websocket.onopen = function(evt) {
    websocket_message({
      'type': 'client_init',
      'reconnect': reconnect
    });
  };
  globals.websocket.onmessage = function(evt) {
    online_updater();
    var data = JSON.parse(evt.data);
    switch (data.type) {
      case 'uptime':
        update_dashboard_uptime(data.data);
        break;
      case 'power_usage_water_flow':
        update_dashboard_power_usage(data.data.power);
        update_dashboard_water_flow(data.data.water);
        break;

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
    // Reset the main content height
    $("#maincontent").height(0);
    // Load the data through AJAX
    $.get(url, function(data) {
      // Get the menu url so that jQuery can match
      var menu_url = $('<a/>').attr('href',url)[0].pathname.replace(/^[^\/]/,'/').substr(1);
      // Clear all submenu's that are not clicked
      $('.child_menu a[href!="' + menu_url + '"]').parent().removeClass('active');
      $('.child_menu a[href="' + menu_url + '"]').parent().addClass('active');
      // Put the content on the page
      $("#maincontent").html(data);

      $("#maincontent a").each(function(index,item){
        $(item).attr('title',$(item).text());
      });
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
            type: 'success',
            title: response.title,
            text: response.message,
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
  var re = /(sensor|switch|webcam|light|sprayer|heater|door)(_\d+)?_(.*)/i;
  var matches = null;
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
        case 'doors':
          if ((matches = re.exec(field_name)) !== null) {
            if (matches.index === re.lastIndex) {
              re.lastIndex++;
            }
            var current_nr = -1;
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
  $('#system_time span').text(moment(data.timestamp * 1000).format('LLLL'));
  $('#system_time i').removeClass('fa-clock-o fa-sun-o fa-moon-o').addClass((data.day ? 'fa-sun-o' : 'fa-moon-o'));
  $("#uptime .progress-bar-success").css('height', (data.load[0] * 100) + '%');
  $("#uptime .progress-bar-warning").css('height', (data.load[1] * 100) + '%');
  $("#uptime .progress-bar-danger").css('height', (data.load[2] * 100) + '%');
}

function update_dashboard_power_usage(data) {
  update_dashboard_tile('power_wattage', data.current + '/' + data.max);
  var percentage = (data.max > 0 ? (data.current / data.max) * 100 : 0);
  $("#power_wattage .progress-bar-success").css('height', percentage + '%');
  data.total /= 1000;
  $("#total_power .count_bottom .costs span").text((data.price * data.total).toFixed(3));
  $("#total_power .count_bottom span.duration").text(moment.duration(data.duration * 1000).humanize());
  update_dashboard_tile('total_power', data.total.toFixed(2));
}

function update_dashboard_water_flow(data) {
  update_dashboard_tile('water_flow', data.current + '/' + data.max);
  var percentage = (data.max > 0 ? (data.current / data.max) * 100 : 0);
  $("#water_flow .progress-bar-info").css('height', percentage + '%');
  $("#total_water .count_bottom .costs span").text((data.price * (data.total / 1000)).toFixed(3));
  $("#total_water .count_bottom span.duration").text(moment.duration(data.duration * 1000).humanize());
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
        $(week_forecast_divs[day_counter]).find('h5').html(value.wind_speed.toFixed(1) + ' <i>' + (data.windspeed === 'ms' ? '{{_('m/s')}}' : '{{_('Km/h')}}') + '</i>');
        $(week_forecast_divs[day_counter]).find('canvas').attr('title',value.weather);
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
  if (systempart.length === 0) {
    return;
  }
  try {
    var enabledColor = '';
    switch (name) {
      case 'light':
        enabledColor = 'orange';
        systempart.find('h4 small span').text(value.modus);
        systempart.find('.on').text(moment(value.on * 1000).format('LT'));
        systempart.find('.off').text(moment(value.off * 1000).format('LT'));
        systempart.find('.duration').text(moment.duration(Math.abs(value.off - value.on) * 1000).humanize());
        break;
      case 'sprayer':
        enabledColor = 'blue';
        systempart.find('.current').text(value.current.toFixed(3) + ' %');
        systempart.find('.alarm_min').text(value.alarm_min.toFixed(3) + ' %');
        systempart.find('span.glyphicon-warning-sign').toggle(value.alarm);
        break;
      case 'heater':
        enabledColor = 'red';
        systempart.find('h4 small span').text(value.modus);
        systempart.find('.current').text(value.current.toFixed(3) + ' °C');
        systempart.find('.alarm_min').text(value.alarm_min.toFixed(3) + ' °C');
        systempart.find('.alarm_max').text(value.alarm_max.toFixed(3) + ' °C');
        systempart.find('span.glyphicon-warning-sign').toggle(value.alarm);
        break;
    }
    systempart.find('h4').removeClass('orange blue red').addClass(value.enabled ? enabledColor : '').attr('title', value.enabled ? '{{_('Enabled')}}' : '{{_('Disabled')}}');
    systempart.find('.state i').removeClass('red green').addClass(value.state === 'on' ? 'green' : 'red').attr('title', value.state === 'on' ? '{{_('On')}}' : '{{_('Off')}}');
  } catch (error) {
      // Just ignore....
  }
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
  var title   = (online ? '{{_('Open')}}' : '{{_('Close')}}');
  var message = (online ? '{{_('Door is open')}}' : '{{_('Door is closed')}}');
  var icon    = (online ? 'fa-unlock' : 'fa-lock');
  var color   = (online ? 'red' : 'green');
  add_notification_message('door_messages', title, message, icon, color);
}

function update_online_messages(online) {
  var title   = (online ? '{{_('Online')}}' : '{{_('Offline')}}');
  var message = (online ? '{{_('Connection restored')}}' : '{{_('Connection lost')}}');
  var icon    = (online ? 'fa-check-circle-o' : 'fa-exclamation-triangle');
  var color   = (online ? 'green' : 'red');
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
    'alt': '{{_('Profile image')}}'
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
  online_indicator.find('span').text('{{_('Online')}}');
  online_indicator.find('i.fa').removeClass('fa-check-circle-o fa-exclamation-triangle red green').addClass('fa-check-circle-o green');
  update_online_messages(true);
}

function is_offline() {
  var online_indicator = $('a#online_indicator');
  online_indicator.find('span').text('{{_('Offline')}}');
  online_indicator.find('i.fa').removeClass('fa-check-circle-o fa-exclamation-triangle red green').addClass('fa-exclamation-triangle red');
  update_online_messages(false);
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
  online_indicator.find('span').text('{{_('Door is open')}}');
  online_indicator.find('i.fa').removeClass('fa-lock fa-unlock red green').addClass('fa-unlock red');
  update_door_messages(true);
}

function door_closed() {
  var online_indicator = $('a#door_indicator');
  online_indicator.find('span').text('{{_('Door is closed')}}');
  online_indicator.find('i.fa').removeClass('fa-lock fa-unlock red green').addClass('fa-lock green');
  update_door_messages(false);
}

function get_theme_color(color) {
  if (color == 'orange') return '#f0ad4e';
  return $('<div>').addClass(color).css('color');
}

var CURRENT_URL = window.location.href.split('#')[0].split('?')[0],
    $BODY = $('body'),
    $MENU_TOGGLE = $('#menu_toggle'),
    $SIDEBAR_MENU = $('#sidebar-menu'),
    $SIDEBAR_FOOTER = $('.sidebar-footer'),
    $LEFT_COL = $('.left_col'),
    $RIGHT_COL = $('.right_col'),
    $NAV_MENU = $('.nav_menu'),
    $FOOTER = $('footer');

// Sidebar
function init_sidebar() {
  // TODO: This is some kind of easy fix, maybe we can improve this
  var setContentHeight = function () {
    // reset height
    $RIGHT_COL.css('min-height', $(window).height());
  
    var bodyHeight = $BODY.outerHeight(),
      footerHeight = $BODY.hasClass('footer_fixed') ? -10 : $FOOTER.height(),
      leftColHeight = $LEFT_COL.eq(1).height() + $SIDEBAR_FOOTER.height(),
      contentHeight = bodyHeight < leftColHeight ? leftColHeight : bodyHeight;
  
    // normalize content
    contentHeight -= $NAV_MENU.height() + footerHeight;
  
    $RIGHT_COL.css('min-height', contentHeight);
  };

  $SIDEBAR_MENU.find('a').on('click', function(ev) {
	  console.log('clicked - sidebar_menu');
        var $li = $(this).parent();

        if ($li.is('.active')) {
            $li.removeClass('active active-sm');
            $('ul:first', $li).slideUp(function() {
                setContentHeight();
            });
        } else {
            // prevent closing menu if we are on child menu
            if (!$li.parent().is('.child_menu')) {
                $SIDEBAR_MENU.find('li').removeClass('active active-sm');
                $SIDEBAR_MENU.find('li ul').slideUp();
            }else
            {
				if ( $BODY.is( ".nav-sm" ) )
				{
					$SIDEBAR_MENU.find( "li" ).removeClass( "active active-sm" );
					$SIDEBAR_MENU.find( "li ul" ).slideUp();
				}
			}
            $li.addClass('active');

            $('ul:first', $li).slideDown(function() {
                setContentHeight();
            });
        }
    });

  // toggle small or large menu 
  $MENU_TOGGLE.on('click', function() {
		console.log('clicked - menu toggle');
		
		if ($BODY.hasClass('nav-md')) {
			$SIDEBAR_MENU.find('li.active ul').hide();
			$SIDEBAR_MENU.find('li.active').addClass('active-sm').removeClass('active');
		} else {
			$SIDEBAR_MENU.find('li.active-sm ul').show();
			$SIDEBAR_MENU.find('li.active-sm').addClass('active').removeClass('active-sm');
		}

  	$BODY.toggleClass('nav-md nav-sm');
  	setContentHeight();
  });

	// check active menu
	$SIDEBAR_MENU.find('a[href="' + CURRENT_URL + '"]').parent('li').addClass('current-page');

	$SIDEBAR_MENU.find('a').filter(function () {
		return this.href == CURRENT_URL;
	}).parent('li').addClass('current-page').parents('ul').slideDown(function() {
		setContentHeight();
	}).parent().addClass('active');

	// recompute content when resizing
	$(window).smartresize(function(){  
		setContentHeight();
	});

	setContentHeight();

	// fixed sidebar
	if ($.fn.mCustomScrollbar) {
		$('.menu_fixed').mCustomScrollbar({
			autoHideScrollbar: true,
			theme: 'minimal',
			mouseWheel:{ preventDefault: true }
		});
	}
};
// /Sidebar

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
  $('[data-toggle="tooltip"]').tooltip({
    container: 'body',
    html: true
  });  
  process_form();
}

function sensor_gauge(name, data) {
  if ($('#' + name + ' .gauge').length == 1) {
    // Update title
    if (data.type !== undefined && data.name !== undefined) {
      $('#' + name + ' span.title').text(data.type + ' {{_('sensor')}}: ' + (data.name !== '' ? data.name : data.address));
    }
    // Update timestamp indicator
    $('#' + name + ' small').text(moment().format('LLL'));
    // Setup a new gauge if needed
    if ($('#' + name + ' .gauge').attr('done') === undefined) {
      var total_area = data.max - data.min;
/*
      var colors = [
        [0.00, '#E74C3C'],
        [0.25, '#f0ad4e'],
        [0.50, '#1ABB9C'],
        [0.75, '#f0ad4e'],
        [1.00, '#E74C3C']
      ];
*/
      var colors = [
        [0.00, '#E74C3C'],
        [(data.alarm_min - data.min) / total_area, '#f0ad4e'],
        [(((data.alarm_min + data.alarm_max)/2) - data.min) / total_area, '#1ABB9C'],
        [(data.alarm_max - data.min) / total_area, '#f0ad4e'],
        [1.00, '#E74C3C']
      ];

      var opts = {
        animationSpeed: 32,
        lines: 12,
        angle: 0,
        lineWidth: 0.6,
        pointer: {
          length: 0.80,
          strokeWidth: 0.070,
          color: '#1D212A'
        },
        limitMax: 'false',
        strokeColor: '#F0F3F3',
        generateGradient: true,
        minValue: data.min,
        maxValue: data.max,
        percentColors: colors,
      };
      // Init Gauge
      $('#' + name + ' .gauge').attr('done',1);
      globals.gauges[name] = new Gauge($('#' + name + ' .gauge')[0]).setOptions(opts);
      globals.gauges[name].setTextField($('#' + name + ' .gauge-value')[0]);
    }
    // Update values
    globals.gauges[name].minValue = data.min;
    globals.gauges[name].maxValue = data.max;
    globals.gauges[name].set(data.current);
    $('div#' + name + ' .x_title h2 .badge').toggle(data.alarm);
  }
}

function load_history_graph(id,type,data_url,nocache) {
  if ($('#' + id + ' .history_graph').length === 1) {
    var now = + new Date();
    var data = [];
    if (type === undefined) {
      type = 'temperature';
    }
    if (nocache === undefined) {
      nocache = 0;
    }
    if (globals.graphs[id] === undefined) {
      globals.graphs[id] = {'timestamp' : 0,
                            'type' : type,
                            'data' : [],
                            'timer': null };
    }

    if ($('#' + id + ' .history_graph.loading').length === 1) {
    // Create period menu items
      var menu_items = $('#' + id + ' ul.dropdown-menu.period a');
      $.each(['day','week','month','year'],function(index,value){
        if (index === 0) {
          $(menu_items[index]).parent().addClass('focus');
        }
        $(menu_items[index]).off('click');
        $(menu_items[index]).on('click', function(){
          $(this).parent().siblings().removeClass('focus');
          $(this).parent().addClass('focus');
          load_history_graph(id,type,data_url + '/' + value ,1);
        });
      });
    }
    if (nocache === 0 && now - globals.graphs[id].timestamp < globals.graph_cache * 1000) {
      history_graph(id, globals.graphs[id].data, type);
      clearTimeout(globals.graphs[id].timer);
      globals.graphs[id].timer = setTimeout(function() {
          load_history_graph(id,type,data_url);
      }, 1 * 60 * 1000);

    } else {
      // Load fresh data...
      $.getJSON(data_url, function(online_data) {
        $.each(online_data, function(dummy, value) {
          $.each(value, function(dummy, data_array) {
            globals.graphs[id].timestamp = now;
            if (type == 'switch') {
              globals.graphs[id].data = process_switch_data(data_array);
            } else if (type == 'door') {
              globals.graphs[id].data = process_door_data(data_array);
            } else {
              globals.graphs[id].data = data_array;
            }
          });
        });

        history_graph(id, globals.graphs[id].data, type);
        clearTimeout(globals.graphs[id].timer);
        globals.graphs[id].timer = setTimeout(function() {
          load_history_graph(id,type,data_url);
        }, 1 * 60 * 1000);

      });
    }

  }
  return false;
}

function history_graph(name, data, type) {
  if (type === undefined) {
    type = 'temperature';
  }

  var graph_data = [];
  var graph_options = {
    tootip: true,
    series: {
      curvedLines: {
        apply: true,
        active: true,
        monotonicFit: true,
      },
      shadowSize: 2
    },
    grid: {
      verticalLines: true,
      hoverable: true,
      clickable: false,
      tickColor: "#d5d5d5",
      borderWidth: 1,
      color: '#fff'
    },
    colors: ["rgba(38, 185, 154, 0.38)", "rgba(3, 88, 106, 0.38)", "rgba(3, 88, 106, 0.38)"],
    xaxis: {
      tickColor: "rgba(51, 51, 51, 0.06)",
      mode: "time",
      timezone: "browser",
      tickSize: [60, "minute"],
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
      ticks: (type === 'door' ? [[0, '{{_('closed')}}'], [1, '{{_('open')}}']] : 8),
      tickColor: "rgba(51, 51, 51, 0.06)",
      tickDecimals: 1,
      tickFormatter: function(val, axis) {
        switch(type) {
          case 'system_memory':
              val = (val / (1024 * 1024)).toFixed(axis.tickDecimals) + ' MB';
            break;

          case 'system_uptime':
              val = moment.duration(val * 1000).humanize();
            break;

          case 'weather':
            val = val.toFixed(axis.tickDecimals) + ' °C';
            break;

          case 'humidity':
            val = val.toFixed(axis.tickDecimals) + ' %';
            break;

          case 'switch':
            val = val.toFixed(axis.tickDecimals) + ' W';
            break;
          
          case 'door':
            val = (val ? '{{_('open')}}' : '{{_('closed')}}');
            break;

          default:
            val = val.toFixed(axis.tickDecimals) + (type.indexOf('temperature') !== -1 ? ' °C' : ' %');
            break;
        }
        return val;
      }
    }
  };

  switch (type) {
    case 'temperature':
    case 'humidity':
      graph_data = [{
        label: '{{_('Current')}}',
        data: data.current
      }, {
        label: '{{_('Alarm min')}}',
        data: data.alarm_min
      }, {
        label: '{{_('Alarm max')}}',
        data: data.alarm_max
      }];
      break;
    case 'weather':
    case 'system_temperature':
      graph_data = [{
        label: '{{_('Temperature')}}',
        data: data
      }];
      break;
    case 'system_uptime':
      delete(graph_options.series.curvedLines);
      graph_options.series.lines = {
        show: true,
        lineWidth: 2,
        fill: false
      };

      graph_data = [{
        label: '{{_('Uptime')}}',
        data: data
      }];

      $('div.row.uptime .x_title small').text(moment.duration(data[data.length-1][1] * 1000).humanize());
      break;
    case 'system_load':
      graph_data = [{
        label: '{{_('Load')}}',
        data: data.load1
      }, {
        label: '{{_('Load 5')}}',
        data: data.load5
      }, {
        label: '{{_('Load 15')}}',
        data: data.load15
      }];
      break;
    case 'system_memory':
      graph_data = [{
        label: '{{_('Used memory')}}',
        data: data.used
      }, {
        label: '{{_('Free memory')}}',
        data: data.free
      }, {
        label: '{{_('Total memory')}}',
        data: data.total
      }];
      break;
    case 'switch':
      delete(graph_options.series.curvedLines);
      graph_options.series.lines = {
        show: true,
        lineWidth: 2,
        fill: true
      };

      graph_data = [data.power_wattage, data.water_flow];
      graph_data = [{
        label: '{{_('Power usage in Watt')}}',
        data: data.power_wattage
      }, {
        label: '{{_('Water flow in L/m')}}',
        data: data.water_flow
      }];
      break;
    case 'door':
      delete(graph_options.series.curvedLines);
      graph_options.series.lines = {
        show: true,
        lineWidth: 2,
        fill: true
      };

      graph_data = [data.state];
      graph_data = [{
        label: '{{_('Door status')}}',
        data: data.state
      }];
      break;
      
  }
  if (graph_data[0].data.length > 0) {
    var total_data_duration = (graph_data[0].data[graph_data[0].data.length - 1][0] - graph_data[0].data[0][0]) / 3600000;
    graph_options.xaxis.tickSize[0] = Math.round(total_data_duration * 2.5);
  }

  if ($('#' + name + ' .history_graph').length == 1) {
    $('#' + name + ' .history_graph').html('').removeClass('{{_('loading')}}');
    $.plot($('#' + name + ' .history_graph'), graph_data, graph_options);

    if (type == 'switch') {
      var usage = '';
      if (data.total_power_usage > 0) {
        usage = '{{_('Total power in kWh')}}: ' + Math.round(data.total_power_usage) / 1000;
      }
      if (data.total_water_usage > 0) {
        usage += (usage != '' ? ', ' : '') + '{{_('Total water in L')}}: ' + Math.round(data.total_water_usage * 100) / 100;
      }
      $('#' + name + ' .total_usage').text(usage);
    }
    $('#' + name + ' .history_graph').bind('plothover', function (event, pos, item) {
      if (item) {
        $('#tooltip').css({top: item.pageY-5, left: item.pageX-5});
        $('#tooltip span').attr('data-original-title',moment(item.datapoint[0]).format('LLL') + '<br />' + item.series.label + ' ' + item.series.yaxis.tickFormatter(item.datapoint[1],item.series.yaxis));
      }
    });
  }
}

function update_power_switch(id, data) {
  var power_switch = $('#switch_' + id);
  power_switch.find('h2 span.title').text('{{_('Switch')}} ' + data.name);
  power_switch.find('h2 small.data_update').text(data.power_wattage + 'W' + (data.water_flow > 0 ? ', ' + data.water_flow + 'L/m' : ''));
  power_switch.find('span.glyphicon').removeClass('blue green').addClass((data.state ? 'green' : 'blue'));
}

function toggleSwitch(id) {
  id = id.split('_')[1];
  $.getJSON('/api/switch/toggle/' + id,function(data){
  });
}

function process_switch_data(raw_data) {
  var graphdata = {
    power_wattage: [],
    water_flow: [],
    total_power_usage : 0,
    total_water_usage : 0
  };
  var state_change = -1;
  $.each(raw_data.state, function(counter, status) {
    if (!status[1]) {
      raw_data.power_wattage[counter][1] = 0;
      raw_data.water_flow[counter][1] = 0;
    }
    var copy = {};
    if (counter > 0 && state_change != status[1]) {
      // Copy previous object to get the right status with current timestamp
      copy = $.extend(true, {}, raw_data.power_wattage[counter - 1]);
      if (copy[0] != 0) {
        graphdata.total_power_usage += (status[0] - copy[0]) / 1000 * copy[1]
      }
      copy[0] = status[0];
      graphdata.power_wattage.push(copy);
      copy = $.extend(true, {}, raw_data.water_flow[counter - 1]);
      if (copy[0] != 0) {
        graphdata.total_water_usage += (status[0] - copy[0]) / 1000 * copy[1]
      }
      copy[0] = status[0];
      graphdata.water_flow.push(copy);
      state_change = status[1];
    }
    graphdata.power_wattage.push(raw_data.power_wattage[counter]);
    graphdata.water_flow.push(raw_data.water_flow[counter]);
    if (counter == raw_data.state.length - 1) {
      // Add endpoint which is a copy of the last point, with current time
      copy = $.extend(true, {}, raw_data.power_wattage[counter]);
      if (copy[0] != 0) {
        graphdata.total_power_usage += ((new Date()).getTime() - copy[0]) / 1000 * copy[1]
      }
      copy[0] = (new Date()).getTime();
      graphdata.power_wattage.push(copy);
      copy = $.extend(true, {}, raw_data.water_flow[counter]);
      if (copy[0] != 0) {
        graphdata.total_water_usage += ((new Date()).getTime() - copy[0]) / 1000 * copy[1]
      }
      copy[0] = (new Date()).getTime();
      graphdata.water_flow.push(copy);
    }
  });
  graphdata.total_power_usage /= 3600
  graphdata.total_water_usage /= 60
  return graphdata;
}

function process_door_data(raw_data) {
  var graphdata = {
    state: []
  };
  var state_change = -1;
  $.each(raw_data.state, function(counter, status) {
    status[1] = (status[1] === 'closed' ? 0 : 1)
    if (!status[1]) {
      raw_data.state[counter][1] = 0;
    }
    var copy = {};
    if (counter > 0 && state_change != status[1]) {
      // Copy previous object to get the right status with current timestamp
      copy = $.extend(true, {}, raw_data.state[counter - 1]);
      copy[0] = status[0];
      graphdata.state.push(copy);
      state_change = status[1];
    }
    graphdata.state.push(raw_data.state[counter]);
    if (counter == raw_data.state.length - 1) {
      // Add endpoint which is a copy of the last point, with current time
      copy = $.extend(true, {}, raw_data.state[counter]);
      copy[0] = (new Date()).getTime();
      graphdata.state.push(copy);
    }
  });
  return graphdata;
}

function update_webcam_preview(name, url) {
  $('img#webcam_' + name + '_preview').attr('src', url);
}

function initWebcam(webcamid, name, maxzoom) {
  if ($('div#webcam_' + webcamid).length === 1) {
    $('div#webcam_' + webcamid).parents('.x_panel').find('h2 small').text(name);
    if (!$('div#webcam_' + webcamid).hasClass('leaflet-container')) {
      globals.webcams[webcamid] = null;
      var webcam = new L.Map('webcam_' + webcamid, {
        layers: [createWebcamLayer(webcamid, maxzoom)],
        fullscreenControl: true,
      }).setView([0, 0], 1);
      var loadingControl = L.Control.loading({
        separate: true
      });
      webcam.addControl(loadingControl);
      updateWebcam(webcam);
    }
  }
}

function updateWebcam(webcam) {
  if ($('div#' + webcam._container.id).length === 1) {
    webcam.eachLayer(function(layer) {
      layer.redraw();
    });
    clearTimeout(globals.webcams[webcam._container.id]);
    globals.webcams[webcam._container.id] = setTimeout(function() { updateWebcam(webcam);},30 * 1000);
  }
}

function createWebcamLayer(webcamid, maxzoom) {
  return L.tileLayer('/webcam/{id}_tile_{z}_{x}_{y}.jpg?_{time}', {
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

function capitalizeFirstLetter(string) {
    return string[0].toUpperCase() + string.slice(1);
}


$(document).ready(function() {
  init_sidebar();

  moment.locale($('html').attr('lang'));
  $('#system_time span').text(moment().format('LLLL'));
  websocket_init(false);
  // Bind to menu links in order to load Ajax calls
  $('#sidebar-menu a').each(function() {
    $(this).on('click', load_page).attr('title',$(this).parents('li').find('a:first').text());
  });
  // NProgress bar animation during Ajax calls
  $(document).on({
    ajaxStart: function() {
      NProgress.start();
    },
    ajaxComplete: function() {
      NProgress.done();
    }
  });

  $("<div id='tooltip'><span title='tooltip' id='tooltiptext' data-toggle='tooltip'>&nbsp;&nbsp;&nbsp;</span></div>").css({
      position: "absolute",
	}).appendTo("body");

  load_page('dashboard.html');

  setInterval(function() {
    notification_timestamps();
    $('#system_time span').text(moment().format('LLLL'));
  }, 30 * 1000);
});
