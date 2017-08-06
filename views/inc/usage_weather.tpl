                  <div class="col-xs-9">
                    <!-- Tab panes -->
                    <div class="tab-content">
                      <div class="tab-pane active" id="usage-tab-weather-weather">
                        <div class="interactive_screenshot">
                          <div id="screenshot_weather_forecast_current" class="click_area" title="{{_('Weather')}} {{_('Current')}}"></div>
                          <div id="screenshot_weather_forecast_day" class="click_area" title="{{_('Day forecast')}}"></div>
                          <div id="screenshot_weather_forecast_week" class="click_area" title="{{_('Week forecast')}}"></div>
                          <img src="static/images/documentation/weather_forecast.png" alt="{{_('Weather forecast screenshot')}}" />
                        </div>
                      </div>
                      <div class="tab-pane" id="usage-tab-weather-forecast-current">
                        <h3 class="lead">{{_('Weather')}} {{_('Current')}}</h3>
                        <img src="static/images/documentation/weather_current.gif" alt="{{_('Current weather widget screenshot')}}" class="thumbnail alignright" />
                        <p>{{_('The forecast widgets shows the forecast at current time and the location for which the forecast is valid. The data is loaded external from the external API source and is not measured by the software.')}}</p>
                        <p>{{_('It shows the current day and time for which the forecast is valid. And what temperature indicator is used.')}}</p>
                        <p>{{_('The forecast is based on the time of the day. During the day, a sun is used in the animation. During the night a moon is used.')}}</p>
                        <p>{{_('The sun rise and sun set are shown on the right side. The line that is bold is indicating the current state.')}}</p>
                        <p>{{_('The week forecast is shown at 13:00 hours of each day.')}}</p>
                      </div>
                      <div class="tab-pane" id="usage-tab-weather-forecast-day">
                        <h3 class="lead">{{_('Day forecast')}}</h3>
                        <img src="static/images/documentation/weather_forecast_day.png" alt="{{_('Weather day forecast screenshot')}}" class="img-thumbnail" /><br /><br />
                        <p>{{_('The day forecast shows the temperature per hour for 24 / 36 hours from now. The title holds the graph period.')}}</p>
                        <p>{{!_('Use the calendar icon %s in the title to select the period for the history graph.') % '<i class="fa fa-calendar"></i>'}}</p>
                      </div>
                      <div class="tab-pane" id="usage-tab-weather-forecast-week">
                        <h3 class="lead">{{_('Week forecast')}}</h3>
                        <img src="static/images/documentation/weather_forecast_week.png" alt="{{_('Week forecast screenshot')}}" class="img-thumbnail" /><br /><br />
                        <p>{{_('The week forecast shows the temperature per hour for 10 days from now. The title holds the graph period.')}}</p>
                        <p>{{!_('Use the calendar icon %s in the title to select the period for the history graph.') % '<i class="fa fa-calendar"></i>'}}</p>
                      </div>
                      <div class="tab-pane" id="usage-tab-weather-settings">
                        <h3 class="lead">{{_('Settings')}}</h3>
                        <p>{{!_('Enter the full URL of the API weather server. For use with Weather.com you need to get a free API key from %s. The temperature are read in Celsius degrees. It can be converted to Fahrenheit.') % '<a href="http://api.wunderground.com/" target="_blank">http://api.wunderground.com/</a>'}}</p>
                        <p>{{!_('All fields with a %s are required.') % '<span class="required">*</span>'}}</p>
                        <div class="row">
                          <div class="col-md-12 col-sm-12 col-xs-12">
                            <div class="x_panel">
                              <div class="x_content">
                                <div class="form-group">
                                  <label class="control-label col-md-3 col-sm-3 col-xs-12" for="location">{{_('Location')}} <span class="required">*</span></label>
                                  <div class="col-md-7 col-sm-6 col-xs-10">
                                    <input class="form-control" id="location" name="location" required="required" type="text" placeholder="{{_('Location')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{!translations.get_translation('weather_field_location')}}">
                                  </div>
                                </div><br /><br />
                                <div class="form-group">
                                  <label class="control-label col-md-3 col-sm-3 col-xs-12" for="windspeed">{{_('Wind speed')}} <span class="required">*</span></label>
                                  <div class="col-md-7 col-sm-6 col-xs-10">
                                    <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('weather_field_wind_speed')}}">
                                      <select class="form-control" name="windspeed" tabindex="-1" placeholder="{{_('Select an option')}}">
                                        <option value="ms">{{_('m/s')}}</option>
                                        <option value="kmh">{{_('Km/h')}}</option>
                                      </select>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                        <ul>
                          <li>
                            <strong>{{_('Location')}}</strong>: {{!translations.get_translation('weather_field_location')}}
                            <ul>
                              <li><strong>YR.no</strong>: https://www.yr.no/place/[COUNTRY]/[PROVANCE]/[CITY]</li>
                              <li><strong>Weather underground</strong>: http://api.wunderground.com/api/[YOUR_API_KEY]/<strong>geolookup/astronomy/hourly10day</strong>/q/[COUNTRY]/[CITY].json</li>
                            </ul>
                          </li>
                          <li>
                            <strong>{{_('Wind speed')}}</strong>: {{translations.get_translation('weather_field_wind_speed')}}
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
                        <a data-toggle="tab" href="#usage-tab-weather-weather" title="{{_('Weather')}}">{{_('Weather')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-weather-forecast-current" title="{{_('Weather')}} {{_('Current')}}">{{_('Weather')}} {{_('Current')}}</a>
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
