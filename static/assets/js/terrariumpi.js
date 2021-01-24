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
Array.prototype.avg = function() {
  let size = this.length;
  return (this.reduce(function(a,b){return a+b;}) / size);
}

String.prototype.capitalize = function() {
  return this.charAt(0).toUpperCase() + this.slice(1);
}

function formatCurrency(amount,minfrac,maxfrac) {
  minfrac = minfrac || 2;
  maxfrac = maxfrac || 2;

  return (1 * amount).toLocaleString(window.terrariumPI.language.replace('_','-'), {
    style: 'currency',
    currency: 'EUR',
    minimumFractionDigits: minfrac,
    maximumFractionDigits: maxfrac
  });
}

function formatNumber(amount,minfrac,maxfrac) {
  minfrac = minfrac || 0;
  maxfrac = maxfrac || 3;

  return (1 * amount).toLocaleString(window.terrariumPI.language.replace('_','-'), {
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

function template_sensor_type_color(type) {
  switch(type) {
    case 'temperature':
      return 'text-danger';
      break;
    case 'humidity':
    case 'watertank':
      return 'text-primary';
      break;
    case 'moisture':
      return 'text-info';
      break;
    case 'distance':
      return 'fa-signal'
      break;
    case 'light':
    case 'lights':
    case 'uvi':
    case 'uva':
    case 'uvb':
    case 'ldr':
      return 'text-warning';
      break;
    case 'ph':
      return 'fa-flask'
      break;
    case 'fertility':
    case 'conductivity':
      return 'text-success'
      break;
    case 'co2':
    case 'altitude':
      return 'text-secondary'
      break;
    case 'pressure':
      return 'fa-cloud-upload-alt'
      break;
    case 'magnetic':
      return 'fa-lock'
      break;
    case 'motion':
      return 'fa-walking'
      break;
  }
}

function template_sensor_type_icon(type) {
  switch(type) {
    case 'temperature':
      return 'fa-thermometer-half'
      break;
    case 'humidity':
      return 'fa-tint'
      break;
    case 'moisture':
      return 'fa-water'
      break;
    case 'distance':
      return 'fa-signal'
      break;
    case 'light':
    case 'lights':
      return 'fa-lightbulb'
      break;
    case 'ph':
      return 'fa-flask'
      break;
    case 'uvi':
      return 'fa-sun'
      break;
    case 'uva':
      return 'fa-adjust'
      break;
    case 'uvb':
      return 'fa-adjust fa-rotate-180'
      break;
    case 'fertility':
    case 'conductivity':
      return 'fa-seedling'
      break;
    case 'co2':
      return 'fa-wind'
      break;
    case 'altitude':
      return 'fa-level-up-alt'
      break;
    case 'pressure':
      return 'fa-cloud-upload-alt'
      break;
    case 'magnetic':
      return 'fa-lock'
      break;
    case 'ldr':
      return 'fa-lightbulb'
      break;
    case 'motion':
      return 'fa-walking'
      break;
    case 'watertank':
      return 'fa-faucet'
      break;
  }
}

function country_icon(value){
  value = value.split('_');
  if (value.length != 2) {
    return false;
  }
  value = value.pop().toLowerCase();
  if (value.length != 2) {
    return false;
  }
  return 'flag-icon-' + value;
}

function formatState (state) {
  if (!state.id) {
    return state.text;
  }

  if (icon = template_sensor_type_icon(state.element.value)) {
    return jQuery('<span><i class="mr-1 fa-fw fas ' + template_sensor_type_icon(state.element.value) + '"></i> ' + state.text + '</span>');
  }
  if (icon = country_icon(state.element.value)) {
    return jQuery('<span><i class="mr-1 flag-icon-background flag-icon ' + country_icon(state.element.value) + '"></i>' + state.text + '</span>');
  }

  return state.text;
};

function get_template_color(classname, transparantcy, hexformat) {
  const hex = d => Number(d).toString(16).padStart(2, '0')

  let span = jQuery('<span>').addClass('d-none').addClass(classname).text('test').appendTo(jQuery('body')); // Need to append to body to make the color rendering work. Else we do not have a color
  let color = span.css('color') || span.css('backgroundColor');
  // Remove the span now we have the color
  span.remove();

  if (transparantcy) {
    color = color.replace('rgb(','rgba(');
    color = color.replace(')',',' + transparantcy + ')');
  }

  if (hexformat) {
    const regex = /rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)/gm;
    color = regex.exec(color);
    color = '#' + hex(color[1]) + hex(color[2]) + hex(color[3])
  }

  return color;
}

function sensor_type_indicator(sensor_type) {
  //console.log('sensor_type_indicator', sensor_type, window.terrariumPI.units[sensor_type])
  return window.terrariumPI.units[sensor_type];
}

function sensor_gauge(canvas, type, current, limit_min, limit_max, alarm_min, alarm_max) {

  sensor_gauge_obj = {
    _redraw : false,
    _gauge : null,
    _canvas : null,
    _indicator : null,
    _type: type,

    _error_badge : null,
    _warning_badge : null,
    _exclude_badge: null,
    _last_update: null,

    get current() {
      return this._current;
    },

    set current(value) {
      if (!this._canvas.is(':visible')) {
        //console.log('Gauge is hidden: ',this._canvas.attr('id'));

        this.stop();
        return
      }
      this._redraw = this._current != value;
      this._current = value;
      this._gauge.set(this.current);
      if (this._type == 'size') {
        this._indicator.text(formatBytes(this.current));
      } else {
        this._indicator.text(formatNumber(this.current) + ' ' + sensor_type_indicator(this._type));
      }


//      console.log(this)

      this._warning_badge.toggle(!(this.alarm_max >= this.current && this.current >= this.alarm_min));

//      this._warning_badge.text(( this.alarm_max >= this.current && this.current >= this.alarm_min  ? '' : this._warning_badge.data('message')));
      this._error_badge.text(value !== null ? '' : this._error_badge.data('message'));


      this._last_update.text(moment().format('LLL'))
    },

    get limit_min() {
      return this._limit_min;
    },

    set limit_min(value) {
      this._redraw = this._current != value;
      this._limit_min = value;
      this.draw();
    },

    get limit_max() {
      return this._limit_max;
    },

    set limit_max(value) {
      this._redraw = this._current != value;
      this._limit_max = value;
      this.draw();
    },

    get alarm_min() {
      return this._alarm_min;
    },

    set alarm_min(value) {
      this._redraw = this._current != value;
      this._alarm_min = value;
      this.draw();
    },

    get alarm_max() {
      return this._alarm_max;
    },

    set alarm_max(value) {
      this._redraw = this._current != value;
      this._alarm_max = value;
      this.draw();
    },

    get _colors() {
      let total_area = this.limit_max - this.limit_min;
      return [
        [0.00, get_template_color('text-danger',false,true)],
        [(this.alarm_min - this.limit_min) / total_area, get_template_color('text-warning',false,true)],
        [(((this.alarm_min + this.alarm_max)/2) - this.limit_min) / total_area, get_template_color('text-success',false,true)],
        [(this.alarm_max - this.limit_min) / total_area, get_template_color('text-warning',false,true)],
        [1.00, get_template_color('text-danger',false,true)]
      ]
    },

    stop: function() {
      delete(this._gauge);
      let id = this._canvas.attr('id')
      this._canvas.remove();

      delete(window.terrariumPI.gauges[id]);
    },

    draw: function() {
      if (this._redraw && this._canvas != null && this._canvas.length == 1) {
        let opts = {
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
          percentColors: this._colors,
        }

        this._gauge = new Gauge(this._canvas[0]).setOptions(opts);
        this._gauge.maxValue = this.limit_max;
        this._gauge.setMinValue(this.limit_min);
      }
    }
  }


  sensor_gauge_obj.limit_min = limit_min;// || 0;
  sensor_gauge_obj.limit_max = limit_max;// || 100;
  sensor_gauge_obj.alarm_min = alarm_min;// || sensor_gauge_obj.limit_min + ((sensor_gauge_obj.limit_max - sensor_gauge_obj.limit_min) * 0.25);
  sensor_gauge_obj.alarm_max = alarm_max;// || sensor_gauge_obj.limit_max - ((sensor_gauge_obj.limit_max - sensor_gauge_obj.limit_min) * 0.25);
  sensor_gauge_obj._canvas = jQuery('#' + canvas + ':visible');

  sensor_gauge_obj._indicator = jQuery('<small>').addClass('d-block').text('indicator');
  sensor_gauge_obj._canvas.parent().append(sensor_gauge_obj._indicator);

  sensor_gauge_obj._error_badge   = sensor_gauge_obj._canvas.parents('.card').find('.badge.badge-danger');
  sensor_gauge_obj._warning_badge = sensor_gauge_obj._canvas.parents('.card').find('.badge.badge-warning');
  sensor_gauge_obj._exclude_badge = sensor_gauge_obj._canvas.parents('.card').find('.badge.badge-primary');

  sensor_gauge_obj._last_update   = sensor_gauge_obj._canvas.parents('.card').find('.last_update');

  sensor_gauge_obj.draw();
  sensor_gauge_obj.current = current;

  // Store global/cached version
  delete(window.terrariumPI.gauges[canvas])
  window.terrariumPI.gauges[canvas] = sensor_gauge_obj;

  return window.terrariumPI.gauges[canvas]
}

function graph(canvas, source, type) {


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

      //console.log(array);

      var sum = 0, count = 0, val = 0;
      for (var i in array){
          val = array[i];
          //console.log(i,array[i],array);
          if (!qualifier || qualifier(val)){
              sum += val;
              count++;
          }
      }

      //console.log('avg:', sum)
      return (sum / count);
  };
  var result = [], val;

  // calculate average for each subarray and add to result
  for (var i=0, len=array.length - count; i <= len; i++){
      val = avg(array.slice(i, i + count), qualifier);
      result.push(val);
  }

  return result;
}

  function getMin(ret, thisVal) {
    thisVal = thisVal || ret;
    return ret < thisVal ? ret : thisVal;
  }

  function getMax(ret, thisVal) {
    thisVal = thisVal || ret;
    return ret > thisVal ? ret : thisVal;
  }

  sensor_graph_obj = {
    _canvas : null,
    _source : null,
    _periods: null,
    _export: null,
    __timer : null,
    __type : type,
    _graph_data : {},
    __animate : 1000,
    __colors : {'min' : get_template_color('text-info',0.7),
                'max' : get_template_color('text-danger',0.7),
                'current' : get_template_color('text-success',0.8),

                'wattage' : get_template_color('text-success',0.7),
                'water_flow' : get_template_color('text-info',0.7),
              },

    get source() {
      return this._source;
    },

    set source(value) {
      this._source = value;
      if (this._export.length == 1) {
        this._export.attr('href', value.replace('/history/','/export/'));
      }

      if (this._periods.find('a').length == 0) {
        let self = this;

        jQuery.each(['day','week','month','year'],function(counter,period) {
          let period_action = jQuery('<a>').addClass('dropdown-item').attr({'href' : self.source +  period + '/', 'title':period}).text(period);
          if ('day' == period) {
            period_action.addClass('active');
          }

          period_action.off('click').on('click',function (event){
            event.preventDefault();
            self._periods.find('a.dropdown-item').removeClass('active');
            self.source  = this.href;
            jQuery(this).addClass('active')
          });

          self._periods.append(period_action);
        });
      }

      //Enable animation when source has changed (day/week/mont/year)
      this._graph.options.animation.duration = 1000;
      this._load_data();
    },


    _load_data: function() {
      if (!this._canvas.is(':visible')) {
        this.stop();
        return
      }

      let self = this;
      jQuery.get(this.source, function(data){
        data = data.data;
        if (data.length == 0) {
          let overlay = self._canvas.parents('.card-body').find('div.overlay');
          overlay.html('<h1>No data...</h1>');
          return false;
        }

        // Parse data and update graph type
        data = self._parse_data(data);

        let graph_data = {
          labels  : data.timestamp,
          datasets : [],
        }

        //let mode = (data.wattage !== undefined ? 'relay' : 'sensor')

        if (data.alarm_max) {
          graph_data.datasets.push({
            label: 'Alarm max',
            data: data.alarm_max,
            fill : false,
            pointRadius : false,
            borderColor: self.__colors['max'],
            backgroundColor: self.__colors['max']
          });
          self._graph.options.scales.yAxes[0].ticks.suggestedMax = Math.max(...data.alarm_max);
        }

        if (data.alarm_min) {
          graph_data.datasets.push({
            label: 'Alarm min',
            data: data.alarm_min,
            fill : false,
            pointRadius : false,
            borderColor: self.__colors['min'],
            backgroundColor: self.__colors['min']
          });
          self._graph.options.scales.yAxes[0].ticks.suggestedMin = Math.min(...data.alarm_min);
        }

        if (data.alarm_max && data.alarm_min) {
          let diff = self._graph.options.scales.yAxes[0].ticks.suggestedMax - self._graph.options.scales.yAxes[0].ticks.suggestedMin;
          self._graph.options.scales.yAxes[0].ticks.suggestedMax += diff * 0.10;
          if (self._graph.options.scales.yAxes[0].ticks.suggestedMin - (diff * 0.10) > 0) {
            self._graph.options.scales.yAxes[0].ticks.suggestedMin -= diff * 0.10;
          }
        }

        if (['wattage','magnetic','motion','ldr'].indexOf(self.__type) == -1) {
          graph_data.datasets.push({
            label: 'Current',
            data: data.value,
            fill : false,
            pointRadius : 1,

            borderColor : function(context) {
              if (!context.chart.chartArea) {
                // This case happens on initial chart load
                return null;
              }

              if (context.chart.data.datasets.length == 1) {
                return self.__colors['current'];
              }

              let index = context.dataIndex;
              let current = context.dataset.data[index] * 1;

              let alarm_max = context.chart.data.datasets[0].data[index] * 1;
              let alarm_min = context.chart.data.datasets[1].data[index] * 1;

              return (current >= alarm_max ? self.__colors['max'] : current <= alarm_min ? self.__colors['min'] : self.__colors['current']);
            },

            backgroundColor : function(context) {
              if (!context.chart.chartArea) {
                // This case happens on initial chart load
                return null;
              }

              if (context.chart.data.datasets.length == 1) {
                return self.__colors['current'];
              }
              let index = context.dataIndex;
              let current = context.dataset.data[index] * 1;

              let alarm_max = context.chart.data.datasets[0].data[index] * 1;
              let alarm_min = context.chart.data.datasets[1].data[index] * 1;

              return (current >= alarm_max ? self.__colors['max'] : current <= alarm_min ? self.__colors['min'] : self.__colors['current']);
            },

          });
        } else if ('wattage' == self.__type) {
          self._graph.options.scales.yAxes[1].display = true;
        }

        if (['magnetic','motion','ldr'].indexOf(self.__type) != -1) {
          graph_data.datasets.push({
            label: self.__type,
            data: data.value,
            fill : 'start',
            pointRadius : false,
            lineTension: 0,
            yAxisID: 'y-axis-1',
            borderColor: self.__colors['current'],
            backgroundColor: self.__colors['current']
          });
          self._graph.options.scales.yAxes[0].ticks.stepSize = 1;
        }

        if (data.wattage) {
          graph_data.datasets.push({
            label: 'Wattage',
            data: data.wattage,
            fill : 'start',
            pointRadius : false,
            lineTension: 0,
            yAxisID: 'y-axis-1',
            borderColor: self.__colors['wattage'],
            backgroundColor: self.__colors['wattage']
          });
          self._graph.options.scales.yAxes[0].ticks.suggestedMax = Math.max(...data.wattage) + 1;
        }

        if (data.flow) {
          graph_data.datasets.push({
            label: 'Water flow',
            indicator: sensor_type_indicator('water_flow'),
            data: data.flow,
            fill : 'start',
            pointRadius : false,
            lineTension: 0,
            yAxisID: 'y-axis-2',
            borderColor: self.__colors['water_flow'],
            backgroundColor: self.__colors['water_flow']
          });
          self._graph.options.scales.yAxes[1].ticks.suggestedMax = Math.max(...data.flow) + 1;
        }

        // Period ticks update
        let period_duration = (moment(data.timestamp[data.timestamp.length-1]) - moment(data.timestamp[0])) / 86340000; // in days

        if (period_duration <= 1) {
          self._graph.options.scales.xAxes[0].time.unit = 'minute';
        } else if (period_duration <= 7) {
          self._graph.options.scales.xAxes[0].time.unit = 'hour';
          self._graph.options.scales.xAxes[0].time.displayFormats.hour = 'D/M LT';
          self._graph.options.scales.xAxes[0].time.stepSize = 6;
        } else if (period_duration <= 31) {
          self._graph.options.scales.xAxes[0].time.unit = 'hour';
          self._graph.options.scales.xAxes[0].time.displayFormats.hour = 'D/M LT';
          self._graph.options.scales.xAxes[0].time.stepSize = 12;
        }

        //console.log(data,graph_data);
        self._graph.data = graph_data;

        self._graph.options.legend.display = graph_data.datasets.length >= 2;

        self._graph.update();
        // Set the duration to zero so it stops animating when new data is loaded every X minutes.
        self._graph.options.animation.duration = 0;
        self._canvas.parents('.card-body').find('div.overlay').remove();
      });
    },

    _parse_data: function(data) {
      this.__type = (data[0].wattage !== undefined ? 'wattage' : this.__type)

      let parsed_data = {};

      for (counter = 0; counter < data.length; counter++) {
        if (data[counter]['timestamp'] != undefined) {
          // Multiplay the timestamp value with 1000 to get javascript miliseconds values
          data[counter]['timestamp'] = data[counter]['timestamp'] * 1000;
        }
        if ('magnetic' == this.__type) {
          // reverse door graphs for now
          data[counter]['value'] = (data[counter]['value'] ? 0 : 1);
        }

        if (['wattage','magnetic','motion','ldr'].indexOf(this.__type) != -1  && counter > 0) {
          // Here we add an extra item. This is the previous item, but with the timestamp of the new/current item
          // This will make the graph nicely showing filled areas when the power is on
          prev_item = data[counter-1]
          prev_item.timestamp = data[counter]['timestamp']
          if (data[counter].value === undefined || prev_item.value != data[counter].value) {
            for (key in prev_item) {
              parsed_data[key].push(prev_item[key])
            }
          }
        }

        for (key in data[counter]) {
          if (parsed_data[key] === undefined) {
            parsed_data[key] = [];
          }
          parsed_data[key].push(data[counter][key])
        }
      }

      if (['wattage','magnetic','motion','ldr'].indexOf(this.__type) != -1) {
        // Add a duplicate record on the 'end' with the current time stamp. This will keep the graph updating at every refresh
        last_item = data[data.length-1]
        last_item.timestamp = moment().format('YYYY-MM-DD[T]HH:mm:ss.SSSSSS');
        for (key in last_item) {
          parsed_data[key].push(last_item[key])
        }
      }

      if (window.terrariumPI.graph_smooth_value > 0) {
//        console.log(parsed_data.value, movingAvg(parsed_data['value'],window.terrariumPI.graph_smooth_value, false));
//        parsed_data.value = movingAvg(parsed_data.value.reverse(),window.terrariumPI.graph_smooth_value);

        // try {
        //   graph_data[1].data = graph_data[1].data.splice(window.terrariumPI.graph_smooth_value);
        // } catch (e) {}
        // try {
        //   graph_data[2].data = graph_data[2].data.splice(window.terrariumPI.graph_smooth_value);
        // } catch (e) {}

      }


      let name = this._canvas.attr('id').replace('graph_','gauge_');
      if (window.terrariumPI.graph_show_min_max_gauge && window.terrariumPI.gauges[name]) {
        // set the min/max values in the guage
        window.terrariumPI.gauges[name]._gauge.options.staticLabels = {
          labels: [parsed_data.value.reduce(getMin), parsed_data.value.reduce(getMax)],
          font: '10px Helvetica Neue,sans-serif',
          color: '#73879C',
          fractionDigits: 3
        };
      }

      return parsed_data;
    },

    stop: function() {
      clearInterval(this.__timer);
      this._graph.destroy();
    },

    run: function() {
      let self = this;
      this.__timer = setInterval(function(){
        self._load_data();
      }, 1 * 60 * 1000)
    },

    draw: function() {
      let self = this;

      let options = {

        animation: {
          duration: this.__animate,
        },

        maintainAspectRatio : false,
        responsive : true,
        legend: {
            display: true,
            align: 'center',
            /*
            labels: {
                fontColor: 'rgb(255, 99, 132)'
            }
            */
        },

        tooltips: {
            callbacks: {
              label: function(tooltipItem, data) {

                  let label = data.datasets[tooltipItem.datasetIndex].label || '';

                  if (label) {
                      label += ': ';
                  }
                  switch (self.__type) {
                    case 'magnetic':
                      label += (tooltipItem.yLabel == 0 ? 'closed' : 'open');

                      break;
                    case 'ldr':
                      label += (tooltipItem.yLabel == 0 ? 'dark' : 'light');
                      break;

                    case 'motion':
                      label += (tooltipItem.yLabel == 0 ? 'still' : 'motion');

                      break;

                    default:
                      //return formatNumber(value) + ' ' + sensor_type_indicator(self.__type);
                      label += formatNumber(tooltipItem.yLabel) + ' ' + (data.datasets[tooltipItem.datasetIndex].indicator || sensor_type_indicator(self.__type));
                    break;
                  }


                  return label;
              }
            }
        },

        scales: {
          xAxes: [{
            type: 'time',
            time: {
              displayFormats: {
                second: 'LTS',
                minute: 'LT',
                hour: 'LT',
                day: 'll',
              },
              unit: 'minute',
              tooltipFormat: 'lll'
            },
            gridLines : {
              display : true,
            },
          }],
          yAxes: [{
            id: 'y-axis-1',
            ticks: {
              suggestedMin: 0,
              callback: function(value, index, values) {
                switch (self.__type) {
                  case 'magnetic':
                    return (value == 0 ? 'closed' : 'open');
                    break;
                  case 'ldr':
                    return (value == 0 ? 'dark' : 'light');
                    break;

                  case 'motion':
                    return (value == 0 ? 'still' : 'motion');
                    break;

                  default:
                    return formatNumber(value) + ' ' + sensor_type_indicator(self.__type);
                  break;
                }
              }
            },
            gridLines : {
              display : true,
            }
          },{
            id: 'y-axis-2',
            position: 'right',
            display: false,
            ticks: {
              min: 0,
              suggestedMin: 0,
              callback: function(value, index, values) {
                return formatNumber(value) + ' ' + sensor_type_indicator('water_flow');
              }
            },
            gridLines : {
              display : false,
            }
          }]
        }
      }

      this._graph = new Chart(this._canvas[0].getContext('2d'), {
        type: 'line',
        data: {},
        options: options
      });
    }
  }

  // Delete existing / old sensor.... else we get multiple times the same sensor and will load data multiple times
  if (window.terrariumPI.graphs[canvas]) {
    window.terrariumPI.graphs[canvas].stop();
    delete(window.terrariumPI.graphs[canvas]);
  }

  sensor_graph_obj._canvas = jQuery('#' + canvas + ':visible');
  if (sensor_graph_obj._canvas.length == 1) {
    sensor_graph_obj._periods = sensor_graph_obj._canvas.parents('.card').find('.btn-group:first div.dropdown-menu');
    sensor_graph_obj._export = sensor_graph_obj._canvas.parents('.card').find('a.export_link');
    //console.log(sensor_graph_obj._export);
    sensor_graph_obj.draw();
    sensor_graph_obj.source  = source;
    sensor_graph_obj.run()

    // Store global/cached version
    window.terrariumPI.graphs[canvas] = sensor_graph_obj;

    return window.terrariumPI.graphs[canvas];
  }
}






let realtime_sensor_data = {};

function updateWebcamLabel(marker) {

  if (marker.options.sensors.length > 0) {
    var message = [];
    $.each(marker.options.sensors,function(counter,value){
      if (message.length == 0) {
        message.push('<strong>' + realtime_sensor_data[value].name + '</strong>');
      }
      message.push(realtime_sensor_data[value].type.substr(0,4) + '. ' +  formatNumber(realtime_sensor_data[value].value) + '' ); // + realtime_sensor_data[value].indicator
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

  var marker = L.marker([x, y],marker_config).bindTooltip('<center><strong>Loading</strong></center>', {
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

function updateWebcamMarkers(layer) {
  let markers = [];
//  var all_markers = '';
  layer.eachLayer(function(datamarker) {
    let pos = datamarker.getLatLng();
//    var pos = datamarker.getLatLng();
    markers.push({
      'lat' : pos.lat,
      'long' : pos.lng,
      'sensors' : datamarker.options.sensors
    })
    //all_markers += pos.lat + ',' + pos.lng + ',' + datamarker.options.sensors.join(',') + ';';
  });
//  console.log('Final markers', markers, JSON.stringify(markers));
  $('#modal-webcam-setup').find('input[name="markers"]').val(JSON.stringify(markers));
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
//    console.log('New marker data', marker.options.sensors);
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

function load_webcam(data) {
  let max_zoom = Math.max(data.width, data.height);
  max_zoom = Math.pow(2,Math.ceil(Math.log2(max_zoom)));
  max_zoom = Math.log2(max_zoom/256)

  var webcam = L.map(jQuery('div#webcam_' + data.id + ' div.webcam_player' + (data.edit === true ? '_preview' : ''))[0],{
    id: 'map_' + data.id,
    fullscreenControl: true,
    last_update : jQuery('div#webcam_' + data.id + ' div.webcam_player' + (data.edit === true ? '_preview' : '')).parents('.card').find('.last_update'),
  }).on('load',function(event){
    //console.log('Webcam load',event)
    //this.options.
  }).setView([0, 0], 1);

  let realtime_data_layer = L.layerGroup([], {
    webcamid : data.id,
    refresh_timer: null
  }).on('remove',function(event){
    clearTimeout(this.options.refresh_timer);
  }).on('add',function(event) {
    this.options.refresh_timer = setInterval(function(){
      if (realtime_data_layer.getLayers().length > 0) {
        $.get('/api/sensors/',function(data) { // TODO: Fix this api sensors url
          realtime_sensor_data = {};
          $.each(data.data,function(counter,value){
            realtime_sensor_data[value.id + ''] = value;
          });
          realtime_data_layer.eachLayer(function(marker) {
            updateWebcamLabel(marker);
          });
        });
      }
      event.target._map.options.last_update.text(moment().format('LLL'));
    },30 * 1000);

    // $.get('/api/sensors/',function(data) {
    //   realtime_sensor_data = {};
    //   $.each(data.data,function(counter,value){
    //     realtime_sensor_data[value.id + ''] = value;
    //   });
    //   realtime_data_layer.eachLayer(function(marker) {
    //     updateWebcamLabel(marker);
    //   });
    // });

  });
  realtime_data_layer.addTo(webcam);

  if (data.markers.length > 0) {
    realtime_sensor_data = {};
    $.get('/api/sensors/',function(sensor_data) { // TODO: Fix this api sensors url
      $.each(sensor_data.data,function(counter,value){
        realtime_sensor_data[value.id + ''] = value;
      });
      $.each(data.markers,function(counter,value) {
//        var tmpdata = value.split(',');

        createWebcamLabel(realtime_data_layer,value.lat,value.long,value.sensors, data.edit === true);
      });
    });
  }

  if (data.is_live) {
    let hls_url = 'webcam/' + data.id + '/stream.m3u8';
    if (data.hardware.indexOf('remote') != -1) {
      hls_url = data.address;
    }

    L.videoOverlay(hls_url, L.latLngBounds([[ 150, -180], [ -150, 180]]), {
      id: 'overlay_' + data.id,
      interactive: false,
      autoplay: true,
      player: null,
      className: 'webcam_live_' + data.id
    }).on('remove',function(event){
      // Stop playback
      this.options.player[0].pause();
      // Set empty source to stop loading m3u8 playlists
      this.options.player[0].src = '';
      // Clear the Hls.js player
      this.options.hls.destroy();
      // Remove from DOM
      this.options.player.remove();
      // Clear the timeout timer
      clearTimeout(this.options.refresh_timer);
    }).on('add',function(event){
      let webcam_tiler_layer = this;
      this.options.refresh_timer = setInterval(function(){
        // Stop the player when the webcam is not visible anymore...
        if (jQuery(webcam_tiler_layer._image).is(':not(:visible)')) {
          webcam_tiler_layer.remove()
        }
      },10 * 1000);
      this.options.player = $('.webcam_live_' + data.id);
      this.options.player[0].muted = true;
      if (this.options.player[0].canPlayType('application/vnd.apple.mpegurl')) {
        this.options.player[0].src = hls_url;
        this.options.player[0].addEventListener('loadedmetadata', function() {
          webcam_tiler_layer.options.player[0].play();
        });
      } else if (Hls.isSupported()) {
        this.options.hls = new Hls({'debug':false});
        this.options.hls.loadSource(hls_url);
        this.options.hls.attachMedia(this.options.player[0]);
        this.options.hls.on(Hls.Events.MANIFEST_PARSED, function() {
          webcam_tiler_layer.options.player[0].play();
        });
      }
    }).addTo(webcam);

  } else {
    L.tileLayer('/webcam/{id}/tiles/tile_{z}_{x}_{y}.jpg?_{time}', {
      time: function() {
        return (new Date()).valueOf();
      },
      id: data.id,
      noWrap: true,
      continuousWorld: false,
      maxNativeZoom: max_zoom,
      maxZoom: max_zoom + 1,
      refresh_timer : null
    }).on('remove',function(event){
      clearTimeout(this.options.refresh_timer);
    }).on('add',function(event){
      var webcam_tiler_layer = this;
      this.options.refresh_timer = setInterval(function(){
        // Redraw the layer, so refresh the images
        if (jQuery(webcam_tiler_layer._container).is(':visible')) {
          webcam_tiler_layer.redraw();
        } else {
          // Webcam is not visible anymore, so clear the refresh timer
          webcam_tiler_layer.remove()
        }
      },30 * 1000);
    }).addTo(webcam);
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
        this.photo_link.title = 'Save RAW photo';
        this.photo_link.target = '_blank';
        this.photo_link.href = '/webcam/' + data.id + '/' + data.id + '_raw.jpg';
        L.DomUtil.create('i', 'fas fa-camera', this.photo_link);

        if ('disabled' !== this.options.archive) {
          this.archive_link = L.DomUtil.create('a', 'leaflet-control-archive-button leaflet-bar-part', container);
          this.archive_link.href = '#';
          this.archive_link.title = 'Archive';
          L.DomEvent.on(this.archive_link, 'click', this._start_archive, this);
          L.DomUtil.create('i', 'fas fa-archive', this.archive_link);
        }
      }

      if (data.markers.length > 0 || data.edit === true) {
        this.info_link = L.DomUtil.create('a', 'leaflet-control-info-button leaflet-bar-part', container);
        this.info_link.href = '#';
        this.info_link.title = 'Toggle information';
        L.DomEvent.on(this.info_link, 'click', this._toggle_realtime_info, map);
        L.DomUtil.create('i', 'fas fa-info', this.info_link);
      }

      if (data.edit === true) {
        this.add_marker_link = L.DomUtil.create('a', 'leaflet-control-addmarker-button leaflet-bar-part', container);
        this.add_marker_link.href = '#';
        this.add_marker_link.title = 'Add marker';
        L.DomEvent.on(this.add_marker_link, 'click', this._add_marker, realtime_data_layer);
        L.DomUtil.create('i', 'fas fa-map-marker', this.add_marker_link);
      }

      if (data.is_live === true) {
        this.toggle_audio = L.DomUtil.create('a', 'leaflet-control-audio-button leaflet-bar-part', container);
        this.toggle_audio.href = '#';
        this.toggle_audio.title = 'Toggle audio';
        L.DomEvent.on(this.toggle_audio, 'click', this._toggle_audio);
        L.DomUtil.create('i', 'fas fa-volume-up', this.toggle_audio);
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
      $(this).find('.fas').removeClass('fa-volume-up fa-volume-mute').addClass(video.muted ? 'fa-volume-up' : 'fa-volume-mute')
    }
  });
  webcam.addControl(new L.Control.ExtraWebcamControls());
  webcam.addControl(L.Control.loading({separate: true}));
}


function webcamArchive(webcamid) {

  let now = new Date();
  let max_days_back = 50;
  let no_data_counter = 0;
  let fancybox = null;

  function getImages(date) {

    $.getJSON('api/webcams/' + webcamid + '/archive/'+ date.getFullYear() + '/' + (date.getMonth() < 9 ? '0' : '') + (date.getMonth() + 1) + '/' + (date.getDate() < 10 ? '0' : '') + date.getDate() + '/', function(data) {
//      var photos = [];
      let date_match = /archive_(\d+)\.jpg$/g;

      no_data_counter += (data.archive_images.length > 0 ? 0 : 1);
      max_days_back--;

      if (no_data_counter > 10 || max_days_back < 0) {
        return false;
      }

      $.each(data.archive_images, function(index,value) {
        value.match(date_match);
        let date_photo = date_match.exec(value);
        if (date_photo != null && date_photo.length == 2) {
          date_photo = moment(date_photo[1]* 1000).format('LLL');
        } else {
          date_photo = 'Unknown date';
        }

        if (fancybox == null) {
          fancybox = $.fancybox.open(
            [{src : value,opts: { caption: 'Webcam' + ' ' + data.name + ': ' + date_photo}}],
            {loop : false,
             buttons : [
               'slideShow',
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
            fancybox.addContent({src : value, opts: { caption: 'Webcam' + ' ' + data.name + ': ' + date_photo}});
          }
        }
      });
      // recursive
      if ($.fancybox.getInstance() || data.archive_images.length == 0) {
        setTimeout(function(){
          getImages(new Date(date.getTime() - (24 * 60 * 60 * 1000)));
          }, ((data.archive_images.length + 1) * 10));
      } else {
        fancybox == null;
      }
    });
  }
  getImages(now);
}

function load_page(url) {
  const title_regex = /<title>(.*)<\/title>/gms;

  if (url === undefined) {
    // Trigger the reload function
    url = window.terrariumPI.page;
  }

  if (!(typeof url === 'string' || url instanceof String)) {
    url.preventDefault();
    url = this.href;
  }

  jQuery.get(url,function(data){
    let document_title = title_regex.exec(data);
    if (document_title.length == 2) {
      document_title = document_title[1].trim();
    }
    document.title = document_title;

    let page = jQuery(data);
    jQuery('div.content-wrapper').html(page.find('div.content-wrapper').html());
    active_menu_trail(url);

    jQuery('[required="required"]').each(function(counter,item){
      jQuery(item).parents('.form-group').addClass('required');
    });

    jQuery('select.select2').select2();
    bootstrap_custom_fileuploads();

    window.terrariumPI.page = url;
  });

  return false;
}

function fix_menu_links() {
  jQuery('nav ul.nav li.nav-item a.nav-link:not([href="#"]):not([data-toggle])').each(function(counter,href){
    jQuery(href).off('click',load_page).on('click',load_page);
  });

  jQuery('nav ul.navbar-nav li.nav-item a.dropdown-footer:not([href="#"]):not([data-toggle])').each(function(counter,href){
    jQuery(href).off('click',load_page).on('click',load_page);
  });

  active_menu_trail();
}

function active_menu_trail(url) {
  url = url || location.href;
  url = url.replace(location.protocol + '//' + location.host,'');
  let menu_item = jQuery('nav ul.nav li.nav-item a.nav-link[href="' +  url+'"]');

  if (menu_item.length == 0) {
    return
  }

  let menu =  jQuery('nav ul.nav');
  menu.find('a').removeClass('active');
  menu_item.addClass('active').parent().addClass('menu-open');
  menu_item.parents('li.nav-item.has-treeview').addClass('menu-open').find('a:first').addClass('active')
}

function animate_socketio_messages() {
  let animation_badge = jQuery('footer .badge.badge-success');

  animation_badge.animate({
    opacity: 1,
  }, 50, function() {
    // Animation complete.
    animation_badge.animate({
      opacity: 0.1
    }, 150);
  });
}

function online_status(online) {
  let indicator = jQuery('#online_status i');
  let old_status = (indicator.hasClass('text-success') ? true : (indicator.hasClass('text-danger') ? false : ''));

  if (online) {
    clearTimeout(window.terrariumPI.online_counter);
    indicator.removeClass('text-danger text-secondary text-success').addClass('text-success');

    window.terrariumPI.online_counter = setTimeout(function(){
      online_status(false);
    }, 60 * 1000);

  } else {
    indicator.removeClass('text-danger text-secondary text-success').addClass('text-danger');
  }

  if (old_status !== online) {
    if (online) {
      toastr["success"]("We are connected", "Online");
    } else {
      toastr["error"]("We are disconnected", "Offline");
    }
  }
}

function uptime_format(duration) {
  let uptime = moment.duration(duration, 'seconds');

  let uptime_text = '';


  if (uptime._data.years > 0 || uptime_text.length > 0) {
    uptime_text += uptime._data.years + ' year' + (uptime._data.years != 1 ? 's' : '') + ', '
  }

  if (uptime._data.months > 0 || uptime_text.length > 0) {
    uptime_text += uptime._data.months + ' month' + (uptime._data.months != 1 ? 's' : '') + ', '
  }

  if (uptime._data.days > 0 || uptime_text.length > 0) {
    uptime_text += uptime._data.days + ' day' + (uptime._data.days != 1 ? 's' : '') + ', '
  }

  if (uptime._data.hours > 0 || uptime_text.length > 0) {
    uptime_text += uptime._data.hours + ' hour' + (uptime._data.hours != 1 ? 's' : '') + ', '
  }

  if (uptime._data.minutes > 0 || uptime_text.length > 0) {
    uptime_text += uptime._data.minutes + ' minute' + (uptime._data.minutes != 1 ? 's' : '') + ', '
  }

  if (uptime._data.seconds > 0 || uptime_text.length > 0) {
    uptime_text += uptime._data.seconds + ' second' + (uptime._data.seconds != 1 ? 's' : '') + ''
  }

  return uptime_text
}

function formToJSON( form ) {
  let output = {};
  jQuery.each(form.find('input,select,textarea'),function(counter,item) {
    console.log(item);
    if (!item.disabled && '' != item.name) {
      let key   = item.name;
      let value = item.value;

      if (item.type == 'select-multiple') {
        value = jQuery(item).val();
      } else if (item.type == 'checkbox') {
        value = (item.checked ? true : false);
      } else if (['true','false'].indexOf(value) != -1) {
        value = 'true' == value;
      } else if ('number' == item.type) {
        value *= 1.0;
      }

      // Check if key already exist
      if (Object.prototype.hasOwnProperty.call( output, key)) {
        let current = output[ key ];
        if ( !Array.isArray( current ) ) {
          // If it's not an array, convert it to an array.
          current = output[ key ] = [ current ];
        }
        current.push( value ); // Add the new value to the array.
      } else {
        output[ key ] = value;
      }
    }
  });
  return output;
}


function calendar_indicator() {

  jQuery.get('/api/calendar/', function(data) {
    let calender_bar = jQuery('nav.main-header li.calendar');

    calender_bar.find('span.navbar-badge').text(data.length);
    calender_bar.find('span.dropdown-header span').text(data.length);
    calender_bar.find('div.events').html('');

    jQuery.each(data, function(counter, event){
      let event_item = jQuery('<a>').attr('href','#').addClass('dropdown-item text-nowrap');
      let duration = moment.duration(moment(event.start).diff(moment())).humanize(true);

      event_item.append(jQuery('<i>').addClass('fas fa-calendar-alt mr-2'));
      event_item.append(event.title);
      event_item.append(jQuery('<span>').addClass('float-right text-muted text-sm').text(duration));

      calender_bar.find('div.events').append(event_item);
    });
  })
}


function button_state(button_data) {
//  console.log('button data:',button_data)
  let button = jQuery('i#button_' + button_data.id);
  let classes = 'fas';

  switch(button_data.hardware) {
    case 'magnetic':
      classes += ' ' + (button_data.value > 0 ? 'fa-lock' : 'fa-lock-open');
      break;

    case 'ldr':
      classes += ' fa-lightbulb';
      break;

    case 'motion':
      classes += ' fa-walking';
      break;
  }

  classes += ' ' + (button_data.value > 0 ? 'text-success' : 'text-secondary')
  button.removeClass().addClass(classes);
}

/* General functions - Websockets  */
function websocket_init(reconnect) {
  websocket_connect();

  window.terrariumPI.websocket.onopen = function(evt) {
    websocket_message({
      'type': 'client_init',
      'reconnect': reconnect
    });
  };

  window.terrariumPI.websocket.onmessage = function(evt) {
    if (window.terrariumPI.reboot) {
      // When a reboot is triggered, the first connection message is also a trigger that the reboot has finished. So reload the page!
      location.reload();
      return;
    }
    online_status(true);

    let message = JSON.parse(evt.data);
    if ('logfile_update' != message.type) {
      animate_socketio_messages();
    }
    //console.log('Websocket received message:', message);
    switch (message.type) {
      case 'sensortypes':
        light_sensors_list = []
        sensor_menu_list = [];

        jQuery.each(message.data,function(counter,data){
          let sensor_type = data.id;
          let sensor_name = data.value;
          let submenu = false;
          let link = '/sensors_' + sensor_type + '.html';
          let tree = null;
          let skip = false;

          if (sensor_type == 'uva' || sensor_type == 'uvb' || sensor_type == 'uvi' || sensor_type == 'light') {

            light_sensors_list.push({
              icon: template_sensor_type_icon(sensor_type),
              title: sensor_name.capitalize(),
              link: link,
              tree: null,
              submenu: null
            })

            if (light_sensors_list.length == 1) {
              submenu = true;
              sensor_type = 'light';
              sensor_name = 'light';
              link = '#';
              tree = 'has-treeview'

            } else {
              skip = true;
            }
          }

          if (!skip) {
            sensor_menu_list.push({
              icon: template_sensor_type_icon(sensor_type),
              title: sensor_name.capitalize(),
              link: link,
              tree: tree,
              submenu: (submenu ? 'fa-angle-left' : null)
            });
          }
        });

        if (sensor_menu_list.length + light_sensors_list.length + 1 != jQuery('#available_sensor_types li.nav-item').length) {
          sensor_menu_list.sort((a, b) => a.title.localeCompare(b.title));

          //console.log('sensortypes Update menu....',jQuery('#available_sensor_types li.nav-item').length,sensor_menu_list.length,light_sensors_list.length);

          jQuery('#available_sensor_types li.nav-item:not(:last)').remove();
          jQuery('#available_sensor_types').loadTemplate(jQuery('#sensor_type_menu'),sensor_menu_list,{prepend: true});

          if (light_sensors_list.length > 0) {
            light_sensors_list.sort((a, b) => a.title.localeCompare(b.title));
            let light_submenu = jQuery('#available_sensor_types li i.' + template_sensor_type_icon('light')).parentsUntil('li').parent();
            light_submenu.append(jQuery('<ul>').addClass('nav nav-treeview').attr('id','available_light_sensor_types'));
            jQuery('#available_light_sensor_types').loadTemplate(jQuery('#sensor_type_menu'),light_sensors_list,{prepend: true});
          }

          fix_menu_links();
        }
      break;

      case 'button':
        button_state(message.data);
        break;

      case 'relay':
        jQuery('button#relay_' + message.data.id + ' i').toggleClass('text-success',message.data.value == 100);
        break;


      case 'gauge_update':
        if (window.terrariumPI.gauges['gauge_' + message.data.id]) {
          window.terrariumPI.gauges['gauge_' + message.data.id].current = message.data.value;
        }
      break;

      case 'logfile_update':
        if (message.data.indexOf('WARNING') != -1 || message.data.indexOf('ERROR') != -1) {
          let badge = jQuery('footer.main-footer .badge-warning');
          if (message.data.indexOf('WARNING') != -1) {
            if (window.terrariumPI.logged_in) {
              toastr.warning(message.data, 'WARNING');
            }
          } else {
            if (window.terrariumPI.logged_in) {
              toastr.error(message.data, 'ERROR');
            }
            badge = jQuery('footer.main-footer .badge-danger');
          }
          let current_val = badge.text() * 1;
          badge.removeClass('opacity-' + (current_val+1)).text(current_val+1).addClass('opacity-' + (current_val+2));
        }

        let logging = jQuery('textarea#logdata');
        if (logging.length == 1) {
          logging.val(message.data + '\n' + logging.val()).trigger('change');
        }
      break;

      case 'systemstats':
        clearTimeout(window.terrariumPI.update_timer);
        jQuery('.info-box:first i.fas').removeClass('fa-hourglass-half fa-hourglass-start animate').addClass('fa-hourglass-end animate');
        window.terrariumPI.update_timer = setTimeout(function(){
          jQuery('.info-box:first i.fas').removeClass('fa-hourglass-end fa-hourglass-half fa-hourglass-start animate').addClass('fa-hourglass-half');

          window.terrariumPI.update_timer = setTimeout(function(){
            jQuery('.info-box:first i.fas').removeClass('fa-hourglass-end fa-hourglass-half fa-hourglass-start animate').addClass('fa-hourglass-end');
          }, 14 * 1000);
        }, 15 * 1000);

        jQuery('.info-box:first .info-box-number').text(uptime_format(message.data.uptime));

        jQuery('.info-box:first div.progress').each(function(counter,progressbar){
          jQuery(progressbar).attr({'title' : 'Load ' + message.data.load.percentage[counter] + '%'}).find('.progress-bar').css('height', message.data.load.percentage[counter] + '%');
        });
        jQuery('#is_day_indicator span').text(moment().format('LLLL'));
        jQuery('#is_day_indicator i').removeClass('fa-moon fa-sun').addClass(( message.data.is_day ? 'fa-sun' : 'fa-moon'));

        christmas();
        fireworks_menu();
      break;

      case 'power_usage_water_flow':
        for (part in message.data) {
          let usage = jQuery('#' + part + '_usage');
          usage.find('span.info-box-number').text( formatNumber(message.data[part].current) + ' / ' + formatNumber(message.data[part].max) );
          usage.find('div.progress-bar').css({'width': ((message.data[part].current/message.data[part].max) * 100) + '%'});

          let total = jQuery('#total_' + part);
          total.find('span.info-box-number').text( formatNumber(message.data[part].total) );
          total.find('span.description-percentage span.text-success').text( formatCurrency(message.data[part].costs) );
          total.find('span.description-percentage span:not(.text-success)').text( moment.duration(message.data[part].duration * 1000).humanize() );
        }
        break;

        case 'enclosure':
          jQuery.each(message.data.areas, function(counter, area){
            if (area.state.powered !== undefined) {
              jQuery('#area_relay_state_' + area.id).removeClass('badge-success badge-secondary').addClass(( area.state.powered ? 'badge-success' : 'badge-secondary'));
            }
            // if (area.state.sensor !== undefined) {
            //   jQuery('#area_current_' + area.id).text(formatNumber(area.state.sensor.current,0,2));
            //   jQuery('#area_alarm_min_' + area.id).text(formatNumber(area.state.sensor.alarm_min,0,2));
            //   jQuery('#area_alarm_max_' + area.id).text(formatNumber(area.state.sensor.alarm_max,0,2));
            // }
            if (area.state.sensors !== undefined) {
              jQuery('#area_current_' + area.id).text(formatNumber(area.state.sensors.current,0,2));
              jQuery('#area_alarm_min_' + area.id).text(formatNumber(area.state.sensors.alarm_min,0,2));
              jQuery('#area_alarm_max_' + area.id).text(formatNumber(area.state.sensors.alarm_max,0,2));
              jQuery('#area_warning_' + area.id).toggle(area.state.sensors.alarm);
            }
            jQuery.each(['day','night','low','high'],function(counter,type){
              if (area.state[type] !== undefined) {
                jQuery('#area_' + type + '_start_' + area.id).text(moment(area.state[type].begin * 1000).format('LTS'));
                jQuery('#area_' + type + '_end_' + area.id).text(moment(area.state[type].end * 1000).format('LTS'));
                jQuery('#area_' + type + '_duration_' + area.id).text(moment.duration(area.state[type].duration * 1000).humanize());
              }
            });
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
    }
  };
  window.terrariumPI.websocket.onclose = function(evt) {
    //update_online_indicator(false);
    clearInterval(window.terrariumPI.websocket_timer);
    window.terrariumPI.websocket_timer = setInterval(function() {
      websocket_init(true);
    }, 10 * 1000);
  };
}

function websocket_connect() {
  try {
    clearInterval(window.terrariumPI.websocket_timer);
    window.terrariumPI.websocket = null;
    url = 'ws' + (location.protocol == 'https:' ? 's' : '') + '://' + location.host + window.terrariumPI.connection
    window.terrariumPI.websocket = new WebSocket(url);
  } catch (error) {
    console.log('websocket_connect', error);
  }
}

function websocket_message(message) {
  try {
    window.terrariumPI.websocket.send(JSON.stringify(message));
  } catch (error) {
    console.log('websocket_message', error, message);
  }
}
/* General functions - End websockets  */


function christmas() {
  if (moment(moment().year() + '-12-25').week() == moment().week()) {
    $('img.christmashat').show().parent().addClass('mt-3');
  } else {
    $('img.christmashat').hide().parent().removeClass('mt-3');
  }
}

function fireworks_menu() {
  if ( '12-31' == moment().format('MM-DD') || '01-01' == moment().format('MM-DD') ) {
    if (jQuery('canvas#fireworks').length == 0) {
      jQuery('a.brand-link').css('backgroundColor','transparent');
      jQuery('aside.main-sidebar').prepend('<canvas id="fireworks" style="position:absolute; z-index:-1; height:100%; width:100%"></canvas>');
      jQuery('body').append('<script src="/static/assets/js/fireworks.js" type="text/javascript"></script>');
    }
  } else {
    jQuery('canvas#fireworks').remove();
  }
}

function bootstrap_custom_fileuploads(){
  jQuery('div.custom-file input[type="file"]').off('change').on('change',function(){
    let filename = '';
    if (this.value !== undefined && this.value !== null && '' !== this.value) {
      filename = this.value.split('\\').pop();
    }
    jQuery(this).siblings('label').text(filename);
  });
}

jQuery(function () {

  christmas();
  fireworks_menu();
  bootstrap_custom_fileuploads();

  // Initialize Select2 Elements
  // Hide search boxes when less then 10 items
  jQuery.fn.select2.defaults.set('minimumResultsForSearch', 10);
  jQuery.fn.select2.defaults.set('templateResult', formatState);
  jQuery.fn.select2.defaults.set('templateSelection', formatState);
  jQuery('select.select2').select2();

  // Fix the menu links so they will load through jQuery AJAX
  fix_menu_links();

  jQuery.addTemplateFormatter('prefixer',
    function(value, prefix) {
      prefix = prefix || '';
      return prefix + value;
  });

  jQuery.addTemplateFormatter('html',
    function(value, option) {
      return value.replace(/\n/g,'<br />');
  });

  jQuery.addTemplateFormatter('datetimeformatter',
    function(value, format) {
      value = value || moment().format('X');
      return moment(value * 1000).format(format);
  });

  jQuery.addTemplateFormatter('durationformatter',
    function(value, option) {
      return moment.duration(value * 1000).humanize();
  });

  jQuery.addTemplateFormatter('unitformatter',
    function(value, option) {
      return window.terrariumPI.units[value];
  });

  jQuery.addTemplateFormatter('numberformatter',
    function(value, frac) {
      return formatNumber(value,0,frac);
  });

  calendar_indicator();
  setInterval(function(){
    calendar_indicator();
  }, 60 * 1000);

  websocket_init(false);

  // window.terrariumPI.websocket = io({
  //   transports: ['websocket']
  // });
//  window.terrariumPI.websocket.on('event',function(){console.log('event',this)});

    // socket.on('connect', function() {
    //     socket.emit('message', { data: 'I\'m connected!'});
    // });

  //   window.terrariumPI.websocket.on('message', function(message) {
  //     online_status(true);
  //     animate_socketio_messages();

  //     switch(message.action) {
  //       case 'sensortypes':

  //         light_sensors_list = []
  //         sensor_menu_list = [];

  //         jQuery.each(message.data,function(counter,data){
  //           let submenu = false;
  //           let link = '/sensors_' + data[0] + '.html';
  //           let tree = null;
  //           let skip = false;

  //           if (data[0] == 'uva' || data[0] == 'uvb' || data[0] == 'uvi' || data[0] == 'light') {

  //             light_sensors_list.push({
  //               icon: template_sensor_type_icon(data[0]),
  //               title: data[1].capitalize(),
  //               link: '/sensors_' + data[0] + '.html',
  //               tree: null,
  //               submenu: null
  //             })

  //             if (light_sensors_list.length == 1) {
  //               submenu = true;
  //               data[0] = 'light';
  //               data[1] = 'light';
  //               link = '#';
  //               tree = 'has-treeview'

  //             } else {
  //               skip = true;
  //             }
  //           }

  //           if (!skip) {
  //             sensor_menu_list.push({
  //               icon: template_sensor_type_icon(data[0]),
  //               title: data[1].capitalize(),
  //               link: link,
  //               tree: tree,
  //               submenu: (submenu ? 'fa-angle-left' : null)
  //             });
  //           }
  //         });

  //         if (sensor_menu_list.length + light_sensors_list.length + 1 != jQuery('#available_sensor_types li.nav-item').length) {
  //           sensor_menu_list.sort((a, b) => a.title.localeCompare(b.title));

  //           console.log('sensortypes Update menu....',jQuery('#available_sensor_types li.nav-item').length,sensor_menu_list.length,light_sensors_list.length);

  //           jQuery('#available_sensor_types li.nav-item:not(:last)').remove();
  //           jQuery('#available_sensor_types').loadTemplate(jQuery('#sensor_type_menu'),sensor_menu_list,{prepend: true});

  //           if (light_sensors_list.length > 0) {
  //             light_sensors_list.sort((a, b) => a.title.localeCompare(b.title));
  //             let light_submenu = jQuery('#available_sensor_types li i.' + template_sensor_type_icon('light')).parentsUntil('li').parent();
  //             light_submenu.append(jQuery('<ul>').addClass('nav nav-treeview').attr('id','available_light_sensor_types'));
  //             jQuery('#available_light_sensor_types').loadTemplate(jQuery('#sensor_type_menu'),light_sensors_list,{prepend: true});
  //           }

  //           fix_menu_links();
  //         }
  //       break;
  //
  //       case 'relay_update':
  //         console.log(message.data);
  //         if (message.data.dimmer) {
  //           jQuery('#relay_' + message.data.id).val(message.data.value).trigger('change');
  //         } else {
  //           jQuery('button#relay_' + message.data.id + ' i').removeClass('text-success').addClass(message.data.value !== null && message.data.value > 0 ? 'text-success' : '');
  //         }
  //         jQuery('#relay_' + message.data.id + ' .card-header .badge-danger').text(message.data.value === null ? 'error' : '');
  //       break;

  //       case 'button_update':
  //         //console.log(message.data);
  //         button_state(message.data);
  //       break;





  //       case 'power_usage':
  //       case 'water_usage':
  //         let usage = jQuery('#' + ('power_usage' == message.action ? 'power' : 'water') + '_usage');
  //         usage.find('span.info-box-number').text( formatNumber(message.data.used) + ' / ' + formatNumber(message.data.total) );
  //         usage.find('div.progress-bar').css({'width': ((message.data.used/message.data.total) * 100) + '%'});

  //         //formatCurrency
  //       break;
  //
  //     }
  // });
});
