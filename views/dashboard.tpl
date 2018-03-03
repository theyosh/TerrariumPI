        <div id="dashboard">
          <!-- top tiles -->
          <div class="row tile_count">
            <div class="col-md-4 col-sm-8 col-xs-12 tile_stats_count" id="uptime">
              <div class="row">
                <div class="pull-left">
                  <span class="count_top"><span aria-hidden="true" class="glyphicon glyphicon-time"></span> {{_('Uptime')}}</span>
                  <div class="count">0</div>
                </div>
                <div class="progress progress-striped active vertical bottom pull-right">
                  <div class="progress-bar progress-bar-danger" data-transitiongoal="0" role="progressbar"></div>
                </div>
                <div class="progress progress-striped active vertical bottom pull-right">
                  <div class="progress-bar progress-bar-warning" data-transitiongoal="0" role="progressbar"></div>
                </div>
                <div class="progress progress-striped active vertical bottom pull-right">
                  <div class="progress-bar progress-bar-success" data-transitiongoal="0" role="progressbar"></div>
                </div>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count" id="power_wattage">
              <div class="row">
                <div class="pull-left">
                  <span class="count_top"><span aria-hidden="true" class="glyphicon glyphicon-flash"></span> {{_('Power usage in Watt')}}</span>
                  <div class="count">0/0</div>
                </div>
                <div class="progress progress-striped active vertical bottom pull-right">
                  <div class="progress-bar progress-bar-success" data-transitiongoal="0" role="progressbar"></div>
                </div>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count" id="water_flow">
              <div class="row">
                <div class="pull-left">
                  <span class="count_top"><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> {{_('Water flow in L/m')}}</span>
                  <div class="count">0/0</div>
                </div>
                <div class="progress progress-striped active vertical bottom pull-right">
                  <div class="progress-bar progress-bar-info" data-transitiongoal="0" role="progressbar"></div>
                </div>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count" id="total_power">
              <div class="row">
                <span class="count_top"><span aria-hidden="true" class="glyphicon glyphicon-flash"></span> {{_('Total power in kWh')}}</span>
                <div class="count">0</div>
                <span class="count_bottom"><i class="green costs"></i> {{_('in')}} <span class="duration"></span></span>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count" id="total_water">
              <div class="row">
                <span class="count_top"><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> {{_('Total water in L')}}</span>
                <div class="count">0</div>
                <span class="count_bottom"><i class="green costs"></i> {{_('in')}} <span class="duration"></span></span>
              </div>
            </div>
          </div><!-- /top tiles -->
          <div class="row environment">
            <div class="col-md-3 col-sm-3 col-xs-12 pull-right">
              <div class="x_panel">
                <div class="x_title">
                  <h2><span aria-hidden="true" class="glyphicon glyphicon-cog"></span> <span class="title">{{_('Environment')}}</span> <small>{{_('Current')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                    <li class="dropdown">
                      <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-wrench" title="{{_('Options')}}"></i></a>
                      <ul class="dropdown-menu" role="menu">
                        <li>
                          <a href="javascript:;" onclick="menu_click('system_environment.html')">{{_('Settings')}}</a>
                        </li>
                      </ul>
                    </li>
                    <li>
                      <a class="close-link"><i class="fa fa-close" title="{{_('Close')}}"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="row environment_light">
                    <h4><span class="fa fa-lightbulb-o"></span> {{_('Lights')}} <small>{{_('mode')}}: <span class="disabled">{{_('Disabled')}}</span><span class="weather">{{_('Weather')}}</span><span class="timer">{{_('Timer')}}</span> <span class="sensor">{{_('Sensor')}}</span></small></h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>{{_('Status')}}</p>
                        </td>
                        <td class="state"><i class="fa fa-square green" title="{{_('On')}}"></i><i class="fa fa-square red" title="{{_('Off')}}"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('On')}}</p>
                        </td>
                        <td class="on">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Off')}}</p>
                        </td>
                        <td class="off">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="duration">...</td>
                      </tr>
                    </table>
                  </div>
                  <div class="row environment_sprayer">
                    <h4><span aria-hidden="true" class="glyphicon glyphicon-warning-sign red" title="{{_('Alarm')}}"></span> <i class="fa fa-umbrella"></i> {{_('Sprayer')}} <small>{{_('mode')}}: <span class="disabled">{{_('Disabled')}}</span><span class="weather">{{_('Weather')}}</span><span class="timer">{{_('Timer')}}</span> <span class="sensor">{{_('Sensor')}}</span></small></h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>{{_('Status')}}</p>
                        </td>
                        <td class="state"><i class="fa fa-square green" title="{{_('On')}}"></i><i class="fa fa-square red" title="{{_('Off')}}"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Current')}}</p>
                        </td>
                        <td class="current">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Alarm min')}}</p>
                        </td>
                        <td class="alarm_min">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('On')}}</p>
                        </td>
                        <td class="on">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Off')}}</p>
                        </td>
                        <td class="off">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="duration">...</td>
                      </tr>
                    </table>
                  </div>
                  <div class="row environment_watertank">
                    <h4><span aria-hidden="true" class="glyphicon glyphicon-warning-sign red" title="{{_('Alarm')}}"></span> <i class="fa fa-tint"></i> {{_('Watertank')}} <small>{{_('mode')}}: <span class="disabled">{{_('Disabled')}}</span><span class="weather">{{_('Weather')}}</span><span class="timer">{{_('Timer')}}</span> <span class="sensor">{{_('Sensor')}}</span></small></h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>{{_('Status')}}</p>
                        </td>
                        <td class="state"><i class="fa fa-square green" title="{{_('On')}}"></i><i class="fa fa-square red" title="{{_('Off')}}"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Current')}}</p>
                        </td>
                        <td class="current">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Alarm min')}}</p>
                        </td>
                        <td class="alarm_min">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('On')}}</p>
                        </td>
                        <td class="on">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Off')}}</p>
                        </td>
                        <td class="off">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="duration">...</td>
                      </tr>
                    </table>
                  </div>
                  <div class="row environment_heater">
                    <h4><span aria-hidden="true" class="glyphicon glyphicon-warning-sign red" title="{{_('Alarm')}}"></span> <i class="fa fa-fire"></i> {{_('Heater')}} <small>{{_('mode')}}: <span class="disabled">{{_('Disabled')}}</span><span class="weather">{{_('Weather')}}</span><span class="timer">{{_('Timer')}}</span> <span class="sensor">{{_('Sensor')}}</span></small></h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>{{_('Status')}}</p>
                        </td>
                        <td class="state"><i class="fa fa-square green" title="{{_('On')}}"></i><i class="fa fa-square red" title="{{_('Off')}}"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('On')}}</p>
                        </td>
                        <td class="on">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Off')}}</p>
                        </td>
                        <td class="off">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="duration">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Current')}}</p>
                        </td>
                        <td class="current">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Range')}}</p>
                        </td>
                        <td class="alarm_min alarm_max">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Day/night difference')}}</p>
                        </td>
                        <td class="night_difference">...</td>
                      </tr>
                    </table>
                  </div>
                  <div class="row environment_cooler">
                    <h4><span aria-hidden="true" class="glyphicon glyphicon-warning-sign red" title="{{_('Alarm')}}"></span> <i class="fa fa-flag-o"></i> {{_('Cooler')}} <small>{{_('mode')}}: <span class="disabled">{{_('Disabled')}}</span><span class="weather">{{_('Weather')}}</span><span class="timer">{{_('Timer')}}</span> <span class="sensor">{{_('Sensor')}}</span></small></h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>{{_('Status')}}</p>
                        </td>
                        <td class="state"><i class="fa fa-square green" title="{{_('On')}}"></i><i class="fa fa-square red" title="{{_('Off')}}"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('On')}}</p>
                        </td>
                        <td class="on">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Off')}}</p>
                        </td>
                        <td class="off">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="duration">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Current')}}</p>
                        </td>
                        <td class="current">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Range')}}</p>
                        </td>
                        <td class="alarm_min alarm_max">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Day/night difference')}}</p>
                        </td>
                        <td class="night_difference">...</td>
                      </tr>
                    </table>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-9 col-sm-9 col-xs-12 pull-left">
              <div class="x_panel" id="average_humidity">
                <div class="x_title">
                  <h2><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> <span class="title">{{_('Average Humidity')}}</span> <small class="data_update">...</small> <span class="badge bg-red" style="display:none;">{{_('warning')}}</span></h2>
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
                        <li>
                          <a href="javascript:;" class="export">{{_('Export data')}}</a>
                        </li>
                      </ul>
                    </li>
                    <li>
                      <a class="close-link"><i class="fa fa-close" title="{{_('Close')}}"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="col-md-4 col-sm-5 col-xs-12">
                    <div class="sidebar-widget text-center">
                      <canvas class="gauge"></canvas>
                      <div class="goal-wrapper">
                        <span class="gauge-value">...</span> <span class="gauge-indicator"></span>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-8 col-sm-7 col-xs-12">
                    <div class="history_graph loading"></div>
                  </div>
                </div>
              </div>
              <div class="x_panel" id="average_temperature">
                <div class="x_title">
                  <h2><span aria-hidden="true" class="glyphicon glyphicon-fire"></span> <span class="title">{{_('Average Temperature')}}</span> <small class="data_update">...</small> <span class="badge bg-red" style="display:none;">{{_('warning')}}</span></h2>
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
                        <li>
                          <a href="javascript:;" class="export">{{_('Export data')}}</a>
                        </li>
                      </ul>
                    </li>
                    <li>
                      <a class="close-link"><i class="fa fa-close" title="{{_('Close')}}"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="col-md-4 col-sm-5 col-xs-12">
                    <div class="sidebar-widget text-center">
                      <canvas class="gauge"></canvas>
                      <div class="goal-wrapper">
                        <span class="gauge-value">...</span> <span class="gauge-indicator"></span>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-8 col-sm-7 col-xs-12">
                    <div class="history_graph loading"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <script type="text/javascript">
          $(document).ready(function() {
            load_history_graph('average_humidity','humidity','/api/history/sensors/average/humidity');
            load_history_graph('average_temperature','temperature','/api/history/sensors/average/temperature');

            websocket_message({
              'type': 'show_dashboard'
            });
          });
        </script>
% include('inc/page_footer.tpl')
