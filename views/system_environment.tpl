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
          <div class="row" id="environment_light">
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
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_mode">{{_('Mode')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_mode')}}">
                        <select class="form-control" name="light_mode" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="disabled">{{_('Disabled')}}</option>
                          <option value="timer">{{_('Timer')}}</option>
                          <!-- <option value="sensor">{{_('Sensor')}}</option> -->
                          <option value="weather">{{_('Weather day/night')}}</option>
                          <option value="weatherinverse">{{_('Weather night/day')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_max_hours">{{_('Maximum hours')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="light_max_hours" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Maximum lights hours')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_lights_max_hours')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_min_hours">{{_('Minimum hours')}}</label>
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
                  <div class="accordion" id="light_accordion" role="tablist" aria-multiselectable="true">
                    <div class="panel">
                      <a class="panel-heading" role="tab" id="light_heading_one" data-toggle="collapse" data-parent="#light_accordion" href="#light_collapse_one" aria-expanded="true" aria-controls="light_collapse_one"><h4 class="panel-title">{{_('Day')}}</h4></a>
                      <div id="light_collapse_one" class="panel-collapse collapse" role="tabpanel" aria-labelledby="light_heading_one">
                        <div class="panel-body">
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_alarm_min_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="light_alarm_min_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_alarm_min_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="light_alarm_min_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_alarm_min_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="light_alarm_min_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_alarm_min_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="light_alarm_min_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_alarm_min_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="light_alarm_min_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="panel">
                      <a class="panel-heading collapsed" role="tab" id="light_heading_two" data-toggle="collapse" data-parent="#light_accordion" href="#light_collapse_two" aria-expanded="false" aria-controls="light_collapse_two"><h4 class="panel-title">{{_('Night')}}</h4></a>
                      <div id="light_collapse_two" class="panel-collapse collapse" role="tabpanel" aria-labelledby="light_heading_two">
                        <div class="panel-body">
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_alarm_max_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="light_alarm_max_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_alarm_max_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="light_alarm_max_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_alarm_max_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="light_alarm_max_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_alarm_max_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="light_alarm_max_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="light_alarm_max_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="light_alarm_max_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row" id="environment_temperature">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 class="red"><i class="fa fa-fire"></i> {{_('Temperature')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_mode">{{_('Mode')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_mode')}}">
                        <select class="form-control" name="temperature_mode" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="disabled">{{_('Disabled')}}</option>
                          <option value="timer">{{_('Timer')}}</option>
                          <option value="sensor">{{_('Sensor')}}</option>
                          <option value="weather">{{_('Weather day/night')}}</option>
                          <option value="weatherinverse">{{_('Weather night/day')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_sensors">{{_('Sensors')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sensors')}}">
                        <select class="form-control" multiple="multiple" name="temperature_sensors" tabindex="-1" placeholder="{{_('Select an option')}}">
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_day_night_difference">{{_('Day/night difference')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="temperature_day_night_difference" required="required" type="text" placeholder="{{_('Value difference during the night')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_day_night_difference')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_day_night_source">{{_('Day/night source')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_day_night_source')}}">
                        <select class="form-control" name="temperature_day_night_source" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="weather">{{_('Weather')}}</option>
                          <option value="lights">{{_('Lights')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="accordion" id="temperature_accordion" role="tablist" aria-multiselectable="true">
                    <div class="panel">
                      <a class="panel-heading" role="tab" id="temperature_heading_one" data-toggle="collapse" data-parent="#temperature_accordion" href="#temperature_collapse_one" aria-expanded="true" aria-controls="temperature_collapse_one"><h4 class="panel-title">Low alarm</h4></a>
                      <div id="temperature_collapse_one" class="panel-collapse collapse" role="tabpanel" aria-labelledby="temperature_heading_one">
                        <div class="panel-body">

                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_min_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="temperature_alarm_min_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_min_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="temperature_alarm_min_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_min_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="temperature_alarm_min_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_min_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="temperature_alarm_min_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_min_light_state">{{_('Light state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_light_state')}}">
                                <select class="form-control" name="temperature_alarm_min_light_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="on">{{_('On')}}</option>
                                  <option value="off">{{_('Off')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_min_door_state">{{_('Door state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_door_state')}}">
                                <select class="form-control" name="temperature_alarm_min_door_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="open">{{_('Open')}}</option>
                                  <option value="closed">{{_('Closed')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_min_duration_on">{{_('Power on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="temperature_alarm_min_duration_on" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_min_settle">{{_('Settle timeout')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="temperature_alarm_min_settle" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_delay')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_min_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="temperature_alarm_min_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="panel">
                      <a class="panel-heading collapsed" role="tab" id="temperature_heading_two" data-toggle="collapse" data-parent="#temperature_accordion" href="#temperature_collapse_two" aria-expanded="false" aria-controls="temperature_collapse_two"><h4 class="panel-title">High alarm</h4></a>
                      <div id="temperature_collapse_two" class="panel-collapse collapse" role="tabpanel" aria-labelledby="temperature_heading_two">
                        <div class="panel-body">
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_max_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="temperature_alarm_max_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_max_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="temperature_alarm_max_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_max_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="temperature_alarm_max_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_max_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="temperature_alarm_max_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_max_light_state">{{_('Light state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_light_state')}}">
                                <select class="form-control" name="temperature_alarm_max_light_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="on">{{_('On')}}</option>
                                  <option value="off">{{_('Off')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_max_door_state">{{_('Door state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_door_state')}}">
                                <select class="form-control" name="temperature_alarm_max_door_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="open">{{_('Open')}}</option>
                                  <option value="closed">{{_('Closed')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_max_duration_on">{{_('Power on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="temperature_alarm_max_duration_on" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_max_settle">{{_('Settle timeout')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="temperature_alarm_max_settle" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_delay')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_alarm_max_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="temperature_alarm_max_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row" id="environment_humidity">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 class="blue"><i class="fa fa-tint"></i> {{_('Humidity')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_mode">{{_('Mode')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_mode')}}">
                        <select class="form-control" name="humidity_mode" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="disabled">{{_('Disabled')}}</option>
                          <option value="timer">{{_('Timer')}}</option>
                          <option value="sensor">{{_('Sensor')}}</option>
                          <option value="weather">{{_('Weather day/night')}}</option>
                          <option value="weatherinverse">{{_('Weather night/day')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_sensors">{{_('Sensors')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sensors')}}">
                        <select class="form-control" multiple="multiple" name="humidity_sensors" tabindex="-1" placeholder="{{_('Select an option')}}">
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_day_night_difference">{{_('Day/night difference')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="humidity_day_night_difference" required="required" type="text" placeholder="{{_('Value difference during the night')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_day_night_difference')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_day_night_source">{{_('Day/night source')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_day_night_source')}}">
                        <select class="form-control" name="humidity_day_night_source" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="weather">{{_('Weather')}}</option>
                          <option value="lights">{{_('Lights')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="accordion" id="humidity_accordion" role="tablist" aria-multiselectable="true">
                    <div class="panel">
                      <a class="panel-heading" role="tab" id="humidity_heading_one" data-toggle="collapse" data-parent="#humidity_accordion" href="#humidity_collapse_one" aria-expanded="true" aria-controls="humidity_collapse_one"><h4 class="panel-title">Low alarm</h4></a>
                      <div id="humidity_collapse_one" class="panel-collapse collapse" role="tabpanel" aria-labelledby="humidity_heading_one">
                        <div class="panel-body">
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_min_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="humidity_alarm_min_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_min_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="humidity_alarm_min_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_min_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="humidity_alarm_min_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_min_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="humidity_alarm_min_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_min_light_state">{{_('Light state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_light_state')}}">
                                <select class="form-control" name="humidity_alarm_min_light_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="on">{{_('On')}}</option>
                                  <option value="off">{{_('Off')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_min_door_state">{{_('Door state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_door_state')}}">
                                <select class="form-control" name="humidity_alarm_min_door_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="open">{{_('Open')}}</option>
                                  <option value="closed">{{_('Closed')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_min_duration_on">{{_('Power on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="humidity_alarm_min_duration_on" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_min_settle">{{_('Settle timeout')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="humidity_alarm_min_settle" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_delay')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_min_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="humidity_alarm_min_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="panel">
                      <a class="panel-heading collapsed" role="tab" id="humidity_heading_two" data-toggle="collapse" data-parent="#humidity_accordion" href="#humidity_collapse_two" aria-expanded="false" aria-controls="humidity_collapse_two"><h4 class="panel-title">High alarm</h4></a>
                      <div id="humidity_collapse_two" class="panel-collapse collapse" role="tabpanel" aria-labelledby="humidity_heading_two">
                        <div class="panel-body">
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_max_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="humidity_alarm_max_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_max_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="humidity_alarm_max_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_max_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="humidity_alarm_max_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_max_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="humidity_alarm_max_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_max_light_state">{{_('Light state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_light_state')}}">
                                <select class="form-control" name="humidity_alarm_max_light_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="on">{{_('On')}}</option>
                                  <option value="off">{{_('Off')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_max_door_state">{{_('Door state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_door_state')}}">
                                <select class="form-control" name="humidity_alarm_max_door_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="open">{{_('Open')}}</option>
                                  <option value="closed">{{_('Closed')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_max_duration_on">{{_('Power on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="humidity_alarm_max_duration_on" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_max_settle">{{_('Settle timeout')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="humidity_alarm_max_settle" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_delay')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="humidity_alarm_max_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="humidity_alarm_max_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row" id="environment_moisture">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 class="blue"><i class="fa fa-tint"></i> {{_('Moisture')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_mode">{{_('Mode')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_mode')}}">
                        <select class="form-control" name="moisture_mode" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="disabled">{{_('Disabled')}}</option>
                          <option value="timer">{{_('Timer')}}</option>
                          <option value="sensor">{{_('Sensor')}}</option>
                          <option value="weather">{{_('Weather day/night')}}</option>
                          <option value="weatherinverse">{{_('Weather night/day')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_sensors">{{_('Sensors')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sensors')}}">
                        <select class="form-control" multiple="multiple" name="moisture_sensors" tabindex="-1" placeholder="{{_('Select an option')}}">
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_day_night_difference">{{_('Day/night difference')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="moisture_day_night_difference" required="required" type="text" placeholder="{{_('Value difference during the night')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_day_night_difference')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_day_night_source">{{_('Day/night source')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_day_night_source')}}">
                        <select class="form-control" name="moisture_day_night_source" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="weather">{{_('Weather')}}</option>
                          <option value="lights">{{_('Lights')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="accordion" id="moisture_accordion" role="tablist" aria-multiselectable="true">
                    <div class="panel">
                      <a class="panel-heading" role="tab" id="moisture_heading_one" data-toggle="collapse" data-parent="#moisture_accordion" href="#moisture_collapse_one" aria-expanded="true" aria-controls="moisture_collapse_one"><h4 class="panel-title">Low alarm</h4></a>
                      <div id="moisture_collapse_one" class="panel-collapse collapse" role="tabpanel" aria-labelledby="moisture_heading_one">
                        <div class="panel-body">
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_min_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="moisture_alarm_min_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_min_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="moisture_alarm_min_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_min_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="moisture_alarm_min_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_min_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="moisture_alarm_min_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_min_light_state">{{_('Light state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_light_state')}}">
                                <select class="form-control" name="moisture_alarm_min_light_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="on">{{_('On')}}</option>
                                  <option value="off">{{_('Off')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_min_door_state">{{_('Door state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_door_state')}}">
                                <select class="form-control" name="moisture_alarm_min_door_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="open">{{_('Open')}}</option>
                                  <option value="closed">{{_('Closed')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_min_duration_on">{{_('Power on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="moisture_alarm_min_duration_on" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_min_settle">{{_('Settle timeout')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="moisture_alarm_min_settle" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_delay')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_min_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="moisture_alarm_min_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="panel">
                      <a class="panel-heading collapsed" role="tab" id="moisture_heading_two" data-toggle="collapse" data-parent="#moisture_accordion" href="#moisture_collapse_two" aria-expanded="false" aria-controls="moisture_collapse_two"><h4 class="panel-title">High alarm</h4></a>
                      <div id="moisture_collapse_two" class="panel-collapse collapse" role="tabpanel" aria-labelledby="moisture_heading_two">
                        <div class="panel-body">
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_max_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="moisture_alarm_max_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_max_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="moisture_alarm_max_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_max_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="moisture_alarm_max_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_max_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="moisture_alarm_max_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_max_light_state">{{_('Light state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_light_state')}}">
                                <select class="form-control" name="moisture_alarm_max_light_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="on">{{_('On')}}</option>
                                  <option value="off">{{_('Off')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_max_door_state">{{_('Door state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_door_state')}}">
                                <select class="form-control" name="moisture_alarm_max_door_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="open">{{_('Open')}}</option>
                                  <option value="closed">{{_('Closed')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_max_duration_on">{{_('Power on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="moisture_alarm_max_duration_on" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_max_settle">{{_('Settle timeout')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="moisture_alarm_max_settle" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_delay')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="moisture_alarm_max_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="moisture_alarm_max_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row" id="environment_conductivity">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 class="orange"><i class="fa fa-flash"></i> {{_('Conductivity')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_mode">{{_('Mode')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_mode')}}">
                        <select class="form-control" name="conductivity_mode" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="disabled">{{_('Disabled')}}</option>
                          <option value="timer">{{_('Timer')}}</option>
                          <option value="sensor">{{_('Sensor')}}</option>
                          <option value="weather">{{_('Weather day/night')}}</option>
                          <option value="weatherinverse">{{_('Weather night/day')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_sensors">{{_('Sensors')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sensors')}}">
                        <select class="form-control" multiple="multiple" name="conductivity_sensors" tabindex="-1" placeholder="{{_('Select an option')}}">
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_day_night_difference">{{_('Day/night difference')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="conductivity_day_night_difference" required="required" type="text" placeholder="{{_('Value difference during the night')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_day_night_difference')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_day_night_source">{{_('Day/night source')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_day_night_source')}}">
                        <select class="form-control" name="conductivity_day_night_source" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="weather">{{_('Weather')}}</option>
                          <option value="lights">{{_('Lights')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="accordion" id="conductivity_accordion" role="tablist" aria-multiselectable="true">
                    <div class="panel">
                      <a class="panel-heading" role="tab" id="conductivity_heading_one" data-toggle="collapse" data-parent="#conductivity_accordion" href="#conductivity_collapse_one" aria-expanded="true" aria-controls="conductivity_collapse_one"><h4 class="panel-title">Low alarm</h4></a>
                      <div id="conductivity_collapse_one" class="panel-collapse collapse" role="tabpanel" aria-labelledby="conductivity_heading_one">
                        <div class="panel-body">
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_min_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="conductivity_alarm_min_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_min_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="conductivity_alarm_min_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_min_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="conductivity_alarm_min_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_min_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="conductivity_alarm_min_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_min_light_state">{{_('Light state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_light_state')}}">
                                <select class="form-control" name="conductivity_alarm_min_light_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="on">{{_('On')}}</option>
                                  <option value="off">{{_('Off')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_min_door_state">{{_('Door state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_door_state')}}">
                                <select class="form-control" name="conductivity_alarm_min_door_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="open">{{_('Open')}}</option>
                                  <option value="closed">{{_('Closed')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_min_duration_on">{{_('Power on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="conductivity_alarm_min_duration_on" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_min_settle">{{_('Settle timeout')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="conductivity_alarm_min_settle" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_delay')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_min_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="conductivity_alarm_min_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="panel">
                      <a class="panel-heading collapsed" role="tab" id="conductivity_heading_two" data-toggle="collapse" data-parent="#conductivity_accordion" href="#conductivity_collapse_two" aria-expanded="false" aria-controls="conductivity_collapse_two"><h4 class="panel-title">High alarm</h4></a>
                      <div id="conductivity_collapse_two" class="panel-collapse collapse" role="tabpanel" aria-labelledby="conductivity_heading_two">
                        <div class="panel-body">
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_max_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="conductivity_alarm_max_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_max_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="conductivity_alarm_max_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_max_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="conductivity_alarm_max_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_max_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="conductivity_alarm_max_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_max_light_state">{{_('Light state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_light_state')}}">
                                <select class="form-control" name="conductivity_alarm_max_light_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="on">{{_('On')}}</option>
                                  <option value="off">{{_('Off')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_max_door_state">{{_('Door state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_door_state')}}">
                                <select class="form-control" name="conductivity_alarm_max_door_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="open">{{_('Open')}}</option>
                                  <option value="closed">{{_('Closed')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_max_duration_on">{{_('Power on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="conductivity_alarm_max_duration_on" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_max_settle">{{_('Settle timeout')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="conductivity_alarm_max_settle" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_delay')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="conductivity_alarm_max_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="conductivity_alarm_max_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row" id="environment_ph">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 class="green"><i class="fa fa-tachometer"></i> {{_('pH')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_mode">{{_('Mode')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_mode')}}">
                        <select class="form-control" name="ph_mode" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="disabled">{{_('Disabled')}}</option>
                          <option value="timer">{{_('Timer')}}</option>
                          <option value="sensor">{{_('Sensor')}}</option>
                          <option value="weather">{{_('Weather day/night')}}</option>
                          <option value="weatherinverse">{{_('Weather night/day')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_sensors">{{_('Sensors')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sensors')}}">
                        <select class="form-control" multiple="multiple" name="ph_sensors" tabindex="-1" placeholder="{{_('Select an option')}}">
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_day_night_difference">{{_('Day/night difference')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="ph_day_night_difference" required="required" type="text" placeholder="{{_('Value difference during the night')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_day_night_difference')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_day_night_source">{{_('Day/night source')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_day_night_source')}}">
                        <select class="form-control" name="ph_day_night_source" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="weather">{{_('Weather')}}</option>
                          <option value="lights">{{_('Lights')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="accordion" id="ph_accordion" role="tablist" aria-multiselectable="true">
                    <div class="panel">
                      <a class="panel-heading" role="tab" id="ph_heading_one" data-toggle="collapse" data-parent="#ph_accordion" href="#ph_collapse_one" aria-expanded="true" aria-controls="ph_collapse_one"><h4 class="panel-title">Low alarm</h4></a>
                      <div id="ph_collapse_one" class="panel-collapse collapse" role="tabpanel" aria-labelledby="ph_heading_one">
                        <div class="panel-body">
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_min_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="ph_alarm_min_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_min_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="ph_alarm_min_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_min_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="ph_alarm_min_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_min_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="ph_alarm_min_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_min_light_state">{{_('Light state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_light_state')}}">
                                <select class="form-control" name="ph_alarm_min_light_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="on">{{_('On')}}</option>
                                  <option value="off">{{_('Off')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_min_door_state">{{_('Door state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_door_state')}}">
                                <select class="form-control" name="ph_alarm_min_door_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="open">{{_('Open')}}</option>
                                  <option value="closed">{{_('Closed')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_min_duration_on">{{_('Power on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="ph_alarm_min_duration_on" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_min_settle">{{_('Settle timeout')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="ph_alarm_min_settle" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_delay')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_min_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="ph_alarm_min_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="panel">
                      <a class="panel-heading collapsed" role="tab" id="ph_heading_two" data-toggle="collapse" data-parent="#ph_accordion" href="#ph_collapse_two" aria-expanded="false" aria-controls="ph_collapse_two"><h4 class="panel-title">High alarm</h4></a>
                      <div id="ph_collapse_two" class="panel-collapse collapse" role="tabpanel" aria-labelledby="ph_heading_two">
                        <div class="panel-body">
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_max_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="ph_alarm_max_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_max_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="ph_alarm_max_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_max_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="ph_alarm_max_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_max_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="ph_alarm_max_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_max_light_state">{{_('Light state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_light_state')}}">
                                <select class="form-control" name="ph_alarm_max_light_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="on">{{_('On')}}</option>
                                  <option value="off">{{_('Off')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_max_door_state">{{_('Door state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_door_state')}}">
                                <select class="form-control" name="ph_alarm_max_door_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="open">{{_('Open')}}</option>
                                  <option value="closed">{{_('Closed')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_max_duration_on">{{_('Power on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="ph_alarm_max_duration_on" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_max_settle">{{_('Settle timeout')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="ph_alarm_max_settle" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_delay')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="ph_alarm_max_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="ph_alarm_max_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row" id="environment_watertank">
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
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_mode">{{_('Mode')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_mode')}}">
                        <select class="form-control" name="watertank_mode" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="disabled">{{_('Disabled')}}</option>
                          <option value="timer">{{_('Timer')}}</option>
                          <option value="sensor">{{_('Sensor')}}</option>
                          <option value="weather">{{_('Weather day/night')}}</option>
                          <option value="weatherinverse">{{_('Weather night/day')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_sensors">{{_('Sensors')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sensors')}}">
                        <select class="form-control" multiple="multiple" name="watertank_sensors" tabindex="-1" placeholder="{{_('Select an option')}}">
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_volume">{{_('Volume')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="watertank_volume" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Volume in liters')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_watertank_volume')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_height">{{_('Height')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="watertank_height" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Height in cm')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_watertank_height')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_offset">{{_('Offset')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="watertank_offset" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Offset in cm')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_watertank_offset')}}">
                    </div>
                  </div>
                  <div class="accordion" id="watertank_accordion" role="tablist" aria-multiselectable="true">
                    <div class="panel">
                      <a class="panel-heading" role="tab" id="watertank_heading_one" data-toggle="collapse" data-parent="#watertank_accordion" href="#watertank_collapse_one" aria-expanded="true" aria-controls="watertank_collapse_one"><h4 class="panel-title">Low alarm</h4></a>
                      <div id="watertank_collapse_one" class="panel-collapse collapse" role="tabpanel" aria-labelledby="watertank_heading_one">
                        <div class="panel-body">
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_alarm_min_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="watertank_alarm_min_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_alarm_min_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="watertank_alarm_min_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_alarm_min_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="watertank_alarm_min_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_alarm_min_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="watertank_alarm_min_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_alarm_min_duration_on">{{_('Power on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="watertank_alarm_min_duration_on" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_alarm_min_settle">{{_('Settle timeout')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="watertank_alarm_min_settle" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_delay')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_alarm_min_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="watertank_alarm_min_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="panel">
                      <a class="panel-heading collapsed" role="tab" id="watertank_heading_two" data-toggle="collapse" data-parent="#watertank_accordion" href="#watertank_collapse_two" aria-expanded="false" aria-controls="watertank_collapse_two"><h4 class="panel-title">High alarm</h4></a>
                      <div id="watertank_collapse_two" class="panel-collapse collapse" role="tabpanel" aria-labelledby="watertank_heading_two">
                        <div class="panel-body">
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_alarm_max_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="watertank_alarm_max_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_alarm_max_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="watertank_alarm_max_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_alarm_max_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="watertank_alarm_max_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_alarm_max_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="watertank_alarm_max_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_alarm_max_duration_on">{{_('Power on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="watertank_alarm_max_duration_on" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_alarm_max_settle">{{_('Settle timeout')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="watertank_alarm_max_settle" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_delay')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="watertank_alarm_max_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="watertank_alarm_max_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row" id="environment_fertility">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 class="green"><i class="fa fa-pagelines"></i> {{_('Fertility')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_mode">{{_('Mode')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_mode')}}">
                        <select class="form-control" name="fertility_mode" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="disabled">{{_('Disabled')}}</option>
                          <option value="timer">{{_('Timer')}}</option>
                          <option value="sensor">{{_('Sensor')}}</option>
                          <option value="weather">{{_('Weather day/night')}}</option>
                          <option value="weatherinverse">{{_('Weather night/day')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_sensors">{{_('Sensors')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sensors')}}">
                        <select class="form-control" multiple="multiple" name="fertility_sensors" tabindex="-1" placeholder="{{_('Select an option')}}">
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_day_night_difference">{{_('Day/night difference')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="fertility_day_night_difference" required="required" type="text" placeholder="{{_('Value difference during the night')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_day_night_difference')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_day_night_source">{{_('Day/night source')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_day_night_source')}}">
                        <select class="form-control" name="fertility_day_night_source" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="weather">{{_('Weather')}}</option>
                          <option value="lights">{{_('Lights')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="accordion" id="fertility_accordion" role="tablist" aria-multiselectable="true">
                    <div class="panel">
                      <a class="panel-heading" role="tab" id="fertility_heading_one" data-toggle="collapse" data-parent="#fertility_accordion" href="#fertility_collapse_one" aria-expanded="true" aria-controls="fertility_collapse_one"><h4 class="panel-title">Low alarm</h4></a>
                      <div id="fertility_collapse_one" class="panel-collapse collapse" role="tabpanel" aria-labelledby="fertility_heading_one">
                        <div class="panel-body">
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_min_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="fertility_alarm_min_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_min_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="fertility_alarm_min_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_min_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="fertility_alarm_min_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_min_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="fertility_alarm_min_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_min_light_state">{{_('Light state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_light_state')}}">
                                <select class="form-control" name="fertility_alarm_min_light_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="on">{{_('On')}}</option>
                                  <option value="off">{{_('Off')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_min_door_state">{{_('Door state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_door_state')}}">
                                <select class="form-control" name="fertility_alarm_min_door_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="open">{{_('Open')}}</option>
                                  <option value="closed">{{_('Closed')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_min_duration_on">{{_('Power on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="fertility_alarm_min_duration_on" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_min_settle">{{_('Settle timeout')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="fertility_alarm_min_settle" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_delay')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_min_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="fertility_alarm_min_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="panel">
                      <a class="panel-heading collapsed" role="tab" id="fertility_heading_two" data-toggle="collapse" data-parent="#fertility_accordion" href="#fertility_collapse_two" aria-expanded="false" aria-controls="fertility_collapse_two"><h4 class="panel-title">High alarm</h4></a>
                      <div id="fertility_collapse_two" class="panel-collapse collapse" role="tabpanel" aria-labelledby="fertility_heading_two">
                        <div class="panel-body">
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_max_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="fertility_alarm_max_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_max_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="fertility_alarm_max_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_max_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="fertility_alarm_max_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_max_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="fertility_alarm_max_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_max_light_state">{{_('Light state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_light_state')}}">
                                <select class="form-control" name="fertility_alarm_max_light_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="on">{{_('On')}}</option>
                                  <option value="off">{{_('Off')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_max_door_state">{{_('Door state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_door_state')}}">
                                <select class="form-control" name="fertility_alarm_max_door_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="open">{{_('Open')}}</option>
                                  <option value="closed">{{_('Closed')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_max_duration_on">{{_('Power on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="fertility_alarm_max_duration_on" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_max_settle">{{_('Settle timeout')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="fertility_alarm_max_settle" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_delay')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="fertility_alarm_max_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="fertility_alarm_max_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row" id="environment_co2">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 class="green"><i class="fa fa-tree"></i> {{_('CO2')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_mode">{{_('Mode')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_mode')}}">
                        <select class="form-control" name="co2_mode" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="disabled">{{_('Disabled')}}</option>
                          <option value="timer">{{_('Timer')}}</option>
                          <option value="sensor">{{_('Sensor')}}</option>
                          <option value="weather">{{_('Weather day/night')}}</option>
                          <option value="weatherinverse">{{_('Weather night/day')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_sensors">{{_('Sensors')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_sensors')}}">
                        <select class="form-control" multiple="multiple" name="co2_sensors" tabindex="-1" placeholder="{{_('Select an option')}}">
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_day_night_difference">{{_('Day/night difference')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control col-md-7 col-xs-12" name="co2_day_night_difference" required="required" type="text" placeholder="{{_('Value difference during the night')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_day_night_difference')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_day_night_source">{{_('Day/night source')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_day_night_source')}}">
                        <select class="form-control" name="co2_day_night_source" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="weather">{{_('Weather')}}</option>
                          <option value="lights">{{_('Lights')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="accordion" id="co2_accordion" role="tablist" aria-multiselectable="true">
                    <div class="panel">
                      <a class="panel-heading" role="tab" id="co2_heading_one" data-toggle="collapse" data-parent="#co2_accordion" href="#co2_collapse_one" aria-expanded="true" aria-controls="co2_collapse_one"><h4 class="panel-title">Low alarm</h4></a>
                      <div id="co2_collapse_one" class="panel-collapse collapse" role="tabpanel" aria-labelledby="co2_heading_one">
                        <div class="panel-body">
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_min_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="co2_alarm_min_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_min_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="co2_alarm_min_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_min_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="co2_alarm_min_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_min_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="co2_alarm_min_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_min_light_state">{{_('Light state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_light_state')}}">
                                <select class="form-control" name="co2_alarm_min_light_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="on">{{_('On')}}</option>
                                  <option value="off">{{_('Off')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_min_door_state">{{_('Door state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_door_state')}}">
                                <select class="form-control" name="co2_alarm_min_door_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="open">{{_('Open')}}</option>
                                  <option value="closed">{{_('Closed')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_min_duration_on">{{_('Power on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="co2_alarm_min_duration_on" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_min_settle">{{_('Settle timeout')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="co2_alarm_min_settle" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_delay')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_min_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="co2_alarm_min_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="panel">
                      <a class="panel-heading collapsed" role="tab" id="co2_heading_two" data-toggle="collapse" data-parent="#co2_accordion" href="#co2_collapse_two" aria-expanded="false" aria-controls="co2_collapse_two"><h4 class="panel-title">High alarm</h4></a>
                      <div id="co2_collapse_two" class="panel-collapse collapse" role="tabpanel" aria-labelledby="co2_heading_two">
                        <div class="panel-body">
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_max_timer_start">{{_('Start')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="co2_alarm_max_timer_start" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_start')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_max_timer_stop">{{_('Stop')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="co2_alarm_max_timer_stop" required="required" type="text" placeholder="{{_('Timestamp')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_stop')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_max_timer_on">{{_('Timer on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="co2_alarm_max_timer_on" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_max_timer_off">{{_('Timer off')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="co2_alarm_max_timer_off" required="required" type="text" placeholder="{{_('Duration in minutes')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_off_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_max_light_state">{{_('Light state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_light_state')}}">
                                <select class="form-control" name="co2_alarm_max_light_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="on">{{_('On')}}</option>
                                  <option value="off">{{_('Off')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_max_door_state">{{_('Door state')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_door_state')}}">
                                <select class="form-control" name="co2_alarm_max_door_state" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                                  <option value="open">{{_('Open')}}</option>
                                  <option value="closed">{{_('Closed')}}</option>
                                  <option value="ignore">{{_('Ignore')}}</option>
                                </select>
                              </div>
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_max_duration_on">{{_('Power on')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="co2_alarm_max_duration_on" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_on_duration')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_max_settle">{{_('Settle timeout')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <input class="form-control col-md-7 col-xs-12" name="co2_alarm_max_settle" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Duration in seconds')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_delay')}}">
                            </div>
                          </div>
                          <div class="form-group">
                            <label class="control-label col-md-3 col-sm-3 col-xs-12" for="co2_alarm_max_powerswitches">{{_('Power switches')}}</label>
                            <div class="col-md-7 col-sm-6 col-xs-10">
                              <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('environment_field_power_switches')}}">
                                <select class="form-control" multiple="multiple" name="co2_alarm_max_powerswitches" tabindex="-1" placeholder="{{_('Select an option')}}">
                                </select>
                              </div>
                            </div>
                          </div>
                        </div>
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
          var sensors_loaded = false;

          $(document).ready(function() {
            init_form_settings('environment');

            $('select[name$="_source"],select[name$="_state"]').select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            });

            $('select[name$="_mode"]').select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            }).on('change',function() {
              var part = this.name.replace('_mode','');
              var environment_part = $('div#environment_' + part);
              var value = this.value;
              environment_part.find('input,select').removeAttr('readonly','disabled');

              switch (value) {
                case 'disabled':
                  environment_part.find('input,select:not(:first)').attr('readonly','readonly');
                  break;

                case 'timer':
                  environment_part.find('input[name*="_max_hours"]').attr('readonly','readonly');
                  environment_part.find('input[name*="_min_hours"]').attr('readonly','readonly');
                  environment_part.find('input[name*="_hours_shift"]').attr('readonly','readonly');
                  break;

                case 'weather':
                case 'weatherinverse':
                  // Load current sun rise and sun set based on weather data
                  $.get('/api/weather',function(data){
                    if ('weatherinverse' == value) {
                      environment_part.find('input[name*="_timer_start"]').val(moment(data.sun.set * 1000).format('LT'));
                      environment_part.find('input[name*="_timer_stop"]').val(moment(data.sun.rise * 1000).format('LT'));
                    } else {
                      environment_part.find('input[name*="_timer_start"]').val(moment(data.sun.rise * 1000).format('LT'));
                      environment_part.find('input[name*="_timer_stop"]').val(moment(data.sun.set * 1000).format('LT'));
                    }
                    if (part == 'light') {
                      // Set the Night lights to opposite of day lights
                      environment_part.find('input[name*="_alarm_max_timer_start"]').val(environment_part.find('input[name*="_alarm_min_timer_stop"]').val());
                      environment_part.find('input[name*="_alarm_max_timer_stop"]').val(environment_part.find('input[name*="_alarm_min_timer_start"]').val());
                    }
                  });

                case 'sensor':
                  environment_part.find('input[name*="_timer_start"]').attr('readonly','readonly');
                  environment_part.find('input[name*="_timer_stop"]').attr('readonly','readonly');
                  environment_part.find('input[name*="_timer_on"]').attr('readonly','readonly');
                  environment_part.find('input[name*="_timer_off"]').attr('readonly','readonly');
                  break;
              }
            }).val('disabled').trigger('change');

            $('select[name*="_powerswitches"],select[name$="_sensors"]').select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            });

            $.get('/api/switches',function(data){
              var select_boxes = $('select[name*="_powerswitches"]');
              select_boxes.on('change',function(evt) {
                // No powerswitches selected, so no required timer fields
                if ('' == this.value) {
                  $('[name^="' + this.name.replace('_powerswitches','_') + '"]').removeAttr('required').attr('readonly','readonly');
                } else {
                  $('[name^="' + this.name.replace('_powerswitches','_') + '"]').removeAttr('readonly','disabled').attr('required','required');
                }
                $('.form-group span.required').remove();
                $('.form-group:has([required="required"]) > label').append('<span class="required"> *</span>');
              });

              $.each(data.switches,function (index,powerswitch){
                if (!powerswitch.timer_enabled) {
                  // We can't use timer enabled switches. They have there own schedule
                  select_boxes.append($('<option>').attr({'value':powerswitch.id}).text(powerswitch.name));
                }
              });
              switches_loaded = true;
            });

            $.get('/api/sensors',function(data){
              $.each(data.sensors,function (index,sensor){
                $('select[name="' + sensor.type + '_sensors"]').append($('<option>').attr({'value':sensor.id}).text(sensor.name));
                if ('distance' == sensor.type || 'volume' == sensor.type) {
                  $('select[name="watertank_sensors"]').append($('<option>').attr({'value':sensor.id}).text(sensor.name));
                }
              });
              sensors_loaded = true;
            });
            load_environment_settings();
          });

          function load_environment_settings() {
            // Wait with loading the environment settings until all selectors are loaded
            if (switches_loaded && sensors_loaded) {
              $.get('/api/config/environment',function(data){
                $.each(data,function (environmentpart,environmentdata){
                  $.each(flatten(environmentdata),function(name,value) {
                    var config_field = $('form [name="' + environmentpart + '_' + name + '"]');
                    if (config_field.length >= 1) {
                      if (name.match(/timer_(start|stop)$/)) {
                        // Load 24H format to local format
                        if (!moment(value,'HH:mm').isValid()) {
                          value = '00:00';
                        }
                        value = moment(value,'HH:mm').format('LT');
                      }
                      switch (config_field.prop('type').toLowerCase()) {
                        case 'text':
                          config_field.val(value);
                          break;
                        case 'select-one':
                        case 'select-multiple':
                          config_field.val(value).trigger('change');
                          break;
                      }
                    }
                  });
                  if ('disabled' == environmentdata.mode) {
                    // Move and hide disabled parts...
                    $('div.row#environment_' + environmentpart).detach().insertBefore('div.row.submit');
                    $('div.row#environment_' + environmentpart + ' a.collapse-link').click();
                  }
                });
                // Make sure all triggers are fired...
                $('select[name$=_mode]').trigger('change');
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
