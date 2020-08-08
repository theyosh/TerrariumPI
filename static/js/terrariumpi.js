'use strict';

var globals = {
  websocket: null,
  connection: 'ws' + (location.protocol == 'https:' ? 's' : '') + '://' + location.host + '/live',
  temperature_indicator: 'C',
  distance_indicator: 'cm',
  gauges: [],
  graphs: {},
  graph_cache: 1 * 60,
  websocket_timer: null,
  online_timer: null,
  current_version: null,
  language: null,
  ajaxloader: 0,
  horizontal_legend: 0,
  reboot: false,
};
// Single variable that is used for loading the status and settings rows for: sensors, power switches, door indicators etc
var source_row = null;
// Translations for dataTable module
var dataTableTranslations = {
  'en' : '//cdn.datatables.net/plug-ins/1.10.19/i18n/English.json',
  'nl' : '//cdn.datatables.net/plug-ins/1.10.19/i18n/Dutch.json',
  'de' : '//cdn.datatables.net/plug-ins/1.10.19/i18n/German.json',
  'it' : '//cdn.datatables.net/plug-ins/1.10.19/i18n/Italian.json',
  'fr' : '//cdn.datatables.net/plug-ins/1.10.19/i18n/France.json',
  'no' : '//cdn.datatables.net/plug-ins/1.10.19/i18n/Norwegian-Bokmal.json'
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

(function() {
  // Got this from MDN:
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toLocaleString#Example:_Checking_for_support_for_locales_and_options_arguments
  function toLocaleStringSupportsLocales() {
    var number = 0;
    try {
      number.toLocaleString("i");
    } catch (e) {
      return e.name === "RangeError";
    }
    return false;
  }

  if (!toLocaleStringSupportsLocales()) {
    var replaceSeparators = function(sNum, separators) {
      var sNumParts = sNum.split('.');
      if (separators && separators.thousands) {
        sNumParts[0] = sNumParts[0].replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1" + separators.thousands);
      }
      sNum = sNumParts.join(separators.decimal);
      return sNum;
    };

    var renderFormat = function(template, props) {
      for (var prop in props) {
        template = template.replace("[[" + prop + "]]", props[prop]);
      }
      return template;
    };

    var mapMatch = function(map, locale) {
      var match = locale;
      var language = locale && locale.toLowerCase().match(/^\w+/);

      if (!map.hasOwnProperty(locale)) {
        if (map.hasOwnProperty(language)) {
          match = language;
        } else {
          match = "en";
        }
      }
      return map[match];
    };

    var dotThousCommaDec = function(sNum) {
      var separators = {
        decimal: ',',
        thousands: '.'
      };
      return replaceSeparators(sNum, separators);
    };

    var commaThousDotDec = function(sNum) {
      var separators = {
        decimal: '.',
        thousands: ','
      };
      return replaceSeparators(sNum, separators);
    };

    var spaceThousCommaDec = function(sNum) {
      var seperators = {
        decimal: ',',
        thousands: '\u00A0'
      };
      return replaceSeparators(sNum, seperators);
    };

    var apostrophThousDotDec = function(sNum) {
      var seperators = {
        decimal: '.',
        thousands: '\u0027'
      };
      return replaceSeparators(sNum, seperators);
    };

    var transformForLocale = {
      en: commaThousDotDec,
      it: dotThousCommaDec,
      fr: spaceThousCommaDec,
      de: dotThousCommaDec,
      nl: dotThousCommaDec,
      "de-DE": dotThousCommaDec,
      "de-AT": dotThousCommaDec,
      "de-CH": apostrophThousDotDec,
      "de-LI": apostrophThousDotDec,
      "de-BE": dotThousCommaDec,
      ro: dotThousCommaDec,
      "ro-RO": dotThousCommaDec,
      hu: spaceThousCommaDec,
      "hu-HU": spaceThousCommaDec,
      "da-DK": dotThousCommaDec,
      "nb-NO": spaceThousCommaDec
    };

    var currencyFormatMap = {
      en: "pre",
      it: "post",
      fr: "post",
      de: "post",
      nl: "prespace",
      "de-DE": "post",
      "de-AT": "prespace",
      "de-CH": "prespace",
      "de-LI": "post",
      "de-BE": "post",
      ro: "post",
      "ro-RO": "post",
      hu: "post",
      "hu-HU": "post",
      "da-DK": "post",
      "nb-NO": "post"
    };

    var currencySymbols = {
      "afn": "؋",
      "ars": "$",
      "awg": "ƒ",
      "aud": "$",
      "azn": "₼",
      "bsd": "$",
      "bbd": "$",
      "byr": "p.",
      "bzd": "BZ$",
      "bmd": "$",
      "bob": "Bs.",
      "bam": "KM",
      "bwp": "P",
      "bgn": "лв",
      "brl": "R$",
      "bnd": "$",
      "khr": "៛",
      "cad": "$",
      "kyd": "$",
      "clp": "$",
      "cny": "¥",
      "cop": "$",
      "crc": "₡",
      "hrk": "kn",
      "cup": "₱",
      "czk": "Kč",
      "dkk": "kr",
      "dop": "RD$",
      "xcd": "$",
      "egp": "£",
      "svc": "$",
      "eek": "kr",
      "eur": "€",
      "fkp": "£",
      "fjd": "$",
      "ghc": "¢",
      "gip": "£",
      "gtq": "Q",
      "ggp": "£",
      "gyd": "$",
      "hnl": "L",
      "hkd": "$",
      "huf": "Ft",
      "isk": "kr",
      "inr": "₹",
      "idr": "Rp",
      "irr": "﷼",
      "imp": "£",
      "ils": "₪",
      "jmd": "J$",
      "jpy": "¥",
      "jep": "£",
      "kes": "KSh",
      "kzt": "лв",
      "kpw": "₩",
      "krw": "₩",
      "kgs": "лв",
      "lak": "₭",
      "lvl": "Ls",
      "lbp": "£",
      "lrd": "$",
      "ltl": "Lt",
      "mkd": "ден",
      "myr": "RM",
      "mur": "₨",
      "mxn": "$",
      "mnt": "₮",
      "mzn": "MT",
      "nad": "$",
      "npr": "₨",
      "ang": "ƒ",
      "nzd": "$",
      "nio": "C$",
      "ngn": "₦",
      "nok": "kr",
      "omr": "﷼",
      "pkr": "₨",
      "pab": "B/.",
      "pyg": "Gs",
      "pen": "S/.",
      "php": "₱",
      "pln": "zł",
      "qar": "﷼",
      "ron": "lei",
      "rub": "₽",
      "shp": "£",
      "sar": "﷼",
      "rsd": "Дин.",
      "scr": "₨",
      "sgd": "$",
      "sbd": "$",
      "sos": "S",
      "zar": "R",
      "lkr": "₨",
      "sek": "kr",
      "chf": "CHF",
      "srd": "$",
      "syp": "£",
      "tzs": "TSh",
      "twd": "NT$",
      "thb": "฿",
      "ttd": "TT$",
      "try": "",
      "trl": "₤",
      "tvd": "$",
      "ugx": "USh",
      "uah": "₴",
      "gbp": "£",
      "usd": "$",
      "uyu": "$U",
      "uzs": "лв",
      "vef": "Bs",
      "vnd": "₫",
      "yer": "﷼",
      "zwd": "Z$"
    };

    var currencyFormats = {
      pre: "[[code]][[num]]",
      post: "[[num]] [[code]]",
      prespace: "[[code]] [[num]]"
    };

    Number.prototype.toLocaleString = function(locale, options) {
      if (locale && locale.length < 2)
        throw new RangeError("Invalid language tag: " + locale);

      var sNum;
      if (options && options.minimumFractionDigits) {
        sNum = this.toFixed(options.minimumFractionDigits);
      } else {
        sNum = this.toString();
      }

      sNum = mapMatch(transformForLocale, locale)(sNum, options);

      if(options && options.currency && options.style === "currency") {
        var format = currencyFormats[mapMatch(currencyFormatMap, locale)];
        if(options.currencyDisplay === "code") {
          sNum = renderFormat(format, {
            num: sNum,
            code: options.currency.toUpperCase()
          });
        } else {
          sNum = renderFormat(format, {
            num: sNum,
            code: currencySymbols[options.currency.toLowerCase()]
          });
        }
      }
      return sNum;
    };
  }
}());

/* General functions */
/* General functions - Numbers, currency, etc formatting  */
function formatCurrency(amount,minfrac,maxfrac) {
  minfrac = minfrac || 2;
  maxfrac = maxfrac || 2;

  var display = 'EUR';
  switch (globals.language) {
    case 'ca':
      display = 'CAD';
      break;

    case 'en_GB':
      display = 'GBP';
      break;

   case 'en_US':
     display = 'USD';
     break

   case 'nb_NO':
    display = 'NOK'
    break;

  }

  return (1 * amount).toLocaleString(globals.language.replace('_','-'), {
    style: 'currency',
    currency: display,
    minimumFractionDigits: minfrac,
    maximumFractionDigits: maxfrac
  });
}

function formatNumber(amount,minfrac,maxfrac) {
  minfrac = minfrac || 0;
  maxfrac = maxfrac || 3;

  return (1 * amount).toLocaleString(globals.language.replace('_','-'), {
    minimumFractionDigits: minfrac,
    maximumFractionDigits: maxfrac
  });
}

function formatBytes(bytes,decimals) {
   if(bytes === 0) return '0 Bytes';
   var k = 1024,
       dm = decimals || 2,
       sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
       i = Math.floor(Math.log(bytes) / Math.log(k));
   return formatNumber(parseFloat((bytes / Math.pow(k, i))),0,2) + ' ' + sizes[i];
}

function formatUptime(uptime) {
  uptime = moment.duration(uptime * 1000);
  var uptime_duration = '';
  uptime_duration += uptime.days() + 'D';
  uptime_duration += (uptime.hours() < 10 ? '0' : '') + uptime.hours() + 'H';
  uptime_duration += (uptime.minutes() < 10 ? '0' : '') + uptime.minutes() + 'M';
  uptime_duration += (uptime.seconds() < 10 ? '0' : '') + uptime.seconds() + 'S';
  return uptime_duration;
}

function capitalizeFirstLetter(string) {
    return string[0].toUpperCase() + string.slice(1);
}

// https://stackoverflow.com/questions/8837454/sort-array-of-objects-by-single-key-with-date-value
function sortByKey(array, key) {
  return array.sort(function(a, b) {
    var x = a[key]; var y = b[key];
    return ((x < y) ? -1 : ((x > y) ? 1 : 0));
  });
}
/* General functions - End numbers, currency, etc formatting  */

/* General functions - Websockets  */
function websocket_init(reconnect) {
  websocket_connect();

  globals.websocket.onopen = function(evt) {
    websocket_message({
      'type': 'client_init',
      'reconnect': reconnect
    });
  };

  globals.websocket.onmessage = function(evt) {
    if (globals.reboot) {
      // When a reboot is triggered, the first connection message is also a trigger that the reboot has finished. So reload the page!
      location.reload();
    }

    online_updater();
    var data = JSON.parse(evt.data);
    switch (data.type) {
      case 'logtail':
        update_logtail(data.data);
        break;
      case 'uptime':
        update_dashboard_uptime(data.data);
        load_calendar_history();
        break;
      case 'power_usage_water_flow':
        update_dashboard_power_usage(data.data.power);
        update_dashboard_water_flow(data.data.water);
        break;

      case 'environment':
        var dashboard = $('div.row.environment div.pull-right div.x_content');
        $.each(data.data, function(key, value) {
          update_dashboard_environment(key, value);
          if ('disabled' == value.config.mode) {
            dashboard.find('div.row.environment_' + key).detach().appendTo(dashboard);
          }
        });
        break;
      case 'sensor_gauge':
        $.each(data.data, function(index, sensor) {
          sensor_gauge(sensor.id !== undefined ? sensor.id : index, sensor);
        });
        break;
      case 'switches':
        $.each(data.data, function(index, switch_data) {
          update_power_switch(switch_data);
        });
        break;
      case 'door_status':
        update_door_indicator(data.data);
        break;
      case 'doors':
        $.each(data.data, function(index, door_data) {
          update_door(door_data);
        });
        break;
      case 'player_indicator':
        update_player_indicator(data.data);
        break;
      case 'update_weather':
        update_weather(data.data);
        break;
    }
  };
  globals.websocket.onclose = function(evt) {
    update_online_indicator(false);
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
    //console.log('websocket_connect', error);
  }
}

function websocket_message(message) {
  try {
    globals.websocket.send(JSON.stringify(message));
  } catch (error) {
    //console.log('websocket_message', error, message);
  }
}
/* General functions - End websockets  */

/* General functions - Notification bubbles */
function notification_bubble(type,title,message) {
  new PNotify({
    type: type,
    title: title,
    text: message,
    nonblock: {
      nonblock: true
    },
    delay: 3000,
    mouse_reset: false,
    styling: 'bootstrap3',
    hide: true,
  });
}

function error_notification_bubble(title,message) {
  notification_bubble('error',title,message);
}

function ok_notification_bubble(title,message) {
  notification_bubble('success',title,message);
}

function info_notification_bubble(title,message) {
  notification_bubble('info',title,message);
}
/* General functions - End notification bubbles */

/* General functions - Notification messages */
function add_notification_message(type, title, message, icon, color, date, link) {
  var notification_date = date || new Date().getTime();
  link = link || false;
  var menu = $('ul#' + type);
  if (menu.find('li:first a span.message').text() == message) {
    // Skip duplicate messages
    return;
  }

  var notification = $('<a>');
  if (type != 'player_messages') {
    notification.on('click', function() {
      if (link !== false) {
        load_page(link);
      } else {
        close_notification_message(this);
      }
    });
  }

  notification.append($('<span>').addClass('image').append($('<img>').attr({
    'src': $('div.profile_pic img:last').attr('src')
  })));
  notification.append($('<span>').append($('<span>').html(title)).append($('<span>').addClass('time notification_timestamp').attr('data-timestamp',notification_date)) );
  notification.append($('<span>').addClass('message').html(message).append($('<span>').addClass('pull-right').html('<i class="fa ' + icon + ' ' + color + '"></i>')));

  // Remove no messages line
  menu.find('li.no_message').hide();
  // Add new message on top
  menu.prepend($('<li>').addClass('notification').append(notification));

  // Only allow 6 messages, more will be removed
  menu.find('li.notification:gt(5)').remove();
  // Update the notifcation time
  notification_timestamps();
}

function close_notification_message(notification) {
  notification = $(notification).parent();
  var list = notification.parent('ul');
  notification.remove();
  list.find('li.no_message').toggle(list.find('li.notification:not(.no_message)').length === 0);
}

function notification_timestamps() {
  var now = (new Date()).getTime();
  $('span.notification_timestamp,strong.notification_timestamp').each(function() {
    var timestamp = $(this).attr('data-timestamp') * 1;
    var duration = moment.duration((now - timestamp) * -1);
    $(this).text(duration.humanize(true));
  });
}

function update_online_messages(online) {
  var title   = (online ? '{{_('Online')}}' : '{{_('Offline')}}');
  var message = (online ? '{{_('Connection restored')}}' : '{{_('Connection lost')}}');
  var icon    = (online ? 'fa-check-circle-o' : 'fa-exclamation-triangle');
  var color   = (online ? 'green' : 'red');
  add_notification_message('online_messages', title, message, icon, color);
}

function update_online_indicator(online) {
  var indicator = $('li#online_indicator');

  indicator.find('span.online, span.offline').hide();
  if (online) {
    indicator.find('span.online').show();
  } else {
    indicator.find('span.offline').show();
  }
  update_online_messages(online);
}
/* General functions - End Notification messages */

/* General functions - Form functions */
function init_form_settings(pType) {
  if (['environment','system','notifications'].indexOf(pType) == -1) {
    $('.page-title').append('<div class="title_right"><h3><button type="button" class="btn btn-primary alignright" data-toggle="modal" data-target=".add-form"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button></h3> </div>');
  }

  $('.form-group:has([required="required"]) > label').append('<span class="required"> *</span>');

  var submit_button = $('.modal-footer button.btn.btn-primary');
  switch (pType) {
    case 'sensor':
      // Load initial HTML data
      source_row = $('.modal-body div.row.sensor').html();
      // Bind to add button
      submit_button.on('click',function(){
        add_sensor();
      });
      break;

    case 'switch':
      // Load initial HTML data
      source_row = $('.modal-body div.row.switch').html();
      // Bind to add button
      submit_button.on('click',function(){
        add_power_switch();
      });
      break;

    case 'door':
      // Load initial HTML data
      source_row = $('.modal-body div.row.door').html();
      // Bind to add button
      submit_button.on('click',function(){
        add_door();
      });
      break;

    case 'webcam':
      // Load initial HTML data
      source_row = $('.modal-body div.row.webcam').html();
      // Bind to add button
      submit_button.on('click',function(){
        add_webcam();
      });
      break;

    case 'playlist':
      // Load initial HTML data
      source_row = $('.modal-body div.row.playlist').html();
      // Bind to add button
      submit_button.on('click',function(){
        add_audio_playlist();
      });
      break;

    case 'environment':
    case 'system':
      $('form').on('submit',function() {
        $(this).find('input[type="radio"]').removeAttr('checked').removeAttr('disabled');
        $(this).find('label.active > input[type="radio"]').attr('checked','checked');
        $(this).find('label:not(.active) > input[type="radio"]').attr('disabled','disabled');
      });
      break;
  }
}

function check_form_data(form) {
  var fieldsok = true;
  form.find('input[required="required"][readonly!="readonly"][readonly!="hidden"]').each(function(counter,item) {
    var field = $(this);
    var empty = field.val() === '';
    if (empty) {
      field.addClass('missing-required');
    } else {
      field.removeClass('missing-required');
    }
    fieldsok = fieldsok && !empty;
  });
  return fieldsok;
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
          ok_notification_bubble(response.title,response.message);
        } else {
          error_notification_bubble(response.title,response.message);
        }
      });
      return false;
    });
  });
}

function prepare_form_data(form) {
  var formdata = [];
  var form_type = form.attr('action').split('/').pop();

  var re = /(calendar|sensor|switch|webcam|light|humidity|temperature|watertank|moisture|conductivity|ph|co2|fertility|door|profile|playlist)(_\d+)?_(.*)/i;
  var matches = null;
  var objectdata = {};
  var prev_nr = -1;
  if (form_type === 'weather' || form_type === 'environment' || form_type === 'system' || form_type === 'profile' || form_type === 'notifications' || form_type === 'hardware' || form_type === 'calendar') {
    formdata = {};
  }
  try {
    form.find('div:visible input:not([disabled="disabled"]),div:visible select:not([disabled="disabled"]),div:visible textarea:not([disabled="disabled"])').each(function() {
      var field_name = $(this).attr('name');
      if (field_name !== undefined) {
        var field_value = $(this).val();
        switch (form_type) {
          case 'profile':
          case 'weather':
          case 'system':
          case 'notifications':
          case 'calendar':
            if (['age','calendar_date','daterangepicker_start','daterangepicker_end'].indexOf(field_name) !== -1) {
              field_value = moment(field_value,'L').unix();
            }
            formdata[field_name] = field_value;
            break;
          case 'hardware':
          case 'sensors':
          case 'switches':
          case 'powerswitches':
          case 'environment':
          case 'webcams':
          case 'doors':
          case 'audio':
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
                    if (form_type === 'environment') {
                      formdata[prev_nr] = $.extend(true, {}, objectdata);
                    } else {
                      formdata.push($.extend(true, {}, objectdata));
                    }
                  }
                  // New item
                  objectdata = {};
                  prev_nr = current_nr;
                }

                if (matches[3].match(/timer_(start|stop)$/)) {
                  // Load from local format, and store in 24h format. Do not use UNIX timestamp formats
                  field_value = moment(field_value, 'LT').format('HH:mm');
                }
                objectdata[matches[3]] = field_value;
              }
            }
            break;
        }
      }
    });
    if (Object.keys(objectdata).length > 1) {
      if (form_type === 'weather' || form_type === 'environment' || form_type === 'system' || form_type === 'notifications' || form_type === 'hardware' || form_type === 'calendar') {
        formdata[prev_nr] = $.extend(true, {}, objectdata);
      } else {
        formdata.push($.extend(true, {}, objectdata));
      }
    }
  } catch (error) {
    console.log(error);
    return false;
  }

  return formdata;
}
/* General functions - End form functions */

function flatten (obj) {
  var newObj = {};
  for (var key in obj) {
    if (obj[key] !== null && obj[key].constructor === Object) {
      var temp = flatten(obj[key])
      for (var key2 in temp) {
        newObj[key+"_"+key2] = temp[key2];
      }
    } else {
      newObj[key] = obj[key];
    }
  }
  return newObj;
}

/* General functions - System functions */
function online_updater() {
  clearTimeout(globals.online_timer);
  update_online_indicator(true);

  globals.online_timer = setTimeout(function() {
    update_online_indicator(false);
  }, 90 * 1000);
}

function version_check() {
  $.getJSON('https://api.github.com/repos/theyosh/TerrariumPI/releases/latest' ,function(data){

    var latest_version = data.tag_name.replace(/\./g,'') * 1;
    var current_version = globals.current_version.replace(/\./g,'') * 1;
    if (latest_version < 100) latest_version *= 10;
    if (current_version < 100) current_version *= 10;

    if (current_version < latest_version) {
      var message = 'New version available! <a href="' + data.html_url + '" target="_blank" title="Download TerrariumPI version ' + data.tag_name + '">Click here to download</a>!';
        info_notification_bubble('New release: ' + data.tag_name, message);
    }
    setTimeout(function() {
      version_check();
    },   24 * 60 * 60 * 1000 ); // Check once a day
  });
}

function parse_remote_data(field,url) {
  $.get(url,function(data) {
    var json_path = url.indexOf('#');
    if (json_path != -1) {
      json_path = url.substring(json_path+1).split('/');
      // TerrariumPI API is known, and can be used to fill in all values
      var is_remote_terrarium_pi = json_path.length == 3
                                   && (json_path[0] === 'sensors' || json_path[0] === 'switches')
                                   && json_path[1] === '0'
                                   && (json_path[2] === 'current' || json_path[2] === 'state');

      if (is_remote_terrarium_pi) {
        // Loop through the fields and fill in the fields with remote information
        $.each(data[json_path[0]][json_path[1]],function(fieldname,value) {
          // Never overrule fields in array below
          if ($.inArray(fieldname,['address','hardwaretype','id']) == -1) {
            $('input[name="' + field + '"]').val(value);
            $('select[name="' + field + '"]').val(value).change();
          }
        });
      } else {
        // Here we loop over the JSON structure to get the end value which should be the current value
        $.each(json_path,function(index,value){
          data = data[value];
        });
        $('input[name="' + field + '"]').val(data);
      }
    }
  });
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
      process_form();
    });
  }
  // Make sure the browser will not fire it's url loading event
  return false;
}

function logout() {
  $.ajax({
      async: false,
      url: 'logout',
      type: 'GET',
      username: 'logout'
  }).done(function(response) {
    if (response.ok) {
      ok_notification_bubble(response.title,response.message);
    } else {
      error_notification_bubble(response.title,response.message);
    }
  });
}
/* General functions - End system functions */

/* General functions - Graph functions */
function sensor_gauge(name, data) {
  // BUG: Missing 'sensor_' part in name.... lazy fix.
  if ($('#' + name + ' .gauge').length == 0 && $('#sensor_' + name + ' .gauge').length == 1) {
    name = 'sensor_' + name;
  }

  if ($('#' + name + ' .gauge').length == 1) {
    // Update timestamp indicator
    $('#' + name + ' span.small:visible:last').text(moment().format('LLL'));
    // Setup a new gauge if needed
    if ($('#' + name + ' .gauge').attr('done') === undefined) {
      var total_area = data.limit_max - data.limit_min;
      var colors = [
        [0.00, '#E74C3C'],
        [(data.alarm_min - data.limit_min) / total_area, '#F0AD4E'],
        [(((data.alarm_min + data.alarm_max)/2) - data.limit_min) / total_area, '#1ABB9C'],
        [(data.alarm_max - data.limit_min) / total_area, '#F0AD4E'],
        [1.00, '#E74C3C']
      ];

      var opts = {
        angle: 0,
        lineWidth: 0.6,
        pointer: {
          length: 0.80,
          strokeWidth: 0.070,
          color: '#1D212A'
        },
        limitMax: false,
        limitMin: true,
        strokeColor: '#F0F3F3',
        generateGradient: true,
        highDpiSupport: true,
        percentColors: colors,
      };

      // Init Gauge
      $('#' + name + ' .gauge').attr('done',1);
      //$('#' + name + ' .goal-wrapper span:nth-child(2)').text('°' + globals.temperature_indicator);
      globals.gauges[name] = new Gauge($('#' + name + ' .gauge')[0]).setOptions(opts);
      // Only set min and max only once. Else the gauge will flicker each data update
      globals.gauges[name].maxValue = data.limit_max;
      globals.gauges[name].setMinValue(data.limit_min);
    }
    // Update values
    if (name == 'system_load') {
      data.current /= data.cores;
    }
    // Chirp light sensor is based on backscattering and is not able to produce LUX values
    if ('light' == data.type && 'chirp' == data.hardwaretype) {
      data.indicator = '%';
    }

    $('#' + name + ' .gauge-indicator').text(data.indicator);
    globals.gauges[name].set(data.current);
    if (name == 'system_disk' || name == 'system_memory') {
      $('#' + name + ' .gauge-value').text(formatBytes(data.current))
    } else {
      $('#' + name + ' .gauge-value').text(formatNumber(data.current,0,3))
    }
    $('div#' + name + ' .x_title h2 .badge.bg-red').toggle(data.alarm);
    $('div#' + name + ' .x_title h2 .badge.bg-orange').toggle(data.error);
    $('div#' + name + ' .x_title h2 .badge.bg-blue').toggle(data.exclude_avg);
  }
}

/**
* returns an array with moving average of the input array
* @param array - the input array
* @param count - the number of elements to include in the moving average calculation
* @param qualifier - an optional function that will be called on each
*  value to determine whether it should be used
*/
function movingAvg(array, count, qualifier){

    // calculate average for subarray
    var avg = function(array, qualifier){

        var sum = 0, count = 0, val;
        for (var i in array){
            val = array[i][1];
            if (!qualifier || qualifier(val)){
                sum += val;
                count++;
            }
        }

        return [array[0][0],sum / count];
    };
    var result = [], val;

    // calculate average for each subarray and add to result
    for (var i=0, len=array.length - count; i <= len; i++){
        val = avg(array.slice(i, i + count), qualifier);
        result.push(val);
    }
    return result;
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
      $.each(['day','week','month','year','lr'],function(index,value){
        if (index < menu_items.length){
          if (index === 0) {
            $(menu_items[index]).parent().addClass('focus');
          }

          $(menu_items[index]).attr('title',$(menu_items[index]).text());
          $(menu_items[index]).off('click');
          $(menu_items[index]).on('click', function(){
            $(this).parent().siblings().removeClass('focus');
            $(this).parent().addClass('focus');
            load_history_graph(id,type,data_url + '/' + value ,1);
          });
        }
      });
      $('#' + id + ' ul.dropdown-menu a.export').off('click').on('click',function(){
        var download = $('iframe#history_export');
        if (download.length == 0) {
          download = $('<iframe>', { id:'history_export', src:'#' }).on('load',function(){
            if (globals.ajaxloader > 0) {
              globals.ajaxloader--;
            }
            NProgress.done();
          }).hide().appendTo('body');
        }
        globals.ajaxloader++;
        NProgress.start();
        download.attr('src',data_url.replace('/history/','/export/'));
      });
    }
    if (nocache === 0 && now - globals.graphs[id].timestamp < globals.graph_cache * 1000) {
      history_graph(id, globals.graphs[id].data, type);
      clearTimeout(globals.graphs[id].timer);
      globals.graphs[id].timer = setTimeout(function() {
          load_history_graph(id,type,data_url);
      }, globals.graph_cache * 1000);

    } else {
      // Load fresh data...
      $.getJSON(data_url, function(online_data) {
        $.each(online_data, function(dummy, value) {
          $.each(value, function(dummy, data_array) {
            globals.graphs[id].timestamp = now;
            globals.graphs[id].data = data_array;
          });
        });

        if ('light' == type && data_url.indexOf('/average/') > 0) {
          globals.graphs[id].data.light_average = true;
          globals.graphs[id].data.light_uvi = false;

          $.getJSON(data_url.replace('/light','/uvi'), function(online_data) {
            if (online_data['uvi'] != undefined && online_data['uvi']['average']['current'].length > 0) {
              // Have UV Index, use that
              globals.graphs[id].data.light_uvi = true;
              $.each(online_data['uvi'], function(name, data) {
                globals.graphs[id].timestamp = now;
                globals.graphs[id].data['alarm_max'] = data.current;
              });
              history_graph(id, globals.graphs[id].data, type);
            } else {
              $.getJSON(data_url.replace('/light','/uva'), function(online_data) {
                $.each(online_data['uva'], function(name, data) {
                  globals.graphs[id].timestamp = now;
                  globals.graphs[id].data['alarm_min'] = data.current;
                });
                $.getJSON(data_url.replace('/light','/uvb'), function(online_data) {
                  $.each(online_data['uvb'], function(name, data) {
                    globals.graphs[id].timestamp = now;
                    globals.graphs[id].data['alarm_max'] = data.current;
                  });
                  history_graph(id, globals.graphs[id].data, type);
                });
              });
            }
          });
        } else {
          history_graph(id, globals.graphs[id].data, type);
        }
        clearTimeout(globals.graphs[id].timer);
        globals.graphs[id].timer = setTimeout(function() {
          load_history_graph(id,type,data_url);
        }, globals.graph_cache * 1000);
      });
    }

  }
  return false;
}

function history_graph(name, data, type) {
  function getMin(ret, thisVal) {
    thisVal = thisVal[1] || ret;
    return ret < thisVal ? ret : thisVal;
  }

  function getMax(ret, thisVal) {
    thisVal = thisVal[1] || ret;
    return ret > thisVal ? ret : thisVal;
  }

  if (type === undefined) {
    type = 'temperature';
  }

  var graph_ticks = 8, smooth = false;
  if (type === 'door') {
    graph_ticks = [[0, '{{_('Closed')}}'], [1, '{{_('Open')}}']];
  }

  var legend_data = {show: true, noColumns: globals.horizontal_legend ? 0 : 1}
  if (globals.horizontal_legend) {
    legend_data.margin = [0, -20];
  }
  var graph_data = [];
  var graph_options = {
    legend: legend_data,
    tootip: true,
    series: {
      curvedLines: {
        apply: false,
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
      ticks: graph_ticks,
      tickColor: "rgba(51, 51, 51, 0.06)",
      tickDecimals: 2,
      tickFormatter: function(val, axis) {
        switch(type) {
          case 'system_memory':
          case 'system_disk':
              val = formatBytes(val);
            break;

          case 'system_uptime':
              val = moment.duration(val * 1000).humanize();
            break;

          case 'system_load':
              val = formatNumber(val);
            break;

          case 'weather':
          case 'temperature':
          case 'average_temperature':
            val = formatNumber(val) + ' ' + globals.temperature_indicator;
            break;

          case 'humidity':
          case 'average_humidity':
          case 'moisture':
            val = formatNumber(val) + ' %';
            break;

          case 'distance':
          case 'average_distance':
            val = formatNumber(val) + ' ' + globals.distance_indicator;
            break;

          case 'ph':
          case 'average_ph':
            val = formatNumber(val) + ' pH';
            break;

          case 'conductivity':
          case 'average_conductivity':
            val = formatNumber(val) + ' mS';
            break;

          case 'switch':
            val = formatNumber(val) + ' W';
            break;

          case 'light':
            val = formatNumber(val) + ' lux';
            break;

          case 'light_percentage':
            val = formatNumber(val) + ' %';
            break;

          case 'fertility':
            val = formatNumber(val) + ' µS/cm';
            break;

          case 'co2':
            val = formatNumber(val) + ' ppm';
            break

          case 'volume':
            val = formatNumber(val) + ' ' + globals.volume_indicator;
            break

          case 'uva':
          case 'uvb':
            val = formatNumber(val) + ' µW/cm^2';
            break;

          case 'uvi':
            val = formatNumber(val);
            break;

          case 'door':
            val = (val ? '{{_('Open')}}' : '{{_('Closed')}}');
            break;
        }
        return val;
      }
    }
  };

  switch (type) {
    case 'light':
      smooth = true;
      if (data.light_average !== undefined && data.light_average) {

        graph_data = [{
          label: '{{_('Light')}}',
          data: data.current
        }];

        graph_options.colors = ['rgba(38, 185, 154, 0.38)'];

        if (data.light_uvi !== undefined && data.light_uvi) {
          graph_data.push({ label: '{{_('UV')}}',
                             data: data.alarm_max,
                             yaxis: 2});

          graph_options.colors.push('rgba(3, 88, 206, 0.38)');
        } else {
          graph_data.push({ label: '{{_('UVA')}}',
                             data: data.alarm_min,
                             yaxis: 2});
          graph_data.push({ label: '{{_('UVB')}}',
                             data: data.alarm_max,
                             yaxis: 2});

          graph_options.colors.push('rgba(3, 88, 106, 0.38)')
          graph_options.colors.push('rgba(3, 88, 206, 0.38)')
        }

        graph_options.xaxes = [jQuery.extend(true, {}, graph_options.xaxes)];

        var yaxis2 = jQuery.extend(true, {}, graph_options.yaxes);
        yaxis2.alignTicksWithAxis = 1;
        yaxis2.position = 'right';

        yaxis2.tickFormatter = function(val, axis) { return val.toFixed(axis.tickDecimals) + (!(data.light_uvi !== undefined && data.light_uvi) ? ' µW/cm^2' : '');}

        graph_options.yaxes = [jQuery.extend(true, {}, graph_options.yaxes),yaxis2];

      } else {
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
      }
      break;
    case 'humidity':
    case 'temperature':
    case 'distance':
    case 'ph':
    case 'moisture':
    case 'conductivity':
    case 'light_percentage':
    case 'uva':
    case 'uvb':
    case 'uvi':
    case 'fertility':
    case 'co2':
    case 'volume':
      smooth = true;
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
      graph_options.series.curvedLines.apply = true;
    case 'system_temperature':
      smooth = true;
      graph_data = [{
        label: '{{_('Temperature')}}',
        data: data
      }];
      break;

    case 'system_uptime':
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
      smooth = true;
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

    case 'system_disk':
      graph_data = [{
        label: '{{_('Used space')}}',
        data: data.used
      }, {
        label: '{{_('Free space')}}',
        data: data.free
      }, {
        label: '{{_('Total space')}}',
        data: data.total
      }];
      break;

    case 'switch':
      graph_options.series.lines = {
        show: true,
        lineWidth: 2,
        fill: true
      };
      graph_options.yaxis.min = 0;
      graph_data = [{
        label: '{{_('Power usage in Watt')}}',
        data: data.power_wattage
      }, {
        label: '{{_('Water flow in L/m')}}',
        data: data.water_flow,
        yaxis: 2
      }];

      graph_options.xaxes = [jQuery.extend(true, {}, graph_options.xaxes)];

      var yaxis2 = jQuery.extend(true, {}, graph_options.yaxes);
      yaxis2.alignTicksWithAxis = 1;
      yaxis2.position = 'right';
      yaxis2.tickFormatter = function(val, axis) { return val.toFixed(axis.tickDecimals) + " L/m";}

      graph_options.yaxes = [jQuery.extend(true, {}, graph_options.yaxes),yaxis2];
      break;

    case 'door':
      graph_options.series.lines = {
        show: true,
        lineWidth: 2,
        fill: true
      };
      graph_options.yaxis.min = 0;
      graph_options.yaxis.max = 1;
      graph_data = [{
        label: '{{_('Door status')}}',
        data: data.state
      }];
      break;
  }

  if (graph_data[0].data !== undefined && graph_data[0].data.length > 0) {
    var total_data_duration = (graph_data[0].data[graph_data[0].data.length - 1][0] - graph_data[0].data[0][0]) / 3600000;

    if (graph_data.length > 1 && graph_data[1].data !== undefined && graph_data[1].data.length > 0) {
      var new_duration = (graph_data[1].data[graph_data[1].data.length - 1][0] - graph_data[1].data[0][0]) / 3600000;
      total_data_duration = new_duration > total_data_duration ? new_duration : total_data_duration
    }
    if (graph_data.length > 2 && graph_data[2].data !== undefined && graph_data[2].data.length > 0) {
      var new_duration = (graph_data[2].data[graph_data[2].data.length - 1][0] - graph_data[2].data[0][0]) / 3600000;
      total_data_duration = new_duration > total_data_duration ? new_duration : total_data_duration
    }
    graph_options.xaxis.tickSize[0] = Math.round(total_data_duration * 2.5);
  }

  if (smooth && globals.graph_smooth_value > 0) {
    graph_data[0].data = movingAvg(graph_data[0].data.reverse(),globals.graph_smooth_value);
    try {
      graph_data[1].data = graph_data[1].data.splice(globals.graph_smooth_value);
    } catch (e) {}
    try {
      graph_data[2].data = graph_data[2].data.splice(globals.graph_smooth_value);
    } catch (e) {}
  }

  if (globals.graph_show_min_max_gauge && name.indexOf('system_') === -1 && globals.gauges[name]) {
    // set the min/max values in the guage
    globals.gauges[name].options.staticLabels = {
      labels: [graph_data[0].data.reduce(getMin), graph_data[0].data.reduce(getMax)],
      font: '10px Helvetica Neue,sans-serif',
      color: '#73879C',
      fractionDigits: 3
    };
    globals.gauges[name].render();
  }

  if ($('#' + name + ' .history_graph').length == 1) {
    $('#' + name + ' .history_graph').html('').removeClass('loading');
    $.plot($('#' + name + ' .history_graph'), graph_data, graph_options);
    $('#' + name + ' .history_graph .legend').toggleClass('horizontal',globals.horizontal_legend);

    if (type == 'switch') {
      var usage = '';
      if (data.totals !== undefined) {
        if (data.totals.duration > 0) {
          usage = '{{_('Duration in hours')}}: ' + Math.round(moment.duration(data.totals.duration * 1000).as('hours')*100)/100;
        }
        if (data.totals.power_wattage > 0) {
          usage += (usage != '' ? ' - ' : '') + '{{_('Total power in kWh')}}: ' + formatNumber(data.totals.power_wattage / (3600 * 1000));
        }
        if (data.totals.water_flow > 0) {
          usage += (usage != '' ? ' - ' : '') + '{{_('Total water in L')}}: ' + formatNumber(data.totals.water_flow);
        }
      }
      $('#' + name + ' .total_usage').text(usage);
    } else if (type == 'door') {
      var usage = '';
      if (data.totals !== undefined) {
        if (data.totals.duration > 0) {
          usage = '{{_('Total open for')}}: ' + moment.duration(data.totals.duration * 1000).humanize();
        }
      }
      $('#' + name + ' .total_usage').text(usage);
    }
    $('#' + name + ' .history_graph').bind('plothover', function (event, pos, item) {
      if (item) {
        $('#tooltipGraph').attr('data-original-title',moment(item.datapoint[0]).format('LLL') + '<br />' + item.series.label + ' ' + item.series.yaxis.tickFormatter(item.datapoint[1],item.series.yaxis));
        $('#tooltipGraph').css({top: item.pageY-5, left: item.pageX-5, display:'block'});
      }
    });
  }
}
/* General functions - End graph functions */

/* General functions - Template functions */
function update_logtail_indicator(type) {
  var indicator = $('footer .label.label-success');
  var opacity = 0.2;
  var count = '&nbsp;';

  if ('warning' == type) {
    indicator = $('footer .label.label-warning');
    opacity = (indicator.css('opacity') * 1) + 0.1;
    count = ((indicator.text()).trim() * 1) + 1;
  } else if ('error' == type) {
    indicator = $('footer .label.label-danger');
    opacity = (indicator.css('opacity') * 1) + 0.1;
    count = ((indicator.text()).trim() * 1) + 1;
  }
  if (opacity > 1) {
    opacity = 1;
  }
  indicator.stop().attr({'title':'{{_("Last update")}}: ' + moment().format('LL LTS')}).css({'opacity': 1.0}).html(count).animate({'opacity': opacity},333);
}

function update_logtail(message) {
  var message_type = 'info';
  if (message.indexOf('WARNING') > 0) {
    message_type = 'warning';
  } else if (message.indexOf('ERROR') > 0) {
    message_type = 'error';
  }
  update_logtail_indicator(message_type);
  $('div.row.logtail div.x_content pre').prepend(message + '\n');
  $('div.row.logtail div.x_title small').text(moment().format('LL LTS'));
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

// TODO: This is some kind of easy fix, maybe we can improve this
function setContentHeight() {
  // reset height
  $RIGHT_COL.css('min-height', $(window).height());

  var bodyHeight = $BODY.outerHeight(),
    footerHeight = $BODY.hasClass('footer_fixed') ? -10 : $FOOTER.height(),
    leftColHeight = $LEFT_COL.eq(1).height() + $SIDEBAR_FOOTER.height(),
    contentHeight = bodyHeight < leftColHeight ? leftColHeight : bodyHeight;

  // normalize content
  contentHeight -= $NAV_MENU.height() + footerHeight;

  $RIGHT_COL.css('min-height', contentHeight - 15);
};

// Sidebar
function init_sidebar() {
  $SIDEBAR_MENU.find('a').on('click', function(ev) {
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
    if ($BODY.hasClass('nav-md')) {
      $SIDEBAR_MENU.find('li.active ul').hide();
      $SIDEBAR_MENU.find('li.active').addClass('active-sm').removeClass('active');
    } else {
      $SIDEBAR_MENU.find('li.active-sm ul').show();
      $SIDEBAR_MENU.find('li.active-sm').addClass('active').removeClass('active-sm');
    }

    $BODY.toggleClass('nav-md nav-sm');
    Cookies.set('hide_menu',$BODY.hasClass('nav-sm'));

    setContentHeight();

    $('.dataTable').each ( function () { $(this).dataTable().fnDraw(); });
  });

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

  // Hide menu bar based on cookie value
  if ($BODY.hasClass('nav-md') && 'true' == Cookies.get('hide_menu')) {
    $('ul.nav.side-menu li:first a:first').trigger('click');
    $MENU_TOGGLE.trigger('click');
  } else {
    $('ul.nav.side-menu li:first a:first').trigger('click');
  }

};
// /Sidebar

function reload_reload_theme() {
  // Panel toolbox
  $('.collapse-link').off('click').on('click', function() {
    var $BOX_PANEL = $(this).closest('.x_panel'),
        $ICON = $(this).find('i'),
        $BOX_CONTENT = $BOX_PANEL.find('.x_content');

    // fix for some div with hardcoded fix class
    if ($BOX_PANEL.attr('style')) {
        $BOX_CONTENT.slideToggle(200, function(){
            $BOX_PANEL.removeAttr('style');
            setContentHeight();
        });
    } else {
        $BOX_CONTENT.slideToggle(200, function() {
          setContentHeight();
        });
        $BOX_PANEL.css('height', 'auto');
    }

    $ICON.toggleClass('fa-chevron-up fa-chevron-down');
  });

  $('.close-link').off('click').click(function () {
    var $BOX_PANEL = $(this).closest('.x_panel');

    $BOX_PANEL.remove();
    setContentHeight();
  });
  // Tooltip
  $('[data-toggle="tooltip"]').tooltip({
    container: 'body',
    html: true
  });
  setContentHeight();
}
/* General functions - End template functions */
/* End general functions */


/* Dashboard code */
/* Dashboard code - Top tiles */
function update_dashboard_tile(tile, text) {
  var div = $('div.tile_count #' + tile + ' div.count');
  if (div.length == 1 && div.text() != text) {
    var oldColor = div.css('color');
    div.text(text);
    div.addClass('green');
    div.animate({
      color: oldColor
    }, 1000, function() {
      $(this).removeClass('green').css('color', '');
    });
  }
}

function update_dashboard_time(data) {
  $('#system_time span').text(moment(data.timestamp * 1000).format('LLLL'));
  $('#system_time i').removeClass('fa-clock-o fa-sun-o fa-moon-o').addClass((data.day ? 'fa-sun-o' : 'fa-moon-o'));
}

function update_dashboard_uptime(data) {
  update_dashboard_time(data);
  update_dashboard_tile('uptime', formatUptime(data.uptime));
  $("#uptime .progress-bar-success").css('height', ((data.load[0] / data.cores) * 100) + '%');
  $("#uptime .progress-bar-warning").css('height', ((data.load[1] / data.cores) * 100) + '%');
  $("#uptime .progress-bar-danger").css('height',  ((data.load[2] / data.cores) * 100) + '%');
}

function update_dashboard_power_usage(data) {
  update_dashboard_tile('power_wattage', formatNumber(data.current) + '/' + formatNumber(data.max));
  $("#power_wattage .progress-bar-success").css('height', (data.max > 0 ? (data.current / data.max) * 100 : 0) + '%');

  update_dashboard_tile('total_power',formatNumber(data.total / 3600 / 1000)); // from total watt to KiloWattHours
  $("#total_power .count_bottom .costs").text(formatCurrency(data.price,2,3));
  $("#total_power .count_bottom .duration").text(moment.duration(data.duration * 1000).humanize());
}

function update_dashboard_water_flow(data) {
  update_dashboard_tile('water_flow', formatNumber(data.current) + '/' + formatNumber(data.max));
  $("#water_flow .progress-bar-info").css('height', (data.max > 0 ? (data.current / data.max) * 100 : 0) + '%');

  update_dashboard_tile('total_water', formatNumber(data.total));
  $("#total_water .count_bottom .costs").text(formatCurrency(data.price,2,3));
  $("#total_water .count_bottom .duration").text(moment.duration(data.duration * 1000).humanize());
}
/* Dashboard code - End Top tiles */

/* Dashboard code - Environment */
function update_dashboard_environment(name, data) {
  if (data === undefined) {
    return false;
  }
  var systempart = $('div.environment_' + name);
  if (!data.enabled) {
    systempart.find('h4').removeClass('orange blue red').addClass('');
    systempart.find('h4 small span').hide().filter('.disabled').show();
    systempart.find('table').toggle(false);
    setContentHeight();
    return false;
  }

  var enabledColor = '';
  var indicator = globals.temperature_indicator;
  switch (name) {
    case 'light':
      enabledColor = 'orange';
      break
    case 'conductivity':
      enabledColor = 'orange';
      indicator = 'mS';
      break
    case 'temperature':
      enabledColor = 'red';
      break;
    case 'humidity':
    case 'moisture':
      indicator = '%';
      enabledColor = 'blue';
      break;
    case 'watertank':
      indicator = 'L';
      enabledColor = 'blue';
      break;
    case 'ph':
      indicator = 'pH';
      enabledColor = 'green';
      break;
    case 'fertility':
      enabledColor = 'green';
      indicator = 'µS/cm';
      break;
    case 'co2':
      enabledColor = 'green';
      indicator = 'ppm';
      break;
    case 'volume':
      enabledColor = 'blue';
      indicator = 'L';
      break;
  }

  systempart.find('h4').removeClass('orange blue red').addClass(data.enabled ? enabledColor : '');
  systempart.find('h4 small span').hide().filter('.' + data.config.mode).show();

  if (data.config.sensors !== undefined && data.config.sensors.length > 0) {
    systempart.find('h4 small span.sensor').show();
  }

  // Hide power state when there are no power switches enabled
  var power_switches = false;
  if (data.config.alarm_min !== undefined && data.config.alarm_min.powerswitches !== undefined) {
    power_switches = power_switches || data.config.alarm_min.powerswitches.length > 0;
  }
  if (data.config.alarm_max !== undefined && data.config.alarm_max.powerswitches !== undefined) {
    power_switches = power_switches || data.config.alarm_max.powerswitches.length > 0;
  }
  systempart.find('td.state').parent().toggle(power_switches);

  $.each(data, function(key, value) {
    switch (key) {
      case 'state':
        // Find all i elements withing the .state table row. Hide them all, then filter the enabled one and show that. Then go up and show the complete state table row... Nice!
        if (power_switches) systempart.find('.state i').hide().filter('.' + (value ? 'green' : 'red')).show().parent().parent().toggle(true);
        break;

      case 'alarm':
        systempart.find('span.glyphicon-warning-sign').toggle(value);
        break;

      case 'error':
        systempart.find('span.glyphicon-exclamation-sign').toggle(value);
        break;

      case 'current':
        systempart.find('.' + key).text(formatNumber(value,3) + ' ' + indicator).parent().toggle(data.config.mode === 'sensor' || data.config.sensors.length > 0);
        break;

      case 'alarm_min':
      case 'alarm_max':
        systempart.find('.' + key).text(formatNumber(data.alarm_min,1) + ' - ' + formatNumber(data.alarm_max,1) + ' ' + indicator).parent().toggle(data.config.mode === 'sensor' || data.config.sensors.length > 0);
        break;

      case 'is_night':
        if (data.config.day_night_difference > 0) {
          systempart.find('.day_night_difference').text(formatNumber(data.config.day_night_difference,3) + ' ' + indicator).parent().toggle(data.config.day_night_difference != 0);
        }
        systempart.find('span.day, span.night').hide();
        systempart.find('span.' + (value ? 'night' : 'day')).show();
        break;

      case 'timer_min':
      case 'timer_max':
        if (value.time_table != undefined && ('timer_min' == key && data.config.alarm_min.powerswitches.length > 0 || 'timer_max' == key && data.config.alarm_max.powerswitches.length > 0 )) {
          systempart.find('.' + key).text(moment(value.time_table[0][0] * 1000).format('LT') + ' - ' + moment(value.time_table[value.time_table.length-1][1] * 1000).format('LT')).parent().toggle(data.config.mode != 'sensor');
          systempart.find('.' + key + '.duration').text(moment.duration(value.duration * 1000).humanize()).parent().toggle(data.config.mode != 'sensor');
        }
        break;
    }
  });

  systempart.find('table').toggle(data.enabled);
  setContentHeight();
}
/* Dashboard code - End Environment */
/* End dashboard code */


/* Weather code */
function update_weather(data) {
  var icons = new Skycons({
    "color": "#73879C"
  });
  var weather_current = $('div#weather_today');
  if (weather_current.length == 1) {
    weather_current.find('.status').html(moment(data.hour_forecast[0].from * 1000).format('[<b>]dddd[</b>,] LT') + ' <span> in <b>' + globals.temperature_indicator + '</b></span>');
    weather_current.find('h2').html(data.city.city + '<br><i>' + data.hour_forecast[0].weather + '</i>');
    weather_current.find('.sunrise').text(moment(data.sun.rise * 1000).format('LT')).parent().css('fontWeight', (data.day ? 'bold' : 'normal'));
    weather_current.find('.sunset').text(moment(data.sun.set * 1000).format('LT')).parent().css('fontWeight', (data.day ? 'normal' : 'bold'));
    weather_current.find('.degrees').text(formatNumber(data.hour_forecast[0].temperature));
    icons.set(weather_current.find('canvas').attr('id'), data.hour_forecast[0].icon);
    var week_forecast_divs = weather_current.find('div.row.weather-days div.daily-weather');
    // Set timestamp to tomorrow at 12 hours. That is the first week forecast we take
    var timestamp = Math.round(new Date(Date.now()).setHours(12) / 1000) + (24 * 60 * 60);
    var day_counter = 0;
    var graphdata = [];
    $.each(data.week_forecast, function(index, value) {
      graphdata.push([(value.to - ((value.to - value.from) / 2)) * 1000, value.temperature]);
      if (value.from - timestamp >= 3600 && day_counter < week_forecast_divs.length) {
        $(week_forecast_divs[day_counter]).show();
        $(week_forecast_divs[day_counter]).find('.day').text(moment(value.from * 1000).format('ddd'));
        $(week_forecast_divs[day_counter]).find('.degrees').text(formatNumber(value.temperature));
        $(week_forecast_divs[day_counter]).find('h5').html(formatNumber(value.wind_speed) + ' <i>' + (data.windspeed === 'ms' ? '{{_('m/s')}}' : '{{_('Km/h')}}') + '</i>');
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
/* End weather code */

/* Sensors code */
function add_sensor_status_row(data) {
  if (source_row === null || source_row === '') {
    return false;
  }
  // Create new row
  var new_row = $('<div>').addClass('row sensor').html(source_row);
  // Set ID
  new_row.attr('id','sensor_' + data.id);
  // Add to page
  $('div#maincontent').append(new_row);
}

function update_sensor(data) {
  // Load the switch row to update the data
  var content_row = $('div.row.sensor#' + 'sensor_' + data.id);
  // Show either the temperature or humidity header and icon
  content_row.find('h2').hide().filter('.' + data.type).show();
  // Update title
  content_row.find('h2 span.title').text(data.name);
  if ('miflora' == data.hardwaretype) {
    content_row.find('h2 span.title').append(' <span class="small">' + data.firmware + ' <i class="fa fa-plug"></i>' + data.battery + '%</span>');
  }

  // Set the values only when empty
  content_row.find('input:not(.knob), select').each(function(counter,item) {
    if (item.name !== undefined && item.name !== '') {
      var name = item.name.replace(/sensor_[0-9]+_/g,'');
      var field_value = $(item).val();
      try {
        if (field_value === '' || field_value === null) {
          var value = data[name];
          if (!$.isArray(value)) {
            // Cast explicit to string to fix dropdown options
            value += '';
          }
          $(item).val(value).trigger('change');
        }
      } catch (e) {
        console.log(e);
      }
    }
  });

  // Open or hide the dimmer values (will not trigger on the select field)
  if ('chirp' === data.hardwaretype) {
    content_row.find('.row.chirp_calibration').show();
  } else {
    // Remove dimmer row, else form submit is 'stuck' on hidden fields that have invalid patterns... :(
    content_row.find('.row.chirp_calibration').remove();
  }
}

function add_sensor_setting_row(data,is_new) {
  if (source_row === null || source_row === '') {
    return false;
  }
  // Create new row
  var setting_row = $('<div>').addClass('row sensor' + (is_new ? ' new' : '')).html(source_row.replace(/\[nr\]/g, $('form div.row.sensor').length));
  if (data.id !== undefined) {
    // Set ID
    setting_row.attr('id','sensor_' + data.id);
  }
  // Re-initialize the select pulldowns
  //setting_row.find('span.select2.select2-container').remove();
  setting_row.find('select').select2({
    placeholder: '{{_('Select an option')}}',
    allowClear: false,
    minimumResultsForSearch: Infinity
  }).on('change',function() {
    if (this.name.indexOf('hardwaretype') >= 0) {
      var chirp_sensor = ('chirp' === this.value);
      if (chirp_sensor) {
        $(this).parents('.x_content').find('.row.chirp_calibration input').attr('required','required');
      } else {
        $(this).parents('.x_content').find('.row.chirp_calibration input').removeAttr('required');
      }
      $(this).parents('.x_content').find('.row.chirp_calibration').toggle(chirp_sensor);

      var address_field = $("input[name='" + this.name.replace('hardwaretype','address') + "']");
      address_field.attr("readonly", this.value == 'owfs' || this.value == 'w1').off('change');
    }
  });

  // Disable hardware select box
  setting_row.find('select[name*="hardwaretype"]').attr("disabled", !is_new);

  // Add on the bottom before the submit row
  setting_row.insertBefore('div.row.submit');
}

function add_sensor() {
  var form = $('.add-form');
  if (!check_form_data(form)) return false;

  // Create power switch data object and fill it with form data
  var data = {};
  form.find('input, select').each(function(counter,item) {
    if (item.name !== undefined && item.name !== '') {
      var fieldname = item.name.replace('sensor_[nr]_','');
      var value = $(item).val();
      data[fieldname] = value;
    }
  });
  data['id'] = Math.floor(Date.now() / 1000);

  // Add new row
  add_sensor_setting_row(data,true);

  // Update new row with new values
  update_sensor(data);

  // Reset form
  form.find('input').val('');
  form.find('select').val(null).trigger('change');
  // Hide form
  form.modal('hide');

  reload_reload_theme();
}
/* End sensors code code */

/* Power switches code */
function toggle_power_switch(id) {
  $.post('/api/switch/toggle/' + id,function(data){
  });
}

function toggle_power_manual_mode(id) {
  $.post('/api/switch/manual_mode/' + id,function(data){
    if (data.ok) {
      $('div.row.switch#powerswitch_' + id).find('h2 span.manual_mode').toggle();
    }
  });
}

function add_power_switch_status_row(data) {
  console.log(data);
  if (source_row === null || source_row === '') {
    return false;
  }
  // Create new row
  var new_row = $('<div>').addClass('row switch').html(source_row);

  // Set ID
  new_row.attr('id','powerswitch_' + data.id);

  // Change the toggle icon with a slider knob
  if (data.hardwaretype.indexOf('-dimmer') !== -1 || 'brightpi' === data.hardwaretype || 'pca9685' == data.hardwaretype) {
    new_row.find('div.x_content div.power_switch')
      .removeClass('big')
      .addClass('dimmer')
      .html('<input type="text" class="knob" data-thickness=".3" data-width="160" data-angleOffset=20 data-angleArc=320 data-fgColor="' + (data.state > data.dimmer_off_percentage ? '#1ABB9C' : '#3498DB') + '" value="' + data.state + '">');

    new_row.find('.knob').knob({
      release: function(value) {
        $.post('/api/switch/state/' + data.id + '/' + value,function(dummy){
        });
      },
      format: function(value) {
        return value + '%';
      },
      change: function(value) {
        this.o.fgColor = (value > data.dimmer_off_percentage ? '#1ABB9C' : '#3498DB');
        $(this.i).css('color',this.o.fgColor);
      }
    });
  } else {
    // Set toggle
    new_row.find('div.power_switch span.glyphicon').on('click',function(){
      toggle_power_switch($(this).parentsUntil('div.row.switch').parent().attr('id').split('_')[1]);
    });
  }
  new_row.find('a.manual_mode').on('click',function(){
    toggle_power_manual_mode($(this).parentsUntil('div.row.switch').parent().attr('id').split('_')[1]);
  });

  if (data.timer_enabled) {
      new_row.find('div.power_switch span.glyphicon').append($('<span>').addClass('glyphicon glyphicon glyphicon-time'));
      new_row.find('div.power_switch.dimmer div').append($('<span>').addClass('glyphicon glyphicon glyphicon-time'));
  }
  $('div#maincontent').append(new_row);
}

function update_power_switch(data) {
  // Load the switch row to update the data
  var content_row = $('div.row.switch#' + 'powerswitch_' + data.id);

  // Update state icon
  var on = data.state;
  // Set the name and status
  var current_status_data = '';
  var dimmer = data.hardwaretype.indexOf('dimmer') !== -1 || 'brightpi' === data.hardwaretype || 'pca9685' === data.hardwaretype;
  if (dimmer) {
    current_status_data = formatNumber(data.current_power_wattage) + 'W / ';
    on = data.state > data.dimmer_off_percentage;
  }
  current_status_data += formatNumber(data.power_wattage) + 'W';
  if (data.water_flow > 0) {
    current_status_data += ' - ' + formatNumber(data.water_flow) + 'L/m';
  }
  content_row.find('span.glyphicon').removeClass('blue green').addClass((on ? 'green' : 'blue'));
  content_row.find('h2 span.title').text(data.name);
  content_row.find('h2 span.current_usage').text(current_status_data);
  content_row.find('h2 span.manual_mode').toggle(data.manual_mode);
  //switch_row.find('.knob').val(power_switch.state).trigger('change');

  // Set the values only when empty
  content_row.find('input:not(.knob), select').each(function(counter,item) {
    if (item.name !== undefined && item.name !== '') {
      var name = item.name.replace(/switch_[0-9]+_/g,'');
      var field_value = $(item).val();
      try {
        if (field_value === '' || field_value === null || field_value == 0 || field_value == '00:00') {
          var value = data[name];
          if (!$.isArray(value)) {
            // Cast explicit to string to fix dropdown options
            value += '';
          }
          if (['timer_start','timer_stop'].indexOf(name) != -1) {
            value = moment(value, "HH:mm").format('LT');
          }
          $(item).val(value).trigger('change');
        }
      } catch (e) {
        console.log(e);
      }
    }
  });

  // Open or hide the dimmer values (will not trigger on the select field)
  if (dimmer) {
    content_row.find('.row.dimmer').show();
  } else {
    // Remove dimmer row, else form submit is 'stuck' on hidden fields that have invalid patterns... :(
    content_row.find('.row.dimmer').remove();
  }
}

function add_power_switch_setting_row(data,is_new) {
  if (source_row === null || source_row === '') {
    return false;
  }
  // Create new row
  var setting_row = $('<div>').addClass('row switch' + (is_new ? ' new' : '')).html(source_row.replace(/\[nr\]/g, $('form div.row.switch').length));
  if (data.id !== undefined) {
    // Set ID
    setting_row.attr('id','powerswitch_' + data.id);
  }
  // Re-initialize the select pulldowns
  //setting_row.find('span.select2.select2-container').remove();
  setting_row.find('select').select2({
    placeholder: '{{_('Select an option')}}',
    allowClear: false,
    minimumResultsForSearch: Infinity
  }).on('change',function() {
      if (this.name.indexOf('_timer_enabled') >= 0) {
        $(this).parents('.x_content').find('.row.timer').toggle('true' === this.value);
        if ('true' === this.value) {
          $(this).parents('.x_content').find('.row.timer input').attr('required','required');
        } else {
          $(this).parents('.x_content').find('.row.timer input').removeAttr('required');
        }
      }
  });
  // Disable hardware select box
  setting_row.find('select[name*="hardwaretype"]').attr("disabled", !is_new);

  // Add on the bottom before the submit row
  setting_row.insertBefore('div.row.submit');
}

function add_power_switch() {
  var form = $('.add-form');
  if (!check_form_data(form)) return false;

  // Create power switch data object and fill it with form data
  var data = {};
  form.find('input, select').each(function(counter,item) {
    if (item.name !== undefined && item.name !== '') {
      var fieldname = item.name.replace('switch_[nr]_','');
      var value = $(item).val();
      data[fieldname] = value;
    }
  });
  data['id'] = Math.floor(Date.now() / 1000);

  // Add new row
  add_power_switch_setting_row(data,true);
  // Update new row with new values
  update_power_switch(data);

  // Reset form
  form.find('input').val('');
  form.find('select').val(null).trigger('change');
  // Hide form
  form.modal('hide');

  reload_reload_theme();
}
/* End power switches code code */

/* Doors code */
function update_door_indicator(status) {
  var indicator = $('li#door_indicator');

  indicator.removeClass('disabled');
  indicator.find('span.open, span.closed, span.disabled').hide();

  if ('disabled' === status) {
    indicator.addClass('disabled');
    indicator.find('span.disabled').show();
    add_notification_message('door_messages',
                             '{{_('Disabled')}}',
                             '{{_('There are zero door sensors configured.')}}',
                             'fa-play-circle-o',
                             'orange');
    return;
  }

  var door_open = 'open' === status;
  if (door_open) {
    indicator.find('span.open').show();
  } else {
    indicator.find('span.closed').show();
  }

  update_door_messages('open' === status);
}

function update_door_messages(open,date) {
  var title   = (open ? '{{_('Open')}}' : '{{_('Closed')}}');
  var message = (open ? '{{_('Door is open')}}' : '{{_('Door is closed')}}');
  var icon    = (open ? 'fa-unlock' : 'fa-lock');
  var color   = (open ? 'red' : 'green');
  add_notification_message('door_messages', title, message, icon, color, date);
}

function load_door_history() {
  $.getJSON('/api/history/doors', function(door_data) {
    var door_status = {};
    $.each(door_data.doors, function(counter, statedata) {
      for (var i = 0; i < statedata.state.length; i++) {
        if (i == 0 || statedata.state[i][1] != statedata.state[i-1][1]) {
          door_status[statedata.state[i][0]] = statedata.state[i][1];
        }
      }
    });
    // Sort door data events on time. Needed if you have more than one door
    $.each(Object.keys(door_status).sort(), function(counter,change_time) {
      update_door_messages((door_status[change_time] === 1), change_time);
    })
  });
}

function add_door_status_row(data) {
  if (source_row === null || source_row === '') {
    return false;
  }
  // Create new row
  var new_row = $('<div>').addClass('row door').html(source_row);
  // Set ID
  new_row.attr('id','door_' + data.id);
  // Add to page
  $('div#maincontent').append(new_row);
}

function update_door(data) {
  // Load the switch row to update the data
  var content_row = $('div.row.door#' + 'door_' + data.id);

  // Update state icon
  content_row.find('div.door_status i').removeClass('fa-lock fa-unlock green red')
                                      .addClass((data.state === 'closed' ? 'fa-lock green' : 'fa-unlock red'))
                                      .attr('title',(data.state === 'closed' ? '{{_('Door is closed')}}' : '{{_('Door is open')}}'));

  // Set the name and status
  content_row.find('h2 span.title').text(data.name);

  // Set the values only when empty
  content_row.find('input:not(.knob), select').each(function(counter,item) {
    if (item.name !== undefined && item.name !== '') {
      var name = item.name.replace(/door_[0-9]+_/g,'');
      var field_value = $(item).val();
      try {
        if (field_value === '' || field_value === null) {
          var value = data[name];
          if (!$.isArray(value)) {
            // Cast explicit to string to fix dropdown options
            value += '';
          }
          $(item).val(value).trigger('change');
        }
      } catch (e) {
        console.log(e);
      }
    }
  });
}

function add_door_setting_row(data,is_new) {
  if (source_row === null || source_row === '') {
    return false;
  }
  // Create new row
  var setting_row = $('<div>').addClass('row door' + (is_new ? ' new' : '')).html(source_row.replace(/\[nr\]/g, $('form div.row.door').length));
  if (data.id !== undefined) {
    // Set ID
    setting_row.attr('id','door_' + data.id);
  }
  // Re-initialize the select pulldowns
  //setting_row.find('span.select2.select2-container').remove();
  setting_row.find('select').select2({
    placeholder: '{{_('Select an option')}}',
    allowClear: false,
    minimumResultsForSearch: Infinity
  });
  // Disable hardware select box
  setting_row.find('select[name*="hardwaretype"]').attr("disabled", !is_new);

  // Add on the bottom before the submit row
  setting_row.insertBefore('div.row.submit');
}

function add_door() {
  var form = $('.add-form');
  if (!check_form_data(form)) return false;

  // Create power switch data object and fill it with form data
  var data = {};
  form.find('input, select').each(function(counter,item) {
    if (item.name !== undefined && item.name !== '') {
      var fieldname = item.name.replace('door_[nr]_','');
      var value = $(item).val();
      data[fieldname] = value;
    }
  });
  data['id'] = Math.floor(Date.now() / 1000);

  // Add new row
  add_door_setting_row(data,true);
  // Update new row with new values
  update_door(data);

  // Reset form
  form.find('input').val('');
  form.find('select').val(null).trigger('change');
  // Hide form
  form.modal('hide');

  reload_reload_theme();
}
/* End Doors code */

/* Webcam code */
var realtime_sensor_data = {};
function updateWebcamLabel(marker) {
  if (marker.options.sensors.length > 0) {
    var message = [];
    $.each(marker.options.sensors,function(counter,value){
      if (message.length == 0) {
        message.push('<strong>' + realtime_sensor_data[value].name + '</strong>');
      }
      message.push(realtime_sensor_data[value].type.substr(0,4) + '. ' + (Math.round((realtime_sensor_data[value].current + Number.EPSILON) * 1000) / 1000) + '' + realtime_sensor_data[value].indicator);
    });
    marker.setTooltipContent(message.join('<br />'));
    $(marker._icon).addClass('reset');
    setTimeout(function(){
      $(marker._icon).removeClass('reset');
    },10);
  }
}

function createWebcamLabel(layer,x,y,sensors,edit) {
  edit = edit === true
  var marker_config = {
    draggable: edit,
    sensors: sensors.slice(0),
    layer: layer
  }

  if (!edit) {
    marker_config.icon = L.icon.pulse({iconSize:[10,10],color:'red'});
  }

  var marker = L.marker([x, y],marker_config).bindTooltip('<center><strong>{{_('Loading')}}...</strong></center>', {
      permanent: true,
      direction: y > 0 ? 'right' : 'left',
      opacity: 0.5,
  }).addTo(layer);

  if (edit) {
    marker.on('dragend',function(event){
      updateWebcamMarkers(layer);
    });

    marker.on('dblclick' ,function(event) {
      editWebcamMarker(this);
    });
  }

  if (marker_config.sensors.length > 0) {
    updateWebcamLabel(marker);
  }
  return marker;
}

function webcamArchive(webcamid) {

  var now = new Date();
  var max_days_back = 50;
  var no_data_counter = 0;
  var fancybox = null;

  function getImages(date) {

    $.getJSON('api/webcams/' + webcamid + '/archive/'+ date.getFullYear() + '/' + (date.getMonth() < 9 ? '0' : '') + (date.getMonth() + 1) + '/' + (date.getDate() < 10 ? '0' : '') + date.getDate(), function(data) {
      var photos = [];
      var date_match = /archive_(\d+)\.jpg$/g;

      no_data_counter += (data.webcams[0].archive_images.length > 0 ? 0 : 1);
      max_days_back--;

      if (no_data_counter > 10 || max_days_back < 0) {
        return false;
      }

      $.each(data.webcams[0].archive_images, function(index,value) {
        value.match(date_match);
        var date_photo = date_match.exec(value);
        if (date_photo != null && date_photo.length == 2) {
          date_photo = moment(date_photo[1]* 1000).format('LLL');
        } else {
          date_photo = '{{_('Unknown date')}}';
        }

        if (fancybox == null) {
          fancybox = $.fancybox.open(
            [{src : value,opts: { caption: '{{_('Webcam')}}' + ' ' + data.webcams[0].name + ': ' + date_photo}}],
            {loop : false,
             buttons : [
                     //'slideShow',
                     'fullScreen',
                     'thumbs',
                     //'share',
                     'download',
                     'zoom',
                     'close']
             }
          );
        } else {
          if ($.fancybox.getInstance()) {
            fancybox.addContent({src : value, opts: { caption: '{{_('Webcam')}}' + ' ' + data.webcams[0].name + ': ' + date_photo}});
          }
        }
      });
      // recursive
      if ($.fancybox.getInstance() || data.webcams[0].archive_images.length == 0) {
        setTimeout(function(){
          getImages(new Date(date.getTime() - (24 * 60 * 60 * 1000)));
          }, ((data.webcams[0].archive_images.length + 1) * 10));
      } else {
        fancybox == null;
      }
    });
  }
  getImages(now);
}

function updateWebcamMarkers(layer) {
  var all_markers = '';
  layer.eachLayer(function(datamarker) {
    var pos = datamarker.getLatLng();
    all_markers += pos.lat + ',' + pos.lng + ',' + datamarker.options.sensors.join(',') + ';';
  });
  $('div.row.webcam#webcam_' + layer.options.webcamid).find('input[type="hidden"][name$="_realtimedata"]').val(all_markers.slice(0,-1));
}

function addWebcamMarker(layer) {
  editWebcamMarker(createWebcamLabel(layer,0,0,[],true));
}

function editWebcamMarker(marker) {
  var pull_down = $('select[name="webcam_realtime_sensors_list"]');
  pull_down[0].marker = marker;
  pull_down.val(marker.options.sensors).trigger('change');

  $('#add_sensors').off('click').on('click',function(event){
    marker.options.sensors = pull_down.val();
    updateWebcamMarkers(marker.options.layer);
    updateWebcamLabel(marker);
  });

  $('#del_marker').off('click').on('click',function(event){
    marker.options.layer.removeLayer(marker);
    updateWebcamMarkers(marker.options.layer);
    marker.remove();
  });
  $('.realtime-data-form').modal('show');
}

function initWebcam(data) {
  if (data.edit !== true) {
    // Init the HTML
    var webcam_row = $(source_row).attr('id','webcam_' + data.id);
    // Set the name and status
    webcam_row.find('h2 span.title').text(data.name);
    // Append the page
    $('div.row.webcam').append(webcam_row);
    // Resize the height to get the maps working
    webcam_row.find('div.webcam_player').height(webcam_row.width()-webcam_row.find('.x_title').height());
  }

  var webcam = L.map($('#webcam_' + data.id + ' div.webcam_player' + (data.edit === true ? '_preview' : ''))[0],{
    id: 'map_' + data.id,
    fullscreenControl: true,
    refresh_timer : null
  }).on('load',function(event){
    this.options.refresh_timer = setInterval(function(){
      if (!webcam._container.clientHeight > 0) {
         clearTimeout(webcam.options.refresh_timer);
         setTimeout(function(){
           webcam.remove();
         },10);
      }
    },10 * 1000);
  }).setView([0, 0], 1);

  if (data.is_live) {
    L.videoOverlay('webcam/' + data.id + '/stream.m3u8', L.latLngBounds([[ 150, -180], [ -150, 180]]), {
      id: 'overlay_' + data.id,
      interactive: false,
      autoplay: true,
      className: 'webcam_live_' + data.id,
    }).addTo(webcam);
  } else {
    L.tileLayer('/webcam/{id}/{id}_tile_{z}_{x}_{y}.jpg?_{time}', {
      time: function() {
        return (new Date()).valueOf();
      },
      id: data.id,
      noWrap: true,
      continuousWorld: false,
      maxNativeZoom: data.max_zoom,
      maxZoom: data.max_zoom + 1,
      refresh_timer : null
    }).on('remove',function(event){
      clearTimeout(this.options.refresh_timer);
    }).on('add',function(event){
      var webcam_tiler = this;
      this.options.refresh_timer = setInterval(function(){
        webcam_tiler.redraw();
      },30 * 1000)
    }).addTo(webcam);
  }

  var realtime_data_layer = L.layerGroup([], {webcamid : data.id, refresh_timer: null});
  realtime_data_layer.on('remove',function(event){
    clearTimeout(this.options.refresh_timer);
  });

  realtime_data_layer.on('add',function(event) {
    this.options.refresh_timer = setInterval(function(){
      if (realtime_data_layer.getLayers().length > 0) {
        $.get('/api/sensors',function(data) {
          realtime_sensor_data = {};
          $.each(data.sensors,function(counter,value){
            realtime_sensor_data[value.id + ''] = value;
          });
          realtime_data_layer.eachLayer(function(marker) {
            updateWebcamLabel(marker);
          });
        });
      }
    },30 * 1000);
  });
  realtime_data_layer.addTo(webcam);

  if ('' !== data.realtimedata) {
    realtime_sensor_data = {};
    $.get('/api/sensors',function(sensor_data) {
      $.each(sensor_data.sensors,function(counter,value){
        realtime_sensor_data[value.id + ''] = value;
      });
      $.each(data.realtimedata.split(';'),function(counter,value) {
        var tmpdata = value.split(',');
        createWebcamLabel(realtime_data_layer,tmpdata.shift(),tmpdata.shift(),tmpdata, data.edit === true);
      });
    });
  }

  L.Control.ExtraWebcamControls = L.Control.extend({
    options: {
      position: 'topleft',
      archive: data.archive
    },
    initialize: function (options) {
      // constructor
      L.Util.setOptions(this, options);
    },
    onAdd: function (map) {
      var container = L.DomUtil.create('div', 'leaflet-control-takephoto leaflet-bar leaflet-control');

      if (data.edit !== true) {
        this.photo_link = L.DomUtil.create('a', 'leaflet-control-takephoto-button leaflet-bar-part', container);
        this.photo_link.title = '{{_('Save RAW photo')}}';
        this.photo_link.target = '_blank';
        this.photo_link.href = '/webcam/' + data.id + '/' + data.id + '_raw.jpg';
        L.DomUtil.create('i', 'fa fa-camera', this.photo_link);

        if (this.options.archive) {
          this.archive_link = L.DomUtil.create('a', 'leaflet-control-archive-button leaflet-bar-part', container);
          this.archive_link.href = '#';
          this.archive_link.title = '{{_('Archive')}}';
          L.DomEvent.on(this.archive_link, 'click', this._start_archive, this);
          L.DomUtil.create('i', 'fa fa-archive', this.archive_link);
        }
      }

      if ('' !== data.realtimedata || data.edit === true) {
        this.info_link = L.DomUtil.create('a', 'leaflet-control-info-button leaflet-bar-part', container);
        this.info_link.href = '#';
        this.info_link.title = '{{_('Toggle information')}}';
        L.DomEvent.on(this.info_link, 'click', this._toggle_realtime_info, map);
        L.DomUtil.create('i', 'fa fa-info', this.info_link);
      }

      if (data.edit === true) {
        this.add_marker_link = L.DomUtil.create('a', 'leaflet-control-addmarker-button leaflet-bar-part', container);
        this.add_marker_link.href = '#';
        this.add_marker_link.title = '{{_('Add marker')}}';
        L.DomEvent.on(this.add_marker_link, 'click', this._add_marker, realtime_data_layer);
        L.DomUtil.create('i', 'fa fa-map-marker', this.add_marker_link);
      }

      if (data.is_live === true) {
        this.toggle_audio = L.DomUtil.create('a', 'leaflet-control-audio-button leaflet-bar-part', container);
        this.toggle_audio.href = '#';
        this.toggle_audio.title = '{{_('Toggle audio')}}';
        L.DomEvent.on(this.toggle_audio, 'click', this._toggle_audio);
        L.DomUtil.create('i', 'glyphicon glyphicon-volume-up', this.toggle_audio);
      }

      return container;
    },
    _start_archive: function (e) {
      L.DomEvent.stopPropagation(e);
      L.DomEvent.preventDefault(e);
      webcamArchive(data.id);
    },
    _toggle_realtime_info: function (e) {
      L.DomEvent.stopPropagation(e);
      L.DomEvent.preventDefault(e);
      if (this.hasLayer(realtime_data_layer)) {
        this.removeLayer(realtime_data_layer);
      } else {
        this.addLayer(realtime_data_layer);
      }
    },
    _add_marker: function(e) {
      L.DomEvent.stopPropagation(e);
      L.DomEvent.preventDefault(e);
      editWebcamMarker(createWebcamLabel(this,0,0,[],true));
    },
    _toggle_audio: function(e) {
      L.DomEvent.stopPropagation(e);
      L.DomEvent.preventDefault(e);
      var video = $('.webcam_live_' + data.id)[0];
      video.muted = !video.muted;
      $(this).find('.glyphicon').removeClass('glyphicon-volume-up glyphicon-volume-down').addClass(video.muted ? 'glyphicon-volume-up' : 'glyphicon-volume-off')
    }
  });
  webcam.addControl(new L.Control.ExtraWebcamControls());
  webcam.addControl(L.Control.loading({separate: true}));

  if (data.is_live) {
    var video = $('.webcam_live_' + data.id)[0];
    video.muted = true;
    if (Hls.isSupported()) {
      var hls = new Hls();
      hls.loadSource('webcam/' + data.id + '/stream.m3u8');
      hls.attachMedia(video);
      hls.on(Hls.Events.MANIFEST_PARSED, function() {
        video.play();
      });
    }
    // hls.js is not supported on platforms that do not have Media Source Extensions (MSE) enabled.
    // When the browser has built-in HLS support (check using `canPlayType`), we can provide an HLS manifest (i.e. .m3u8 URL) directly to the video element through the `src` property.
    // This is using the built-in support of the plain video element, without using hls.js.
    // Note: it would be more normal to wait on the 'canplay' event below however on Safari (where you are most likely to find built-in HLS support) the video.src URL must be on the user-driven
    // white-list before a 'canplay' event will be emitted; the last video event that can be reliably listened-for when the URL is not on the white-list is 'loadedmetadata'.
    else if (video.canPlayType('application/vnd.apple.mpegurl')) {
      video.src = 'webcam/' + data.id + '/stream.m3u8';
      video.addEventListener('loadedmetadata', function() {
        video.play();
      });
    }
  }
}

function add_webcam_setting_row(data,is_new) {
  if (source_row === null || source_row === '') {
    return false;
  }
  // Create new row
  var setting_row = $('<div>').addClass('row webcam' + (is_new ? ' new' : '')).html(source_row.replace(/\[nr\]/g, $('form div.row.webcam').length));
  if (data.id !== undefined) {
    // Set ID
    setting_row.attr('id','webcam_' + data.id);
  }

  // Re-initialize the select pulldowns
  //setting_row.find('span.select2.select2-container').remove();
  setting_row.find('select').select2({
    placeholder: '{{_('Select an option')}}',
    allowClear: false,
    minimumResultsForSearch: Infinity
  }).on('change',function() {
    $(this).parents('.x_content').find('img').removeClass('webcam_90 webcam_180 webcam_270 webcam_H webcam_V').addClass('webcam_' + this.value);

    if (this.name.endsWith('_archive')) {
      var motionEnabled = ('motion' === this.value);
      $(this).parents('.x_content').find('.motion_option').toggle(motionEnabled);
    }
  });
  // Add on the bottom before the submit row
  setting_row.insertBefore('div.row.submit');
}

function update_webcam(data) {
  // Load the switch row to update the data
  var content_row = $('div.row.webcam#' + 'webcam_' + data.id);

  content_row.find('h2 span.title').text(data.name);

  // Set the values only when empty
  content_row.find('input:not(.knob), select').each(function(counter,form_field) {
    if (form_field.name !== undefined && form_field.name !== '') {
      var field_value = $(form_field).val();
      if (field_value === '' || field_value === null) {
        var name = form_field.name.replace(/webcam_[0-9]+_/g,'').split('_');
        var value = data[name[0]];
        // Loop over array data or objects
        for (var i = 1; i < name.length; i++) {
          value = value[name[i]];
        }
        if (!$.isArray(value)) {
          // Cast explicit to string to fix dropdown options
          value += '';
        }
        $(form_field).val(value).trigger('change');
      }
    }
  });
}

function add_webcam() {
  var form = $('.add-form');
  if (!check_form_data(form)) return false;

  // Create power switch data object and fill it with form data
  var data = {};
  form.find('input, select').each(function(counter,item) {
    if (item.name !== undefined && item.name !== '') {
      var fieldname = item.name.replace('webcam_[nr]_','');
      var value = $(item).val();
      data[fieldname] = value;
    }
  });
  data['id'] = Math.floor(Date.now() / 1000);
  // Dirty hack...
  data.resolution = {'width' : data.resolution_width, 'height' : data.resolution_height};

  // Add new row
  add_webcam_setting_row(data,true);
  // Update new row with new values
  update_webcam(data);

  // Reset form
  form.find('input').val('');
  form.find('select').val(null).trigger('change');
  // Hide form
  form.modal('hide');

  reload_reload_theme();
}
/* End webcam code */


/* Audio code */
/* Audio player */
function update_player_messages(data) {
  update_player_volume(data.volume);
  var title   = (data.running ? '{{_('Playing')}}' : '{{_('Stopped')}}');
  var message = (data.running ? '{{_('Playlist')}}: ' + data.name + ' - ' + moment(data.start, "HH:mm").format('LT') + '-' + moment(data.stop, "HH:mm").format('LT'): '{{_('Not playing')}}');
  var icon    = (data.running ? 'fa-play-circle-o' : 'fa-play-circle-o');
  var color   = (data.running ? 'green' : 'red');
  add_notification_message('player_messages', title, message, icon, color);
}

function update_player_volume(volume) {
  var menu = $('ul#player_messages');
  menu.find('li.notification:not(:has(.player_volume))').remove();

  if ($('div.row.player_volume').length == 0) {
    var volume_control = $('<div>').addClass('row player_volume');
    volume_control.append($('<div>').addClass('col-md-1').append($('<span>').addClass('fa fa-volume-down').on('click',function(){
      $.post('/api/audio/player/volumedown');
      return false;
    })));
    volume_control.append($('<div>').addClass('col-md-10  progress progress-striped active').append($('<div>').addClass('progress-bar progress-bar-success').attr('data-transitiongoal',volume).text(volume + '%')));
    volume_control.append($('<div>').addClass('col-md-1').append($('<span>').addClass('fa fa-volume-up').on('click',function(){
      $.post('/api/audio/player/volumeup');
      return false;
    })));
    menu.prepend($('<li>').addClass('notification').append(volume_control));
    $('ul#player_messages .progress .progress-bar').progressbar();
  } else {
    $('div.row.player_volume .progress-bar.progress-bar-success').css('width', volume + '%').text(volume + '%');
  }
}

function load_player_status() {
  $.getJSON('/api/audio/playing', function(player_data) {
    update_player_indicator(player_data);
  });
}

function update_player_indicator(data) {
  var indicator = $('li#player_indicator');
  indicator.removeClass('disabled');
  indicator.find('span.running, span.stopped, span.disabled').hide();

  if ('disabled' === data.running) {
    indicator.addClass('disabled');
    indicator.find('span.disabled').show();
    add_notification_message('player_messages',
                             '{{_('Disabled')}}',
                             '{{_('Either add audio files and playlists. Or you have a pwm-dimmer switch configured.')}}',
                             'fa-play-circle-o',
                             'orange');
    return;
  }

  if (data.running) {
    indicator.find('span.running').show();
  } else {
    indicator.find('span.stopped').show();
  }
  update_player_messages(data);
}
/* End audio player */

/* Audio playlist code */
function update_audio_playlist(data) {
  // Load the switch row to update the data
  var content_row = $('div.row.playlist#' + 'playlist_' + data.id);

  // Update title
  content_row.find('h2 span.title').text(data.name);

  // Update duration
  content_row.find('h2 small').text(moment.duration(( data.repeat ? data.duration : data.songs_duration ) * 1000).humanize());

  // Set the values only when empty
  content_row.find('input:not(.knob), select').each(function(counter,item) {
    if (item.name !== undefined && item.name !== '') {
      var name = item.name.replace(/playlist_[0-9]+_/g,'');
      var field_value = $(item).val();
      try {
        if (field_value === '' || field_value === null || ['repeat','shuffle'].indexOf(name) != -1) {
          var value = data[name];
          if (!$.isArray(value)) {
            // Cast explicit to string to fix dropdown options
            value += '';
          }
          if (['repeat','shuffle'].indexOf(name) != -1) {
            value = (value == 'true' || value == true || value == 1);
          }
          $(item).val(value).trigger('change');
        }
      } catch (e) {
        console.log(e);
      }
    }
  });
}

function add_audio_playlist_setting_row(data,is_new) {
  if (source_row === null || source_row === '') {
    return false;
  }
  // Create new row
  var setting_row = $('<div>').addClass('row playlist' + (is_new ? ' new' : '')).html(source_row.replace(/\[nr\]/g, $('form div.row.playlist').length));
  if (data.id !== undefined) {
    // Set ID
    setting_row.attr('id','playlist_' + data.id);
  }
  // Re-initialize the select pulldowns
  setting_row.find('select').select2({
    placeholder: '{{_('Select an option')}}',
    allowClear: false,
    minimumResultsForSearch: Infinity
  });

  setting_row.find('.js-switch').each(function(index,html_element){
    this.checked = (this.name.indexOf('_repeat') != -1 && data.repeat == true) || (this.name.indexOf('_shuffle') != -1 && data.shuffle == true)
    var switchery = new Switchery(this);
    html_element.onchange = function() {
      this.value = this.checked;
    };
  });

  // Add on the bottom before the submit row
  setting_row.insertBefore('div.row.submit');
}

function add_audio_playlist() {
  var form = $('.add-form');
  if (!check_form_data(form)) return false;

  // Create power switch data object and fill it with form data
  var data = {};
  form.find('input, select').each(function(counter,item) {
    if (item.name !== undefined && item.name !== '') {
      var fieldname = item.name.replace('playlist_[nr]_','');
      var value = $(item).val();
      if (['repeat','shuffle'].indexOf(fieldname) != -1) {
        value = (value == 'true' || value == true || value == 1);
      }
      data[fieldname] = value;
    }
  });
  data['id'] = Math.floor(Date.now() / 1000);

  // Add new row
  add_audio_playlist_setting_row(data,true);
  // Update new row with new values
  update_audio_playlist(data);

  // Reset form
  form.find('input').val('');

  form.find('input[name="repeat"]').val(false);
  form.find('input[name="shuffle"]').val(false);

  form.find('select').val(null).trigger('change');
  // Hide form
  form.modal('hide');

  reload_reload_theme();
}
/* End audio playlist code */

/* Audio files code */
function preview_audio_file(audio_file_id, audio_file_name) {
  var modal = $('.modal.fade.preview_player');
  modal.find('.modal-body h4').text(audio_file_name);
  modal.find('.modal-body p').html('<audio controls autoplay><source src="/audio/' + audio_file_name + '" /></audio>');
}

function delete_audio_file(audio_file_id, audio_file_name) {
  if (confirm('{{_('Are you sure to delete the file')}}: \'' + audio_file_name + '\' ?')) {
    $.ajax({
      url: "/api/audio/file/" + audio_file_id,
      type: "DELETE",
      dataType : "json",
    }).done(function(response) {
      if (response.ok) {
        ok_notification_bubble(response.title,response.message);
      } else {
        error_notification_bubble(response.title,response.message);
      }
    });
  }
}
/* End audio files code */
/* End audio code */

/* Profile code */
function init_wysiwyg() {
  function init_ToolbarBootstrapBindings() {

    var fonts = [ 'Serif', 'Sans', 'Arial', 'Arial Black', 'Courier',
                  'Courier New', 'Comic Sans MS', 'Helvetica', 'Impact', 'Lucida Grande', 'Lucida Sans', 'Tahoma', 'Times',
                  'Times New Roman', 'Verdana'
                ],
        fontTarget = $('.fa.fa-font').parent().siblings('.dropdown-menu');
    $.each(fonts, function(idx, fontName) {
      fontTarget.append($('<li><a data-edit="fontName ' + fontName + '" style="font-family:\'' + fontName + '\'">' + fontName + '</a></li>'));
    });
/*
    $('.btn-toolbar.editor a[title]').tooltip({
      container: 'body'
    });
*/
    $('.dropdown-menu input').click(function() {
      return false;
    }).change(function() {
      $(this).parent('.dropdown-menu').siblings('.dropdown-toggle').dropdown('toggle');
    }).keydown('esc', function() {
      this.value = '';
      $(this).change();
    });

    $('[data-role=magic-overlay]').each(function() {
      var overlay = $(this),
          target = $(overlay.data('target'));
      overlay.css('opacity', 0).css('position', 'absolute').offset(target.offset()).width(target.outerWidth()).height(target.outerHeight());
    });

    if ("onwebkitspeechchange" in document.createElement("input")) {
      var editorOffset = $('#editor').offset();

      $('.voiceBtn').css('position', 'absolute').offset({
        top: editorOffset.top,
        left: editorOffset.left + $('#editor').innerWidth() - 35
      });
    } else {
      $('.voiceBtn').hide();
    }
  }

  function showErrorAlert(reason, detail) {
    var msg = '';
    if (reason === 'unsupported-file-type') {
      msg = "Unsupported format " + detail;
    } else {
      console.log("error uploading file", reason, detail);
    }
    $('<div class="alert"> <button type="button" class="close" data-dismiss="alert">&times;</button>' +
      '<strong>File upload error</strong> ' + msg + ' </div>').prependTo('#alerts');
  }

  $('.editor-wrapper').each(function(){
    var id = $(this).attr('id');	//editor-one
    $(this).wysiwyg({
      toolbarSelector: '[data-target="#' + id + '"]',
      fileUploadError: showErrorAlert
    });
  });

  init_ToolbarBootstrapBindings();
  window.prettyPrint;
  prettyPrint();
};

function edit_profile() {
  $('form#profile').toggleClass('edit');
  if ($('form#profile').hasClass('edit')) {
    init_wysiwyg();

    $('input[name="age"]').daterangepicker({
      singleDatePicker: true,
    });
  }
  return false;
}

function uploadProfileImage() {
  var file = $('<input>').attr({'type':'file','name':'profile_image'}).on('change',function() {
    var fd = new FormData();
    fd.append('profile_image',file[0].files[0]);
    $.ajax({
        url: '/api/config/profile',
        type: 'POST',
        data: fd,
        enctype: 'multipart/form-data',
        success:function(data){
           load_page('profile.html');
        },
        cache: false,
        contentType: false,
        processData: false
    });
  });
  file.click();
}
/* End profile code */

function load_calendar_history() {
  $.getJSON('/api/calendar', function(data) {
    $('ul.nav.navbar-nav.navbar-right ul#calendar_messages li.notification:not(.no_message)').remove();
    var messages_in_future = 0;
    var now = new Date();
    $.each(data, function(counter, calendardata) {
      var event_date = new Date(calendardata.start);
      if (new Date(calendardata.end) > now) {
        messages_in_future++;
      }
      add_notification_message('calendar_messages',
                               calendardata.title,
                               calendardata.description,
                               'fa-calendar',
                               'green',
                               event_date.getTime() + (event_date.getTimezoneOffset() * 60000),
                               'calendar.html');
    });
    if (messages_in_future == 0) {
      $('ul.nav.navbar-nav.navbar-right li#calendar span.badge.bg-green').addClass('hidden');
    } else {
      $('ul.nav.navbar-nav.navbar-right li#calendar span.badge.bg-green').removeClass('hidden').text(messages_in_future);
    }
    $('ul.nav.navbar-nav.navbar-right ul#calendar_messages li.no_message').toggle(data.length==0);
  });
}

function calendar_item(options) {
  if (options === undefined) {
      options = {id : null,
                 start : new Date(),
                 end : new Date(),
                 title: '',
                 description: ''};
  }

  if (options.end === undefined || options.end === null || '' === options.end) {
    options.end = options.start;
  }

  $('input[name="calendar_id"').val(options.id);
  $('input[name="calendar_title"').val(options.title);
  $('input[name="calendar_description"').val(options.description);
  $('#editor-one').html(options.description);

  $('#calendar_date').daterangepicker({
    startDate: options.start,
    endDate: options.end,
    singleDatePicker: false,
    autoUpdateInput: true,
    autoApply: true,
    parentEl: '#calendar_date_picker'
  });

  // Create a trigger to toggle the calendar. But we have to wait until the modal window is starting to show...
  modalWindow = $('.add-form').on('show.bs.modal',function(event) {
    setTimeout(function(){
      $('#calendar_date').trigger('click');
      init_wysiwyg();
    },250);
  });

  modalWindow.modal('show');
}

/**
 * Sort values alphabetically in select
 * source: http://stackoverflow.com/questions/12073270/sorting-options-elements-alphabetically-using-jquery
 */
$.fn.extend({
  sortSelect() {
    var options = this.find("option"),
      arr = options.map(function(_, o) { return { t: $(o).text(), v: o.value }; }).get();

    arr.sort(function(o1, o2) { // sort select
      var t1 = o1.t.toLowerCase(),
          t2 = o2.t.toLowerCase();
      return t1 > t2 ? 1 : t1 < t2 ? -1 : 0;
    });

    options.each(function(i, o) {
      o.value = arr[i].v;
      $(o).text(arr[i].t);
    });
  }
});

function terrariumpi_select2_option(state){
  if (!state.id) {
    return state.text;
  }
  return $('<div class="terrariumpi_select2_option" title="' + state.text + '">' + state.text + '</div>');
}
$.fn.select2.defaults.set("templateResult", terrariumpi_select2_option);

function christmas() {
  if (moment(moment().year() + '-12-25').week() == moment().week()) {
    $('img.christmashat').show();
  } else {
    $('img.christmashat').hide();
  }
}

function fireworks() {
  if ('12-31' == moment().format('MM-DD') || '01-01' == moment().format('MM-DD')) {
    $('div.left_col.menu div.profile').after('<canvas id="fireworks" width="100%"></canvas><br>');
    $('body').append('<script src="/static/js/fireworks.js" type="text/javascript"></script>');
  }
}


// Start it all.....
$(document).ready(function() {
  moment.locale(globals.language);
  // NProgress bar animation during Ajax calls
  $(document).on({
    ajaxSend: function() {
      if (globals.ajaxloader === 0) {
        NProgress.start();
      }
      globals.ajaxloader++;
    },
    ajaxComplete: function() {
      globals.ajaxloader--;
      if (globals.ajaxloader === 0) {
        NProgress.done();
      }
    }
  });

  init_sidebar();

  $('#system_time span').text(moment().format('LLLL'));
  websocket_init(false);
  // Bind to menu links in order to load Ajax calls
  $('#sidebar-menu a').each(function() {
    $(this).on('click', load_page).attr('title',$(this).parents('li').find('a:first').text());
  });

  $("<div id='tooltipGraph' title='tooltip'>&nbsp;&nbsp;&nbsp;</div>").css({
      position: "absolute",
  }).appendTo("body").tooltip({html:true}).on('hidden.bs.tooltip',function(event){
    $('#tooltipGraph').hide();
  })

  load_door_history();
  load_calendar_history();
  load_player_status();
  load_page('dashboard.html');

  setInterval(function() {
    notification_timestamps();
    $('#system_time span').text(moment().format('LLLL'));
    christmas();
    fireworks();
  }, 30 * 1000);

  christmas();
  fireworks();
  version_check();
});
