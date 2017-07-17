                  <h2>{{_('Home')}}</h2>
                  <p>Hover over the screenshot below to see the areas defined in the tabs menu on the right side</p>
                  <div class="col-xs-9">
                    <!-- Tab panes -->
                    <div class="tab-content">
                      <div class="tab-pane active" id="usage-tab-dashboard-dashboard">
                        <div class="interactive_screenshot">
                          <div id="screenshot_dashboard_top_indicators" class="click_area" title="{{_('Top indicators')}}"></div>
                          <div id="screenshot_dashboard_top_tiles" class="click_area" title="{{_('Top tiles')}}"></div>
                          <div id="screenshot_dashboard_environment" class="click_area" title="{{_('Environment')}}"></div>
                          <div id="screenshot_dashboard_graphs" class="click_area" title="{{_('Graphs')}}"></div>
                          <img src="static/images/documentation/dashboard.png" alt="Dashboard screenshot" />
                        </div>
                      </div>
                      <div class="tab-pane" id="usage-tab-dashboard-top-indicators">
                        <h3 class="lead">{{_('Top indicators')}}</h3>
                        <p>The dashboard has two indicators and a clock on the top row at the right site.</p>
                        <div class="row">
                          <h4>{{_('Status indicator')}}</h4>
                          <p>
                            <i class="fa fa-check-circle-o green"></i> <strong>{{_('Online')}}</strong>
                            <br />
                            <img src="static/images/documentation/dashboard_top_indicators_online.png" alt="Dashboard top indicators online screenshot" />
                            <br />
                            The first green round check mark shows that the interface is connected with the server and that it is working as expected.
                          </p>
                          <p>
                            <i class="fa fa-exclamation-triangle red"></i> <strong>{{_('Offline')}}</strong>
                            <br />
                            <img src="static/images/documentation/dashboard_top_indicators_offline.png" alt="Dashboard top indicators offline screenshot" />
                            <br />
                            When there is a connection problem, the first round check mark will turn to a red explanation mark which indicates that there is a problem.
                          </p>
                          <p>
                            <strong>{{_('History')}}</strong>
                            <br />
                            <img src="static/images/documentation/dashboard_top_indicators_history.png" alt="Dashboard top indicators history screenshot" />
                            <br />
                            Click on the online/offline indicator to get some history. The history is cleared when the web interface is reloaded.
                          </p>
                        </div>
                        <div class="row">
                          <h4>{{_('Door indicator')}}</h4>
                          <p>
                            <strong><i class="fa fa-lock green"></i> {{_('Door is closed')}}</strong>
                            <br />
                            <img src="static/images/documentation/dashboard_top_indicators_online.png" alt="Dashboard top indicators online screenshot" />
                            <br />
                            The second indicator is a lock that shows the status of the door(s). It is green when all doors are closed.
                          </p>
                          <p>
                            <strong><i class="fa fa-unlock red"></i> {{_('Door is open')}}</strong>
                            <br />
                            <img src="static/images/documentation/dashboard_top_indicators_door_open.png" alt="Dashboard top indicators online screenshot" />
                            <br />
                            When a door is opened, the indicator will change to a red open lock. This indicator is near realtime, so
                          </p>
                          <p>
                            <strong>{{_('History')}}</strong>
                            <br />
                            <img src="static/images/documentation/dashboard_top_indicators_door_history.png" alt="Dashboard top indicators history screenshot" />
                            <br />
                            Click on the door indicator to see the last 6 notifications. During loading of the dashboard the door changes for the last 24 hours are loaded from history.
                          </p>
                        </div>
                        <div class="row">
                          <h4>{{_('Date and time')}}</h4>
                          <p>
                            <strong><i class="fa fa-sun-o"></i> {{_('Day')}}</strong>
                            <br />
                            <img src="static/images/documentation/dashboard_top_indicators_online.png" alt="Dashboard top indicators online screenshot" />
                            <br />
                            The last indicator is the current time. When it is day time, a sun is shown.
                          </p>
                          <p>
                            <strong><i class="fa fa-moon-o"></i> {{_('Night')}}</strong>
                            <br />
                            <img src="static/images/documentation/dashboard_top_indicators_night.png" alt="Dashboard top indicators online screenshot" />
                            <br />
                            When the sun sets, the icon of the date time indicator in a moon.
                          </p>
                        </div>
                      </div>
                      <div class="tab-pane" id="usage-tab-dashboard-top-tiles">
                        <h3 class="lead">{{_('Top tiles')}}</h3>
                        <p>All tiles will be updated in realtime. When a switch is toggled, either by hand or by the system, the tiles will update instantly</p>
                        <img src="static/images/documentation/dashboard_top_tiles.gif" alt="Dashboard top indicators online screenshot" />
                        <div class="row">
                          <h4><span aria-hidden="true" class="glyphicon glyphicon-time"></span> {{_('Uptime')}}</h4>
                          <p>
                            The first tile shows the hardware uptime. And it shows three bars which indicates the load off the hardware. First bar is actual load, second is load during 5 minutes and last is load during 15 minutes.
                          </p>
                        </div>
                        <div class="row">
                          <h4><span aria-hidden="true" class="glyphicon glyphicon-flash"></span> {{_('Power usage in Watt')}}</h4>
                          <p>
                            The second tile shows the current power usage in Watts. The amount is calculated based on the power switch settings and what the state is of the switches. The bar shows a percentage of the max usage.
                          </p>
                        </div>
                        <div class="row">
                          <h4><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> {{_('Water flow in L/m')}}</h4>
                          <p>
                            The third tile shows the current water flow in liters per minute. The amount is calculated based on the power switch settings and what the state is of the switches. The bar shows a percentage of the max usage.
                          </p>
                        </div>
                        <div class="row">
                          <h4><span aria-hidden="true" class="glyphicon glyphicon-flash"></span> {{_('Total power in kWh')}}</h4>
                          <p>
                            The fourth tile shows the total power usage from the start of using this software. It will calculate the total power usage every 10 minutes based on all historical data. It is shown in kilo Watt per hour. When the power price is entered, it will show the costs of the powerbill and the amount of days it is calculated on.
                          </p>
                        </div>
                        <div class="row">
                          <h4><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> {{_('Total water in L')}}</h4>
                          <p>
                            The fith tile shows the total water usage from the start of using this software. It will calculate the total water usage every 10 minutes based on all historical data. It is shown in liters. When the water price is entered, it will show the costs of the waterbill and the amount of days it is calculated on.
                          </p>
                        </div>
                      </div>
                      <div class="tab-pane" id="usage-tab-dashboard-environment">
                        <h3 class="lead">{{_('Environment')}}</h3>
                        <img src="static/images/documentation/dashboard_environment.gif" alt="Dashboard top indicators online screenshot" class="alignright" />
                        <p>The environment section shows the current state of the environment. The environment is devided in three parts. There is a lighting system, a spray system and a heating system.</p>
                        <p>When a part is active the title is in color. If the title is gray that part is than not running or configured.</p>
                        <h4><span class="fa fa-lightbulb-o"></span> {{_('Lights')}}</h4>
                        <p>
                          The lights part give the basic information about how the lightsystem is configured. It shows the chosen mode out of 'clock' or 'weather'. There are no triggers or warnings used by the lightsystem.<br />
                          The state indicator is either green or red. Green means that it is switched on. When it is red, the lights are switched of<br />
                          The on value is the timestamp when the lights are turned on.<br />
                          The off valus is the timestamp when the lights will be turned off.<br />
                          The duration holds the amount of hours that the lights are on.
                        </p>
                        <h4><i class="fa fa-tint"></i> {{_('Sprayer')}}</h4>
                        <p>
                          The sprayer part give the basic information about how the spray system is configured. The spray system uses humidity sensors to determen the current and minimal humidity value. When the current value is below the minimal value a warning sign (<span aria-hidden="true" class="glyphicon glyphicon-warning-sign red"></span>) will be shown. There is no mode, the spray system just works on sensor data.<br />
                          The state indicator is either green or red. Green means that it is switched on. When it is red, the sprayer is switched of<br />
                          The current value shows the current humidity in percentage.<br />
                          The alarm min value shows the lowest value that is valid. When the current value become less then the alarm min value, an alarm message will be shown and the trigger to spraying is activated.
                        </p>
                        <h4><i class="fa fa-fire"></i> {{_('Heater')}}</h4>
                        <p>
                          The heater part give the basic information about how the heating system is configured. The heating system uses temperature sensors to determen the current, minimal and maximun temperature value. When the current value is outside the minimal or maximum value a warning sign (<span aria-hidden="true" class="glyphicon glyphicon-warning-sign red"></span>) will be shown.<br />
                          There are three modees available. 'Clock', 'Weather', 'Sensor'.<br />
                          The state indicator is either green or red. Green means that it is switched on. When it is red, the heater is switched of<br />
                          The current value shows the current temperature in degress.<br />
                          The alarm min value shows the lowest value that is valid. When the current value become less then the alarm min value, an alarm message will be shown and the trigger to heating is activated.<br />
                          The alarm max value shows the highest value that is valid. When the current value become more then the alarm max value, an alarm message will be shown and the heating is deactivated.
                        </p>
                      </div>
                      <div class="tab-pane" id="usage-tab-dashboard-graphs">
                        <h3 class="lead">{{_('Graphs')}}</h3>
                        <p>The graphs on the home are combined graphs from all temperature and humidity sensors. The gauge meters are realtime and show the current value. The historical graphs shows also the minimal and maximun value and will be updated once every 5 minutes.</p>
                        <p>Every sensor has his own type and a minimal and maximum value. To get the graph data all the data is combined and devided by the amount of sensors. This way the average of the sensors is used.</p>
                        <img src="static/images/documentation/dashboard_graphs.gif" alt="Dashboard top indicators online screenshot" />
                        <div class="row">
                          <h4><span aria-hidden="true" class="glyphicon glyphicon-tint"></span>/<span aria-hidden="true" class="glyphicon glyphicon-fire"></span> </span> {{_('Type')}}</h4>
                          <p>
                            There are multiple graph times. On the home there is a humidty and a temperature graph shown.
                            <ul>
                              <li><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> Humidity</li>
                              <li><span aria-hidden="true" class="glyphicon glyphicon-fire"></span> Temperature</li>
                            </ul>
                          </p>
                        </div>
                        <div class="row">
                          <h4>{{_('Last update')}}</h4>
                          <p>
                            When there is new data, the gauge part of the graph is updated and will also update the last update timestamp.
                          </p>
                        </div>
                        <div class="row">
                          <h4><span class="badge bg-red">{{_('warning')}}</span> {{_('warning')}}</h4>
                          <p>
                            When the current value is outside the minimal of maximum value a red warning badge is shown.
                          </p>
                        </div>
                        <div class="row">
                          <h4><i class="fa fa-calendar" title="{{_('Period')}}"></i> {{_('Period')}}</h4>
                          <img src="static/images/documentation/graph_period.png" class="alignright" />
                          <p>
                            With the calendar icon you can select multiple periods for the historical graph. The valid periods are:
                            <ul>
                              <li>Day</li>
                              <li>Week</li>
                              <li>Month</li>
                              <li>Year</li>
                            </ul>
                          </p>
                        </div>
                        <div class="row">
                          <h4><i class="fa fa-wrench" title="{{_('Options')}}"></i> {{_('Options')}}</h4>
                          <img src="static/images/documentation/graph_options.png" class="alignright" />
                          <p>
                            With the wrench you will get an options menu.
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="col-xs-3">
                    <!-- required for floating -->
                    <!-- Nav tabs -->
                    <ul class="nav nav-tabs tabs-right">
                      <li class="active">
                        <a data-toggle="tab" href="#usage-tab-dashboard-dashboard" title="{{_('Home')}}">{{_('Home')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-dashboard-top-indicators" title="{{_('Top indicators')}}">{{_('Top indicators')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-dashboard-top-tiles" title="{{_('Top tiles')}}">{{_('Top tiles')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-dashboard-environment" title="{{_('Environment')}}">{{_('Environment')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-dashboard-graphs" title="{{_('Graphs')}}">{{_('Graphs')}}</a>
                      </li>
                    </ul>
                  </div>
