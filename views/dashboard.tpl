          <div id="dashboard">
            <!-- top tiles -->
            <div class="row tile_count">
              <div class="col-md-4 col-sm-4 col-xs-6 tile_stats_count" id="uptime">
                <div class="pull-left">
                  <span class="count_top"><span class="glyphicon glyphicon-time" aria-hidden="true"></span> Uptime</span>
                  <div class="count">0</div>
                </div>
                <div class="progress progress-striped active vertical bottom pull-right">
                  <div class="progress-bar progress-bar-danger" role="progressbar" data-transitiongoal="0"></div>
                </div>
                <div class="progress progress-striped active vertical bottom pull-right">
                  <div class="progress-bar progress-bar-warning" role="progressbar" data-transitiongoal="0"></div>
                </div>
                <div class="progress progress-striped active vertical bottom pull-right">
                  <div class="progress-bar progress-bar-success" role="progressbar" data-transitiongoal="0"></div>
                </div>
              </div>
              <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count" id="power_wattage">
                <div class="pull-left">
                  <span class="count_top"><span class="glyphicon glyphicon-flash" aria-hidden="true"></span> Power usage in W</span>
                  <div class="count">0/0</div>
                </div>
                <div class="progress progress-striped active vertical bottom pull-right">
                  <div class="progress-bar progress-bar-success" role="progressbar" data-transitiongoal="0"></div>
                </div>
              </div>
              <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count" id="water_flow">
                <div class="pull-left">
                  <span class="count_top"><span class="glyphicon glyphicon-tint" aria-hidden="true"></span> Water flow in L/m</span>
                  <div class="count">0/0</div>
                </div>
                <div class="progress progress-striped active vertical bottom pull-right">
                  <div class="progress-bar progress-bar-info" role="progressbar" data-transitiongoal="0"></div>
                </div>
              </div>
              <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count" id="total_power">
                <span class="count_top"><span class="glyphicon glyphicon-flash" aria-hidden="true"></span> Total power in kWh</span>
                <div class="count">0</div>
              </div>
              <div class="col-md-2 col-sm-4 col-xs-6 tile_stats_count" id="total_water">
                <span class="count_top"><span class="glyphicon glyphicon-tint" aria-hidden="true"></span> Total water in L</span>
                <div class="count">0</div>
              </div>
            </div>
            <!-- /top tiles -->

            <div class="row">
              <div class="col-md-9 col-sm-9 col-xs-12">
                <div class="row sensor" id="sensor_temperature">
                <div class="x_panel">
                  <div class="x_title">
                    <h2><span class="glyphicon glyphicon-fire" aria-hidden="true"></span> <span class="title">Temperature </span> <small class="data_update">live...</small> <span class="badge bg-red" style="display:none;">warning</span></h2>
                    <ul class="nav navbar-right panel_toolbox">
                      <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                      </li>
                      <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false"><i class="fa fa-wrench"></i></a>
                        <ul class="dropdown-menu" role="menu">
                          <li><a href="#" onclick="menu_click('sensor_settings.html')">Settings</a>
                          </li>
                       </ul>
                      </li>
                      <li><a class="close-link"><i class="fa fa-close"></i></a>
                      </li>
                    </ul>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                    <div class="col-md-4 col-sm-4 col-xs-12">
                      <div class="sidebar-widget">
                        <canvas class="" id="gauge_canvas_temperature"></canvas>
                        <div class="goal-wrapper">
                          <span class="gauge-value pull-left" id="gauge_text_temperature">...</span>
                          <span class="gauge-value pull-left"> °C</span>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <div class="history_graph loading" style="display:block!important;" id="history_graph_temperature"></div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="row sensor" id="sensor_humidity">
               <div class="x_panel">
                 <div class="x_title">
                   <h2><span class="glyphicon glyphicon-tint" aria-hidden="true"></span> <span class="title">Humidity </span> <small class="data_update">live...</small> <span class="badge bg-red" style="display:none;">warning</span></h2>
                   <ul class="nav navbar-right panel_toolbox">
                     <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                     </li>
                     <li class="dropdown">
                       <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false"><i class="fa fa-wrench"></i></a>
                       <ul class="dropdown-menu" role="menu">
                         <li><a href="#" onclick="menu_click('sensor_settings.html')">Settings</a>
                          </li>
                       </ul>
                     </li>
                     <li><a class="close-link"><i class="fa fa-close"></i></a>
                     </li>
                   </ul>
                   <div class="clearfix"></div>
                 </div>
                 <div class="x_content">
                   <div class="col-md-4 col-sm-4 col-xs-12">
                     <div class="sidebar-widget">
                       <canvas class="" id="gauge_canvas_humidity"></canvas>
                       <div class="goal-wrapper">
                         <span class="gauge-value pull-left" id="gauge_text_humidity">...</span>
                         <span class="gauge-value pull-left"> °C</span>
                       </div>
                     </div>
                   </div>
                   <div class="col-md-8 col-sm-8 col-xs-12">
                     <div class="history_graph loading" style="display:block!important;" id="history_graph_humidity"></div>
                   </div>
                 </div>
               </div>
              </div>
            </div>
              <div class="col-md-3 col-sm-3 col-xs-12">
                <div class="x_panel">
                  <div class="x_title">
                    <h2><span class="glyphicon glyphicon-cloud" aria-hidden="true"></span> Weather <small>current</small></h2>
                    <ul class="nav navbar-right panel_toolbox">
                      <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                      </li>
                      <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false"><i class="fa fa-wrench"></i></a>
                        <ul class="dropdown-menu" role="menu">
                          <li><a href="#" onclick="menu_click('weather_settings.html')">Settings</a>
                          </li>
                        </ul>
                      </li>
                      <li><a class="close-link"><i class="fa fa-close"></i></a>
                      </li>
                    </ul>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content" id='weather_today'>
                    <div class="row">
                      <div class="col-sm-12">
                        <div class="temperature">
                        </div>
                      </div>
                    </div>
                    <div class="row">
                      <div class="col-sm-4">
                        <div class="weather-icon">
                          <canvas height="96" width="96" id="weather_icon_1"></canvas>
                        </div>
                      </div>
                      <div class="col-sm-5">
                        <div class="weather-text">
                          <h2>City <br><i>...</i></h2>
                        </div>
                      </div>
                      <div class="col-sm-3">
                        <div class="weather-text">
                          <div class="row">
                            <i class="fa fa-sun-o"></i>
                            <span class="sunrise">...</span>
                          </div>
                          <div class="row">
                            <i class="fa fa-moon-o"></i>
                            <span class="sunset">...</span>
                          </div>
                          <div class="row">
                            <br />
                            <h3 class="degrees pull-right">0</h3>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="clearfix"></div>
                    <div class="row weather-days">
                      <div class="col-sm-2">
                        <div class="daily-weather">
                          <h2 class="day">Mon</h2>
                          <h3 class="degrees">0</h3>
                          <canvas id="weather_icon_2" width="32" height="32"></canvas>
                          <h5>0 <i>km/h</i></h5>
                        </div>
                      </div>
                      <div class="col-sm-2">
                        <div class="daily-weather">
                          <h2 class="day">Tue</h2>
                          <h3 class="degrees">0</h3>
                          <canvas height="32" width="32" id="weather_icon_3"></canvas>
                          <h5>0 <i>km/h</i></h5>
                        </div>
                      </div>
                      <div class="col-sm-2">
                        <div class="daily-weather">
                          <h2 class="day">Wed</h2>
                          <h3 class="degrees">0</h3>
                          <canvas height="32" width="32" id="weather_icon_4"></canvas>
                          <h5>0 <i>km/h</i></h5>
                        </div>
                      </div>
                      <div class="col-sm-2">
                        <div class="daily-weather">
                          <h2 class="day">Thu</h2>
                          <h3 class="degrees">0</h3>
                          <canvas height="32" width="32" id="weather_icon_5"></canvas>
                          <h5>0 <i>km/h</i></h5>
                        </div>
                      </div>
                      <div class="col-sm-2">
                        <div class="daily-weather">
                          <h2 class="day">Fri</h2>
                          <h3 class="degrees">0</h3>
                          <canvas height="32" width="32" id="weather_icon_6"></canvas>
                          <h5>0 <i>km/h</i></h5>
                        </div>
                      </div>
                      <div class="col-sm-2">
                        <div class="daily-weather">
                          <h2 class="day">Sat</h2>
                          <h3 class="degrees">0</h3>
                          <canvas height="32" width="32" id="weather_icon_7"></canvas>
                          <h5>0 <i>km/h</i></h5>
                        </div>
                      </div>
                      <div class="clearfix"></div>
                    </div>
                  </div>
                  <!-- end of weather widget -->
                </div>
                <div class="x_panel">
                  <div class="x_title">
                    <h2><span class="glyphicon glyphicon-flash" aria-hidden="true"></span> Switches <small>current</small></h2>
                    <ul class="nav navbar-right panel_toolbox">
                      <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                      </li>
                      <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false"><i class="fa fa-wrench"></i></a>
                        <ul class="dropdown-menu" role="menu">
                          <li><a href="#" onclick="menu_click('switch_settings.html')">Settings</a>
                          </li>
                        </ul>
                      </li>
                      <li><a class="close-link"><i class="fa fa-close"></i></a>
                      </li>
                    </ul>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                    <div class="sidebar-widget">
                      <div class="col-sm-3">
                        <div class="power-switch" id="pw1">
                          <h2 class="title">Switch1</h2>
                          <span class="glyphicon glyphicon-off" aria-hidden="true"></span>
                          <h5>0 <i>W</i></h5>
                        </div>
                      </div>
                      <div class="col-sm-3">
                        <div class="power-switch" id="pw2">
                          <h2 class="title">Switch2</h2>
                          <span class="glyphicon glyphicon-off" aria-hidden="true"></span>
                          <h5>0 <i>W</i></h5>
                        </div>
                      </div>
                      <div class="col-sm-3">
                        <div class="power-switch" id="pw3">
                          <h2 class="title">Switch3</h2>
                          <span class="glyphicon glyphicon-off" aria-hidden="true"></span>
                          <h5>0 <i>W</i></h5>
                        </div>
                      </div>
                      <div class="col-sm-3">
                        <div class="power-switch" id="pw4">
                          <h2 class="title">Switch4</h2>
                          <span class="glyphicon glyphicon-off" aria-hidden="true"></span>
                          <h5>0 <i>W</i></h5>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <script type="text/javascript">
              $(document).ready(function() {
                globals.gauges = [];

                $.getJSON('/api/uptime',function(data){
                  update_dashboard_uptime(data);
                });

                $.getJSON('/api/power_usage',function(data){
                  update_dashboard_power_usage(data);
                });

                $.getJSON('/api/water_usage',function(data){
                  update_dashboard_water_flow(data);
                });

                $.getJSON('/api/total_usage',function(data){
                  update_dashboard_tile('total_power', data.total_power.toFixed(2));
                  update_dashboard_tile('total_water', data.total_water.toFixed(2));
                });

                $.getJSON('/api/weather',function(data){
                  update_dashboard_weather(data);
                });

                $.getJSON('/api/switches',function(data){
                  update_dashboard_power_switches(data);
                });

                $.getJSON('/api/environment',function(data){
                  $.each(data.environment,function(index,value){
                    sensor_gauge(index,value);
                  });
                });
                update_dashboard_history();
              });
              function update_dashboard_history() {
                if ($('#sensor_temperature, #sensor_humidity').length >= 1) {
                  $.getJSON('/api/history/environment',function(data){
                    $.each(data,function(index,value){
                      history_graph(index,value.summary);
                    });
                    clearTimeout(globals.updatetimer);
                    globals.updatetimer = setTimeout(function(){
                      update_dashboard_history();
                    } , 1 * 60 * 1000)
                  });
                }
              }
              document.title = '{{title}} | {{page_title}}';
            </script>
