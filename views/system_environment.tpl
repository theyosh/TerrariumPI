% include('inc/page_header.tpl')
        <div class="x_panel help">
          <div class="x_title">
            <h2><span class="glyphicon glyphicon-info-sign" aria-hidden="true" title="{{_('Information')}}"></span> {{_('Help')}}<small></small></h2>
            <ul class="nav navbar-right panel_toolbox">
              <li>
                <a class="collapse-link"><i class="fa fa-chevron-down"></i></a>
              </li>
              <li>
                <a class="close-link"><i class="fa fa-close" title="{{_('Close')}}"></i></a>
              </li>
            </ul>
            <div class="clearfix"></div>
          </div>
          <div class="x_content">
            <p>{{_('Here you can configure your environment.')}}
               {{!_('Required fields are marked with \'%s\'.') % ('<span class="required">*</span>',)}}
               {{_('Hover over the fields to get extra information.')}}
            </p>
          </div>
        </div>
        <form action="/api/config/environment" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
          <div class="row">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 class="orange"><i class="fa fa-lightbulb-o"></i> {{_('Lights')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_mode">{{_('Light mode')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_lights_mode')}}">
                        <select class="form-control" name="light_mode" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="disabled">{{_('Disabled')}}</option>
                          <option value="timer">{{_('Timer')}}</option>
                          <option value="weather">{{_('Weather')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_on">{{_('Lights on')}} </label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="light_on" required="required" type="text" placeholder="{{_('Lights on')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_lights_on')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_off">{{_('Lights off')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="light_off" required="required" type="text" placeholder="{{_('Lights off')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_lights_off')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_on_duration">{{_('Timer on duration')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="light_on_duration" required="required" type="text" placeholder="{{_('Timer on duration')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_lights_on_duration')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_off_duration">{{_('Timer off duration')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="light_off_duration" required="required" type="text" placeholder="{{_('Timer off duration')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_lights_off_duration')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_max_hours">{{_('Maximum lights hours')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="light_max_hours" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Maximum lights hours')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_lights_max_hours')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_min_hours">{{_('Minimum light hours')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="light_min_hours" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Minimum light hours')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_lights_min_hours')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_hours_shift">{{_('Hours shift')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="light_hours_shift" required="required" type="text" pattern="[\-0-9\.]+" placeholder="{{_('Hours shift')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_lights_hour_shift')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_power_switches">{{_('Power switches')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_lights_power_switches')}}">
                        <select class="form-control" multiple="multiple" name="light_power_switches" tabindex="-1" placeholder="{{_('Select an option')}}">
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
                  <h2 class="blue"><i class="fa fa-umbrella"></i> {{_('Sprayer')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sprayer_mode">{{_('Sprayer mode')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sprayer_mode')}}">
                        <select class="form-control" name="sprayer_mode" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="disabled">{{_('Disabled')}}</option>
                          <option value="timer">{{_('Timer')}}</option>
                          <option value="sensor">{{_('Sensor')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Enabled when lights are off')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sprayer_enable_during_night')}}">
                      <div class="btn-group" data-toggle="buttons">
                        <label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="sprayer_night_enabled" type="radio" value="true">{{_('Yes')}}</label>
                        <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="sprayer_night_enabled" type="radio" value="false">{{_('No')}}</label>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sprayer_on_duration">{{_('Timer on duration')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="sprayer_on_duration" required="required" type="text" placeholder="{{_('Timer on duration')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sprayer_on_duration')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sprayer_off_duration">{{_('Timer off duration')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="sprayer_off_duration" required="required" type="text" placeholder="{{_('Timer off duration')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sprayer_off_duration')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sprayer_spray_timeout">{{_('Sprayer wait timeout (seconds)')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="sprayer_spray_timeout" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Sprayer wait timeout (seconds)')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sprayer_delay')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sprayer_spray_duration">{{_('Spray duration (seconds)')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="sprayer_spray_duration" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Sprayer spray duration (seconds)')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sprayer_duration')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sprayer_power_switches">{{_('Power switches')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sprayer_power_switches')}}">
                        <select class="form-control" multiple="multiple" name="sprayer_power_switches" tabindex="-1" placeholder="{{_('Select an option')}}">
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sprayer_sensors">{{_('Humidity sensors')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sprayer_humidity_sensors')}}">
                        <select class="form-control" multiple="multiple" name="sprayer_sensors" tabindex="-1" placeholder="{{_('Select an option')}}">
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
                  <h2 class="blue"><i class="fa fa-umbrella"></i> {{_('Moisture')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_mode">{{_('Moisture mode')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_moisture_mode')}}">
                        <select class="form-control" name="moisture_mode" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="disabled">{{_('Disabled')}}</option>
                          <option value="timer">{{_('Timer')}}</option>
                          <option value="sensor">{{_('Sensor')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Enabled when lights are off')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_moisture_enable_during_night')}}">
                      <div class="btn-group" data-toggle="buttons">
                        <label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="moisture_night_enabled" type="radio" value="true">{{_('Yes')}}</label>
                        <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="moisture_night_enabled" type="radio" value="false">{{_('No')}}</label>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_on_duration">{{_('Timer on duration')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="moisture_on_duration" required="required" type="text" placeholder="{{_('Timer on duration')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_moisture_on_duration')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_off_duration">{{_('Timer off duration')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="moisture_off_duration" required="required" type="text" placeholder="{{_('Timer off duration')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_moisture_off_duration')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_spray_timeout">{{_('Moisture wait timeout (seconds)')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="moisture_spray_timeout" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Moisture wait timeout (seconds)')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_moisture_delay')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_spray_duration">{{_('Spray duration (seconds)')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="moisture_spray_duration" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Sprayer spray duration (seconds)')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_moisture_duration')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sprayer_power_switches">{{_('Power switches')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_moisture_power_switches')}}">
                        <select class="form-control" multiple="multiple" name="moisture_power_switches" tabindex="-1" placeholder="{{_('Select an option')}}">
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sprayer_sensors">{{_('Moisture sensors')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_moisture_moisture_sensors')}}">
                        <select class="form-control" multiple="multiple" name="moisture_sensors" tabindex="-1" placeholder="{{_('Select an option')}}">
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
                  <h2 class="blue"><i class="fa fa-tint"></i> {{_('Water tank')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_mode">{{_('Water tank mode')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_watertank_mode')}}">
                        <select class="form-control" name="watertank_mode" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="disabled">{{_('Disabled')}}</option>
                          <option value="weather">{{_('Weather')}}</option>
                          <option value="timer">{{_('Timer')}}</option>
                          <option value="sensor">{{_('Sensor')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_on">{{_('Water pump on')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="watertank_on" required="required" type="text" placeholder="{{_('Water pump on')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_watertank_on')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_off">{{_('Water pump off')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="watertank_off" required="required" type="text" placeholder="{{_('Water pump off')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_watertank_off')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_on_duration">{{_('Timer on duration')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="watertank_on_duration" required="required" type="text" placeholder="{{_('Timer on duration')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_watertank_on_duration')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_off_duration">{{_('Timer off duration')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="watertank_off_duration" required="required" type="text" placeholder="{{_('Timer off duration')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_watertank_off_duration')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_pump_duration">{{_('Water tank pump duration (seconds)')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="watertank_pump_duration" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Water tank pump duration (seconds)')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_watertank_duration')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_volume">{{_('Water tank volume in liters')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="watertank_volume" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Water tank volume in liters')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_watertank_volume')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_height">{{_('Water tank height')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="watertank_height" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Water tank height')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_watertank_height')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_power_switches">{{_('Power switches')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_watertank_power_switches')}}">
                        <select class="form-control" multiple="multiple" name="watertank_power_switches" tabindex="-1" placeholder="{{_('Select an option')}}">
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_sensors">{{_('Distance sensors')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_watertank_distance_sensors')}}">
                        <select class="form-control" multiple="multiple" name="watertank_sensors" tabindex="-1" placeholder="{{_('Select an option')}}">
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
                  <h2 class="red"><i class="fa fa-fire"></i> {{_('Heater')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_mode">{{_('Heater mode')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_heater_mode')}}">
                        <select class="form-control" name="heater_mode" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="disabled">{{_('Disabled')}}</option>
                          <option value="timer">{{_('Timer')}}</option>
                          <option value="weather">{{_('Weather')}}</option>
                          <option value="sensor">{{_('Sensor')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Enabled when lights are on')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_heater_enable_during_day')}}">
                      <div class="btn-group" data-toggle="buttons">
                        <label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="heater_day_enabled" type="radio" value="true">{{_('Yes')}}</label>
                        <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="heater_day_enabled" type="radio" value="false">{{_('No')}}</label>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_on">{{_('Heater on')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="heater_on" required="required" type="text" placeholder="{{_('Heater on')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_heater_on')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_off">{{_('Heater off')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="heater_off" required="required" type="text" placeholder="{{_('Heater off')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_heater_off')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_on_duration">{{_('Timer on duration')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="heater_on_duration" required="required" type="text" placeholder="{{_('Timer on duration')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_heater_on_duration')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_off_duration">{{_('Timer off duration')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="heater_off_duration" required="required" type="text" placeholder="{{_('Timer off duration')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_heater_off_duration')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_settle_timeout">{{_('Temperature settle time')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="heater_settle_timeout" required="required" type="text" placeholder="{{_('Temperature settle time')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_heater_settle_timeout')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_night_difference">{{_('Day/night difference temperature')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="heater_night_difference" required="required" type="text" placeholder="{{_('Temperature difference during the night')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_heater_night_difference')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_night_source">{{_('Day/night difference source')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('heater_night_source')}}">
                        <select class="form-control" name="heater_night_source" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="weather">{{_('Weather')}}</option>
                          <option value="lights">{{_('Lights')}}</option>
                        </select>
                      </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_power_switches">{{_('Power switches')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_heater_power_switches')}}">
                        <select class="form-control" multiple="multiple" name="heater_power_switches" tabindex="-1" placeholder="{{_('Select an option')}}">
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_sensors">{{_('Temperature sensors')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_heater_temperature_sensors')}}">
                        <select class="form-control" multiple="multiple" name="heater_sensors" tabindex="-1" placeholder="{{_('Select an option')}}">
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
                  <h2 class="blue"><i class="fa fa-flag-o"></i> {{_('Cooling')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cooler_mode">{{_('Cooler mode')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_cooler_mode')}}">
                        <select class="form-control" name="cooler_mode" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="disabled">{{_('Disabled')}}</option>
                          <option value="timer">{{_('Timer')}}</option>
                          <option value="weather">{{_('Weather')}}</option>
                          <option value="sensor">{{_('Sensor')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Enabled when lights are off')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_cooler_enable_during_night')}}">
                      <div class="btn-group" data-toggle="buttons">
                        <label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="cooler_night_enabled" type="radio" value="true">{{_('Yes')}}</label>
                        <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="cooler_night_enabled" type="radio" value="false">{{_('No')}}</label>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cooler_on">{{_('Cooler on')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="cooler_on" required="required" type="text" placeholder="{{_('Cooler on')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_cooler_on')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cooler_off">{{_('Cooler off')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="cooler_off" required="required" type="text" placeholder="{{_('Cooler off')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_cooler_off')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cooler_on_duration">{{_('Timer on duration')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="cooler_on_duration" required="required" type="text" placeholder="{{_('Timer on duration')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_cooler_on_duration')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cooler_off_duration">{{_('Timer off duration')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="cooler_off_duration" required="required" type="text" placeholder="{{_('Timer off duration')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_cooler_off_duration')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cooler_power_switches">{{_('Power switches')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_cooler_power_switches')}}">
                        <select class="form-control" multiple="multiple" name="cooler_power_switches" tabindex="-1" placeholder="{{_('Select an option')}}">
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cooler_sensors">{{_('Temperature sensors')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_cooler_temperature_sensors')}}">
                        <select class="form-control" multiple="multiple" name="cooler_sensors" tabindex="-1" placeholder="{{_('Select an option')}}">
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row submit">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="ln_solid"></div>
              <div class="form-group">
                <div class="col-md-11 col-sm-11 col-xs-12 text-center">
                  <button class="btn btn-success" type="submit">{{_('Submit')}}</button>
                </div>
              </div>
            </div>
          </div>
        </form>
        <script type="text/javascript">
          var switches_loaded = false;
          var humidity_sensors_loaded = false;
          var temperature_sensors_loaded = false;
          var distance_sensors_loaded = false;
          var moisture_sensors_loaded = false;

          $(document).ready(function() {
            init_form_settings('environment');

            $('select[name="heater_night_source"]').select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            });

            $('select[name$="_mode"]').select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            }).on('change',function() {
              var part = this.name.replace('_mode','')
              $('input[name^="' + part + '"], select[name^="' + part + '"]').removeAttr('readonly','disabled');
              switch (this.value) {
                case 'disabled':
                  $('input[name^="' + part + '"], select[name^="' + part + '"]:not(:first)').attr('readonly','readonly');
                  break;

                case 'timer':
                  $('input[name="' + part + '_max_hours"]').attr('readonly','readonly');
                  $('input[name="' + part + '_min_hours"]').attr('readonly','readonly');
                  $('input[name="' + part + '_hours_shift"]').attr('readonly','readonly');
                  break;

                case 'weather':
                  // Load current sun rise and sun set based on weather data
                  $.get('/api/weather',function(data){
                    if (part == 'heater') {
                      // For heater we swap the times, because heater should not be running when it is 'day'
                      $('input[name="' + part + '_on"]').val(moment(data.sun.set * 1000).format('LT'));
                      $('input[name="' + part + '_off"]').val(moment(data.sun.rise * 1000).format('LT'));
                    } else {
                      $('input[name="' + part + '_on"]').val(moment(data.sun.rise * 1000).format('LT'));
                      $('input[name="' + part + '_off"]').val(moment(data.sun.set * 1000).format('LT'));
                    }
                  });

                case 'sensor':
                  $('input[name="' + part + '_on"]').attr('readonly','readonly');
                  $('input[name="' + part + '_off"]').attr('readonly','readonly');
                  $('input[name="' + part + '_on_duration"]').attr('readonly','readonly');
                  $('input[name="' + part + '_off_duration"]').attr('readonly','readonly');
                  break;
              }
            });

            $('select[name$="_power_switches"],select[name$="_sensors"]').select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            });

            $.get('/api/switches',function(data){
              var select_boxes = $('select[name$="_power_switches"]');
              $.each(data.switches,function (index,powerswitch){
                if (!powerswitch.timer_enabled) {
                  // We can't use timer enabled switches. They have there own schedule
                  select_boxes.append($('<option>').attr({'value':powerswitch.id}).text(powerswitch.name));
                }
              });
              switches_loaded = true;
            });

            $.get('/api/sensors/humidity',function(data){
              var select_boxes = $('select[name="sprayer_sensors"]');
              $.each(data.sensors,function (index,sensor){
                select_boxes.append($('<option>').attr({'value':sensor.id}).text(sensor.name));
              });
              humidity_sensors_loaded = true;
            });

            $.get('/api/sensors/temperature',function(data){
              var select_boxes = $('select[name="heater_sensors"],select[name="cooler_sensors"]');
              $.each(data.sensors,function (index,sensor){
                select_boxes.append($('<option>').attr({'value':sensor.id}).text(sensor.name));
              });
              temperature_sensors_loaded = true;
            });

            $.get('/api/sensors/distance',function(data){
              var select_boxes = $('select[name="watertank_sensors"]');
              $.each(data.sensors,function (index,sensor){
                select_boxes.append($('<option>').attr({'value':sensor.id}).text(sensor.name));
              });
              distance_sensors_loaded = true;
            });

            $.get('/api/sensors/moisture',function(data){
              var select_boxes = $('select[name="moisture_sensors"]');
              $.each(data.sensors,function (index,sensor){
                select_boxes.append($('<option>').attr({'value':sensor.id}).text(sensor.name));
              });
              moisture_sensors_loaded = true;
            });

            setContentHeight();
            load_environment_settings();
          });

          function load_environment_settings() {
            // Wait with loading the environment settings until all selectors are loaded
            if (switches_loaded && humidity_sensors_loaded && temperature_sensors_loaded && distance_sensors_loaded && moisture_sensors_loaded) {
              $.get('/api/config/environment',function(data){
                $.each(data,function (environmentpart,environmentdata){
                  $.each(environmentdata,function(name,value) {
                    var config_field = $('form [name="' + environmentpart + '_' + name + '"]');
                    if (config_field.length >= 1) {
                      switch (config_field.prop('type').toLowerCase()) {
                        case 'text':
                          config_field.val(value);
                          break;

                        case 'radio':
                          $('input[name="' + environmentpart + '_' + name + '"][value="' + value + '"]').attr('checked','checked').parent().addClass('active');
                          break;

                        case 'select-one':
                        case 'select-multiple':
                          config_field.val(value).trigger('change');
                          break;
                      }
                    }
                  });
                });
              });
            } else {
              // Not all selectors are loaded... wait for 100 miliseconds and try again
              setTimeout(function() {
                load_environment_settings();
              }, 100);
            }
          }
        </script>
% include('inc/page_footer.tpl')
