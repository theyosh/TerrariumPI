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
                    <h4><span class="fa fa-lightbulb-o"></span> {{_('Lights')}} <small>{{_('mode')}}: <span class="disabled">{{_('Disabled')}}</span><span class="weather">{{_('Weather day/night')}}</span><span class="weatherinverse">{{_('Weather night/day')}}</span><span class="timer">{{_('Timer')}}</span> <span class="sensor">{{_('Sensor')}}</span></small></h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>{{_('Status')}}</p>
                        </td>
                        <td class="state"><i class="fa fa-square green" title="{{_('On')}}"></i><i class="fa fa-square red" title="{{_('Off')}}"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Day')}}</p>
                        </td>
                        <td class="timer_min">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_min duration">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Night')}}</p>
                        </td>
                        <td class="timer_max">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_max duration">...</td>
                      </tr>
                    </table>
                  </div>
                  <div class="row environment_temperature">
                    <h4><span aria-hidden="true" class="glyphicon glyphicon-warning-sign red" title="{{_('Alarm')}}"></span> <i class="fa fa-fire"></i> {{_('Temperature')}} <small>{{_('mode')}}: <span class="disabled">{{_('Disabled')}}</span><span class="weather">{{_('Weather day/night')}}</span><span class="weatherinverse">{{_('Weather night/day')}}</span><span class="timer">{{_('Timer')}}</span> <span class="sensor">{{_('Sensor')}} <span aria-hidden="true" class="glyphicon glyphicon-exclamation-sign orange" title="{{_('Error')}}"></span></span></small></h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>{{_('Status')}}</p>
                        </td>
                        <td class="state"><i class="fa fa-square green" title="{{_('On')}}"></i><i class="fa fa-square red" title="{{_('Off')}}"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_min">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_min duration">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_max">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_max duration">...</td>
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
                          <p>{{_('Day/night difference')}} <span class="day" title="{{_('Day')}}"><i class="fa fa-sun-o"></i></span><span class="night" title="{{_('Night')}}"><i class="fa fa-moon-o"></i></span></p>
                        </td>
                        <td class="day_night_difference">...</td>
                      </tr>
                    </table>
                  </div>
                  <div class="row environment_humidity">
                    <h4><span aria-hidden="true" class="glyphicon glyphicon-warning-sign red" title="{{_('Alarm')}}"></span> <i class="fa fa-tint"></i> {{_('Humidity')}} <small>{{_('mode')}}: <span class="disabled">{{_('Disabled')}}</span><span class="weather">{{_('Weather day/night')}}</span><span class="weatherinverse">{{_('Weather night/day')}}</span><span class="timer">{{_('Timer')}}</span> <span class="sensor">{{_('Sensor')}} <span aria-hidden="true" class="glyphicon glyphicon-exclamation-sign orange" title="{{_('Error')}}"></span></span></small></h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>{{_('Status')}}</p>
                        </td>
                        <td class="state"><i class="fa fa-square green" title="{{_('On')}}"></i><i class="fa fa-square red" title="{{_('Off')}}"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_min">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_min duration">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_max">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_max duration">...</td>
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
                          <p>{{_('Day/night difference')}} <span class="day" title="{{_('Day')}}"><i class="fa fa-sun-o"></i></span><span class="night" title="{{_('Night')}}"><i class="fa fa-moon-o"></i></span></p>
                        </td>
                        <td class="day_night_difference">...</td>
                      </tr>
                    </table>
                  </div>
                  <div class="row environment_moisture">
                    <h4><span aria-hidden="true" class="glyphicon glyphicon-warning-sign red" title="{{_('Alarm')}}"></span> <i class="fa fa-tint"></i> {{_('Moisture')}} <small>{{_('mode')}}: <span class="disabled">{{_('Disabled')}}</span><span class="weather">{{_('Weather day/night')}}</span><span class="weatherinverse">{{_('Weather night/day')}}</span><span class="timer">{{_('Timer')}}</span> <span class="sensor">{{_('Sensor')}} <span aria-hidden="true" class="glyphicon glyphicon-exclamation-sign orange" title="{{_('Error')}}"></span></span></small></h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>{{_('Status')}}</p>
                        </td>
                        <td class="state"><i class="fa fa-square green" title="{{_('On')}}"></i><i class="fa fa-square red" title="{{_('Off')}}"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_min">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_min duration">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_max">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_max duration">...</td>
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
                          <p>{{_('Day/night difference')}} <span class="day" title="{{_('Day')}}"><i class="fa fa-sun-o"></i></span><span class="night" title="{{_('Night')}}"><i class="fa fa-moon-o"></i></span></p>
                        </td>
                        <td class="day_night_difference">...</td>
                      </tr>
                    </table>
                  </div>
                  <div class="row environment_ph">
                    <h4><span aria-hidden="true" class="glyphicon glyphicon-warning-sign red" title="{{_('Alarm')}}"></span> <i class="fa fa-tachometer"></i> {{_('pH')}} <small>{{_('mode')}}: <span class="disabled">{{_('Disabled')}}</span><span class="weather">{{_('Weather day/night')}}</span><span class="weatherinverse">{{_('Weather night/day')}}</span><span class="timer">{{_('Timer')}}</span> <span class="sensor">{{_('Sensor')}} <span aria-hidden="true" class="glyphicon glyphicon-exclamation-sign orange" title="{{_('Error')}}"></span></span></small></h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>{{_('Status')}}</p>
                        </td>
                        <td class="state"><i class="fa fa-square green" title="{{_('On')}}"></i><i class="fa fa-square red" title="{{_('Off')}}"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_min">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_min duration">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_max">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_max duration">...</td>
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
                          <p>{{_('Day/night difference')}} <span class="day" title="{{_('Day')}}"><i class="fa fa-sun-o"></i></span><span class="night" title="{{_('Night')}}"><i class="fa fa-moon-o"></i></span></p>
                        </td>
                        <td class="day_night_difference">...</td>
                      </tr>
                    </table>
                  </div>
                  <div class="row environment_conductivity">
                    <h4><span aria-hidden="true" class="glyphicon glyphicon-warning-sign red" title="{{_('Alarm')}}"></span> <i class="fa fa-flash"></i> {{_('Conductivity')}} <small>{{_('mode')}}: <span class="disabled">{{_('Disabled')}}</span><span class="weather">{{_('Weather day/night')}}</span><span class="weatherinverse">{{_('Weather night/day')}}</span><span class="timer">{{_('Timer')}}</span> <span class="sensor">{{_('Sensor')}} <span aria-hidden="true" class="glyphicon glyphicon-exclamation-sign orange" title="{{_('Error')}}"></span></span></small></h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>{{_('Status')}}</p>
                        </td>
                        <td class="state"><i class="fa fa-square green" title="{{_('On')}}"></i><i class="fa fa-square red" title="{{_('Off')}}"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_min">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_min duration">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_max">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_max duration">...</td>
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
                          <p>{{_('Day/night difference')}} <span class="day" title="{{_('Day')}}"><i class="fa fa-sun-o"></i></span><span class="night" title="{{_('Night')}}"><i class="fa fa-moon-o"></i></span></p>
                        </td>
                        <td class="day_night_difference">...</td>
                      </tr>
                    </table>
                  </div>
                  <div class="row environment_watertank">
                    <h4><span aria-hidden="true" class="glyphicon glyphicon-warning-sign red" title="{{_('Alarm')}}"></span> <i class="fa fa-tint"></i> {{_('Water tank')}} <small>{{_('mode')}}: <span class="disabled">{{_('Disabled')}}</span><span class="weather">{{_('Weather day/night')}}</span><span class="weatherinverse">{{_('Weather night/day')}}</span><span class="timer">{{_('Timer')}}</span> <span class="sensor">{{_('Sensor')}} <span aria-hidden="true" class="glyphicon glyphicon-exclamation-sign orange" title="{{_('Error')}}"></span></span></small></h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>{{_('Status')}}</p>
                        </td>
                        <td class="state"><i class="fa fa-square green" title="{{_('On')}}"></i><i class="fa fa-square red" title="{{_('Off')}}"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_min">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_min duration">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_max">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_max duration">...</td>
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
                          <p>{{_('Day/night difference')}} <span class="day" title="{{_('Day')}}"><i class="fa fa-sun-o"></i></span><span class="night" title="{{_('Night')}}"><i class="fa fa-moon-o"></i></span></p>
                        </td>
                        <td class="day_night_difference">...</td>
                      </tr>
                    </table>
                  </div>
                  <div class="row environment_fertility">
                    <h4><span aria-hidden="true" class="glyphicon glyphicon-warning-sign red" title="{{_('Alarm')}}"></span> <i class="fa fa-pagelines"></i> {{_('Fertility')}} <small>{{_('mode')}}: <span class="disabled">{{_('Disabled')}}</span><span class="weather">{{_('Weather day/night')}}</span><span class="weatherinverse">{{_('Weather night/day')}}</span><span class="timer">{{_('Timer')}}</span> <span class="sensor">{{_('Sensor')}} <span aria-hidden="true" class="glyphicon glyphicon-exclamation-sign orange" title="{{_('Error')}}"></span></span></small></h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>{{_('Status')}}</p>
                        </td>
                        <td class="state"><i class="fa fa-square green" title="{{_('On')}}"></i><i class="fa fa-square red" title="{{_('Off')}}"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_min">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_min duration">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_max">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_max duration">...</td>
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
                          <p>{{_('Day/night difference')}} <span class="day" title="{{_('Day')}}"><i class="fa fa-sun-o"></i></span><span class="night" title="{{_('Night')}}"><i class="fa fa-moon-o"></i></span></p>
                        </td>
                        <td class="day_night_difference">...</td>
                      </tr>
                    </table>
                  </div>
                  <div class="row environment_co2">
                    <h4><span aria-hidden="true" class="glyphicon glyphicon-warning-sign red" title="{{_('Alarm')}}"></span> <i class="fa fa-tree"></i> {{_('CO2')}} <small>{{_('mode')}}: <span class="disabled">{{_('Disabled')}}</span><span class="weather">{{_('Weather day/night')}}</span><span class="weatherinverse">{{_('Weather night/day')}}</span><span class="timer">{{_('Timer')}}</span> <span class="sensor">{{_('Sensor')}} <span aria-hidden="true" class="glyphicon glyphicon-exclamation-sign orange" title="{{_('Error')}}"></span></span></small></h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>{{_('Status')}}</p>
                        </td>
                        <td class="state"><i class="fa fa-square green" title="{{_('On')}}"></i><i class="fa fa-square red" title="{{_('Off')}}"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_min">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_min duration">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_max">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_max duration">...</td>
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
                          <p>{{_('Day/night difference')}} <span class="day" title="{{_('Day')}}"><i class="fa fa-sun-o"></i></span><span class="night" title="{{_('Night')}}"><i class="fa fa-moon-o"></i></span></p>
                        </td>
                        <td class="day_night_difference">...</td>
                      </tr>
                    </table>
                  </div>
                  <div class="row environment_volume">
                    <h4><span aria-hidden="true" class="glyphicon glyphicon-warning-sign red" title="{{_('Alarm')}}"></span> <i class="fa fa-tint"></i> {{_('Volume')}} <small>{{_('mode')}}: <span class="disabled">{{_('Disabled')}}</span><span class="weather">{{_('Weather day/night')}}</span><span class="weatherinverse">{{_('Weather night/day')}}</span><span class="timer">{{_('Timer')}}</span> <span class="sensor">{{_('Sensor')}} <span aria-hidden="true" class="glyphicon glyphicon-exclamation-sign orange" title="{{_('Error')}}"></span></span></small></h4>
                    <table class="tile_info">
                      <tr>
                        <td>
                          <p>{{_('Status')}}</p>
                        </td>
                        <td class="state"><i class="fa fa-square green" title="{{_('On')}}"></i><i class="fa fa-square red" title="{{_('Off')}}"></i></td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_min">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_min duration">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Period')}}</p>
                        </td>
                        <td class="timer_max">...</td>
                      </tr>
                      <tr>
                        <td>
                          <p>{{_('Duration')}}</p>
                        </td>
                        <td class="timer_max duration">...</td>
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
                          <p>{{_('Day/night difference')}} <span class="day" title="{{_('Day')}}"><i class="fa fa-sun-o"></i></span><span class="night" title="{{_('Night')}}"><i class="fa fa-moon-o"></i></span></p>
                        </td>
                        <td class="day_night_difference">...</td>
                      </tr>
                    </table>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-9 col-sm-9 col-xs-12 pull-left">
              <div class="x_panel" id="average_temperature">
                <div class="x_title">
                  <h2><span aria-hidden="true" class="glyphicon glyphicon-fire"></span> <span class="title">{{_('Average Temperature')}}</span> <span class="small data_update">...</span> <span class="badge bg-red" style="display:none;">{{_('warning')}}</span></h2>
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
              <div class="x_panel" id="average_humidity">
                <div class="x_title">
                  <h2><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> <span class="title">{{_('Average Humidity')}}</span> <span class="small data_update">...</span> <span class="badge bg-red" style="display:none;">{{_('warning')}}</span></h2>
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
              <div class="x_panel" id="average_moisture">
                <div class="x_title">
                  <h2><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> <span class="title">{{_('Average Moisture')}}</span> <span class="small data_update">...</span> <span class="badge bg-red" style="display:none;">{{_('warning')}}</span></h2>
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
              <div class="x_panel" id="average_conductivity">
                <div class="x_title">
                  <h2><span aria-hidden="true" class="glyphicon glyphicon-oil"></span> <span class="title">{{_('Average Conductivity')}}</span> <span class="small data_update">...</span> <span class="badge bg-red" style="display:none;">{{_('warning')}}</span></h2>
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
              <div class="x_panel" id="average_distance">
                <div class="x_title">
                  <h2><span aria-hidden="true" class="glyphicon glyphicon-signal"></span> <span class="title">{{_('Average Distance')}}</span> <span class="small data_update">...</span> <span class="badge bg-red" style="display:none;">{{_('warning')}}</span></h2>
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
              <div class="x_panel" id="average_ph">
                <div class="x_title">
                  <h2><span aria-hidden="true" class="glyphicon glyphicon-scale"></span> <span class="title">{{_('Average pH')}}</span> <span class="small data_update">...</span> <span class="badge bg-red" style="display:none;">{{_('warning')}}</span></h2>
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
              <div class="x_panel" id="average_light">
                <div class="x_title">
                  <h2><span aria-hidden="true" class="glyphicon glyphicon-adjust"></span> <span class="title">{{_('Average Light')}}</span> <span class="small data_update">...</span> <span class="badge bg-red" style="display:none;">{{_('warning')}}</span></h2>
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
              <div class="x_panel" id="average_fertility">
                <div class="x_title">
                  <h2><span aria-hidden="true" class="glyphicon glyphicon-grain"></span> <span class="title">{{_('Average Fertility')}}</span> <span class="small data_update">...</span> <span class="badge bg-red" style="display:none;">{{_('warning')}}</span></h2>
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
              <div class="x_panel" id="average_co2">
                <div class="x_title">
                  <h2><span aria-hidden="true" class="glyphicon glyphicon-tree-conifer"></span> <span class="title">{{_('Average CO2')}}</span> <span class="small data_update">...</span> <span class="badge bg-red" style="display:none;">{{_('warning')}}</span></h2>
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
              <div class="x_panel" id="average_volume">
                <div class="x_title">
                  <h2><span aria-hidden="true" class="glyphicon glyphicon-signal"></span> <span class="title">{{_('Average Volume')}}</span> <span class="small data_update">...</span> <span class="badge bg-red" style="display:none;">{{_('warning')}}</span></h2>
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
          % if hide_environment:
            $('div#dashboard div.row.environment div.pull-right').remove();
            $('div#dashboard div.row.environment div.pull-left').removeClass().addClass('col-md-12 col-sm-12 col-xs-12 pull-left');
          % end

            // The a click event is not working due to template system. So bind it to the inner i object
            $('div#dashboard div.row.environment div.pull-right a.close-link i').on('click',function(event){
              $('div#dashboard div.row.environment div.pull-left').removeClass().addClass('col-md-12 col-sm-12 col-xs-12 pull-left');
            });

            $('div#dashboard div.pull-left div.x_panel').hide();

            $.get('/api/sensors/average',function(json_data) {
              var active_sensor_types = ['settings'];

              if (globals.show_gauge_overview) {
                active_sensor_types.push('gauge_overview');
              }

              $.each(json_data.sensors,function(index,sensor_data){
                if ($('div#' + sensor_data.type + ':hidden')) {
                  $('div#' + sensor_data.type).show();

                  var sensortype = sensor_data.type.replace('average_','');
                  sensor_gauge(sensor_data.type, sensor_data);
                  load_history_graph(sensor_data.type,sensortype,'/api/history/sensors/average/' + sensortype);
                  if (sensortype == 'uva' || sensortype == 'uvb') {
                    sensortype = 'light';
                  }
                  active_sensor_types.push(sensortype);
                }
              });

              const regex = /\/sensor_([^\.]+)\.html/;
              var sensor_type;
              $('div#sidebar-menu li a[href^="sensor_"]').each(function(index,data){
                if ((sensor_type = regex.exec(this.href)) !== null) {
                  if (active_sensor_types.indexOf(sensor_type[1]) === -1) {
                    $(this).hide();
                  }
                }
              });
              reload_reload_theme();
            });
            websocket_message({
              'type': 'show_dashboard'
            });
          });
        </script>
% include('inc/page_footer.tpl')
