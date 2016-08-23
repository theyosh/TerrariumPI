        <div id="dashboard">
          <!-- top tiles -->
          <div class="row tile_count">
            <div class="col-md-4 col-sm-8 col-xs-12 tile_stats_count" id="uptime">
              <div class="row">
                <div class="pull-left">
                  <span class="count_top"><span aria-hidden="true" class="glyphicon glyphicon-time"></span> Uptime</span>
                  <div class="count">
                    0
                  </div>
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
                  <span class="count_top"><span aria-hidden="true" class="glyphicon glyphicon-flash"></span> Power usage in W</span>
                  <div class="count">
                    0/0
                  </div>
                </div>
                <div class="progress progress-striped active vertical bottom pull-right">
                  <div class="progress-bar progress-bar-success" data-transitiongoal="0" role="progressbar"></div>
                </div>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count" id="water_flow">
              <div class="row">
                <div class="pull-left">
                  <span class="count_top"><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> Water flow in L/m</span>
                  <div class="count">
                    0/0
                  </div>
                </div>
                <div class="progress progress-striped active vertical bottom pull-right">
                  <div class="progress-bar progress-bar-info" data-transitiongoal="0" role="progressbar"></div>
                </div>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count" id="total_power">
              <div class="row">
                <span class="count_top"><span aria-hidden="true" class="glyphicon glyphicon-flash"></span> Total power in kWh</span>
                <div class="count">
                  0
                </div>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count" id="total_water">
              <div class="row">
                <span class="count_top"><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> Total water in L</span>
                <div class="count">
                  0
                </div>
              </div>
            </div>
          </div><!-- /top tiles -->
          <div class="row">
            <div class="col-md-3 col-sm-3 col-xs-12 pull-right">
              <div class="x_panel">
                <div class="x_title">
                  <h2><span class="fa fa-lightbulb-o"></span> <span class="title">Environment</span> <small>current</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                    <li class="dropdown">
                      <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="#" role="button"><i class="fa fa-wrench"></i></a>
                      <ul class="dropdown-menu" role="menu">
                        <li>
                          <a href="#" onclick="menu_click('environment.html')">Settings</a>
                        </li>
                      </ul>
                    </li>
                    <li>
                      <a class="close-link"><i class="fa fa-close"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="row environment_light">
                    <h4><span aria-hidden="true" class="glyphicon glyphicon-flash"></span> Lights <small>modus</small></h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>State</p>
                        </td>
                        <td class="state"><i class="fa fa-square"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>On</p>
                        </td>
                        <td class="on">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>Off</p>
                        </td>
                        <td class="off">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>Duration</p>
                        </td>
                        <td class="duration">...</td>
                      </tr>
                    </table>
                  </div>
                  <div class="row environment_sprayer">
                    <h4><span aria-hidden="true" class="glyphicon glyphicon-warning-sign red"></span> <span aria-hidden="true" class="glyphicon glyphicon-tint"></span> Sprayer</h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>State</p>
                        </td>
                        <td class="state"><i class="fa fa-square"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>Current</p>
                        </td>
                        <td class="current">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>Alarm min</p>
                        </td>
                        <td class="alarm_min">...</td>
                      </tr>
                    </table>
                  </div>
                  <div class="row environment_heater">
                    <h4><span aria-hidden="true" class="glyphicon glyphicon-warning-sign red"></span> <span aria-hidden="true" class="glyphicon glyphicon-fire"></span> Heater <small>sensor</small></h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>State</p>
                        </td>
                        <td class="state"><i class="fa fa-square"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>Current</p>
                        </td>
                        <td class="current">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>Alarm min</p>
                        </td>
                        <td class="alarm_min">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>Alarm max</p>
                        </td>
                        <td class="alarm_max">...</td>
                      </tr>
                    </table>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-9 col-sm-9 col-xs-12 pull-left">
              <div class="x_panel" id="sensor_humidity">
                <div class="x_title">
                  <h2><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> <span class="title">Average Humidity</span> <small class="data_update">live...</small> <span class="badge bg-red" style="display:none;">warning</span></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                    <li class="dropdown">
                      <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="#" role="button"><i class="fa fa-wrench"></i></a>
                      <ul class="dropdown-menu" role="menu">
                        <li>
                          <a href="#" onclick="menu_click('sensor_settings.html')">Settings</a>
                        </li>
                      </ul>
                    </li>
                    <li>
                      <a class="close-link"><i class="fa fa-close"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="col-md-4 col-sm-5 col-xs-12">
                    <div class="sidebar-widget">
                      <canvas class="gauge" id="gauge_canvas_humidity"></canvas>
                      <div class="goal-wrapper">
                        <span class="gauge-value pull-left" id="gauge_text_humidity">...</span> <span class="gauge-value pull-left">%</span>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-8 col-sm-7 col-xs-12">
                    <div class="history_graph loading" id="history_graph_humidity"></div>
                  </div>
                </div>
              </div>
              <div class="x_panel" id="sensor_temperature">
                <div class="x_title">
                  <h2><span aria-hidden="true" class="glyphicon glyphicon-fire"></span> <span class="title">Average Temperature</span> <small class="data_update">live...</small> <span class="badge bg-red" style="display:none;">warning</span></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                    <li class="dropdown">
                      <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="#" role="button"><i class="fa fa-wrench"></i></a>
                      <ul class="dropdown-menu" role="menu">
                        <li>
                          <a href="#" onclick="menu_click('sensor_settings.html')">Settings</a>
                        </li>
                      </ul>
                    </li>
                    <li>
                      <a class="close-link"><i class="fa fa-close"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="col-md-4 col-sm-5 col-xs-12">
                    <div class="sidebar-widget">
                      <canvas class="gauge" id="gauge_canvas_temperature"></canvas>
                      <div class="goal-wrapper">
                        <span class="gauge-value pull-left" id="gauge_text_temperature">...</span> <span class="gauge-value pull-left">°C</span>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-8 col-sm-7 col-xs-12">
                    <div class="history_graph loading" id="history_graph_temperature"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <script type="text/javascript">
          $(document).ready(function() {
            globals.gauges = [];
            websocket_message({
              'type': 'show_dashboard'
            });
            update_dashboard_history();
          });
        </script>
