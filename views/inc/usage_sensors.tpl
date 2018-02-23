                  <div class="col-xs-9">
                    <!-- Tab panes -->
                    <div class="tab-content">
                      <div class="tab-pane active" id="usage-tab-sensors-list">
                        <div class="interactive_screenshot">
                          <div id="screenshot_sensors_title" class="click_area" title="{{_('Title')}}"></div>
                          <div id="screenshot_sensors_current" class="click_area" title="{{_('Current value')}}"></div>
                          <div id="screenshot_sensors_graph" class="click_area" title="{{_('History graph')}}"></div>
                          <img src="static/images/documentation/sensors_list.gif" alt="{{_('Sensors overview screenshot')}}" />
                        </div>
                      </div>
                      <div class="tab-pane" id="usage-tab-sensors-graphs">
                        <p>{{_('On the sensors page you can find all the available sensors page grouped by type. Select temperature from the menu to get all the temperature sensors. Select humidity for all humidity sensors.')}}</p>
                        <p>{{_('Per graph you have the following options and indicators.')}}</p>
                      </div>
                      <div class="tab-pane" id="usage-tab-sensors-title">
                        <h3 class="lead">{{_('Title')}}</h3>
                        <p>{{_('Per sensor the title shows some values and options.')}}</p>
                        <div class="x_panel">
                          <div class="x_title">
                            <h2>
                              <span aria-hidden="true" class="glyphicon glyphicon-tint"></span>
                              <span class="title">{{_('Sensor')}} '{{_('Name')}}'</span>
                              <small>...</small>
                              <span class="badge bg-red">{{_('warning')}}</span>
                            </h2>
                            <ul class="nav navbar-right panel_toolbox">
                              <li>
                                <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                              </li>
                              <li class="dropdown">
                                <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-calendar" title="{{_('Period')}}"></i></a>
                                <ul class="dropdown-menu period" role="menu">
                                  <li>
                                    <a href="javascript:;" >{{_('Day')}}</a>
                                  </li>
                                  <li>
                                    <a href="javascript:;" >{{_('Week')}}</a>
                                  </li>
                                  <li>
                                    <a href="javascript:;" >{{_('Month')}}</a>
                                  </li>
                                  <li>
                                    <a href="javascript:;" >{{_('Year')}}</a>
                                  </li>
                                </ul>
                              </li>
                              <li class="dropdown">
                                <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-wrench" title="{{_('Options')}}"></i></a>
                                <ul class="dropdown-menu" role="menu">
                                  <li>
                                    <a href="javascript:;" onclick="menu_click('sensor_settings.html')">{{_('Settings')}}</a>
                                  </li>
                                </ul>
                              </li>
                              <li>
                                <a class="close-link"><i class="fa fa-close" title="{{_('Close')}}"></i></a>
                              </li>
                            </ul>
                            <div class="clearfix"></div>
                          </div>
                        </div>
                        <h4>{{_('Left side')}} <small>({{_('values')}})</small></h4>
                        <ul>
                          <li>{{_('The sensor type')}}
                            <ul>
                              <li><span aria-hidden="true" class="glyphicon glyphicon-tint"></span>: {{_('Humidity sensor')}}</li>
                              <li><span aria-hidden="true" class="glyphicon glyphicon-fire"></span>: {{_('Temperature sensor')}}</li>
                              <li><span aria-hidden="true" class="glyphicon glyphicon-signal"></span>: {{_('Distance sensor')}}</li>
                            </ul>
                          </li>
                          <li>{{_('The configured name')}}</li>
                          <li>{{_('The time stamp of the last measurement.')}}</li>
                          <li>{{_('Warning badge when the sensor value is outside the defined save operating values.')}}</li>
                        </ul>
                        <h4>{{_('Right side')}} <small>({{_('Options')}})</small></h4>
                        <ul>
                          <li><i class="fa fa-chevron-up"></i>: {{_('Show or hide the sensor')}}</li>
                          <li><i class="fa fa-calendar" title="{{_('Period')}}"></i>: {{_('Select history graph period')}}</li>
                          <li><i class="fa fa-wrench" title="{{_('Options')}}"></i>: {{_('Options menu')}}</li>
                          <li><i class="fa fa-close" title="{{_('Close')}}"></i>: {{_('Close')}}</li>
                        </ul>
                      </div>
                      <div class="tab-pane" id="usage-tab-sensors-current">
                        <h3 class="lead">{{_('Current')}}</h3>
                        <div id="currentvalue" class="sidebar-widget text-center alignright">
                          <canvas class="gauge"></canvas>
                          <div class="goal-wrapper">
                            <span class="gauge-value">...</span> <span>C/F / % / cm/inch</span>
                          </div>
                        </div>
                        <p>{{_('The gauge graph shows the current temperature or humidity value. The color of the graph depends on the current value and the alarm values. When the value gets more to the minimum or maximum value, it will gets more red/orange.')}}</p>
                        <p>{{_('The values are updated every 30 seconds and updated in real time on the page.')}}</p>
                        <p>{{_('The current value is also written below the graph in degrees, percentage or distance.')}}</p>
                      </div>
                      <div class="tab-pane" id="usage-tab-sensors-graph">
                        <h3 class="lead">{{_('History graph')}}</h3>
                        <img src="static/images/documentation/history_graph_sensor.png" alt="{{_('Sensor history graph')}}" class="img-thumbnail" /><br /><br />
                        <p>{{_('The history graph will shows the measured value. The flat lines are the minimum and maximum values that are configured. When the measured value is outside this range an alarm will be given. Hover above the graph lines to get detailed information.')}}</p>
                        <p>{{!_('Use the calendar icon %s in the title to select the period for the history graph.') % '<i class="fa fa-calendar"></i>'}}</p>
                      </div>
                      <div class="tab-pane" id="usage-tab-sensors-settings">
                        <h3 class="lead">{{_('Settings')}}</h3>
                        <p>{{!_('On the door settings page you can configure all needed doors. Click on %s button to add a new door. And empty form like below is shown and has to be filled in. Make sure the right values are filled in. All fields with a %s are required.') % ('<button type="button" class="btn btn-primary"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button>','<span class="required">*</span>',)}}</p>
                        <div class="row">
                          <div class="x_panel">
                            <div class="x_content">
                              <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                                <label for="sensor_[nr]_hardwaretype">{{_('Hardware')}} <span class="required">*</span></label>
                                <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{!translations.get_translation('sensor_field_hardware')}}">
                                  <select class="form-control" name="sensor_[nr]_hardwaretype" tabindex="-1" placeholder="{{_('Select an option')}}" required="required">
                                    <option value="owfs">{{_('OWFS')}}</option>
                                    <option value="dht11">{{_('DHT11')}}</option>
                                    <option value="dht22">{{_('DHT22')}}</option>
                                    <option value="am2302">{{_('AM2302')}}</option>
                                    <option value="w1">{{_('1Wire')}}</option>
                                    <option value="remote">{{_('Remote')}}</option>
                                    <option value="hc-sr04">{{_('HC-SR04')}}</option>
                                  </select>
                                </div>
                              </div>
                              <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                                <label for="sensor_[nr]_address">{{_('Address')}}</label> <span class="required">*</span>
                                <input class="form-control" name="sensor_[nr]_address" placeholder="{{_('Address')}}" readonly="readonly"  required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('sensor_field_address')}}">
                                <input class="form-control" name="sensor_[nr]_id" placeholder="{{_('ID')}}" readonly="readonly" type="hidden">
                              </div>
                              <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                                <label for="sensor_[nr]_type">{{_('Type')}} <span class="required">*</span></label>
                                <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{!translations.get_translation('sensor_field_type')}}">
                                  <select class="form-control" name="sensor_[nr]_type" tabindex="-1" placeholder="{{_('Select an option')}}" required="required">
                                    <option value="temperature">{{_('Temperature')}}</option>
                                    <option value="humidity">{{_('Humidity')}}</option>
                                  </select>
                                </div>
                              </div>
                              <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                                <label for="sensor_[nr]_name">{{_('Name')}}</label> <span class="required">*</span>
                                <input class="form-control" name="sensor_[nr]_name" placeholder="{{_('Name')}}" type="text" required="required" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{!translations.get_translation('sensor_field_name')}}">
                              </div>
                              <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                                <label for="sensor_[nr]_alarm_min">{{_('Alarm min')}} <span class="required">*</span></label>
                                <input class="form-control" name="sensor_[nr]_alarm_min" placeholder="{{_('Alarm min')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('sensor_field_alarm_min')}}">
                              </div>
                              <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                                <label for="sensor_[nr]_alarm_max">{{_('Alarm max')}} <span class="required">*</span></label>
                                <input class="form-control" name="sensor_[nr]_alarm_max" placeholder="{{_('Alarm max')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('sensor_field_alarm_max')}}">
                              </div>
                              <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                                <label for="sensor_[nr]_min">{{_('Limit min')}} <span class="required">*</span></label>
                                <input class="form-control" name="sensor_[nr]_limit_min" placeholder="{{_('Limit min')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('sensor_field_limit_min')}}">
                              </div>
                              <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                                <label for="sensor_[nr]_max">{{_('Limit max')}} <span class="required">*</span></label>
                                <input class="form-control" name="sensor_[nr]_limit_max" placeholder="{{_('Limit max')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('sensor_field_limit_max')}}">
                              </div>
                              <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                                <label for="sensor_[nr]_current">{{_('Current')}}</label>
                                <input class="form-control" name="sensor_[nr]_current" placeholder="{{_('Current')}}" readonly="readonly" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('sensor_field_current')}}">
                              </div>
                            </div>
                          </div>
                        </div>
                        <ul>
                          <li>
                            <strong>{{_('Hardware')}}</strong>: {{!translations.get_translation('sensor_field_hardware')}}
                          </li>
                          <li>
                            <strong>{{_('Address')}}</strong>: {{!translations.get_translation('sensor_field_address')}}
                          </li>
                          <li>
                            <strong>{{_('Type')}}</strong>: {{!translations.get_translation('sensor_field_type')}}
                          </li>
                          <li>
                            <strong>{{_('Name')}}</strong>: {{translations.get_translation('sensor_field_name')}}
                          </li>
                          <li>
                            <strong>{{_('Alarm min')}}</strong>: {{translations.get_translation('sensor_field_alarm_min')}}
                          </li>
                          <li>
                            <strong>{{_('Alarm max')}}</strong>: {{translations.get_translation('sensor_field_alarm_max')}}
                          </li>
                          <li>
                            <strong>{{_('Limit min')}}</strong>: {{translations.get_translation('sensor_field_limit_min')}}
                          </li>
                          <li>
                            <strong>{{_('Limit max')}}</strong>: {{translations.get_translation('sensor_field_limit_max')}}
                          </li>
                          <li>
                            <strong>{{_('Current')}}</strong>: {{translations.get_translation('sensor_field_current')}}
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
                        <a data-toggle="tab" href="#usage-tab-sensors-list" title="{{_('Overview')}}">{{_('Overview')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-sensors-title" title="{{_('Title')}}">{{_('Title')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-sensors-current" title="{{_('Current')}}">{{_('Current')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-sensors-graph" title="{{_('History graph')}}">{{_('History graph')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-sensors-settings" title="{{_('Settings')}}">{{_('Settings')}}</a>
                      </li>
                    </ul>
                  </div>
                  <script type="text/javascript">
                    $(function() {
                      var observer = new MutationObserver(function(mutations) {
                        data = {'limit_max': 60,
                                'limit_min': 20,
                                'alarm_max': 45,
                                'alarm_min': 35,
                                'current': 30,
                                'alarm': false };

                        data.current = Math.floor(Math.random() * (data.limit_max - data.limit_min) + data.limit_min);
                        sensor_gauge('currentvalue',data);
                      });

                      var target = document.querySelector('#usage-tab-sensors-current');
                      observer.observe(target, {
                        attributes: true
                      });

                      $('.x_title h2 small').text(moment().format('LLL'));
                      $('.x_title h2 span.glyphicon').removeClass('glyphicon-tint glyphicon-fire')
                                                     .addClass('glyphicon-' + (Math.random() > 0.5 ? 'tint' : 'fire'));
                    });
                  </script>
