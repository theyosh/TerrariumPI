% include('inc/page_header.tpl')
        <div class="x_panel help">
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
          <div class="x_content">
            <p>{{_('Here you can configure your TerrariumPI server.')}} {{!_('Required fields are marked with \'%s\'.') % ('<span class="required">*</span>',)}}</p>
            <ul>
              <li>
                <strong>{{_('Weather location')}}</strong>: {{!translations.get_translation('weather_field_location_long')}}
              </li>
            </ul>
          </div>
        </div>
        <div class="x_panel reboot">
          <div class="x_title">
            <h2><span class="glyphicon glyphicon-info-sign" aria-hidden="true" title="{{_('System actions')}}"></span> {{_('System actions')}}<small></small></h2>
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
          <div class="x_content" style="text-align: center">
            <div class="col-md-6 col-sm-6 col-xs-6">
              <p>{{_('Here you can reboot your TerrariumPI server. You will have to confirm the action when clicked.')}}</p>
              <p>
                <button type="button" id="reboot_pi"><span class="glyphicon glyphicon-refresh red" style="font-size: 12rem" aria-hidden="true" title="{{_('Reboot')}}"></button>
              </p>
            </div>
            <div class="col-md-6 col-sm-6 col-xs-6">
              <p>{{_('Here you can shutdown your TerrariumPI server. You will have to confirm the action when clicked.')}}</p>
              <p>
                <button type="button" id="shutdown_pi"><span class="glyphicon glyphicon-off red" style="font-size: 12rem" aria-hidden="true" title="{{_('Shutdown')}}"></button>
              </p>
            </div>
          </div>
        </div>
        <div class="row">
          <form action="/api/config/system" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 id="deviceid">{{_('TerrariumPI')}} <small>{{device}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="language">{{_('Language')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_language')}}">
                        <select class="form-control" required="required" name="language" tabindex="-1" placeholder="{{_('Select an option')}}">
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="location">{{_('Weather location')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" id="location" name="location" type="text" placeholder="{{_('Weather location')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{!translations.get_translation('weather_field_location')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="windspeed_indicator">{{_('Wind speed indicator')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('weather_field_wind_speed')}}">
                        <select class="form-control" name="windspeed_indicator" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="ms">{{_('m/s')}}</option>
                          <option value="kmh">{{_('Km/h')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature_indicator">{{_('Temperature indicator')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_temperature_indicator')}}">
                        <select class="form-control" required="required" name="temperature_indicator" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="C">{{_('Celsius')}}</option>
                          <option value="F">{{_('Fahrenheit')}}</option>
                          <option value="K">{{_('Kelvin')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="distance_indicator">{{_('Distance indicator')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_distance_indicator')}}">
                        <select class="form-control" required="required" name="distance_indicator" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="cm">{{_('Centimetre')}}</option>
                          <option value="inch">{{_('Inches')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="volume_indicator">{{_('Volume indicator')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_volume_indicator')}}">
                        <select class="form-control" required="required" name="volume_indicator" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="L">{{_('Litres')}}</option>
                          <option value="usgall">{{_('US Gallons')}}</option>
                          <option value="ukgall">{{_('UK Gallons')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="admin">{{_('Admin name')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="admin" required="required" type="text" placeholder="{{_('Admin name')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_admin')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="new_password">{{_('New admin password')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="new_password" type="password" placeholder="{{_('New admin password')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_new_password')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cur_password">{{_('Current admin password')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="cur_password" type="password" placeholder="{{_('Current admin password')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_current_password')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="always_authenticate">{{_('Authentication')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_always_authentication')}}">
                        <select class="form-control" name="always_authenticate" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="true">{{_('Full authentication')}}</option>
                          <option value="false">{{_('Changes only')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="soundcard">{{_('Soundcard')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_soundcard')}}">
                        <select class="form-control" required="required" name="soundcard" tabindex="-1" placeholder="{{_('Select an option')}}">
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="power_usage">{{_('External calendar')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="external_calendar_url" type="text" placeholder="{{_('External calendar url')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_external_calendar_url')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="horizontal_graph_legend">{{_('Graph legend layout')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_horizontal_graph_legend')}}">
                        <select class="form-control" name="horizontal_graph_legend" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="true">{{_('Horizontal')}}</option>
                          <option value="false">{{_('Vertical')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="graph_smooth_value">{{_('Graph smoothing value')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="graph_smooth_value" required="required" type="text" pattern="[0-9]+" placeholder="{{_('Graph smoothing value')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_graph_smooth_value')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="graph_show_min_max_gauge">{{_('Show min and max values in gauge graphs')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_graph_show_min_max_gauge')}}">
                        <select class="form-control" name="graph_show_min_max_gauge" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="true">{{_('True')}}</option>
                          <option value="false">{{_('False')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="hide_environment_on_dashboard">{{_('Hide environment summary on the dashboard')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_hide_environment_on_dashboard')}}">
                        <select class="form-control" name="hide_environment_on_dashboard" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="true">{{_('True')}}</option>
                          <option value="false">{{_('False')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="sensor_gauge_overview">{{_('Show all sensors gauges on 1 page')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_all_sensors_gauges_page')}}">
                        <select class="form-control" name="sensor_gauge_overview" required="required" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option value="true">{{_('True')}}</option>
                          <option value="false">{{_('False')}}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="power_usage">{{_('Pi power usage in W')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="power_usage" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Pi power usage in W')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_pi_power')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="power_price">{{_('Power price')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="power_price" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Power price')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_power_price')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="water_price">{{_('Water price')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="water_price" required="required" type="text" pattern="[0-9\.]+" placeholder="{{_('Water price')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_water_price')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="host">{{_('IP or hostname')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="host" required="required" type="text" placeholder="{{_('IP or hostname')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_hostname')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="port">{{_('Port number')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="port" required="required" type="text" placeholder="{{_('Port number')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_port_number')}}">
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2><span aria-hidden="true" class="glyphicon glyphicon-cloud-download"></span> {{_('Meross Cloud')}}</h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="meross_username">{{_('Meross Cloud username')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="meross_username" type="text" placeholder="{{_('Meross Cloud username')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_meross_username')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="meross_password">{{_('Meross Cloud password')}}</label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="meross_password" type="password" placeholder="{{_('Meross Cloud password')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_meross_password')}}">
                      </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="ln_solid"></div>
            <div class="form-group">
              <div class="col-md-11 col-sm-11 col-xs-12 text-center">
                <button class="btn btn-success" type="submit">{{_('Submit')}}</button>
              </div>
            </div>
          </form>
        </div>
        <script type="text/javascript">
          $(document).ready(function() {
            init_form_settings('system');

            var language_selector = $("select[name='language']").select2({
                placeholder: '{{_('Select an option')}}',
                allowClear: false,
                minimumResultsForSearch: Infinity
            });

            var windspeed_indicator = $("select[name='windspeed_indicator']").select2({
                placeholder: '{{_('Select an option')}}',
                allowClear: false,
                minimumResultsForSearch: Infinity
            });

            var volume_indicator = $("select[name='volume_indicator']").select2({
                placeholder: '{{_('Select an option')}}',
                allowClear: false,
                minimumResultsForSearch: Infinity
            });

            var soundcard_selector = $("select[name='soundcard']").select2({
                placeholder: '{{_('Select an option')}}',
                allowClear: false,
                minimumResultsForSearch: Infinity
            });

            $("select[name='temperature_indicator'],select[name='distance_indicator'],select[name='always_authenticate'],select[name='horizontal_graph_legend'],select[name='sensor_gauge_overview'],select[name='hide_environment_on_dashboard'],select[name='graph_show_min_max_gauge']").select2({
                placeholder: '{{_('Select an option')}}',
                allowClear: false,
                minimumResultsForSearch: Infinity
            });

            $.get('/api/audio/hardware',function(data) {
              $(Object.keys(data.audiohardware)).each(function(index,hardware_device){
                soundcard_selector.append($('<option>').attr({'value':hardware_device}).text(data.audiohardware[hardware_device].name));
              });

              $.get('/api/config/weather',function(data) {
                $('input[name="location"]').val(data.location);
                windspeed_indicator.val(data.windspeed_indicator).trigger('change');
                volume_indicator.val(data.volume_indicator).trigger('change');

                $.get($('form').attr('action'),function(data){
                  $.each(data.available_languages.sort(),function(index,value){
                    language_selector.append($('<option>').attr({'value':value}).text(value));
                  });
                  $.each(Object.keys(data), function(key,value){
                    var config_field = $('form [name="' + value + '"]');
                    if (config_field.length >= 1) {
                      switch (config_field.prop('type').toLowerCase()) {
                        case 'text':
                        case 'password':
                          config_field.val(data[value]);
                          break;

                        case 'select-one':
                        case 'select-multiple':
                          config_field.val(data[value]).trigger('change');
                          break;
                      }
                    }
                  });
                  setContentHeight();
                });
              });
            });

            var reboot_html = $('<div class="offline_animation"><div class="message"></div><div class="blackscreen"></div></div>');
            $('button#reboot_pi').on('click',function(){
              if (confirm('{{_("Are you sure you want to reboot Terrarium PI?")}}')) {

                $('html').addClass('_off');
                $('body').addClass('_off').append(reboot_html);

                $('.message').html('<h1>{{_("Rebooting")}}...</h1><span class="timer">0 {{_("seconds")}}</span>');

                var timer = 1;
                setInterval(function(){
                  globals.reboot = true;
                  $('body._off div.offline_animation div.message span.timer').text(timer++ + ' {{_("seconds")}}');
                },1000);

                $.post('/api/reboot');
              }
            });

            $('button#shutdown_pi').on('click',function(){
              if (confirm('{{_("Are you sure you want to shutdown Terrarium PI?")}}')) {

                $('html').addClass('_off');
                $('body').addClass('_off').append(reboot_html);

                $('.message').html('<h1>{{_("Shutdown!")}}</h1>{{_("bye bye")}}');

                $.post('/api/shutdown');
              }
            });
          });
        </script>
% include('inc/page_footer.tpl')
