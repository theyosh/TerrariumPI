var sensorList = {};
var sensorTimerTimeOut = 30;

function loadSensors(runonce) {
  runonce = runonce || false
  jQuery.ajax({
    url: '/sensor/list',
    dataType: 'json'
  }).done(function(result){
    var counter = 0;
    jQuery.each(result.value,function(){
      if (sensorList[this.id] == undefined) {
        // Create the sensor
        switch (this.type) {
          case 'humidity':
            sensorList[this.id] = new HumiditySensor( this.id,
                                                      this.name,
                                                      {min:this.minlimit, max: this.maxlimit},
                                                      {min: this.min, max: this.max, current: this.current},
                                                      this.alarm,
                                                      this.alarm_enabled,
                                                      this.logging_enabled,
                                                      this.indicator);
          break;
          case 'temperature':
            sensorList[this.id] = new TemperatureSensor(this.id,
                                                        this.name,
                                                        {min:this.minlimit, max: this.maxlimit},
                                                        {min: this.min, max: this.max, current: this.current},
                                                        this.alarm,
                                                        this.alarm_enabled,
                                                        this.logging_enabled,
                                                        this.indicator);
          break;
        }
      } else {
        // Update the sensor
        sensorList[this.id].update(this);
      }
    });
  });
  if (!runonce) setTimeout(function(){loadSensors()}, sensorTimerTimeOut * 1000);
}

function Sensor(id,name,limits,values,type,alarm,alarm_enabled,logging_enabled,indicator) {
  this._id = id;
  this._name = name || '{unknown}';
  this._type = type || 'temperature';

  limits = limits || {};
  values = values || {};

  this._limits = {min : limits['min'] || 0, max : limits['max'] || 0};
  this._values = {current : values.current || 0, min : values.min || 0, max : values.max || 0};

  this._alarm           = alarm || false;
  this._alarm_enabled   = alarm_enabled || false;
  this._logging_enabled = logging_enabled || false;
  this._indicator       = indicator || '°C';
  this._lastupdate      = moment().format("dddd D MMMM YYYY, HH:mm:ss");

  this._canvas            = null;
  this._canvas_indicator  = null;
  this._canvas_name       = null;
  this._canvas_animation  = null;
  this._canvas_value      = null;

  this._canvas_alarm      = null;
  this._canvas_graph      = null;
  this._canvas_options    = null;
  this._canvas_updater    = null;


  this._createcanvas = function() {
    this._canvas            = jQuery('<div>').attr('id','sensor_' + this._type + '_' + this._id).addClass(this._type + ' pointer');
    this._canvas_indicator  = jQuery('<span>').addClass('indicator').text(this._indicator);
    this._canvas_name       = jQuery('<span>').addClass('name').text(this._name);
    this._canvas_animation  = jQuery('<div>');
    this._canvas_value      = jQuery('<span>').addClass('value').text(this._values.current);
    this._canvas_alarm      = jQuery('<span>').addClass('icon alarm');
    this._canvas_graph      = jQuery('<span>').addClass('icon graph pointer');
    this._canvas_options    = jQuery('<span>').addClass('icon options');
    this._canvas_updater    = jQuery('<span>').addClass('updater');

    this._lastupdate        = moment().format("dddd D MMMM YYYY, HH:mm:ss");

    this._canvas_options.bind('click',{object: this}, function (event){
      var fields = [];
      fields.push({'name':'id','type':'text','value':event.data.object.id(),'label':'ID','help':'Enter the md5 hash of the sensor address','readonly':true});
      fields.push({'name':'name','type':'text','value':event.data.object.name(),'label':'Name','help':'Enter a name of this sensor'});
      fields.push({'name':'limit_min','type':'number','value':event.data.object.limitMin(),'label':'Minimum value','help':'Enter a number between -100 and 100'});
      fields.push({'name':'limit_max','type':'number','value':event.data.object.limitMax(),'label':'Maximum value','help':'Enter a number between -100 and 100'});
      if (event.data.object.type() == 'temperature') {
        fields.push({'name':'indicator','type':'dropdown','values':new Array({'name':'°C','value':'°C'},{'name':'°F','value':'°F'}),'label':'Indicator','help':'Indicator'});
      } else{
        fields.push({'name':'indicator','type':'text','value':event.data.object.indicator(),'label':'Indicator','help':'Enter the indicator in degrees or farenheit'});
      }
      fields.push({'name':'alarm_enabled','type':'switch','value':event.data.object.alarm_enabled(),'label':'Alarm enabled','help':'Enabled alarm notifications'});
      fields.push({'name':'logging_enabled','type':'switch','value':event.data.object.logging_enabled(),'label':'Logging enabled','help':'Enabled data logging'});
      showEditForm(event.data.object.type() + ' sensor ' + event.data.object.name(),fields,'/sensor/' + event.data.object.id() + '/set','loadSensors(true)');
    });

    this._canvas_graph.bind('click',{object:this},function (event){
        showGraph((event.data.object.id().indexOf('weather') != -1 ? '' : 'sensor_') + event.data.object.id(), event.data.object.name(),event.data.object.type());
    });

    this._canvas.jqxTooltip({ trigger : 'click',
                              content: '<b>Loading...</b>',
                              showArrow: true,
                              showDelay: 5000,
                              position: 'bottom',
                              name: 'sensorInfo'
                            }).bind('opening', {object:this}, function (event) {
                              var content = jQuery('<div>').addClass('tooltipContent');
                              if (event.data.object.alarm()) content.addClass('alarm');
                              content.append(event.data.object._canvas_graph);
                              if (loggedin) content.append(event.data.object._canvas_options);
                              content.append(event.data.object._getToolTipTitle('html'));
                              jQuery(this).jqxTooltip({content:content})
                            });
  }

  this._draw = function() {
    jQuery('.sensors').append(
      this._canvas.append(this._canvas_animation)
                  .append(this._canvas_name)
                  .append(this._canvas_value)
                  .append(this._canvas_indicator)
                  .append(this._canvas_alarm)
                  .append(this._canvas_updater)
    );
  }

  this._animate = function () {
    // Toggle alarm on or off
    this._canvas_alarm.removeClass('on off').addClass((this.alarm() === true ? 'on' : 'off'));
    // Update the indicator
    this._canvas_indicator.text(this.indicator());
    // Set the current value
    this._canvas_value.text(Math.round(this.val()*100)/100);
    // Update the name
    this._canvas_name.text(this.name());
    // Update tooltip text
    this._canvas.attr({'title':this._getToolTipTitle()});
  }

  this._getToolTipTitle = function(format) {
    format = format || 'txt';
    value = this._type.charAt(0).toUpperCase() + this._type.slice(1) + ' sensor ' + this.name() + "\n"
              + 'current: ' + this.val() + this.indicator() + (this.alarm() === true ? ' (Alarm!)' : '') + "\n"
              + 'min: ' + this.valueMin() + this.indicator() + "\n"
              + 'max: ' + this.valueMax() + this.indicator() + "\n"
              + 'range: ' + this.limitMin() + ' - ' + this.limitMax() + this.indicator() + "\n"
              + 'Last update: ' + this._lastupdate;

    if (format == 'html') {
      var contents = value.split("\n");
      value = '';
      for (var i = 0; i < contents.length; i++) {
        if (i == 0) {
          contents[i] = '<strong>' + contents[i] + '</strong>';
        }
        value += contents[i] + '<br />';
      }
    }
    return value;
  }

  this.id = function() {
    return this._id;
  }

  this.type = function() {
    return this._type;
  }

  this.name = function(value) {
    if (value == undefined) return this._name
    if (value != '') this._name = value;
  }

  this.setCurrent = function(data) {
    data.current = parseFloat(data.current);
    data.min = parseFloat(data.min);
    data.max = parseFloat(data.max);

    if (data.current != 'NaN') this._values.current = data.current;
    if (data.min != 'NaN') this._values.min = data.min;
    if (data.max != 'NaN') this._values.max = data.max;
  }

  this.setLimits = function(data) {
    data.min = parseFloat(data.min);
    data.max = parseFloat(data.max);

    if (data.min != 'NaN') this._limits.min = data.min;
    if (data.max != 'NaN') this._limits.max = data.max;
  }

  this.val = function(value) {
    if (value == undefined) return this._values.current
    value = parseFloat(value);
    if (value != 'NaN') this._values.current = value;
  }

  this.alarm = function(value) {
    if (value == undefined) return this._alarm === true;
    this._alarm = value == 1 || value == true || value == 'true' || value === true;
  }

  this.logging_enabled = function(value) {
    if (value == undefined) return this._logging_enabled === true;
    this._logging_enabled = value == 1 || value == true || value == 'true' || value === true;
  }

  this.alarm_enabled = function(value) {
    if (value == undefined) return this._alarm_enabled === true;
    this._alarm_enabled = value == 1 || value == true || value == 'true' || value === true;
  }

  this.limitMin = function(value) {
    if (value == undefined) return this._limits.min
    value = parseFloat(value);
    if (value != 'NaN') this._limits.min = value;
  }

  this.limitMax = function(value) {
    if (value == undefined) return this._limits.max
    value = parseFloat(value);
    if (value != 'NaN') this._limits.max = value;
  }

  this.valueMin = function(value) {
    if (value == undefined) return this._values.min
    value = parseFloat(value);
    if (value != 'NaN') this._values.min = value;
  }

  this.valueMax = function(value) {
    if (value == undefined) return this._values.max
    value = parseFloat(value);
    if (value != 'NaN') this._values.max = value;
  }

  this.indicator = function(value) {
    if (value == undefined) return this._indicator
    if (value != '') this._indicator = value;
  }

  this.update = function(data) {
    updater(this._canvas.attr('id'));
    this.name(data.name);
    this.setCurrent({current: data.current, min: data.min, max: data.max});
    this.setLimits({min: data.minlimit, max: data.maxlimit});
    this.alarm(data.alarm);
    this.alarm_enabled(data.alarm_enabled);
    this.logging_enabled(data.logging_enabled);
    this.indicator(data.indicator);
    this._lastupdate = moment().format("dddd D MMMM YYYY, HH:mm:ss");
    this.animate();
  }

  this.start = function() {
    this.draw();
    this.animate();
  };
  this._createcanvas();
}

function HumiditySensor(id,name,limits,values,alarm,alarm_enabled,logging_enabled,indicator) {
  if (jQuery('#sensor_humidity_' + id).length != 0) return;
  Sensor.call(this,id,name,limits,values,'humidity',alarm,alarm_enabled,logging_enabled,indicator);

  this.draw = function() {
    this._draw();
  };

  this.animate = function() {
    // Basic animations
    this._animate();

    // Start custom animations:
    this._canvas_value.append(this.indicator());
    this._canvas_animation.animate({'opacity':Math.round(this.val())/100},2500);
  };
  this.start();
}

function TemperatureSensor(id,name,limits,values,alarm,alarm_enabled,logging_enabled,indicator) {
  if (jQuery('#sensor_temperature_' + id).length != 0) return;
  Sensor.call(this,id,name,limits,values,'temperature',alarm,alarm_enabled,logging_enabled,indicator);

  // Extra canvases
  this._canvas_animation.addClass('window') .append(jQuery('<span>').addClass('liquid'))
                                            .append(jQuery('<span>').addClass('range'))
                                            .append(jQuery('<span>').addClass('minmax'));
  this.draw = function() {
    this._draw();
  };

  this.animate = function() {
    // Basic animations
    this._animate();

    // Start custom animations:
    // Toggle warm or cold thermometer
    this._canvas.removeClass('cold warm').addClass((this.val() > 0 ? 'warm' : 'cold'));
    // first set the range and min/max
    jQuery(this._canvas_animation).find('span.range').css({'top':(95 - this.limitMax()) +'%','height':Math.abs(this.limitMax()-this.limitMin()) + '%'});
    jQuery(this._canvas_animation).find('span.minmax').css({'top':(95 - this.valueMax()) +'%','height':Math.abs(this.valueMax()-this.valueMin()) + '%'});
    // Animate the temperature
    jQuery(this._canvas_animation).find('span.liquid').animate({'top':(95 - this.val()) +'%'},2500);
  }
  this.start();
}
