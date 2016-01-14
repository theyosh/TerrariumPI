var switchList = {};
var switchTimerTimeOut = 30;

function loadSwitches(runonce) {
  runonce = runonce || false
  jQuery.ajax({
    url: '/switch/list',
    dataType: 'json'
  }).done(function(result){
    var counter = 0;
    jQuery.each(result.value,function(){
      if (switchList[this.id] == undefined) {
        // Create the switch
        switchList[this.id] = new Switch( this.id,
                                          this.name,
                                          this.nr,
                                          this.current,
                                          'power',
                                          this.wattage,
                                          this.waterflow);
      } else {
        // Update the switch
        switchList[this.id].update(this);
      }
    });
  });
  if (!runonce) setTimeout(function(){loadSwitches()}, switchTimerTimeOut * 1000);
}

function Switch(id, name, nr, state, type, wattage, waterflow) {
  this._id = id;
  this._name = name || '{unknown}';
  this._type = type || 'power';
  this._state = state == 1 || state == true || state == 'true' || state === true || false;
  this._nr = nr || -1;
  this._wattage = wattage || 0;
  this._waterflow = waterflow || 0;

  this._lastupdate = moment().format("dddd D MMMM YYYY, HH:mm:ss");

  this._canvas            = null;
  this._canvas_name       = null;
  this._canvas_lightbulb  = null;
  this._canvas_switch     = null;

  this._canvas_graph      = null;
  this._canvas_options    = null;
  this._canvas_updater    = null;

  this._createcanvas = function() {
    this._canvas            = jQuery('<div>').attr({'id': 'switch_' + this._type + '_' + this._id}).addClass(this._type).addClass(this.state() ? 'on' : 'off');
    this._canvas_name       = jQuery('<span>').addClass('name').html('<svg><defs><linearGradient id=\'textgradient\' x1=\'0%\' x2=\'100%\' y1=\'0%\' y2=\'0%\'><stop stop-color = \'#000\' offset = \'0%\'/><stop stop-color = \'#fff\' offset = \'100%\'/></linearGradient></defs><text x=\'50%\' y=\'0.8em\' text-anchor=\'middle\' letter-spacing=\'-1\' font-size=\'10\' fill=\'url(#textgradient)\' >' + this._name + '</text></svg>');
    this._canvas_lightbulb  = jQuery('<div>').addClass('light_bulb pointer').append(jQuery('<span>').text(wattage + 'W'));
    this._canvas_switch     = jQuery('<div>').addClass('switch');
    this._canvas_options    = jQuery('<span>').addClass('icon options edit').attr('title','Options (logged in)');
    this._canvas_graph      = jQuery('<span>').addClass('icon graph edit').attr('title','Show history');
    this._canvas_updater    = jQuery('<span>').addClass('updater');

    this._canvas_options.bind('click',{object: this}, function (event){
      var fields = [];
      fields.push({'name':'id','type':'text','value':event.data.object.id(),'label':'ID','help':'Enter the md5 hash of the switch address','readonly':true});
      fields.push({'name':'type','type':'text','value':event.data.object.type(),'label':'Type','help':'Enter switch type','readonly':true});
      fields.push({'name':'name','type':'text','value':event.data.object.name(),'label':'Name','help':'Enter a name of this switch'});
      fields.push({'name':'logging_enabled','type':'switch','value':true,'label':'Logging enabled','help':'Enabled data logging'});
      fields.push({'name':'wattage','type':'number','value':event.data.object.wattage(),'label':'Power usage in Watt','help':'Enter the amount of power this switch consumes when switched on'})
      fields.push({'name':'waterflow','type':'number','value':event.data.object.waterflow(),'label':'Waterflow','help':'Enter the amount of water that is used  when switched on'})
      showEditForm(event.data.object.type() + ' switch ' + event.data.object.name(),fields,'/switch/' + event.data.object.id() + '/set','loadSwitches(true)');
    });

    this._canvas_graph.bind('click',{object:this},function (event){
        showGraph('switch_' + event.data.object.id(), event.data.object.name(),event.data.object.type());
    });

    this._canvas_switch.bind('click',{object:this},function (event) {
      if (loggedin) event.data.object.toggle();
    });

    this._canvas_lightbulb.jqxTooltip({ trigger : 'click',
                            content: '<b>Loading...</b>',
                            showArrow: true,
                            showDelay: 5000,
                            position: 'bottom',
                            name: 'sensorInfo'
                          }).bind('opening', {object:this}, function (event) {
                            var content = jQuery('<div>').addClass('tooltipContent');
                            content.append(event.data.object._canvas_graph);
                            if (loggedin) content.append(event.data.object._canvas_options);
                            content.append(event.data.object._getToolTipTitle('html'));
                            jQuery(this).jqxTooltip({content:content})
                          });
  }

  this._draw = function() {
    jQuery('.switches').append(
      this._canvas.append(this._canvas_lightbulb)
                  .append(this._canvas_switch.append(this._canvas_name))
                  .append(this._canvas_updater)
    );
  }

  this._animate = function() {
    this._canvas.removeClass('on off').addClass(this.state() === true ? 'on' : 'off');
    this._canvas_name.html('<svg><defs><linearGradient id="textgradient" x1="0%" x2="100%" y1="0%" y2="0%"><stop stop-color = "#000" offset = "0%"/><stop stop-color = "#fff" offset = "100%"/></linearGradient></defs><text x="50%" y="0.8em" text-anchor="middle" letter-spacing="-1" font-size="10" fill="url(#textgradient)" >' + this._name + '</text></svg>');
    this._canvas.attr({'title':this._getToolTipTitle()});
    jQuery(this._canvas_lightbulb).find('span').text(this.wattage() + 'W');
  }

  this._getToolTipTitle = function(format) {
    format = format || 'txt';
    value = 'Switch ' + this.name() + "\n"
          + 'current state ' + (this.state() ? '(on)' : '(off)')  + "\n"
          + 'power usage: ' + this.wattage() + ' (when on)' + "\n"
          + 'water usage: ' + this.waterflow() + ' (when on)' + "\n"
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
    if (value == undefined) return this._name;
    if (value != '') this._name = value;
  }

  this.state = function(value) {
    if (value == undefined) return this._state === true;
    this._state = value == 1 || value == true || value == 'true' || value === true;
  }

  this.wattage = function(value) {
    if (value == undefined) return this._wattage;
    if (value != '') this._wattage = value;
  }

  this.waterflow = function(value) {
    if (value == undefined) return this._waterflow;
    if (value != '') this._waterflow = value;
  }

  this.update = function(data) {
    updater(this._canvas.attr('id'));
    this.name(data.name);
    this.state(data.current);
    this.wattage(data.wattage);
    this._lastupdate = moment().format("dddd D MMMM YYYY, HH:mm:ss");
    this._animate();
  }

  this.toggle = function() {
    jQuery.ajax({
      url: '/switch/' + this._id + '/' + (this.state() ? 'off' : 'on') ,
      dataType: 'json'
    }).done(function(result){
      loadSwitches(true);
    });
  }

  this._createcanvas();
  this._draw();
  this._animate();
}
