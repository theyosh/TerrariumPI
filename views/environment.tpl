% include('inc/page_header.tpl')
              <form id="" data-parsley-validate class="form-horizontal form-label-left" method="put" action="/api/config/environment">
                <div class="row">
                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="x_panel">
                      <div class="x_title">
                        <h2 class="orange"><i class="fa fa-lightbulb-o"></i> Lights <small class="data_update">settings</small></h2>
                        <ul class="nav navbar-right panel_toolbox">
                          <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a></li>
                          <li><a class="close-link"><i class="fa fa-close"></i></a></li>
                        </ul>
                        <div class="clearfix"></div>
                      </div>
                      <div class="x_content">
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12">Status</label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <div class="btn-group" data-toggle="buttons">
                              <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default">
                              <input type="radio" name="light_enabled" value="false"> Disabled
                              </label>
                              <label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default">
                              <input type="radio" name="light_enabled" value="true"> Enabled
                              </label>
                            </div>
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12">Light modus</label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <div class="form-group">
                              <select class="form-control" tabindex="-1" name="light_modus">
                                <option></option>
                                <option value="timer">Timer</option>
                                <option value="weather">Weather</option>
                              </select>
                            </div>
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12" for="lights_on">Lights on <span class="required">*</span></label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="text" name="light_on" required="required" class="form-control col-md-7 col-xs-12">
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12" for="lights_off">Lights off <span class="required">*</span></label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="text" name="light_off" required="required" class="form-control col-md-7 col-xs-12">
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12" for="lights_max_hours">Maximal lights hours <span class="required">*</span></label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="text" name="light_max_hours" required="required" class="form-control col-md-7 col-xs-12">
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12" for="lights_min_hours">Minimal light hours <span class="required">*</span></label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="text" name="light_min_hours" required="required" class="form-control col-md-7 col-xs-12">
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12" for="lights_hours_shift">Hours shift <span class="required">*</span></label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="text" name="light_hours_shift" required="required" class="form-control col-md-7 col-xs-12">
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12">Power switches</label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <div class="form-group">
                              <select class="form-control" tabindex="-1" name="light_power_switches" multiple="multiple">
                              </select>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="x_panel">
                      <div class="x_title">
                        <h2 class="blue"><i class="fa fa-tint"></i> Sprayer <small class="data_update">settings</small></h2>
                        <ul class="nav navbar-right panel_toolbox">
                          <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a></li>
                          <li><a class="close-link"><i class="fa fa-close"></i></a></li>
                        </ul>
                        <div class="clearfix"></div>
                      </div>
                      <div class="x_content">
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12">Status</label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <div class="btn-group" data-toggle="buttons">
                              <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default">
                              <input type="radio" name="sprayer_enabled" value="false"> Disabled
                              </label>
                              <label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default">
                              <input type="radio" name="sprayer_enabled" value="true"> Enabled
                              </label>
                            </div>
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12">Enabled during the night</label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <div class="btn-group" data-toggle="buttons">
                              <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default">
                              <input type="radio" name="sprayer_night_enabled" value="false"> Disabled
                              </label>
                              <label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default">
                              <input type="radio" name="sprayer_night_enabled" value="true"> Enabled
                              </label>
                            </div>
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12" for="lights_on">Sprayer wait timeout (seconds) <span class="required">*</span></label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="text" name="sprayer_spray_timeout" required="required" class="form-control col-md-7 col-xs-12">
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12" for="lights_off">Sprayer spray duration (seconds) <span class="required">*</span></label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="text" name="sprayer_spray_duration" required="required" class="form-control col-md-7 col-xs-12">
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12">Power switches</label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <div class="form-group">
                              <select class="form-control" tabindex="-1" name="sprayer_power_switches" multiple="multiple">
                              </select>
                            </div>
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12">Humidity sensors</label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <div class="form-group">
                              <select class="form-control" tabindex="-1" name="sprayer_sensors" multiple="multiple">
                              </select>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="x_panel">
                      <div class="x_title">
                        <h2 class="red"><i class="fa fa-fire"></i> Heater <small class="data_update">settings</small></h2>
                        <ul class="nav navbar-right panel_toolbox">
                          <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a></li>
                          <li><a class="close-link"><i class="fa fa-close"></i></a></li>
                        </ul>
                        <div class="clearfix"></div>
                      </div>
                      <div class="x_content">
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12">Status</label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <div class="btn-group" data-toggle="buttons">
                              <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default">
                              <input type="radio" name="heater_enabled" value="false"> Disabled
                              </label>
                              <label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default">
                              <input type="radio" name="heater_enabled" value="true"> Enabled
                              </label>
                            </div>
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12">Enabled during the day</label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <div class="btn-group" data-toggle="buttons">
                              <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default">
                              <input type="radio" name="heater_day_enabled" value="false"> Disabled
                              </label>
                              <label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default">
                              <input type="radio" name="heater_day_enabled" value="true"> Enabled
                              </label>
                            </div>
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12">Heater modus</label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <div class="form-group">
                              <select class="form-control" tabindex="-1" name="heater_modus">
                                <option></option>
                                <option value="timer">Timer</option>
                                <option value="weather">Weather</option>
                                <option value="sensor">Sensor</option>
                              </select>
                            </div>
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_on">Heater on <span class="required">*</span></label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="text" name="heater_on" required="required" class="form-control col-md-7 col-xs-12">
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_off">Heater off <span class="required">*</span></label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="text" name="heater_off" required="required" class="form-control col-md-7 col-xs-12">
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12">Power switches</label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <div class="form-group">
                              <select class="form-control" tabindex="-1" name="heater_power_switches" multiple="multiple">
                              </select>
                            </div>
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12">Temperature sensors</label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <div class="form-group">
                              <select class="form-control" tabindex="-1" name="heater_sensors" multiple="multiple">
                              </select>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="ln_solid"></div>
                    <div class="form-group">
                      <div class="col-md-11 col-sm-11 col-xs-12 text-center">
                        <button type="submit" class="btn btn-success">Submit</button>
                      </div>
                    </div>
                  </div>
                </div>
              </form>
              <script type="text/javascript">
                $(document).ready(function() {

                  $('form').on('submit',function() {
                    $(this).find('input[type="radio"]').removeAttr('checked').removeAttr('disabled');
                    $(this).find('label.active > input[type="radio"]').attr('checked','checked');
                    $(this).find('label:not(.active) > input[type="radio"]').attr('disabled','disabled');
                  });

                  var light_modus_selector = $("select[name='light_modus']");
                  light_modus_selector.select2({
                    placeholder: "Select an option",
                    allowClear: false,
                    minimumResultsForSearch: Infinity
                  });

                  light_modus_selector.on('change',function() {
                    var choice = this.value;
                    switch (choice) {
                      case 'timer':
                        $('input[name="light_on"]').removeAttr('readonly');
                        $('input[name="light_off"]').removeAttr('readonly');
                        break;

                      case 'weather':
                        $('input[name="light_on"]').attr('readonly','readonly');
                        $('input[name="light_off"]').attr('readonly','readonly');

                        $.get('/api/weather',function(data){
                          $('input[name="light_on"]').val(moment(data.sun.rise * 1000).format('LT'));
                          $('input[name="light_off"]').val(moment(data.sun.set * 1000).format('LT'));
                        });
                        break;
                    }
                  });

                  var light_power_switches_selector = $("select[name='light_power_switches']");
                  light_power_switches_selector.select2({
                    placeholder: "Select an option",
                    allowClear: false,
                    minimumResultsForSearch: Infinity
                  });

                  var sprayer_power_switches_selector = $("select[name='sprayer_power_switches']");
                  sprayer_power_switches_selector.select2({
                    placeholder: "Select an option",
                    allowClear: false,
                    minimumResultsForSearch: Infinity
                  });

                  var sprayer_sensors_selector = $("select[name='sprayer_sensors']");
                  sprayer_sensors_selector.select2({
                    placeholder: "Select an option",
                    allowClear: false,
                    minimumResultsForSearch: Infinity
                  });

                  var heater_modus_selector = $("select[name='heater_modus']");
                  heater_modus_selector.select2({
                    placeholder: "Select an option",
                    allowClear: false,
                    minimumResultsForSearch: Infinity
                  });

                  var heater_power_switches_selector = $("select[name='heater_power_switches']");
                  heater_power_switches_selector.select2({
                    placeholder: "Select an option",
                    allowClear: false,
                    minimumResultsForSearch: Infinity
                  });

                  var heater_sensors_selector = $("select[name='heater_sensors']");
                  heater_sensors_selector.select2({
                    placeholder: "Select an option",
                    allowClear: false,
                    minimumResultsForSearch: Infinity
                  });

                  heater_modus_selector.on('change',function() {
                    var choice = this.value;
                    switch (choice) {
                      case 'timer':
                        $('input[name="heater_on"]').removeAttr('readonly').removeAttr('disabled');
                        $('input[name="heater_off"]').removeAttr('readonly').removeAttr('disabled');
                        break;

                      case 'sensor':
                        $('input[name="heater_on"]').attr('disabled','disabled');
                        $('input[name="heater_off"]').attr('disabled','disabled');
                        break;

                      case 'weather':
                        $('input[name="heater_on"]').attr('readonly','readonly').removeAttr('disabled');
                        $('input[name="heater_off"]').attr('readonly','readonly').removeAttr('disabled');

                        $.get('/api/weather',function(data){
                          $('input[name="heater_on"]').val(moment(data.sun.rise * 1000).format('LT'));
                          $('input[name="heater_off"]').val(moment(data.sun.set * 1000).format('LT'));
                        });
                        break;
                    }
                  });

                  $.get('/api/switches',function(data){
                    $.each(data.switches,function (index,powerswitch){
                      light_power_switches_selector.append($('<option>').attr({'value':powerswitch.id}).text(powerswitch.name));
                      sprayer_power_switches_selector.append($('<option>').attr({'value':powerswitch.id}).text(powerswitch.name));
                      heater_power_switches_selector.append($('<option>').attr({'value':powerswitch.id}).text(powerswitch.name));
                    });
                  });

                  $.get('/api/sensors/humidity',function(data){
                    $.each(data.sensors,function (index,sensor){
                      sprayer_sensors_selector.append($('<option>').attr({'value':sensor.id}).text(sensor.name));
                    });
                  });

                  $.get('/api/sensors/temperature',function(data){
                    $.each(data.sensors,function (index,sensor){
                      heater_sensors_selector.append($('<option>').attr({'value':sensor.id}).text(sensor.name));
                    });
                  });

                  $.get('/api/config/environment',function(data){
                    $.each(data,function (index,type){
                      console.log(index,type);
                      $.each(type,function(name,value) {
                        var config_field = $('form [name="' + index + '_' + name + '"]');
                        var config_value = value;
                        if (name == 'on' || name == 'off') {
                          config_value = moment(config_value).format('LT');
                        }
                        if (config_field.attr('type') == 'text') {
                          config_field.val(config_value);
                        } else if (config_field.attr('type') == 'radio') {
                          $('input[name="' + index + '_' + name + '"][value="' + config_value + '"]').attr('checked','checked').parent().addClass('active');
                        } else if (config_field.prop("tagName").toLowerCase() == 'select') {
                          config_field.val(value).trigger('change');
                        }
                      });
                    });
                  });
                });
              </script>
% include('inc/page_footer.tpl')
