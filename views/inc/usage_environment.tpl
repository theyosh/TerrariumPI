                  <div class="col-xs-9">
                    <!-- Tab panes -->
                    <div class="tab-content">
                      <div class="tab-pane active" id="usage-tab-environment-overview">
                        <div class="interactive_screenshot">
                          <div id="screenshot_environment_lights" class="click_area" title="{{_('Lights')}}"></div>
                          <div id="screenshot_environment_sprayer" class="click_area" title="{{_('Sprayer')}}"></div>
                          <div id="screenshot_environment_watertank" class="click_area" title="{{_('Water tank')}}"></div>
                          <div id="screenshot_environment_heater" class="click_area" title="{{_('Heater')}}"></div>
                          <div id="screenshot_environment_cooler" class="click_area" title="{{_('Cooler')}}"></div>
                          <img src="static/images/documentation/environment_overview.png" alt="{{_('System environment screenshot')}}" />
                        </div>
                      </div>
                      <div class="tab-pane" id="usage-tab-environment-lights">
                        <h3 class="lead">{{_('Lights')}}</h3>
                        <p>{{_('The light system always works on time. You can use the weather sun rise and sun set as time values or fixed time values. When selecting weather it can happen that the lights will be on for to long or to short. Use the desired values for the maximum and minimum hours. And the hours shift will shift the hours for on and off by the amount of hours  entered here.')}}</p>
                        <p>{{!_('All fields with a %s are required.') % '<span class="required">*</span>'}}</p>
                        <div class="row">
                          <div class="x_panel">
                            <div class="x_content">
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Status')}}</label>
                                <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_lights_enable')}}">
                                  <div class="btn-group" data-toggle="buttons">
                                    <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="light_enabled" type="radio" value="false"> {{_('Disabled')}}</label> <label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="light_enabled" type="radio" value="true"> {{_('Enabled')}}</label>
                                  </div>
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_mode">{{_('Light mode')}}</label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_lights_mode')}}">
                                    <select class="form-control" name="light_mode" tabindex="-1" placeholder="{{_('Select an option')}}">
                                      <option value="timer">{{_('Timer')}}</option>
                                      <option value="weather">{{_('Weather')}}</option>
                                    </select>
                                  </div>
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_on">{{_('Lights on')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control col-md-7 col-xs-12" name="light_on" required="required" type="text" placeholder="{{_('Lights on')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_lights_on')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_off">{{_('Lights off')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control col-md-7 col-xs-12" name="light_off" required="required" type="text" placeholder="{{_('Lights off')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_lights_off')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_max_hours">{{_('Maximum lights hours')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control col-md-7 col-xs-12" name="light_max_hours" required="required" type="text" placeholder="{{_('Maximum lights hours')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_lights_max_hours')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_min_hours">{{_('Minimum light hours')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control col-md-7 col-xs-12" name="light_min_hours" required="required" type="text" placeholder="{{_('Minimum light hours')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_lights_min_hours')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_hours_shift">{{_('Hours shift')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control col-md-7 col-xs-12" name="light_hours_shift" required="required" type="text" placeholder="{{_('Hours shift')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_lights_hour_shift')}}">
                                </div>
                              </div><br /><br />
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
                        <ul>
                          <li>
                            <strong>{{_('Status')}}</strong>: {{translations.get_translation('environment_field_lights_enable')}}
                          </li>
                          <li>
                            <strong>{{_('Light mode')}}</strong>: {{translations.get_translation('environment_field_lights_mode')}}
                          </li>
                          <li>
                            <strong>{{_('Lights on')}}</strong>: {{translations.get_translation('environment_field_lights_on')}}
                          </li>
                          <li>
                            <strong>{{_('Lights off')}}</strong>: {{translations.get_translation('environment_field_lights_off')}}
                          </li>
                          <li>
                            <strong>{{_('Maximum lights hours')}}</strong>: {{translations.get_translation('environment_field_lights_max_hours')}}
                          </li>
                          <li>
                            <strong>{{_('Minimum light hours')}}</strong>: {{translations.get_translation('environment_field_lights_min_hours')}}
                          </li>
                          <li>
                            <strong>{{_('Hours shift')}}</strong>: {{translations.get_translation('environment_field_lights_hour_shift')}}
                          </li>
                          <li>
                            <strong>{{_('Power switches')}}</strong>: {{translations.get_translation('environment_field_lights_power_switches')}}
                          </li>
                        </ul>
                      </div>
                      <div class="tab-pane" id="usage-tab-environment-sprayer">
                        <h3 class="lead">{{_('Sprayer')}}</h3>
                        <p>{{_('The sprayer is only working in sensor mode. This means it needs to have at least one humidity sensor and one switch to activate a spray system. When multiple humidity sensors are used, the averages of the minimum, maximum and current values are used.')}}</p>
                        <p>{{_('The sprayer will not operate when a door is open.')}}</p>
                        <p>{{!_('All fields with a %s are required.') % '<span class="required">*</span>'}}</p>
                        <div class="row">
                          <div class="x_panel">
                            <div class="x_content">
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Status')}}</label>
                                <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sprayer_enable')}}">
                                  <div class="btn-group" data-toggle="buttons">
                                    <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="sprayer_enabled" type="radio" value="false"> {{_('Disabled')}}</label><label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="sprayer_enabled" type="radio" value="true"> {{_('Enabled')}}</label>
                                  </div>
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Enabled when lights are off')}}</label>
                                <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sprayer_enable_during_night')}}">
                                  <div class="btn-group" data-toggle="buttons">
                                    <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="sprayer_night_enabled" type="radio" value="false"> {{_('Disabled')}}</label><label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="sprayer_night_enabled" type="radio" value="true"> {{_('Enabled')}}</label>
                                  </div>
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sprayer_mode">{{_('Sprayer mode')}}</label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sprayer_mode')}}">
                                    <select class="form-control" name="sprayer_mode" tabindex="-1" placeholder="{{_('Select an option')}}">
                                      <option value="sensor" selected="selected">{{_('Sensor')}}</option>
                                    </select>
                                  </div>
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sprayer_spray_timeout">{{_('Sprayer wait timeout (seconds)')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control col-md-7 col-xs-12" name="sprayer_spray_timeout" required="required" type="text" placeholder="{{_('Sprayer wait timeout (seconds)')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sprayer_delay')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sprayer_spray_duration">{{_('Spray duration (seconds)')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control col-md-7 col-xs-12" name="sprayer_spray_duration" required="required" type="text" placeholder="{{_('Sprayer spray duration (seconds)')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sprayer_duration')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sprayer_power_switches">{{_('Power switches')}}</label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sprayer_power_switches')}}">
                                    <select class="form-control" multiple="multiple" name="sprayer_power_switches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                    </select>
                                  </div>
                                </div>
                              </div><br /><br />
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
                        <ul>
                          <li>
                            <strong>{{_('Status')}}</strong>: {{translations.get_translation('environment_field_sprayer_enable')}}
                          </li>
                          <li>
                            <strong>{{_('Enabled when lights are off')}}</strong>: {{translations.get_translation('environment_field_sprayer_enable_during_night')}}
                          </li>
                          <li>
                            <strong>{{_('Sprayer mode')}}</strong>: {{translations.get_translation('environment_field_sprayer_mode')}}
                          </li>
                          <li>
                            <strong>{{_('Sprayer wait timeout (seconds)')}}</strong>: {{translations.get_translation('environment_field_sprayer_delay')}}
                          </li>
                          <li>
                            <strong>{{_('Spray duration (seconds)')}}</strong>: {{translations.get_translation('environment_field_sprayer_duration')}}
                          </li>
                          <li>
                            <strong>{{_('Power switches')}}</strong>: {{translations.get_translation('environment_field_sprayer_power_switches')}}
                          </li>
                          <li>
                            <strong>{{_('Humidity sensors')}}</strong>: {{translations.get_translation('environment_field_sprayer_humidity_sensors')}}
                          </li>
                        </ul>
                      </div>
                      <div class="tab-pane" id="usage-tab-environment-heater">
                        <h3 class="lead">{{_('Heater')}}</h3>
                        <p>{{_('When the heater is used in sensor mode the system will toggle the switches based on the alarms of the sensors. When the temperature is to cold it will toggle on the switches. Until the temperature gets above the maximum value the switch stays on. When the maximum temperature is reached, the switches will be toggled off and stay out until the temperature hits the minimum value.')}}</p>
                        <p>{{_('When used in Timer or Weather mode, the switches will be toggled on and of on the selected times regardless of the temperature.')}}</p>
                        <p>{{_('But when there are sensors used in combination with Timer or Weather mode the switches will toggle on and off when there is an alarm based on the sensors and within the selected time frame.')}}</p>
                        <p>{{!_('All fields with a %s are required.') % '<span class="required">*</span>'}}</p>
                        <div class="row">
                          <div class="x_panel">
                            <div class="x_content">
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Status')}}</label>
                                <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_heater_enable')}}">
                                  <div class="btn-group" data-toggle="buttons">
                                    <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="heater_enabled" type="radio" value="false"> {{_('Disabled')}}</label><label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="heater_enabled" type="radio" value="true"> {{_('Enabled')}}</label>
                                  </div>
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Enabled when lights are on')}}</label>
                                <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_heater_enable_during_day')}}">
                                  <div class="btn-group" data-toggle="buttons">
                                    <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="heater_day_enabled" type="radio" value="false"> {{_('Disabled')}}</label><label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="heater_day_enabled" type="radio" value="true"> {{_('Enabled')}}</label>
                                  </div>
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_mode">{{_('Heater mode')}}</label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_heater_mode')}}">
                                    <select class="form-control" name="heater_mode" tabindex="-1" placeholder="{{_('Select an option')}}">
                                      <option value="timer">{{_('Timer')}}</option>
                                      <option value="weather">{{_('Weather')}}</option>
                                      <option value="sensor">{{_('Sensor')}}</option>
                                    </select>
                                  </div>
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_on">{{_('Heater on')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control col-md-7 col-xs-12" name="heater_on" required="required" type="text" placeholder="{{_('Heater on')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_heater_on')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_off">{{_('Heater off')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control col-md-7 col-xs-12" name="heater_off" required="required" type="text" placeholder="{{_('Heater off')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_heater_off')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="heater_power_switches">{{_('Power switches')}}</label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_heater_power_switches')}}">
                                    <select class="form-control" multiple="multiple" name="heater_power_switches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                    </select>
                                  </div>
                                </div>
                              </div><br /><br />
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
                        <ul>
                          <li>
                            <strong>{{_('Status')}}</strong>: {{translations.get_translation('environment_field_heater_enable')}}
                          </li>
                          <li>
                            <strong>{{_('Enabled when lights are on')}}</strong>: {{translations.get_translation('environment_field_heater_enable_during_day')}}
                          </li>
                          <li>
                            <strong>{{_('Heater mode')}}</strong>: {{translations.get_translation('environment_field_heater_mode')}}
                          </li>
                          <li>
                            <strong>{{_('Heater on')}}</strong>: {{translations.get_translation('environment_field_heater_on')}}
                          </li>
                          <li>
                            <strong>{{_('Heater off')}}</strong>: {{translations.get_translation('environment_field_heater_off')}}
                          </li>
                          <li>
                            <strong>{{_('Power switches')}}</strong>: {{translations.get_translation('environment_field_sprayer_power_switches')}}
                          </li>
                          <li>
                            <strong>{{_('Temperature sensors')}}</strong>: {{translations.get_translation('environment_field_heater_temperature_sensors')}}
                          </li>
                        </ul>
                      </div>
                      <div class="tab-pane" id="usage-tab-environment-cooler">
                        <h3 class="lead">{{_('Cooling')}}</h3>
                        <p>{{_('When the cooler is used in sensor mode the system will toggle the switches based on the alarms of the sensors. When the temperature is to hot it will toggle on the switches. Until the temperature drops below the minimum value the switch stays on. When the minimum temperature is reached, the switches will be toggled off and stay out until the temperature hits the maximum value.')}}</p>
                        <p>{{_('When used in Timer or Weather mode, the switches will be toggled on and of on the selected times regardless of the temperature.')}}</p>
                        <p>{{_('But when there are sensors used in combination with Timer or Weather mode the switches will toggle on and off when there is an alarm based on the sensors and within the selected time frame.')}}</p>
                        <p>{{!_('All fields with a %s are required.') % '<span class="required">*</span>'}}</p>
                        <div class="row">
                          <div class="x_panel">
                            <div class="x_content">
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Status')}}</label>
                                <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_cooler_enable')}}">
                                  <div class="btn-group" data-toggle="buttons">
                                    <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="cooler_enabled" type="radio" value="false"> {{_('Disabled')}}</label><label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="cooler_enabled" type="radio" value="true"> {{_('Enabled')}}</label>
                                  </div>
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12">{{_('Enabled when lights are off')}}</label>
                                <div class="col-md-7 col-sm-6 col-xs-10" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_cooler_enable_during_night')}}">
                                  <div class="btn-group" data-toggle="buttons">
                                    <label class="btn btn-default" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="cooler_night_enabled" type="radio" value="false"> {{_('Disabled')}}</label><label class="btn btn-primary" data-toggle-class="btn-primary" data-toggle-passive-class="btn-default"><input name="cooler_night_enabled" type="radio" value="true"> {{_('Enabled')}}</label>
                                  </div>
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cooler_mode">{{_('Cooler mode')}}</label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_cooler_mode')}}">
                                    <select class="form-control" name="cooler_mode" tabindex="-1" placeholder="{{_('Select an option')}}">
                                      <option value="timer">{{_('Timer')}}</option>
                                      <option value="weather">{{_('Weather')}}</option>
                                      <option value="sensor">{{_('Sensor')}}</option>
                                    </select>
                                  </div>
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cooler_on">{{_('Cooler on')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control col-md-7 col-xs-12" name="cooler_on" required="required" type="text" placeholder="{{_('Cooler on')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_cooler_on')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cooler_off">{{_('Cooler off')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control col-md-7 col-xs-12" name="cooler_off" required="required" type="text" placeholder="{{_('Cooler off')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_cooler_off')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cooler_power_switches">{{_('Power switches')}}</label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_cooler_power_switches')}}">
                                    <select class="form-control" multiple="multiple" name="cooler_power_switches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                    </select>
                                  </div>
                                </div>
                              </div><br /><br />
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
                        <ul>
                          <li>
                            <strong>{{_('Status')}}</strong>: {{translations.get_translation('environment_field_cooler_enable')}}
                          </li>
                          <li>
                            <strong>{{_('Enabled when lights are on')}}</strong>: {{translations.get_translation('environment_field_cooler_enable_during_night')}}
                          </li>
                          <li>
                            <strong>{{_('Heater mode')}}</strong>: {{translations.get_translation('environment_field_cooler_mode')}}
                          </li>
                          <li>
                            <strong>{{_('Heater on')}}</strong>: {{translations.get_translation('environment_field_cooler_on')}}
                          </li>
                          <li>
                            <strong>{{_('Heater off')}}</strong>: {{translations.get_translation('environment_field_cooler_off')}}
                          </li>
                          <li>
                            <strong>{{_('Power switches')}}</strong>: {{translations.get_translation('environment_field_cooler_power_switches')}}
                          </li>
                          <li>
                            <strong>{{_('Temperature sensors')}}</strong>: {{translations.get_translation('environment_field_cooler_temperature_sensors')}}
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                  <div class="col-xs-3">
                    <!-- required for floating -->
                    <!-- Nav tabs -->
                    <ul class="nav nav-tabs tabs-right">
                      <li class="active">
                        <a data-toggle="tab" href="#usage-tab-environment-overview" title="{{_('Overview')}}">{{_('Overview')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-environment-lights" title="{{_('Lights')}}">{{_('Lights')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-environment-sprayer" title="{{_('Sprayer')}}">{{_('Sprayer')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-environment-heater" title="{{_('Heater')}}">{{_('Heater')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-environment-cooler" title="{{_('Cooling')}}">{{_('Cooling')}}</a>
                      </li>
                    </ul>
                  </div>
