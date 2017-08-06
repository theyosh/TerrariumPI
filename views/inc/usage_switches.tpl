                  <div class="col-xs-9">
                    <!-- Tab panes -->
                    <div class="tab-content">
                      <div class="tab-pane active" id="usage-tab-switches-list">
                        <div class="interactive_screenshot">
                          <div id="screenshot_switches_title" class="click_area" title="{{_('Title')}}"></div>
                          <div id="screenshot_switches_toggle" class="click_area" title="{{_('Status and toggle')}}"></div>
                          <div id="screenshot_switches_graph" class="click_area" title="{{_('History graph')}}"></div>
                          <img src="static/images/documentation/switches_status.png" alt="{{_('Switches overview screenshot')}}" />
                        </div>
                      </div>
                      <div class="tab-pane" id="usage-tab-switches-title">
                        <h3 class="lead">{{_('Title')}}</h3>
                        <p>{{_('Per switch the title holds shows some values and options.')}}</p>
                        <div class="x_panel">
                          <div class="x_title">
                            <h2>
                              <span aria-hidden="true" class="glyphicon glyphicon-flash"></span>
                              <span class="title">{{_('Switch')}} '{{_('Name')}}'</span>
                              <small class="data_update">50W, 0.2L/m</small>
                              <small class="total_usage">{{_('Total power in kWh')}}: 0.05, {{_('Total water in L')}}: 0.0002</small>
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
                                    <a href="javascript:;">{{_('Settings')}}</a>
                                  </li>
                                </ul>
                              </li>
                              <li>
                                <a class="close-link" href="javascript:;"><i class="fa fa-close" title="{{_('Close')}}"></i></a>
                              </li>
                            </ul>
                            <div class="clearfix"></div>
                          </div>
                        </div>
                        <h4>{{_('Left side')}} <small>({{_('values')}})</small></h4>
                        <ul>
                          <li>{{_('The configured name')}}</li>
                          <li>{{_('The power usage and/or water flow per minute when switched on')}}</li>
                          <li>{{_('The total amount of power usage and/or water usage for the selected history period')}}</li>
                        </ul>
                        <h4>{{_('Right side')}} <small>({{_('Options')}})</small></h4>
                        <ul>
                          <li><i class="fa fa-chevron-up"></i>: {{_('Show or hide the switch')}}</li>
                          <li><i class="fa fa-calendar" title="{{_('Period')}}"></i>: {{_('Select history graph period')}}</li>
                          <li><i class="fa fa-wrench" title="{{_('Options')}}"></i>: {{_('Options menu')}}</li>
                          <li><i class="fa fa-close" title="{{_('Close')}}"></i>: {{_('Close')}}</li>
                        </ul>
                      </div>
                      <div class="tab-pane" id="usage-tab-switches-toggle">
                        <h3 class="lead">{{_('Status and toggle')}}</h3>
                        <div class="power_switch big alignright" style="margin: 0px;" title="{{_('Switch is off')}}">
                          <span aria-hidden="true" class="glyphicon glyphicon-off blue"></span>
                        </div>
                        <div class="power_switch big alignright" style="margin: 0px;" title="{{_('Switch is on')}}">
                          <span aria-hidden="true" class="glyphicon glyphicon-off green"></span>
                        </div>
                        <p>{{_('On the switch page there are power buttons that toggle the power switches. Every switch will be listed, and can be controlled from the status page. In order to toggle the switch, a request for a username and password is being made. Use here the username and password that are configured at the system configuration page.')}}</p>
                        <p>{{_('The list is also updating when the environment toggles a switch. The state off the switch is shown here in real time.')}}</p>
                        <h4>{{_('Status')}}</h4>
                        <ul>
                          <li><span aria-hidden="true" class="glyphicon glyphicon-off green"></span>: {{_('Switch is on')}}</li>
                          <li><span aria-hidden="true" class="glyphicon glyphicon-off blue"></span>: {{_('Switch is off')}}</li>
                        </ul>
                      </div>
                      <div class="tab-pane" id="usage-tab-switches-graph">
                        <h3 class="lead">{{_('History graph')}}</h3>
                        <img src="static/images/documentation/history_graph_power_switch.png" alt="{{_('Switch history graph')}}" class="img-thumbnail" /><br /><br />
                        <p>{{_('The history graph will shows when a switch was powered on. It will show the power usage on the y-axis and time on the x-axis. When hovering over the graph it will also show the water usage.')}}</p>
                        <p>{{!_('Use the calendar icon %s in the title to select the period for the history graph.') % '<i class="fa fa-calendar"></i>'}}</p>
                      </div>
                      <div class="tab-pane" id="usage-tab-switches-settings">
                        <h3 class="lead">{{_('Settings')}}</h3>
                        <p>{{!_('On the switch settings page you can configure all needed switches. Click on %s button to add a new switch. And empty form like below is shown and has to be filled in. Make sure the right values are filled in. All fields with a %s are required.') % ('<button type="button" class="btn btn-primary"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button>','<span class="required">*</span>',)}}</p>
                        <div class="row">
                          <div class="col-md-12 col-sm-12 col-xs-12">
                            <div class="x_panel">
                              <div class="x_content">
                                <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                                  <label for="switch_[nr]_hardwaretype">{{_('Hardware')}} <span class="required">*</span></label>
                                  <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{!translations.get_translation('switch_field_hardware')}}">
                                    <select class="form-control" name="switch_[nr]_hardwaretype" tabindex="-1" placeholder="{{_('Select an option')}}" required="required">
                                      <option value="ftdi">{{_('FTDI')}}</option>
                                      <option value="gpio">{{_('GPIO')}}</option>
                                    </select>
                                  </div>
                                </div>
                                <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                                  <label for="switch_[nr]_address">{{_('Address')}}</label> <span class="required">*</span>
                                  <input class="form-control" name="switch_[nr]_address" placeholder="{{_('Address')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_address')}}">
                                  <input class="form-control" name="switch_[nr]_id" placeholder="{{_('ID')}}" readonly="readonly" type="hidden">
                                </div>
                                <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                                  <label for="switch_[nr]_name">{{_('Name')}}</label> <span class="required">*</span>
                                  <input class="form-control" name="switch_[nr]_name" placeholder="{{_('Name')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_name')}}">
                                </div>
                                <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                                  <label for="switch_[nr]_power_wattage">{{_('Power usage in Watt')}}</label>
                                  <input class="form-control" name="switch_[nr]_power_wattage" placeholder="{{_('Power usage in Watt')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_power_wattage')}}">
                                </div>
                                <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                                  <label for="switch_[nr]_water_flow">{{_('Water flow in L/m')}}</label>
                                  <input class="form-control" name="switch_[nr]_water_flow" placeholder="{{_('Water flow in L/m')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_water_flow')}}">
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                        <ul>
                          <li>
                            <strong>{{_('Hardware')}}</strong>: {{!translations.get_translation('switch_field_hardware')}}
                          </li>
                          <li>
                            <strong>{{_('Address')}}</strong>: {{!translations.get_translation('switch_field_address')}}
                          </li>
                          <li>
                            <strong>{{_('Name')}}</strong>: {{translations.get_translation('switch_field_name')}}
                          </li>
                          <li>
                            <strong>{{_('Power usage in Watt')}}</strong>: {{translations.get_translation('switch_field_power_wattage')}}
                          </li>
                          <li>
                            <strong>{{_('Water flow in L/m')}}</strong>: {{translations.get_translation('switch_field_water_flow')}}
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
                        <a data-toggle="tab" href="#usage-tab-switches-list" title="{{_('Overview')}}">{{_('Overview')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-switches-title" title="{{_('Title')}}">{{_('Title')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-switches-toggle" title="{{_('Status and toggle')}}">{{_('Status and toggle')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-switches-graph" title="{{_('History graph')}}">{{_('History graph')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-switches-settings" title="{{_('Settings')}}">{{_('Settings')}}</a>
                      </li>
                    </ul>
                  </div>
                  <script type="text/javascript">
                    $("select").select2({
                      placeholder: '{{_('Select an option')}}',
                      allowClear: false,
                      minimumResultsForSearch: Infinity
                    });
                  </script>
