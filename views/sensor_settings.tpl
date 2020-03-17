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
            <p>{{_('Here you can configure your sensors.')}} {{!_('Required fields are marked with \'%s\'.') % ('<span class="required">*</span>',)}}</p>
            <ul>
              <li>
                <strong>{{_('Hardware')}}</strong>: {{!translations.get_translation('sensor_field_hardware')}}
              </li>
              <li>
                <strong>{{_('Address')}}</strong>: {{!translations.get_translation('sensor_field_address')}}
              </li>
              <li>
                <strong>{{_('Type')}}</strong>: {{!translations.get_translation('sensor_field_type')}}
              </li>
              <li>
                <strong>{{_('Name')}}</strong>: {{translations.get_translation('sensor_field_name')}}
              </li>
              <li>
                <strong>{{_('Alarm min')}}</strong>: {{translations.get_translation('sensor_field_alarm_min')}}
              </li>
              <li>
                <strong>{{_('Alarm max')}}</strong>: {{translations.get_translation('sensor_field_alarm_max')}}
              </li>
              <li>
                <strong>{{_('Limit min')}}</strong>: {{translations.get_translation('sensor_field_limit_min')}}
              </li>
              <li>
                <strong>{{_('Limit max')}}</strong>: {{translations.get_translation('sensor_field_limit_max')}}
              </li>
              <li>
                <strong>{{_('Max diff')}}</strong>: {{translations.get_translation('sensor_field_max_diff')}}
              </li>
              <li>
                <strong>{{_('Current')}}</strong>: {{translations.get_translation('sensor_field_current')}}
              </li>
            </ul>
          </div>
        </div>
        <form action="/api/config/sensors" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
          <div class="row submit">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="ln_solid"></div>
              <div class="form-group">
                <div class="col-md-11 col-sm-11 col-xs-12 text-center">
                  <button class="btn btn-success" type="submit">{{_('Submit')}}</button>
                </div>
              </div>
            </div>
          </div>
        </form>
        <div class="modal fade add-form" tabindex="-1" role="dialog" aria-hidden="true">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">
                  <span aria-hidden="true">×</span>
                </button>
                <h4 class="modal-title">{{_('Add new sensor')}}</h4>
              </div>
              <div class="modal-body">
                <div class="row sensor">
                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="x_panel">
                      <div class="x_title">
                        <h2 class="temperature"><span aria-hidden="true" class="glyphicon glyphicon-fire"></span> {{_('Temperature sensor')}} <span class="title">{{_('new')}}</span></h2>
                        <h2 class="humidity" style="display:none"><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> {{_('Humidity sensor')}} <span class="title">{{_('new')}}</span></h2>
                        <h2 class="moisture" style="display:none"><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> {{_('Moisture sensor')}} <span class="title">{{_('new')}}</span></h2>
                        <h2 class="conductivity" style="display:none"><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> {{_('Conductivity sensor')}} <span class="title">{{_('new')}}</span></h2>
                        <h2 class="distance" style="display:none"><span aria-hidden="true" class="glyphicon glyphicon-signal"></span> {{_('Distance sensor')}} <span class="title">{{_('new')}}</span></h2>
                        <h2 class="ph" style="display:none"><span aria-hidden="true" class="glyphicon glyphicon-scale"></span> {{_('pH sensor')}} <span class="title">{{_('new')}}</span></h2>
                        <h2 class="light uva uvb uvi" style="display:none"><span aria-hidden="true" class="glyphicon glyphicon-adjust"></span> {{_('Light sensor')}} <span class="title">{{_('new')}}</span></h2>
                        <h2 class="fertility" style="display:none"><span aria-hidden="true" class="glyphicon glyphicon-grain"></span> {{_('Fertility sensor')}} <span class="title">{{_('new')}}</span></h2>
                        <h2 class="co2" style="display:none"><span aria-hidden="true" class="glyphicon glyphicon-tree-conifer"></span> {{_('CO2 sensor')}} <span class="title">{{_('new')}}</span></h2>
                        <h2 class="volume" style="display:none"><span aria-hidden="true" class="glyphicon glyphicon-signal"></span> {{_('Volume sensor')}} <span class="title">{{_('new')}}</span></h2>
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
                        <div class="row">
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="sensor_[nr]_hardwaretype">{{_('Hardware')}}</label>
                            <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{!translations.get_translation('sensor_field_hardware')}}">
                              <select class="form-control" name="sensor_[nr]_hardwaretype" tabindex="-1" placeholder="{{_('Select an option')}}" required="required">
                                <option value="">{{_('Select an option')}}</option>
                                <option value="owfs">{{_('OWFS')}}</option>
                                <option value="dht11">{{_('DHT11')}}</option>
                                <option value="dht22">{{_('DHT22')}}</option>
                                <option value="am2302">{{_('AM2302')}}</option>
                                <option value="sht2x">{{_('SHT2X')}}</option>
                                <option value="sht3x">{{_('SHT3X')}}</option>
                                <option value="sht3xd">{{_('SHT3XD')}}</option>
                                <option value="htu21d">{{_('HTU21D')}}</option>
                                <option value="si7021">{{_('SI7021')}}</option>
                                <option value="bme280">{{_('BME280 / BMP280')}}</option>
                                <option value="chirp">{{_('Chirp')}}</option>
                                <option value="w1">{{_('1Wire')}}</option>
                                <option value="ytxx-digital">{{_('YTXX-digital')}}</option>
                                <option value="remote">{{_('Remote')}}</option>
                                <option value="script">{{_('Custom script')}}</option>
                                <option value="hc-sr04">{{_('HC-SR04')}}</option>
                                <option value="sku-sen0161">{{_('pH SKU-SEN0161')}}</option>
                                <option value="veml6075">{{_('VEML6075')}}</option>
                                <option value="miflora">{{_('MiFlora')}}</option>
                                <option value="mitemp">{{_('Mi Temperature & Humidity')}}</option>
                                <option value="mh-z19">{{_('mh-z19')}}</option>
                                <option value="k30co2">{{_('K30 CO2')}}</option>
                                <option value="cozirco2">{{_('COZIR CO2')}}</option>
                                <option value="mlx90614">{{_('MLX90614')}}</option>
                                <option value="am2320">{{_('AM2320')}}</option>
                                <option value="amg8833">{{_('AMG8833')}}</option>
                              </select>
                            </div>
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="sensor_[nr]_type">{{_('Type')}}</label>
                            <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{!translations.get_translation('sensor_field_type')}}">
                              <select class="form-control" name="sensor_[nr]_type" tabindex="-1" placeholder="{{_('Select an option')}}" required="required">
                                <option value="">{{_('Select an option')}}</option>
                                <option value="temperature">{{_('Temperature')}}</option>
                                <option value="humidity">{{_('Humidity')}}</option>
                                <option value="moisture">{{_('Moisture')}}</option>
                                <option value="conductivity">{{_('Conductivity')}}</option>
                                <option value="distance">{{_('Distance')}}</option>
                                <option value="ph">{{_('pH')}}</option>
                                <option value="light">{{_('Light')}}</option>
                                <option value="uva">{{_('UVA')}}</option>
                                <option value="uvb">{{_('UVB')}}</option>
                                <option value="uvi">{{_('UV Index')}}</option>
                                <option value="fertility">{{_('Fertility')}}</option>
                                <option value="co2">{{_('CO2')}}</option>
                                <option value="volume">{{_('Volume')}}</option>
                              </select>
                            </div>
                          </div>
                          <div class="col-md-4 col-sm-4 col-xs-12 form-group">
                            <label for="sensor_[nr]_address">{{_('Address')}}</label>
                            <input class="form-control" name="sensor_[nr]_address" placeholder="{{_('Address')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('sensor_field_address')}}">
                            <input class="form-control" name="sensor_[nr]_id" placeholder="{{_('ID')}}" readonly="readonly" type="hidden">
                          </div>
                          <div class="col-md-4 col-sm-4 col-xs-12 form-group">
                            <label for="sensor_[nr]_name">{{_('Name')}}</label>
                            <input class="form-control" name="sensor_[nr]_name" placeholder="{{_('Name')}}" type="text" required="required" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{!translations.get_translation('sensor_field_name')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="sensor_[nr]_alarm_min">{{_('Alarm min')}}</label>
                            <input class="form-control" name="sensor_[nr]_alarm_min" placeholder="{{_('Alarm min')}}" type="text" required="required" pattern="[0-9\.-]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('sensor_field_alarm_min')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="sensor_[nr]_alarm_max">{{_('Alarm max')}}</label>
                            <input class="form-control" name="sensor_[nr]_alarm_max" placeholder="{{_('Alarm max')}}" type="text" required="required" pattern="[0-9\.-]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('sensor_field_alarm_max')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="sensor_[nr]_min">{{_('Limit min')}}</label>
                            <input class="form-control" name="sensor_[nr]_limit_min" placeholder="{{_('Limit min')}}" type="text" required="required" pattern="[0-9\.-]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('sensor_field_limit_min')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="sensor_[nr]_max">{{_('Limit max')}}</label>
                            <input class="form-control" name="sensor_[nr]_limit_max" placeholder="{{_('Limit max')}}" type="text" required="required" pattern="[0-9\.-]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('sensor_field_limit_max')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="sensor_[nr]_max_diff">{{_('Max diff')}}</label>
                            <input class="form-control" name="sensor_[nr]_max_diff" placeholder="{{_('Max diff')}}" type="text" required="required" pattern="[0-9\.-]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('sensor_field_max_diff')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="sensor_[nr]_current">{{_('Current')}}</label>
                            <input class="form-control" name="sensor_[nr]_current" placeholder="{{_('Current')}}" readonly="readonly" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('sensor_field_current')}}">
                          </div>
                        </div>
                        <div class="row chirp_calibration" style="display:none;">
                          <div class="col-md-4 col-sm-4 col-xs-4 form-group">
                            <label for="sensor_[nr]_min_moist">{{_('Min moist value')}}</label>
                            <input class="form-control" name="sensor_[nr]_min_moist" placeholder="{{_('Min moist value')}}" required="required" type="text" pattern="[0-9\.]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('sensor_field_min_moist')}}">
                          </div>
                          <div class="col-md-4 col-sm-4 col-xs-4 form-group">
                            <label for="sensor_[nr]_max_moist">{{_('Max moist value')}}</label>
                            <input class="form-control" name="sensor_[nr]_max_moist" placeholder="{{_('Max moist value')}}" required="required" type="text" pattern="[0-9\.-]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('sensor_field_max_moist')}}">
                          </div>
                          <div class="col-md-4 col-sm-4 col-xs-4 form-group">
                            <label for="sensor_[nr]_temperature_offset">{{_('Temperature offset')}}</label>
                            <input class="form-control" name="sensor_[nr]_temp_offset" placeholder="{{_('Temperature offset')}}" required="required" type="text" pattern="[0-9\.\-]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('sensor_field_temperature_offset')}}">
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">{{_('Close')}}</button>
                <button type="button" class="btn btn-primary">{{_('Add')}}</button>
              </div>
            </div>
          </div>
        </div>
        <script type="text/javascript">
          $(document).ready(function() {
            // Create add button
            init_form_settings('sensor');

            $('select[name^="sensor_[nr]_"]').select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            }).on('change',function() {
              if (this.name.indexOf('hardwaretype') >= 0) {
                var chirp_sensor = ('chirp' === this.value);
                if (chirp_sensor) {
                  $(this).parents('.x_content').find('.row.chirp_calibration input').attr('required','required');
                } else {
                  $(this).parents('.x_content').find('.row.chirp_calibration input').removeAttr('required');
                }
                $(this).parents('.x_content').find('.row.chirp_calibration').toggle(chirp_sensor);

                var address_field = $("input[name='" + this.name.replace('hardwaretype','address') + "']");
                address_field.attr("readonly", this.value == 'owfs' || this.value == 'w1').off('change');

                if ('remote' === this.value) {
                  address_field.on('change',function(){
                      parse_remote_data(address_field,this.value);
                  });
                }
              } else if (this.name.indexOf('type') >= 0 && this.value != '') {
                $(this).parentsUntil('.row').find('h2').hide().filter('.' + this.value).show();
              }
            }).val(null).trigger('change');

            // Load existing switches
            $.get($('form').attr('action'),function(json_data){
              $.each(sortByKey(json_data.sensors,'name'), function(index,sensor_data) {
                add_sensor_setting_row(sensor_data);
                update_sensor(sensor_data);
              });
              reload_reload_theme();
            });
          });
        </script>
% include('inc/page_footer.tpl')
