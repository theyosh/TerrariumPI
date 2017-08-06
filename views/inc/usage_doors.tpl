                  <div class="col-xs-9">
                    <!-- Tab panes -->
                    <div class="tab-content">
                      <div class="tab-pane active" id="usage-tab-doors-list">
                        <div class="interactive_screenshot">
                          <div id="screenshot_doors_title" class="click_area" title="{{_('Title')}}"></div>
                          <div id="screenshot_doors_status" class="click_area" title="{{_('Status')}}"></div>
                          <div id="screenshot_doors_graph" class="click_area" title="{{_('History graph')}}"></div>
                          <img src="static/images/documentation/doors_status.png" alt="{{_('Doors overview screenshot')}}" />
                        </div>
                      </div>
                      <div class="tab-pane" id="usage-tab-doors-title">
                        <h3 class="lead">{{_('Title')}}</h3>
                        <p>{{_('Per door the title holds shows some values and options.')}}</p>
                        <div class="x_panel">
                          <div class="x_title">
                            <h2>
                              <span aria-hidden="true" class="glyphicon glyphicon-lock"></span>
                              <span class="title">{{_('Door')}} '{{_('Name')}}'</span>
                              <small class="total_usage">...</small>
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
                          <li>{{_('The total time the door has been open')}}</li>
                          <li>{{_('Warning badge when the door is open')}}</li>
                        </ul>
                        <h4>{{_('Right side')}} <small>({{_('Options')}})</small></h4>
                        <ul>
                          <li><i class="fa fa-chevron-up"></i>: {{_('Show or hide the door')}}</li>
                          <li><i class="fa fa-calendar" title="{{_('Period')}}"></i>: {{_('Select history graph period')}}</li>
                          <li><i class="fa fa-wrench" title="{{_('Options')}}"></i>: {{_('Options menu')}}</li>
                          <li><i class="fa fa-close" title="{{_('Close')}}"></i>: {{_('Close')}}</li>
                        </ul>
                      </div>
                      <div class="tab-pane" id="usage-tab-doors-status">
                        <h3 class="lead">{{_('Status')}}</h3>
                        <i class="fa fa-lock big red alignright" title="{{_('Door is open')}}"></i>
                        <i class="fa fa-lock big green alignright" title="{{_('Door is closed')}}"></i>
                        <p>{{_('On the door page there is a list of door sensors that show the current status of the doors. There can be as much doors added to the system as needed.')}}</p>
                        <p>{{_('The list is also updating when a door is opened by hand. The state off the door is shown here in real time.')}}</p>
                        <h4>{{_('Status')}}</h4>
                        <ul>
                          <li><i class="fa fa-lock red"></i>: {{_('Door is open')}}</li>
                          <li><i class="fa fa-lock green"></i>: {{_('Door is closed')}}</li>
                        </ul>
                      </div>
                      <div class="tab-pane" id="usage-tab-doors-graph">
                        <h3 class="lead">{{_('History graph')}}</h3>
                        <img src="static/images/documentation/history_graph_door.png" alt="{{_('Door history graph')}}" class="img-thumbnail" /><br /><br />
                        <p>{{_('The history graph will shows when a door was opened.')}}</p>
                        <p>{{!_('Use the calendar icon %s in the title to select the period for the history graph.') % '<i class="fa fa-calendar"></i>'}}</p>
                      </div>
                      <div class="tab-pane" id="usage-tab-doors-settings">
                        <h3 class="lead">{{_('Settings')}}</h3>
                        <p>{{!_('On the door settings page you can configure all needed doors. Click on %s button to add a new door. And empty form like below is shown and has to be filled in. Make sure the right values are filled in. All fields with a %s are required.') % ('<button type="button" class="btn btn-primary"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button>','<span class="required">*</span>',)}}</p>
                        <div class="row">
                          <div class="x_panel">
                            <div class="x_content">
                              <div class="col-md-4 col-sm-4 col-xs-12 form-group">
                                <label for="door_[nr]_hardwaretype">{{_('Hardware')}} <span class="required">*</span></label>
                                <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{!translations.get_translation('door_field_hardware')}}">
                                  <select class="form-control" name="door_[nr]_hardwaretype" tabindex="-1" placeholder="{{_('Select an option')}}" required="required">
                                    <option value="gpio">{{_('GPIO')}}</option>
                                  </select>
                                </div>
                              </div>
                              <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                                <label for="door_[nr]_address">{{_('Address')}}</label> <span class="required">*</span>
                                <input class="form-control" name="door_[nr]_address" placeholder="{{_('Address')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('door_field_address')}}">
                                <input class="form-control" name="door_[nr]_id" placeholder="{{_('ID')}}" readonly="readonly" type="hidden">
                              </div>
                              <div class="col-md-5 col-sm-5 col-xs-12 form-group">
                                <label for="door_[nr]_name">{{_('Name')}}</label> <span class="required">*</span>
                                <input class="form-control" name="door_[nr]_name" placeholder="{{_('Name')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('door_field_name')}}">
                              </div>
                            </div>
                          </div>
                        </div>
                        <ul>
                          <li>
                            <strong>{{_('Hardware')}}</strong>: {{!translations.get_translation('door_field_hardware')}}
                          </li>
                          <li>
                            <strong>{{_('Address')}}</strong>: {{!translations.get_translation('door_field_address')}}
                          </li>
                          <li>
                            <strong>{{_('Name')}}</strong>: {{translations.get_translation('door_field_name')}}
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
                        <a data-toggle="tab" href="#usage-tab-doors-list" title="{{_('Overview')}}">{{_('Overview')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-doors-title" title="{{_('Title')}}">{{_('Title')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-doors-status" title="{{_('Status')}}">{{_('Status')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-doors-graph" title="{{_('Graph')}}">{{_('Graph')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-doors-settings" title="{{_('Settings')}}">{{_('Settings')}}</a>
                      </li>
                    </ul>
                  </div>
                  <script type="text/javascript">
                    $('.total_usage').text('{{_('Total open for')}}: ' + moment.duration(30).humanize());
                  </script>
