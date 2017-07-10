                  <h2>{{_('Weather')}}</h2>
                  <div class="col-xs-9">
                    <!-- Tab panes -->
                    <div class="tab-content">
                      <div class="tab-pane active" id="usage-tab-weather-weather">
                        <div class="interactive_screenshot">
                          <div id="screenshot_weather_forecast_current" class="click_area" title="{{_('Weather')}} {{_('current')}}"></div>
                          <div id="screenshot_weather_forecast_day" class="click_area" title="{{_('Day forecast')}}"></div>
                          <div id="screenshot_weather_forecast_week" class="click_area" title="{{_('Week forecast')}}"></div>
                          <img src="static/images/documentation/weather_forecast.png" alt="{{_('Weather forceast screenshot')}}" />
                        </div>
                      </div>
                      <div class="tab-pane" id="usage-tab-weather-forecast-current">
                        <h3 class="lead">{{_('Weather')}} {{_('current')}}</h3>
                        <img src="static/images/documentation/weather_forecast.gif" alt="Dashboard top indicators online screenshot" class="alignright" />
                        <p>The forecast widgest shows the forecast at current time. The data is loaded external and is not measered by the software.</p>
                        <p>It shows the current day and time for which the forecast is valid. And what indicator is used.</p>
                        <p>The forecast is based on the time of the day. During the day, a sun is used in the animation. During the night a moon is used.</p>
                        <p>The sun rise and sun set are shown on the right side. The line that is bold is indicating the current state.</p>
                        <p>The week forecast is shown at a 24 hours interval. Which means current forecast is 10 AM, all the week forecast are shown at 10 AM.</p>
                      </div>
                      <div class="tab-pane" id="usage-tab-weather-forecast-day">
                        <h3 class="lead">{{_('Day forecast')}}</h3>
                        <img src="static/images/documentation/weather_forecast_day.png" alt="Dashboard top indicators online screenshot" />
                        <p></p>
                      </div>
                      <div class="tab-pane" id="usage-tab-weather-forecast-week">
                        <h3 class="lead">{{_('Week forecast')}}</h3>
                        <img src="static/images/documentation/weather_forecast_week.png" alt="Dashboard top indicators online screenshot" />
                        <p></p>
                      </div>
                      <div class="tab-pane" id="usage-tab-weather-settings">
                        <h3 class="lead">{{_('Settings')}}</h3>
                        <p>Settings for weather</p>
                        <div class="row">
                          <h4>{{_('Location')}}</h4>
                          <p>{{translations.get_translation('weather_field_location')}}</p>
                        </div>
                        <div class="row">
                          <h4>{{_('Wind speed')}}</h4>
                          <p>{{translations.get_translation('weather_field_wind_speed')}}</p>
                        </div>

                        <div class="row">
                          <h4>{{_('Temperature')}}</h4>
                          <p>{{translations.get_translation('weather_field_temperature')}}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="col-xs-3">
                    <!-- required for floating -->
                    <!-- Nav tabs -->
                    <ul class="nav nav-tabs tabs-right">
                      <li class="active">
                        <a data-toggle="tab" href="#usage-tab-weather-weather" title="{{_('Weather')}}">{{_('Weather')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-weather-forecast-current" title="{{_('Weather')}} {{_('current')}}">{{_('Weather')}} {{_('current')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-weather-forecast-day" title="{{_('Day forecast')}}">{{_('Day forecast')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-weather-forecast-week" title="{{_('Week forecast')}}">{{_('Week forecast')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-weather-settings" title="{{_('Settings')}}">{{_('Settings')}}</a>
                      </li>
                    </ul>
                  </div>
