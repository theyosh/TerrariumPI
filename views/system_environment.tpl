% include('inc/page_header.tpl')
        <div class="x_panel">
          <div class="x_title">
            <h2><span class="glyphicon glyphicon-info-sign" aria-hidden="true" title="{{_('Information')}}"></span> {{_('Help')}}<small></small></h2>
            <ul class="nav navbar-right panel_toolbox">
              <li>
                <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
              </li>
              <li>
                <a class="close-link"><i class="fa fa-close" title="{{_('Close')}}"></i></a>
              </li>
            </ul>
            <div class="clearfix"></div>
          </div>
          <div class="x_content">
            <p>{{_('Here you can adjust the overall environment system. Hover above the settings to get more information. Or go to the help section.')}}</p>
          </div>
        </div>
        <form action="/api/config/environment" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
          <div class="row">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 class="orange"><i class="fa fa-lightbulb-o"></i> {{_('Lights')}} <small class="data_update">{{_('settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Status')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enable or disable the lighting system. When enabled, you can make changes below. By disabling it will not lose the current settings. You can temporary stop the lightning system.')}}">
                      <div class="btn-group" data-toggle="buttons">
                        <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="light_enabled" type="radio" value="false"> {{_('Disabled')}}</label> <label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="light_enabled" type="radio" value="true"> {{_('Enabled')}}</label>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_modus">{{_('Light modus')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Select the modus on which the lights will be put on and off. Select weather to use the sun rise and sun set at your location. This will make the amount of lighting variable to the actual amount of daylight. When selecting clock, the light will put on and off at sellected times')}}">
                        <select class="form-control" name="light_modus" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="timer">
                            {{_('Timer')}}
                          </option>
                          <option value="weather">
                            {{_('Weather')}}
                          </option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_on">{{_('Lights on')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="light_on" required="required" type="text" placeholder="{{_('Lights on')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the time when the light should be put on. Only available when running in \'%s\' modus.') % (_('Timer'),)}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_off">{{_('Lights off')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="light_off" required="required" type="text" placeholder="{{_('Lights off')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the time when the lights should be put off. Only available when running in \'%s\' modus.') % (_('Timer'),)}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_max_hours">{{_('Maximal lights hours')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="light_max_hours" required="required" type="text" placeholder="{{_('Maximal lights hours')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the maximum amount of lights time in hours. When the time between on and off is more then this maximum, the on and off time will be shifted more to each other.')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_min_hours">{{_('Minimal light hours')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="light_min_hours" required="required" type="text" placeholder="{{_('Minimal light hours')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the minimal amount of lights time in hours. When the time between on and off is less then this amount of hours, the on and off time will be widenend untill the minimum amount of hours entered here.')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_hours_shift">{{_('Hours shift')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="light_hours_shift" required="required" type="text" placeholder="{{_('Hours shift')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the amount of hours that the lights should shift. Is only needed when running in the \'%s\' modus. Enter a positive number for adding hours to the start time. Use negative numbers for subtracking from the start time') % (_('Weather'),)}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_power_switches">{{_('Power switches')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Select the power switches that should be toggled on the selected times above. Normally these are the switches connected to the lights. Select all needed switches below.')}}">
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
                  <h2 class="blue"><i class="fa fa-tint"></i> {{_('Sprayer')}} <small class="data_update">{{_('settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Status')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enable or disable the spraying system.')}}">
                      <div class="btn-group" data-toggle="buttons">
                        <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="sprayer_enabled" type="radio" value="false"> {{_('Disabled')}}</label><label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="sprayer_enabled" type="radio" value="true"> {{_('Enabled')}}</label>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Enabled during the night')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enable spraying when the lights are off. This can cause water flow when there is not enough heat to vaporize the water.')}}">
                      <div class="btn-group" data-toggle="buttons">
                        <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="sprayer_night_enabled" type="radio" value="false"> {{_('Disabled')}}</label><label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="sprayer_night_enabled" type="radio" value="true"> {{_('Enabled')}}</label>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sprayer_spray_timeout">{{_('Sprayer wait timeout (seconds)')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="sprayer_spray_timeout" required="required" type="text" placeholder="{{_('Sprayer wait timeout (seconds)')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Now much time must there be between two spray times and during startup. This is the amount of time that the humidity can settle and the new hudmity values are read.')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sprayer_spray_duration">{{_('Sprayer spray duration (seconds)')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="sprayer_spray_duration" required="required" type="text" placeholder="{{_('Sprayer spray duration (seconds)')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('How long is the system spraying. Enter the amount of seconds that the system is on when the humidity is to low.')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sprayer_power_switches">{{_('Power switches')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Select the power switche(s) which controll the spray system. You can select multiple switches.')}}">
                        <select class="form-control" multiple="multiple" name="sprayer_power_switches" tabindex="-1" placeholder="{{_('Select an option')}}">
                          </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sprayer_sensors">{{_('Humidity sensors')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Select the humidity sensors that are use to controll the final humidity. When selecting multiple sensors, the average is used for determing the humidity. This is also shown on the dashboard on the right side.')}}">
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
                  <h2 class="red"><i class="fa fa-fire"></i> {{_('Heater')}} <small class="data_update">{{_('settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Status')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enable or disable the heating system.')}}">
                      <div class="btn-group" data-toggle="buttons">
                        <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="heater_enabled" type="radio" value="false"> {{_('Disabled')}}</label><label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="heater_enabled" type="radio" value="true"> {{_('Enabled')}}</label>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Enabled during the day')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enable the heating system during day time. Normally the day time lighting will produce enough heat.')}}">
                      <div class="btn-group" data-toggle="buttons">
                        <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="heater_day_enabled" type="radio" value="false"> {{_('Disabled')}}</label><label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="heater_day_enabled" type="radio" value="true"> {{_('Enabled')}}</label>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_modus">{{_('Heater modus')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Select the operating modus. Use \'%s\' modus to select the time period in which the heating is running. Select \'%s\' modus to use the sun rise and sun set as on and off times. When the sun rises the heating system will stop. Use \'%s\' modus to have the heating running when the lights are off.') % (_('Timer'),_('Weather'),_('Sensor'))}}">
                        <select class="form-control" name="heater_modus" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="timer">
                            {{_('Timer')}}
                          </option>
                          <option value="weather">
                            {{_('Weather')}}
                          </option>
                          <option value="sensor">
                            {{_('Sensor')}}
                          </option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_on">{{_('Heater on')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="heater_on" required="required" type="text" placeholder="{{_('Heater on')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the time when the heating should be put on. Only available when running in \'%s\' modus.') % (_('Timer'),)}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_off">{{_('Heater off')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="heater_off" required="required" type="text" placeholder="{{_('Heater off')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the time when the heating should be put off. Only available when running in \'%s\' modus.') % (_('Timer'),)}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_power_switches">{{_('Power switches')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Select the power switche(s) which controll the heating system. You can select multiple switches.')}}">
                        <select class="form-control" multiple="multiple" name="heater_power_switches" tabindex="-1" placeholder="{{_('Select an option')}}">
                          </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_sensors">{{_('Temperature sensors')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Select the temperature sensors that are use to controll the final temperature. When selecting multiple sensors, the average is used for determing the temperature. This is also shown on the dashboard right side.')}}">
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
                  <h2 class="blue"><i class="fa fa-flag-o"></i> {{_('Cooling')}} <small class="data_update">{{_('settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Status')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enable or disable the cooling system.')}}">
                      <div class="btn-group" data-toggle="buttons">
                        <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="coller_enabled" type="radio" value="false"> {{_('Disabled')}}</label><label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="cooler_enabled" type="radio" value="true"> {{_('Enabled')}}</label>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Enabled during the night')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enable the cooling system during night time. Normally the night time it will cool down by it selfs.')}}">
                      <div class="btn-group" data-toggle="buttons">
                        <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="cooler_night_enabled" type="radio" value="false"> {{_('Disabled')}}</label><label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="cooler_night_enabled" type="radio" value="true"> {{_('Enabled')}}</label>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cooler_modus">{{_('Cooler modus')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Select the operating modus. Use \'%s\' modus to select the time period in which the cooling is running. Select \'%s\' modus to use the sun rise and sun set as on and off times. When the sun sets the cooling system will stop. Use \'%s\' modus to have the cooling running when the lights are on.') % (_('Timer'),_('Weather'),_('Sensor'))}}">
                        <select class="form-control" name="cooler_modus" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="timer">
                            {{_('Timer')}}
                          </option>
                          <option value="weather">
                            {{_('Weather')}}
                          </option>
                          <option value="sensor">
                            {{_('Sensor')}}
                          </option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cooler_on">{{_('Cooler on')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="cooler_on" required="required" type="text" placeholder="{{_('Cooler on')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the time when the cooling should be put on. Only available when running in \'%s\' modus.') % (_('Timer'),)}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cooler_off">{{_('Cooler off')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="cooler_off" required="required" type="text" placeholder="{{_('Cooler off')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the time when the cooling should be put off. Only available when running in \'%s\' modus.') % (_('Timer'),)}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cooler_power_switches">{{_('Power switches')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Select the power switche(s) which controll the cooling system. You can select multiple switches.')}}">
                        <select class="form-control" multiple="multiple" name="cooler_power_switches" tabindex="-1" placeholder="{{_('Select an option')}}">
                          </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cooler_sensors">{{_('Temperature sensors')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Select the temperature sensors that are use to controll the final temperature. When selecting multiple sensors, the average is used for determing the temperature. This is also shown on the dashboard right side.')}}">
                        <select class="form-control" multiple="multiple" name="cooler_sensors" tabindex="-1" placeholder="{{_('Select an option')}}">
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
                  <button class="btn btn-success" type="submit">{{_('Submit')}}</button>
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

            $('select[name$="_modus"]').select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            }).on('change',function() {
              var part = this.name.replace('_modus','')
              switch (this.value) {
                case 'timer':
                  $('input[name="' + part + '_on"]').removeAttr('readonly').removeAttr('disabled');
                  $('input[name="' + part + '_off"]').removeAttr('readonly').removeAttr('disabled');
                  break;

                case 'weather':
                  $('input[name="' + part + '_on"]').attr('readonly','readonly').removeAttr('disabled');
                  $('input[name="' + part + '_off"]').attr('readonly','readonly').removeAttr('disabled');
                  // Load current sun rise and sun set based on weather data
                  $.get('/api/weather',function(data){
                    $('input[name="' + part + '_on"]').val(moment(data.sun.rise * 1000).format('LT'));
                    $('input[name="' + part + '_off"]').val(moment(data.sun.set * 1000).format('LT'));
                  });
                  break
                case 'sensor':
                  $('input[name="' + part + '_on"]').attr('disabled','disabled');
                  $('input[name="' + part + '_off"]').attr('disabled','disabled');
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
                select_boxes.append($('<option>').attr({'value':powerswitch.id}).text(powerswitch.name));
              });
            });

            $.get('/api/sensors/humidity',function(data){
              var select_boxes = $('select[name="sprayer_sensors"]');
              $.each(data.sensors,function (index,sensor){
                select_boxes.append($('<option>').attr({'value':sensor.id}).text(sensor.name));
              });
            });

            $.get('/api/sensors/temperature',function(data){
              var select_boxes = $('select[name="heater_sensors"],select[name="cooler_sensors"]');
              $.each(data.sensors,function (index,sensor){
                select_boxes.append($('<option>').attr({'value':sensor.id}).text(sensor.name));
              });
            });

            $.get('/api/config/environment',function(data){
              $.each(data,function (index,type){
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
