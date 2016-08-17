% include('inc/page_header.tpl')
          <div class="pull-right col-md-6 col-sm-6 col-xs-6" id="weather_credits"></div>
            <div class="row">
              <div class="col-md-4 col-sm-5 col-xs-12">

                  <div class="x_panel">
                    <div class="x_title">
                      <h2><span class="glyphicon glyphicon-cloud" aria-hidden="true"></span> Weather <small>current</small></h2>
                      <ul class="nav navbar-right panel_toolbox">
                        <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                        </li>
                        <li class="dropdown">
                          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false"><i class="fa fa-wrench"></i></a>
                          <ul class="dropdown-menu" role="menu">
                            <li><a href="#" onclick="menu_click('weather_settings.html')">Settings</a></li>
                          </ul>
                        </li>
                        <li><a class="close-link"><i class="fa fa-close"></i></a>
                        </li>
                      </ul>
                      <div class="clearfix"></div>
                    </div>
                    <div class="x_content" id='weather_today'>
                      <div class="row">
                        <div class="col-md-12 col-sm-12 col-xs-12">
                          <div class="status">
                          </div>
                        </div>
                      </div>
                      <div class="row">
                        <div class="col-md-4 col-sm-4 col-xs-4">
                          <div class="weather-icon">
                            <canvas height="96" width="96" id="weather_icon_1"></canvas>
                          </div>
                        </div>
                        <div class="col-md-5 col-sm-5 col-xs-5">
                          <!-- <div class="weather-text"> -->
                            <h2>City <br><i>...</i></h2>
                          <!-- </div> -->
                        </div>
                        <div class="col-md-3 col-sm-3 col-xs-3">
                         <!--  <div class="weather-text"> -->
                            <div class="row" style="text-align:right">
                              <i class="fa fa-sun-o"></i>
                              <span class="sunrise">...</span>
                            </div>
                            <div class="row" style="text-align:right">
                              <i class="fa fa-moon-o"></i>
                              <span class="sunset">...</span>
                            </div>
                            <div class="row">
                              <br />
                              <h3 class="degrees pull-right">0</h3>
                            </div>
                          </div>
                       <!--  </div> -->
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
                  </div>
                  <!-- end of weather widget -->
              </div>

              <div class="col-md-8 col-sm-7 col-xs-12">

                  <div class="x_panel">
                  <div class="x_title">
                    <h2>Day forecast <small id="weather_hourly">...</small></h2>
                    <ul class="nav navbar-right panel_toolbox">
                      <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                      </li>
                      <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false"><i class="fa fa-wrench"></i></a>
                        <ul class="dropdown-menu" role="menu">
                          <li><a href="#">Settings 1</a>
                          </li>
                          <li><a href="#">Settings 2</a>
                          </li>
                        </ul>
                      </li>
                      <li><a class="close-link"><i class="fa fa-close"></i></a>
                      </li>
                    </ul>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                    <div class="history_graph loading" id="history_graph_weather_day"></div>
                  </div>
                </div>



                  <div class="x_panel">
                  <div class="x_title">
                    <h2>Week forecast <small id="weather_daily">...</small></h2>
                    <ul class="nav navbar-right panel_toolbox">
                      <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                      </li>
                      <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false"><i class="fa fa-wrench"></i></a>
                        <ul class="dropdown-menu" role="menu">
                          <li><a href="#">Settings 1</a>
                          </li>
                          <li><a href="#">Settings 2</a>
                          </li>
                        </ul>
                      </li>
                      <li><a class="close-link"><i class="fa fa-close"></i></a>
                      </li>
                    </ul>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                    <div class="history_graph loading" id="history_graph_weather_week"></div>
                  </div>
                </div>

              </div>
            </div>
            <script type="text/javascript">
               $.getJSON('/api/weather',function(data){
                $('#weather_credits').html('<a href="' + data.credits.url + '" target="_blank">' + data.credits.text + '</a>');
                  var period = moment(data.hour_forecast[0].from * 1000).format('lll') + ' - ' + moment(data.hour_forecast[data.hour_forecast.length-1].to * 1000).format('lll') + ', ' + moment.duration( (data.hour_forecast[data.hour_forecast.length-1].to - data.hour_forecast[0].from) * 1000).humanize();
                  $('#weather_hourly').text(period);
                  period = moment(data.week_forecast[0].from * 1000).format('lll') + ' - ' + moment(data.week_forecast[data.week_forecast.length-1].to * 1000).format('lll') + ', ' +  moment.duration( (data.week_forecast[data.week_forecast.length-1].to - data.week_forecast[0].from) * 1000).humanize();
                  $('#weather_daily').text(period);
                  update_weather(data);
                });

            </script>
% include('inc/page_footer.tpl')
