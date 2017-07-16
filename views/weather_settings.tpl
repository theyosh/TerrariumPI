% include('inc/page_header.tpl')
        <div class="x_panel">
          <div class="x_title">
            <h2><span class="glyphicon glyphicon-info-sign" aria-hidden="true" title="{{_('Information')}}"></span> {{_('Help')}}<small></small></h2>
            <ul class="nav navbar-right panel_toolbox">
              <li>
                <a class="collapse-link"><i class="fa fa-chevron-down"></i></a>
              </li>
              <li>
                <a class="close-link"><i class="fa fa-close" title="{{_('Close')}}"></i></a>
              </li>
            </ul>
            <div class="clearfix"></div>
          </div>
          <div class="x_content" style="display:none">
            <p>{{_('Here you can configure the weather settings.')}} {{!_('Required fields are marked with \'%s\'.') % ('<span class="required">*</span>',)}}</p>
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
              <li>
                <strong>{{_('Temperature')}}</strong>: {{translations.get_translation('weather_field_temperature')}}
              </li>
            </ul>
          </div>
        </div>
        <form action="/api/config/weather" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
          <div class="row">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 id="deviceid">{{_('Weather')}} <small>...</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="location">{{_('Location')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" id="location" name="location" required="required" type="text" placeholder="{{_('Location')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{!translations.get_translation('weather_field_location')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="windspeed">{{_('Wind speed')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('weather_field_wind_speed')}}">
                        <select class="form-control" name="windspeed" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="ms">{{_('m/s')}}</option>
                          <option value="kmh">{{_('km/h')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature">{{_('Temperature')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('weather_field_temperature')}}">
                        <select class="form-control" name="temperature" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="C">C</option>
                          <option value="F">F</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="ln_solid"></div>
                  <div class="form-group">
                    <div class="col-md-11 col-sm-11 col-xs-12 text-center">
                      <button class="btn btn-success" type="submit">{{_('Submit')}}</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </form>
        <script type="text/javascript">
          $(document).ready(function() {
            var windspeed_selector = $("select[name='windspeed']").select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            });

            var temperature_selector = $("select[name='temperature']").select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            });

            $.get($('form').attr('action'),function(data){
              $('form h2 small').text(data.type);
              $('input[name="location"]').val(data.location);

              windspeed_selector.val(data.windspeed);
              windspeed_selector.trigger('change');
              temperature_selector.val(data.temperature);
              temperature_selector.trigger('change');
            });
          });
        </script>
% include('inc/page_footer.tpl')
