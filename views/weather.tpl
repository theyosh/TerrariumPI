% include('inc/page_header.tpl')
        <div class="pull-right col-md-6 col-sm-6 col-xs-6" id="weather_credits"></div>
        <div class="row">
          <div class="col-md-4 col-sm-5 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2><span aria-hidden="true" class="glyphicon glyphicon-cloud"></span> {{_('Weather')}} <small>{{_('Current')}}</small></h2>
                <ul class="nav navbar-right panel_toolbox">
                  <li>
                    <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                  </li>
                  <li class="dropdown">
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-wrench" title="{{_('Options')}}"></i></a>
                    <ul class="dropdown-menu" role="menu">
                      <li>
                        <a href="javascript:;" onclick="menu_click('system_settings.html')">{{_('Settings')}}</a>
                      </li>
                    </ul>
                  </li>
                  <li>
                    <a class="close-link"><i class="fa fa-close" title="{{_('Close')}}"></i></a>
                  </li>
                </ul>
                <div class="clearfix"></div>
              </div>
              <div class="x_content" id='weather_today'>
                <div class="row">
                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="status"></div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4 col-sm-4 col-xs-4">
                    <div class="weather-icon">
                      <canvas height="96" id="weather_icon_1" width="96"></canvas>
                    </div>
                  </div>
                  <div class="col-md-5 col-sm-5 col-xs-5">
                    <h2>{{_('City')}}<br><i>...</i></h2>
                  </div>
                  <div class="col-md-3 col-sm-3 col-xs-3">
                    <div class="row" style="text-align:right">
                      <i class="fa fa-sun-o"></i> <span class="sunrise">...</span>
                    </div>
                    <div class="row" style="text-align:right">
                      <i class="fa fa-moon-o"></i> <span class="sunset">...</span>
                    </div>
                    <div class="row">
                      <br>
                      <h3 class="degrees pull-right">0</h3>
                    </div>
                  </div>
                </div>
                <div class="clearfix"></div>
                <div class="row weather-days">
                  <div class="col-sm-2">
                    <div class="daily-weather">
                      <h2 class="day">{{_('Mon')}}</h2>
                      <h3 class="degrees">0</h3>
                      <canvas height="32" id="weather_icon_2" width="32"></canvas>
                      <h5>0 <i>km/h</i></h5>
                    </div>
                  </div>
                  <div class="col-sm-2">
                    <div class="daily-weather">
                      <h2 class="day">{{_('Tue')}}</h2>
                      <h3 class="degrees">0</h3>
                      <canvas height="32" id="weather_icon_3" width="32"></canvas>
                      <h5>0 <i>km/h</i></h5>
                    </div>
                  </div>
                  <div class="col-sm-2">
                    <div class="daily-weather">
                      <h2 class="day">{{_('Wed')}}</h2>
                      <h3 class="degrees">0</h3>
                      <canvas height="32" id="weather_icon_4" width="32"></canvas>
                      <h5>0 <i>km/h</i></h5>
                    </div>
                  </div>
                  <div class="col-sm-2">
                    <div class="daily-weather">
                      <h2 class="day">{{_('Thu')}}</h2>
                      <h3 class="degrees">0</h3>
                      <canvas height="32" id="weather_icon_5" width="32"></canvas>
                      <h5>0 <i>km/h</i></h5>
                    </div>
                  </div>
                  <div class="col-sm-2">
                    <div class="daily-weather">
                      <h2 class="day">{{_('Fri')}}</h2>
                      <h3 class="degrees">0</h3>
                      <canvas height="32" id="weather_icon_6" width="32"></canvas>
                      <h5>0 <i>km/h</i></h5>
                    </div>
                  </div>
                  <div class="col-sm-2">
                    <div class="daily-weather">
                      <h2 class="day">{{_('Sat')}}</h2>
                      <h3 class="degrees">0</h3>
                      <canvas height="32" id="weather_icon_7" width="32"></canvas>
                      <h5>0 <i>km/h</i></h5>
                    </div>
                  </div>
                  <div class="clearfix"></div>
                </div>
              </div>
            </div><!-- end of weather widget -->
          </div>
          <div class="col-md-8 col-sm-7 col-xs-12">
            <div class="x_panel" id="weather_day">
              <div class="x_title">
                <h2><span aria-hidden="true" class="glyphicon glyphicon-cloud"></span> {{_('Day forecast')}} <small id="weather_hourly">...</small>
                </h2>
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
                <div class="history_graph loading"></div>
              </div>
            </div>
            <div class="x_panel" id="weather_week">
              <div class="x_title">
                <h2><span aria-hidden="true" class="glyphicon glyphicon-cloud"></span> {{_('Week forecast')}} <small id="weather_daily">...</small>
                </h2>
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
                <div class="history_graph loading"></div>
              </div>
            </div>
          </div>
        </div>
        <script type="text/javascript">
          $.get('/api/weather',function(data){
            $('#weather_credits').append($('<a>').attr({'href': data.credits.url,
                                                        'target':'_blank',
                                                        'title' : data.credits.text})
                                                 .text(data.credits.text));
            var period = moment(data.hour_forecast[0].from * 1000).format('lll') + ' - ' + moment(data.hour_forecast[data.hour_forecast.length-1].to * 1000).format('lll') + ', ' + moment.duration( (data.hour_forecast[data.hour_forecast.length-1].to - data.hour_forecast[0].from) * 1000).humanize();
            $('#weather_hourly').text(period);
            period = moment(data.week_forecast[0].from * 1000).format('lll') + ' - ' + moment(data.week_forecast[data.week_forecast.length-1].to * 1000).format('lll') + ', ' +  moment.duration( (data.week_forecast[data.week_forecast.length-1].to - data.week_forecast[0].from) * 1000).humanize();
            $('#weather_daily').text(period);
            update_weather(data);
          });
        </script>
% include('inc/page_footer.tpl')
