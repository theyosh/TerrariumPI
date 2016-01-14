var environmentTimerTimeOut = 30; // In seconds
var environment_counter = null;

function loadEnvironment() {
  loadEnvironmentDashboard();
  updateEnvironment();
}

function loadEnvironmentDashboard(){
  var table = jQuery('<table>');
  // Dashboard title row
  table.append(jQuery('<tr>') .append(jQuery('<td>').append(jQuery('<span>').addClass('icon authentication edit loggedout').attr('title','Login to make changes')))
                              .append(jQuery('<td>').append(jQuery('<h1>').text('Environment')))
                              .append(jQuery('<td>').append(jQuery('<span>').addClass('icon counter').attr({'id':'env_counter'})))
  );

  // Last update row
  table.append(jQuery('<tr>').append(jQuery('<td>').attr({'colspan':3,'id':'env_update'}).text('updating...')));

  // Door status
  table.append(jQuery('<tr>').append(jQuery('<td>').attr({'colspan':3,'id':'door_update'})
        .append(jQuery('<span>').addClass('icon enabled'))
	.append(jQuery('<span>').attr({'id':'door_update_text'}).text('updating...'))

  ));

  // Lights title
  table.append(jQuery('<tr>').append(jQuery('<td>').attr('colspan',3).append(jQuery('<h2>').text('Lights'))));
  // Lights control
  table.append(jQuery('<tr>') .attr({'id':'env_lights'})
                              .append(jQuery('<td>').text('enabled').append(jQuery('<span>').addClass('icon inactive enabled'))
                                                    .append('trigger').append(jQuery('<span>').addClass('icon inactive trigger').attr('title','Trigger inactive')))
                              .append(jQuery('<td>').append(jQuery('<div>') .addClass('animation inactive')
                                                                            .append(jQuery('<div>').addClass('light_bulb'))
                                                                            .append(jQuery('<div>').addClass('light_bulb on')))
                                                    .append(jQuery('<div>').addClass('period')))
                              .append(jQuery('<td>').text('on').append(jQuery('<span>').addClass('icon inactive running'))
                                                    .append('graph').append(jQuery('<span>').addClass('icon inactive graph pointer').attr('title','Show graph'))
                                                    .append('options').append(jQuery('<span>').addClass('icon inactive options').attr('title','Options (login to make changes)')))
  );

  // Heater title
  table.append(jQuery('<tr>').append(jQuery('<td>').attr('colspan',3).append(jQuery('<h2>').text('Heater'))));
  // Heater control
  table.append(jQuery('<tr>') .attr({'id':'env_heater'})
                              .append(jQuery('<td>').text('enabled').append(jQuery('<span>').addClass('icon inactive enabled'))
                                                    .append('trigger').append(jQuery('<span>').addClass('icon inactive trigger').attr('title','Trigger inactive'))
                                                    .append('alarm').append(jQuery('<span>').addClass('icon inactive alarm').css({'display':'none'}).attr('title','Alarm!')))
                              .append(jQuery('<td>').append(jQuery('<div>') .addClass('animation inactive')
                                                                            .append(jQuery('<span>').addClass('value'))
                                                                            .append(jQuery('<div>').addClass('flame1'))
                                                                            .append(jQuery('<div>').addClass('flame2'))
                                                                            .append(jQuery('<div>').addClass('flame3'))
                                                                            )
                                                    .append(jQuery('<div>').addClass('period')))
                              .append(jQuery('<td>').text('on').append(jQuery('<span>').addClass('icon inactive running'))
                                                    .append('graph').append(jQuery('<span>').addClass('icon inactive graph pointer').attr('title','Show graph'))
                                                    .append('options').append(jQuery('<span>').addClass('icon inactive options').attr('title','Options (login to make changes)')))
  );

  // Humidity title
  table.append(jQuery('<tr>').append(jQuery('<td>').attr('colspan',3).append(jQuery('<h2>').text('Humidity'))));
  // Humidity control
  table.append(jQuery('<tr>') .attr({'id':'env_humidity'})
                              .append(jQuery('<td>').text('enabled').append(jQuery('<span>').addClass('icon inactive enabled'))
                                                    .append('trigger').append(jQuery('<span>').addClass('icon inactive trigger').attr('title','Trigger inactive'))
                                                    .append('alarm')
                                                    .append(jQuery('<span>').addClass('icon inactive alarm').css({'display':'none'}).attr('title','Alarm!')))
                              .append(jQuery('<td>').append(jQuery('<div>').addClass('animation inactive'))
                                                    .append(jQuery('<div>').addClass('period')))
                              .append(jQuery('<td>').text('on') .append(jQuery('<span>').addClass('icon inactive running'))
                                                    .append('graph').append(jQuery('<span>').addClass('icon inactive graph pointer').attr('title','Show graph'))
                                                    .append('options').append(jQuery('<span>').addClass('icon inactive options').attr('title','Options (login to make changes)')))
  );

  jQuery('#environment').append(table);
  
  environment_counter = new JustGage({
      id: 'env_counter',
      value: environmentTimerTimeOut,
      min: 0,
      max: environmentTimerTimeOut,
      donut: true,
      gaugeWidthScale: 0.3,
      hideInnerShadow: true,
      counter: true,
      valueMinFontSize: 12,
      startAnimationTime: 250,
      refreshAnimationTime: 250,
  });

  jQuery('#environment #env_humidity .animation').jqxGauge({
        ranges: [ { startValue: 0, endValue: 33, style: { fill: 'red', stroke: 'darkred' }, startDistance: '5%', endDistance: '5%', endWidth: 5, startWidth: 5 },
                  { startValue: 33, endValue: 66, style: { fill: 'green', stroke: 'darkgreen' }, startDistance: '5%', endDistance: '5%', endWidth: 5, startWidth: 5 },
                  { startValue: 66, endValue: 100, style: { fill: 'orange', stroke: 'darkorange' }, startDistance: '5%', endDistance: '5%', endWidth: 5, startWidth: 5 },
                ],
        cap: { size: '10%' },
        value: 50,
        style: { stroke: '#ffffff', 'stroke-width': '2px', fill: '#ffffff' },
        animationDuration: 3000,
        labels: { visible: true, position: 'outside' },
        ticksMinor: { visible : false},
        ticksMajor: { visible : false },
        width: '100%',
        height: '100%',
        max: 100,
        pointer: {length: '95%', width: '5%'},
        caption: {value : '50%'}
      });

  jQuery('#environment span.icon.authentication.edit').bind('click',function() {
    showLoginForm();
  });

  jQuery('#environment span.icon.graph').each(function() {
      jQuery(this).bind('click',function(event){
        var id = jQuery(this).parents('tr').attr('id').split('_')[1];
        var type = id;
        var title = '';

        switch(id){
          case 'lights':
            title = 'Lights environment';
          break;
          case 'heater':
            title = 'Heater environment';
          break;
          case 'humidity':
            title = 'Humidity environment';
          break;
        }
        showGraph('environment_' + id,title,type);
    });
  });

  // Start the animations
  animateLights();
  animateHeater();
}

function updateEnvironment(runonce) {
  runonce = runonce || false
  jQuery.ajax({
    url: '/environment/all/status',
    dataType: 'json'
  }).done(function(result){
    loadEnvironmentLights(result.value.lights.value);
    loadEnvironmentHeater(result.value.heater.value);
    loadEnvironmentHumidity(result.value.humidity.value);
    jQuery('#environment #door_update').removeClass('open closed').addClass(result.value.door.value);
    jQuery('#environment #door_update_text').text('Door is ' + result.value.door.value);
    jQuery('#environment #env_update').html('Last update:<br />' + moment().format("dddd D MMMM YYYY, HH:mm:ss"));
  });
  if (!runonce) {
    setTimeout(function() {updateEnvironment()}, environmentTimerTimeOut * 1000);
    setTimeout(function() {environmentCounter()}, 1000);
  }
}

var timer = null;
function environmentCounter() {
  var currentvalue = environment_counter.config.value;
  currentvalue--;
  if ( currentvalue > 0) {
    environment_counter.refresh(currentvalue);
    clearTimeout(timer);
    timer = setTimeout(function() {
      environmentCounter();
    }, 1000);
  } else {
    environment_counter.refresh(environmentTimerTimeOut);
  }
}

function animateLights(){
  if (!jQuery('#env_lights div.animation').hasClass('inactive')) {
    jQuery('#env_lights div.animation .light_bulb.on').fadeTo(3000,0.4,function(){
      jQuery(this).fadeTo(3000,1);
    });
  }
  setTimeout(function() {animateLights()}, 7000);
}

function animateHeater(){
  if (!jQuery('#env_heater div.animation').hasClass('inactive')) {

    var frame = jQuery('#env_heater div.animation').attr('frame');
    if (frame == undefined) {
      // Initialize
      frame = 1;
      jQuery('#env_heater div.animation div.flame3').hide();
    }
    if (frame % 2 == 0) {
      jQuery('#env_heater div.animation .flame3').fadeOut(3000);
      jQuery('#env_heater div.animation .flame2').fadeIn(3000);
      frame = 0;
    } else {
      jQuery('#env_heater div.animation .flame2').fadeOut(3000);
      jQuery('#env_heater div.animation .flame3').fadeIn(3000);
    }
    jQuery('#env_heater div.animation').attr('frame',++frame);
  }
  setTimeout(function() {animateHeater()}, 4000);
}

function loadEnvironmentLights(data) {
  jQuery('#environment #env_lights .inactive:not(.options)').removeClass('inactive');
  jQuery('#environment #env_lights .trigger').toggleClass('inactive',data.active != true);
  jQuery('#environment #env_lights .trigger').attr('title','Trigger is ' + (data.active == true ? 'active' : 'disabled'));

  jQuery('#environment #env_lights .enabled').toggleClass('on',data.enabled == true);
  jQuery('#environment #env_lights .enabled').toggleClass('off',data.enabled != true);
  jQuery('#environment #env_lights .enabled').attr('title','Lights control is ' + (data.enabled ? 'enabled' : 'disabled'));
  jQuery('#environment #env_lights .running').toggleClass('on',data.current_state == 'on');
  jQuery('#environment #env_lights .running').toggleClass('off',data.current_state == 'off');
  jQuery('#environment #env_lights .running').attr('title','Lights are currently ' + data.current_state);
  jQuery('#environment #env_lights .period').text('on: ' + moment.unix(data.current_on).format('HH:mm:ss') + ' - off: ' + moment.unix(data.current_off).format('HH:mm:ss'));
}

function showEnvironmentLightsSettingsForm() {
  jQuery.ajax({
    url: '/environment/lights/settings',
    dataType: 'json'
  }).done(function(result){

    var fields = [];
    fields.push({'name':'id','type':'hidden','value':'lights','readonly':true});
    fields.push({'name':'enabed','type':'switch','value':result.value.enabled,'label':'Lights enabled','help':'Enabled alarm notifications'});

    fields.push({'name':'modus','type':'radio','value':'Weather','label':'Light modus','checked':result.value.trigger_on == 'sunrise' || result.value.trigger_off == 'sunset' });
    fields.push({'name':'modus','type':'radio','value':'Timer','checked':!(result.value.trigger_on == 'sunrise' || result.value.trigger_off == 'sunset')});

    fields.push({'name':'on','type':'text','value':result.value.trigger_on,'label':'Lights on','help':'Enter the time when the lights should be on'});
    fields.push({'name':'off','type':'text','value':result.value.trigger_off,'label':'Lights off','help':'Enter the time when the lights should be off'});

    fields.push({'name':'switch','type':'list','value':'','label':'Select the power switches','help':'Select the right power switches'});

    //fields.push({'name':'sensor','type':'list','value':'','label':'Select the sensors','help':'Select the right sensors'});

    fields.push({'name':'maxhours','type':'number','value':Math.round(result.value.max_duration/3600),'label':'Maximum hours of light','help':'Enter a number between -100 and 100'});
    fields.push({'name':'minhours','type':'number','value':Math.round(result.value.min_duration/3600),'label':'Minimum hours of light','help':'Enter a number between -100 and 100'});
    fields.push({'name':'shifthours','type':'number','value':Math.round(result.value.time_shift/3600),'label':'Shift light hours','help':'Enter a number between -100 and 100'});

    showEditForm('lights environment system',fields,'/environment/lights/settings/save','updateEnvironment(true)');
    // prepare the data
    var source =
    {
        datatype: "json",
        datafields: [
            { name: 'id' },
            { name: 'name' }
        ],
        id: 'id',
        url: '/switch/list',
        loadComplete:
      function(data) {
        console.log(data);
      }
    };
    var dataAdapter = new $.jqx.dataAdapter(source);
    // Create a jqxListBox
    jQuery("#list_switch").jqxListBox({ source: dataAdapter, displayMember: "name", valueMember: "id", width: 250, height: 75, multiple: true});
    jQuery("#list_switch").on('bindingComplete', function (event) {
      var items = jQuery("#list_switch").jqxListBox('getItems');

      var list = [];
      for (var i = 0; i < items.length; i++) {
        list.push(items[i].value);
      }
      for (var i = 0; i < result.value.switches.length; i++) {
        var pos = false;
        console.log(result.value.switches[i].id);
        if ( (pos = jQuery.inArray( result.value.switches[i].id, list )) != -1) {
          jQuery("#list_switch").jqxListBox('selectIndex', pos );
        }
      }
    });

    jQuery("#list_switch").on('change', function () {
      var items = jQuery('#list_switch').jqxListBox('getSelectedItems');
      var selection = '';
      for (var i = 0; i < items.length; i++) {
        selection += items[i].value + (i < items.length - 1 ? "," : "");
      }
      jQuery('#switch').val(selection);
    });

    jQuery('#radio_modus').on('selected', function (event) {
      var value = jQuery(this).children('div:eq(' + event.args.index + ')').attr('id').toLowerCase();
      jQuery('#modus').val(value);

      if (value == 'weather') {
        jQuery('input#on').attr('readonly','readonly').val('sunrise');
        jQuery('input#off').attr('readonly','readonly').val('sunset');
      } else {
        jQuery('input#on').removeAttr('readonly').val(result.value.trigger_on);
        jQuery('input#off').removeAttr('readonly').val(result.value.trigger_off);
      }
    });

    // Initialize the current modus
    var modus = (result.value.trigger_on == 'sunrise' || result.value.trigger_off == 'sunset' ? 'Weather' : 'Timer');
    jQuery('#radio_modus').jqxButtonGroup('setSelection', $('div#' + modus).index());
  });
}

function showEnvironmentHeaterSettingsForm() {
  jQuery.ajax({
    url: '/environment/heater/settings',
    dataType: 'json'
  }).done(function(result){

    var fields = [];

    fields.push({'name':'id',           'type':'hidden',  'value':'heater',                 'readonly':true});
    fields.push({'name':'enabed',       'type':'switch',  'value':result.value.enabled,     'label':'Heater enabled',       'help':'Enabled alarm notifications'});

    var modus = 'unknown';

    fields.push({'name':'modus',        'type':'radio',   'value':'Weather',                'label':'Heater modus', 'checked': modus == 'weather' });
    fields.push({'name':'modus',        'type':'radio',   'value':'Timer',                                          'checked': modus == 'timer' });
    fields.push({'name':'modus',        'type':'radio',   'value':'Sensor',                                         'checked': modus == 'sensor' });
    fields.push({'name':'on',           'type':'text',    'value':result.value.trigger_on,  'label':'Heater on',    'help':'Enter the time when the lights should be on'});
    fields.push({'name':'off',          'type':'text',    'value':result.value.trigger_off, 'label':'Heater off',   'help':'Enter the time when the lights should be off'});
    fields.push({'name':'switch',       'type':'list',    'value':'',                        'label':'Select the power switches', 'help':'Select the right power switches'});
    fields.push({'name':'sensor',       'type':'list',    'value':'',                        'label':'Select the temperature sensors', 'help':'Select the right sensors'});
    fields.push({'name':'dayactive',    'type':'switch',  'value':result.value.day_active,    'label':'Heater enabled during the day',       'help':'Enabled alarm notifications'});

    showEditForm('heater environment system',fields,'/environment/heater/settings/save','loadEnvironmentHeater()');

    // prepare the data
    var source =
    {
        datatype: "json",
        datafields: [
            { name: 'id' },
            { name: 'name' }
        ],
        id: 'id',
        url: '/switch/list',
        loadComplete:
      function(data) {
        console.log(data);
      }
    };
    var dataAdapter = new $.jqx.dataAdapter(source);
    // Create a jqxListBox
    jQuery("#list_switch").jqxListBox({ source: dataAdapter, displayMember: "name", valueMember: "id", width: 250, height: 75, multiple: true});
    jQuery("#list_switch").on('bindingComplete', function (event) {
      var items = jQuery("#list_switch").jqxListBox('getItems');

      var list = [];
      for (var i = 0; i < items.length; i++) {
        list.push(items[i].value);
      }
      for (var i = 0; i < result.value.switches.length; i++) {
        var pos = false;
        console.log(result.value.switches[i].id);
        if ( (pos = jQuery.inArray( result.value.switches[i].id, list )) != -1) {
          jQuery("#list_switch").jqxListBox('selectIndex', pos );
        }
      }
    });

    // prepare the data
    var source =
    {
        datatype: "json",
        datafields: [
            { name: 'id' },
            { name: 'name' }
        ],
        id: 'id',
        url: '/sensor/list/temperature',
        loadComplete:
      function(data) {
        console.log(data);
      }
    };
    var dataAdapter = new $.jqx.dataAdapter(source);
    // Create a jqxListBox
    jQuery("#list_sensor").jqxListBox({ source: dataAdapter, displayMember: "name", valueMember: "id", width: 250, height: 75, multiple: true});
    jQuery("#list_sensor").on('bindingComplete', function (event) {
      var items = jQuery("#list_sensor").jqxListBox('getItems');

      var list = [];
      for (var i = 0; i < items.length; i++) {
        list.push(items[i].value);
      }
      for (var i = 0; i < result.value.sensors.length; i++) {
        var pos = false;
        console.log(result.value.sensors[i].id);
        if ( (pos = jQuery.inArray( result.value.sensors[i].id, list )) != -1) {
          jQuery("#list_sensor").jqxListBox('selectIndex', pos );
        }
      }
    });

    jQuery("#list_switch").on('change', function () {
      var items = jQuery('#list_switch').jqxListBox('getSelectedItems');
      var selection = '';
      for (var i = 0; i < items.length; i++) {
        selection += items[i].value + (i < items.length - 1 ? "," : "");
      }
      jQuery('#switch').val(selection);
    });

    jQuery("#list_sensor").on('change', function () {
      var items = jQuery('#list_sensor').jqxListBox('getSelectedItems');
      var selection = '';
      for (var i = 0; i < items.length; i++) {
        selection += items[i].value + (i < items.length - 1 ? "," : "");
      }
      jQuery('#sensor').val(selection);
    });

    jQuery('#radio_modus').on('selected', function (event) {
      var value = jQuery(this).children('div:eq(' + event.args.index + ')').attr('id').toLowerCase();
      jQuery('#modus').val(value);

      if (value == 'weather') {
        jQuery('input#on').attr('readonly','readonly').val('sunset');
        jQuery('input#off').attr('readonly','readonly').val('sunrise');
      } else if (value == 'timer') {
        jQuery('input#on').removeAttr('readonly').val(result.value.trigger_on);
        jQuery('input#off').removeAttr('readonly').val(result.value.trigger_off);
      } else if (value == 'sensor') {
        jQuery('input#on').attr('readonly','readonly').val('sensor');
        jQuery('input#off').attr('readonly','readonly').val('sensor');
      }
    });

    // Initialize the current modus
    var modus = 'Weather';
    switch (result.value.modus) {
      case 'timer':
        modus = 'Timer';
      break;
      case 'sensor':
        modus = 'Sensor';
      break;
    }
    jQuery('#radio_modus').jqxButtonGroup('setSelection', $('div#' + modus).index());
  });
}

function loadEnvironmentHeater(data) {
  jQuery('#environment #env_heater .inactive:not(.options)').removeClass('inactive');
  jQuery('#environment #env_heater .trigger').toggleClass('inactive',data.active != true);
  jQuery('#environment #env_heater .trigger').attr('title','Trigger is ' + (data.active == true ? 'active' : 'disabled'));
  jQuery('#environment #env_heater .enabled').toggleClass('on',data.enabled == true);
  jQuery('#environment #env_heater .enabled').toggleClass('off',data.enabled != true);
  jQuery('#environment #env_heater .enabled').attr('title','Heater control is ' + (data.enabled ? 'enabled' : 'disabled'));
  jQuery('#environment #env_heater .running').toggleClass('on',data.current_state == 'on');
  jQuery('#environment #env_heater .running').toggleClass('off',data.current_state == 'off');
  jQuery('#environment #env_heater .running').attr('title','Heater is currently ' + data.current_state);

  jQuery('#environment #env_heater span.value').text(Math.round(data.avg_val * 100) / 100 + ' C');

  var alarmOn = data.alarm == 1 || data.alarm == true || data.alarm == 'true';
  jQuery('#environment #env_heater .alarm').toggleClass('on',alarmOn === true);
  jQuery('#environment #env_heater .alarm').toggleClass('off',alarmOn !== true);

  jQuery('#environment #env_heater .period').text('on: ' + moment.unix(data.current_on).format('HH:mm:ss') + ' - off: ' + moment.unix(data.current_off).format('HH:mm:ss'));
}

function showEnvironmentHumiditySettingsForm() {
  jQuery.ajax({
    url: '/environment/humidity/settings',
    dataType: 'json'
  }).done(function(result){

    var fields = [];
    fields.push({'name':'id','type':'hidden','value':'humidity','readonly':true});
    fields.push({'name':'enabed',       'type':'switch',  'value':result.value.enabled,       'label':'Humidity enabled','help':'Enabled alarm notifications'});
    fields.push({'name':'switch',       'type':'list',    'value':'',                         'label':'Select the power switches','help':'Select the right power switches'});
    fields.push({'name':'sensor',       'type':'list',    'value':'',                         'label':'Select the humidity sensors','help':'Select the right sensors'});
    fields.push({'name':'timeout',      'type':'text',    'value':result.value.switch_timeout,'label':'Humidity wait timeout (seconds)','help':'Enter the time when the lights should be on'});
    fields.push({'name':'duration',     'type':'number',  'value':result.value.duration,      'label':'Humidity spray duration (seconds)','help':'Enter a number between -100 and 100'});
    fields.push({'name':'night_enabled','type':'switch',  'value':result.value.night_active,  'label':'Humidity enabled when the lights are off','help':'Enabled alarm notifications'});

    showEditForm('humidity environment system',fields,'/environment/humidity/settings/save','updateEnvironment()');

    // prepare the data
    var source =
    {
        datatype: "json",
        datafields: [
            { name: 'id' },
            { name: 'name' }
        ],
        id: 'id',
        url: '/switch/list',
        loadComplete:
      function(data) {
        console.log(data);
      }
    };
    var dataAdapter = new $.jqx.dataAdapter(source);
    // Create a jqxListBox
    jQuery("#list_switch").jqxListBox({ source: dataAdapter, displayMember: "name", valueMember: "id", width: 250, height: 75, multiple: true});
    jQuery("#list_switch").on('bindingComplete', function (event) {
      var items = jQuery("#list_switch").jqxListBox('getItems');

      var list = [];
      for (var i = 0; i < items.length; i++) {
        list.push(items[i].value);
      }
      for (var i = 0; i < result.value.switches.length; i++) {
        var pos = false;
        console.log(result.value.switches[i].id);
        if ( (pos = jQuery.inArray( result.value.switches[i].id, list )) != -1) {
          jQuery("#list_switch").jqxListBox('selectIndex', pos );
        }
      }
    });

    // prepare the data
    var source =
    {
        datatype: "json",
        datafields: [
            { name: 'id' },
            { name: 'name' }
        ],
        id: 'id',
        url: '/sensor/list/humidity',
        loadComplete:
      function(data) {
        console.log(data);
      }
    };
    var dataAdapter = new $.jqx.dataAdapter(source);
    // Create a jqxListBox
    jQuery("#list_sensor").jqxListBox({ source: dataAdapter, displayMember: "name", valueMember: "id", width: 250, height: 75, multiple: true});
    jQuery("#list_sensor").on('bindingComplete', function (event) {
      var items = jQuery("#list_sensor").jqxListBox('getItems');

      var list = [];
      for (var i = 0; i < items.length; i++) {
        list.push(items[i].value);
      }
      for (var i = 0; i < result.value.sensors.length; i++) {
        var pos = false;
        console.log(result.value.sensors[i].id);
        if ( (pos = jQuery.inArray( result.value.sensors[i].id, list )) != -1) {
          jQuery("#list_sensor").jqxListBox('selectIndex', pos );
        }
      }
    });


    jQuery("#list_switch").on('change', function () {
      var items = jQuery('#list_switch').jqxListBox('getSelectedItems');
      var selection = '';
      for (var i = 0; i < items.length; i++) {
        selection += items[i].value + (i < items.length - 1 ? "," : "");
      }
      jQuery('#switch').val(selection);
    });

    jQuery("#list_sensor").on('change', function () {
      var items = jQuery('#list_sensor').jqxListBox('getSelectedItems');
      var selection = '';
      for (var i = 0; i < items.length; i++) {
        selection += items[i].value + (i < items.length - 1 ? "," : "");
      }
      jQuery('#sensor').val(selection);
    });
  });
}

function loadEnvironmentHumidity(data) {
  var ranges = jQuery('#environment #env_humidity .animation').jqxGauge('ranges');
  ranges[0].endValue    = data.avg_min;
  ranges[1].startValue  = ranges[0].endValue;
  ranges[1].endValue    = data.avg_max;
  ranges[2].startValue  = ranges[1].endValue;

  jQuery('#environment #env_humidity .animation').jqxGauge({ ranges: ranges, caption: { value: Math.round(data.avg_val * 100) / 100 + '%'} });
  jQuery('#environment #env_humidity .animation').val(data.avg_val);

  jQuery('#environment #env_humidity .inactive:not(.options)').removeClass('inactive');
  jQuery('#environment #env_humidity .trigger').toggleClass('inactive',data.active != true);
  jQuery('#environment #env_humidity .trigger').attr('title','Trigger is ' + (data.active == true ? 'active' : 'disabled'));
  jQuery('#environment #env_humidity .enabled').toggleClass('on',data.enabled == true);
  jQuery('#environment #env_humidity .enabled').toggleClass('off',data.enabled != true);
  jQuery('#environment #env_humidity .enabled').attr('title','Humidity control is ' + (data.enabled ? 'enabled' : 'disabled'));
  jQuery('#environment #env_humidity .running').toggleClass('on',data.current_state == 'on');
  jQuery('#environment #env_humidity .running').toggleClass('off',data.current_state == 'off');
  jQuery('#environment #env_humidity .running').toggleClass('inactive',data.current_state == 'inactive');

  var alarmOn = data.alarm == 1 || data.alarm == true || data.alarm == 'true';
  jQuery('#environment #env_humidity .alarm').toggleClass('on',alarmOn === true);
  jQuery('#environment #env_humidity .alarm').toggleClass('off',alarmOn !== true);
  jQuery('#environment #env_humidity .running').attr('title','Humidity is currently ' + data.current_state);
  jQuery('#environment #env_humidity .period').text('range: ' + ranges[1].startValue + '% - ' + ranges[1].endValue  + '%');
}
