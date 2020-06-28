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
            <p>{{_('Here you can configure your power switches.')}} {{!_('Required fields are marked with \'%s\'.') % ('<span class="required">*</span>',)}}</p>
            <ul>
              <li>
                <strong>{{_('Hardware')}}</strong>: {{!translations.get_translation('switch_field_hardware')}} {{!_('When you have a %s type switch added the audio player will not work. More information can be found here: %s.') % ('<strong>pwm-dimmer</strong>','<a href="http://www.raspberry-projects.com/pi/programming-in-c/pwm/using-the-pwm-pin" target="_blank">http://www.raspberry-projects.com/pi/programming-in-c/pwm/using-the-pwm-pin</a>')}}
              </li>
              <li>
                <strong>{{_('Address')}}</strong>: {{!translations.get_translation('switch_field_address')}}
              </li>
              <li>
                <strong>{{_('Name')}}</strong>: {{translations.get_translation('switch_field_name')}}
              </li>
              <li>
                <strong>{{_('Power usage in Watt')}}</strong>: {{translations.get_translation('switch_field_power_wattage')}}
              </li>
              <li>
                <strong>{{_('Water flow in L/m')}}</strong>: {{translations.get_translation('switch_field_water_flow')}}
              </li>
              <li>
                <strong>{{_('Timer')}}</strong>: {{translations.get_translation('switch_field_timer_enabled')}}
              </li>
              <li>
                <strong>{{_('Timer start time')}}</strong>: {{!translations.get_translation('switch_field_timer_start')}}
              </li>
              <li>
                <strong>{{_('Timer stop time')}}</strong>: {{translations.get_translation('switch_field_timer_stop')}}
              </li>
              <li>
                <strong>{{_('Timer on duration')}}</strong>: {{translations.get_translation('switch_field_timer_on_duration')}}
              </li>
              <li>
                <strong>{{_('Timer off duration')}}</strong>: {{translations.get_translation('switch_field_timer_off_duration')}}
              </li>
              <li>
                <strong>{{_('Dimmer action duration')}}</strong>: {{!translations.get_translation('switch_field_dimmer_duration')}}
              </li>
              <li>
                <strong>{{_('Dimmer on duration')}}</strong>: {{translations.get_translation('switch_field_dimmer_on_duration')}}
              </li>
              <li>
                <strong>{{_('Dimmer on percentage')}}</strong>: {{translations.get_translation('switch_field_dimmer_on_percentage')}}
              </li>
              <li>
                <strong>{{_('Dimmer off duration')}}</strong>: {{translations.get_translation('switch_field_dimmer_off_duration')}}
              </li>
              <li>
                <strong>{{_('Dimmer off percentage')}}</strong>: {{translations.get_translation('switch_field_dimmer_off_percentage')}}
              </li>
            </ul>
          </div>
        </div>
        <form action="/api/config/switches" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
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
                <h4 class="modal-title">{{_('Add new switch')}}</h4>
              </div>
              <div class="modal-body">
                <div class="row switch">
                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="x_panel">
                      <div class="x_title">
                        <h2><span aria-hidden="true" class="glyphicon glyphicon-flash"></span> {{_('Switch')}} <span class="title">{{_('new')}}</span> <small class="current_usage"></small> <small class="total_usage"></small></h2>
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
                            <label for="switch_[nr]_hardwaretype">{{_('Hardware')}}</label>
                            <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{!translations.get_translation('switch_field_hardware')}}">
                              <select class="form-control" name="switch_[nr]_hardwaretype" tabindex="-1" placeholder="{{_('Select an option')}}" required="required">
                                <option value="">{{_('Select an option')}}</option>
                                <option value="ftdi">{{_('FTDI')}}</option>
                                <option value="gpio">{{_('GPIO')}}</option>
                                <option value="gpio-inverse">{{_('GPIO Inverse')}}</option>
                                <option value="8relay-stack_v1">{{_('8-RELAYS Stack (v1 & v2)')}}</option>
                                <option value="8relay-stack_v3">{{_('8-RELAYS Stack (v3)')}}</option>
                                <option value="pwm-dimmer">{{_('PWM Dimmer')}}</option>
                                <option value="dc-dimmer">{{_('DC Dimmer')}}</option>
                                <option value="brightpi">{{_('Bright Pi')}}</option>
                                <option value="pca9685-dimmer">{{_('PCA9685 Dimmer')}}</option>
                                <option value="irf520-dimmer">{{_('IRF520 Mosfet Dimmer')}}</option>
                                <option value="remote">{{_('Remote')}}</option>
                                <option value="remote-dimmer">{{_('Remote Dimmer')}}</option>
                                <option value="eg-pm-usb">{{_('Energenie USB')}}</option>
                                <option value="eg-pm-lan">{{_('Energenie LAN')}}</option>
                                <option value="eg-pm-rf">{{_('Energenie Pi-Mote')}}</option>
                                <option value="wemo">{{_('WeMo')}}</option>
                                <option value="mss425e">{{_('MSS425E')}}</option>
                                <option value="sonoff">{{_('Sonoff')}}</option>
                                <option value="denkovi_v2_4">{{_('DenkoviV2 4 relays')}}</option>
                                <option value="denkovi_v2_8">{{_('DenkoviV2 8 relays')}}</option>
                                <option value="denkovi_v2_16">{{_('DenkoviV2 16 relays')}}</option>
                                <option value="tplinkkasa">{{_('TP-Link Kasa')}}</option>
                                <option value="script">{{_('Custom script')}}</option>
                              </select>
                            </div>
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="switch_[nr]_address">{{_('Address')}}</label>
                            <input class="form-control" name="switch_[nr]_address" placeholder="{{_('Address')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_address')}}">
                            <input class="form-control" name="switch_[nr]_id" placeholder="{{_('ID')}}" readonly="readonly" type="hidden">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                            <label for="switch_[nr]_name">{{_('Name')}}</label>
                            <input class="form-control" name="switch_[nr]_name" placeholder="{{_('Name')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_name')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="switch_[nr]_power_wattage">{{_('Power usage in Watt')}}</label>
                            <input class="form-control" name="switch_[nr]_power_wattage" placeholder="{{_('Power usage in Watt')}}" required="required" type="text" pattern="[0-9\.]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_power_wattage')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="switch_[nr]_water_flow">{{_('Water flow in L/m')}}</label>
                            <input class="form-control" name="switch_[nr]_water_flow" placeholder="{{_('Water flow in L/m')}}" required="required" type="text" pattern="[0-9\.]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_water_flow')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                            <label for="switch_[nr]_timer_enabled">{{_('Timer')}}</label>
                            <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{!translations.get_translation('switch_field_timer_enabled')}}">
                              <select class="form-control" name="switch_[nr]_timer_enabled" tabindex="-1" placeholder="{{_('Select an option')}}" required="required">
                                <option value="">{{_('Select an option')}}</option>
                                <option value="true">{{_('Enabled')}}</option>
                                <option value="false">{{_('Disabled')}}</option>
                              </select>
                            </div>
                          </div>
                        </div>
                        <div class="row dimmer" style="display:none;">
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="switch_[nr]_dimmer_duration">{{_('Dimmer action duration')}}</label>
                            <input class="form-control" name="switch_[nr]_dimmer_duration" placeholder="{{_('Dimmer action duration')}}" required="required" type="text" pattern="[0-9\.]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_dimmer_duration')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="switch_[nr]_dimmer_step">{{_('Dimmer environment step')}}</label>
                            <input class="form-control" name="switch_[nr]_dimmer_step" placeholder="{{_('Dimmer environment step in %')}}" required="required" type="text" pattern="[0-9\.-]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_dimmer_step')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="switch_[nr]_dimmer_on_duration">{{_('Dimmer on duration')}}</label>
                            <input class="form-control" name="switch_[nr]_dimmer_on_duration" placeholder="{{_('Dimmer on duration')}}" required="required" type="text" pattern="[0-9\.]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_dimmer_on_duration')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="switch_[nr]_dimmer_on_percentage">{{_('Dimmer on percentage')}}</label>
                            <input class="form-control" name="switch_[nr]_dimmer_on_percentage" placeholder="{{_('Dimmer on percentage')}}" required="required" type="text" pattern="[0-9\.]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_dimmer_on_percentage')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="switch_[nr]_dimmer_off_duration">{{_('Dimmer off duration')}}</label>
                            <input class="form-control" name="switch_[nr]_dimmer_off_duration" placeholder="{{_('Dimmer off duration')}}" required="required" type="text" pattern="[0-9\.]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_dimmer_off_duration')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="switch_[nr]_dimmer_off_percentage">{{_('Dimmer off percentage')}}</label>
                            <input class="form-control" name="switch_[nr]_dimmer_off_percentage" placeholder="{{_('Dimmer off percentage')}}" required="required" type="text" pattern="[0-9\.]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_dimmer_off_percentage')}}">
                          </div>
                        </div>
                        <div class="row timer" style="display:none;">
                          <div class="col-md-3 col-sm-3 col-xs-6 form-group">
                            <label for="switch_[nr]_timer_start">{{_('Timer start time')}}</label>
                            <input class="form-control" name="switch_[nr]_timer_start" placeholder="{{_('Timer start time')}}" required="required" type="text" value="00:00" pattern="[0-9: APM]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_timer_start')}}">
                          </div>
                          <div class="col-md-3 col-sm-3 col-xs-6 form-group">
                            <label for="switch_[nr]_timer_stop">{{_('Timer stop time')}}</label>
                            <input class="form-control" name="switch_[nr]_timer_stop" placeholder="{{_('Timer stop time')}}" required="required" type="text" value="00:00" pattern="[0-9: APM]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_timer_stop')}}">
                          </div>
                          <div class="col-md-3 col-sm-2 col-xs-6 form-group">
                            <label for="switch_[nr]_timer_on_duration">{{_('Timer on duration')}}</label>
                            <input class="form-control" name="switch_[nr]_timer_on_duration" placeholder="{{_('Timer period on duration in minutes')}}" required="required" type="text" value="0" pattern="[0-9\.]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_timer_on_duration')}}">
                          </div>
                          <div class="col-md-3 col-sm-2 col-xs-6 form-group">
                            <label for="switch_[nr]_timer_off_duration">{{_('Timer off duration')}}</label>
                            <input class="form-control" name="switch_[nr]_timer_off_duration" placeholder="{{_('Timer period off duration in minutes')}}" required="required" type="text" value="0" pattern="[0-9\.]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_timer_off_duration')}}">
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
        <script tpe="text/javascript">
          $(document).ready(function() {
            // Create add button
            init_form_settings('switch');

            // Setup initial pulldowns in the add form
            $('select[name^="switch_[nr]_"]').select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            }).on('change',function() {
              if ('switch_[nr]_hardwaretype' === this.name) {
                var dimmer = this.value.indexOf('-dimmer') !== -1 || 'brightpi' === this.value || 'pca9685' == this.value;
                if (dimmer) {
                  $(this).parents('.x_content').find('.row.dimmer input').attr('required','required');
                } else {
                  $(this).parents('.x_content').find('.row.dimmer input').removeAttr('required');
                }

                $(this).parents('.x_content').find('.row.dimmer').toggle(dimmer);

                var address_field = $("input[name='" + this.name.replace('hardwaretype','address') + "']");
                address_field.off('change');
                if ('remote' === this.value || 'remote-dimmer' === this.value) {
                  address_field.on('change',function(){
                    parse_remote_data('switch',this.value);
                  });
                }
              } else if ('switch_[nr]_timer_enabled' === this.name) {
                if ('true' === this.value) {
                  $(this).parents('.x_content').find('.row.timer input').attr('required','required');
                } else {
                  $(this).parents('.x_content').find('.row.timer input').removeAttr('required');
                }
                $(this).parents('.x_content').find('.row.timer').toggle('true' === this.value);
              }
            }).val(null).trigger('change');


            // Load existing switches
            $.get($('form').attr('action'),function(json_data){
              $.each(sortByKey(json_data.switches,'name'), function(index,switch_data) {
                add_power_switch_setting_row(switch_data);
                update_power_switch(switch_data);
              });
              reload_reload_theme();
            });
          });
        </script>
% include('inc/page_footer.tpl')
