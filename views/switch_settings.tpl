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
        <div class="modal fade new-switch-form" tabindex="-1" role="dialog" aria-hidden="true">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">
                  <span aria-hidden="true">×</span>
                </button>
                <h4 class="modal-title" id="myModalLabel">{{_('Add new switch')}}</h4>
              </div>
              <div class="modal-body">
                <div class="row switch">
                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="x_panel">
                      <div class="x_title" style="display: none">
                        <div class="power_switch small">
                          <span aria-hidden="true" class="glyphicon glyphicon-off" onclick="toggleSwitch($(this).parent().attr('id'));"></span>
                        </div>
                        <h2><span class="switch_[nr]_icon"></span> {{_('Switch')}} <small>{{_('new')}}</small></h2>
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
                          <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                            <label for="switch_[nr]_hardwaretype">{{_('Hardware')}} <span class="required">*</span></label>
                            <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{!translations.get_translation('switch_field_hardware')}}">
                              <select class="form-control" name="switch_[nr]_hardwaretype" tabindex="-1" placeholder="{{_('Select an option')}}" required="required">
                                <option value="ftdi">{{_('FTDI')}}</option>
                                <option value="gpio">{{_('GPIO')}}</option>
                                <option value="gpio-inverse">{{_('GPIO Inverse')}}</option>
                                <option value="pwm-dimmer">{{_('PWM Dimmer')}}</option>
                                <option value="remote">{{_('Remote')}}</option>
                                <option value="remote-dimmer">{{_('Remote Dimmer')}}</option>
                              </select>
                            </div>
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                            <label for="switch_[nr]_address">{{_('Address')}}</label> <span class="required">*</span>
                            <input class="form-control" name="switch_[nr]_address" placeholder="{{_('Address')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_address')}}">
                            <input class="form-control" name="switch_[nr]_id" placeholder="{{_('ID')}}" readonly="readonly" type="hidden">
                          </div>
                          <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                            <label for="switch_[nr]_name">{{_('Name')}}</label> <span class="required">*</span>
                            <input class="form-control" name="switch_[nr]_name" placeholder="{{_('Name')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_name')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                            <label for="switch_[nr]_power_wattage">{{_('Power usage in Watt')}}</label>
                            <input class="form-control" name="switch_[nr]_power_wattage" placeholder="{{_('Power usage in Watt')}}" type="text" pattern="[0-9\.]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_power_wattage')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                            <label for="switch_[nr]_water_flow">{{_('Water flow in L/m')}}</label>
                            <input class="form-control" name="switch_[nr]_water_flow" placeholder="{{_('Water flow in L/m')}}" type="text" pattern="[0-9\.]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_water_flow')}}">
                          </div>
                        </div>
                        <div class="row dimmer" style="display:none;">
                          <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                            <label for="switch_[nr]_dimmer_duration">{{_('Dimmer action duration')}}</label>
                            <input class="form-control" name="switch_[nr]_dimmer_duration" placeholder="{{_('Dimmer action duration')}}" type="text" pattern="[0-9\.]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_dimmer_duration')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                            <label for="switch_[nr]_dimmer_on_duration">{{_('Dimmer on duration')}}</label>
                            <input class="form-control" name="switch_[nr]_dimmer_on_duration" placeholder="{{_('Dimmer on duration')}}" type="text" pattern="[0-9\.]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_dimmer_on_duration')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                            <label for="switch_[nr]_dimmer_on_percentage">{{_('Dimmer on percentage')}}</label>
                            <input class="form-control" name="switch_[nr]_dimmer_on_percentage" placeholder="{{_('Dimmer on percentage')}}" type="text" pattern="[0-9\.]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_dimmer_on_percentage')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                            <label for="switch_[nr]_dimmer_off_duration">{{_('Dimmer off duration')}}</label>
                            <input class="form-control" name="switch_[nr]_dimmer_off_duration" placeholder="{{_('Dimmer off duration')}}" type="text" pattern="[0-9\.]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_dimmer_off_duration')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                            <label for="switch_[nr]_dimmer_off_percentage">{{_('Dimmer off percentage')}}</label>
                            <input class="form-control" name="switch_[nr]_dimmer_off_percentage" placeholder="{{_('Dimmer off percentage')}}" type="text" pattern="[0-9\.]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_field_dimmer_off_percentage')}}">
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">{{_('Close')}}</button>
                <button type="button" class="btn btn-primary" onclick="add_switch()" >{{_('Add')}}</button>
              </div>
            </div>
          </div>
        </div>
        <script tpe="text/javascript">
          $(document).ready(function() {
            $('.page-title').append('<div class="title_right"><h3><button type="button" class="btn btn-primary alignright" data-toggle="modal" data-target=".new-switch-form"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button></h3> </div>');
            $('select[name^="switch_[nr]_"]').select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            }).on('change',function() {
              $(this).parents('.x_content').find('.row.dimmer').toggle('pwm-dimmer' === this.value || 'remote-dimmer' === this.value);

              var address_field = $("input[name='" + this.name.replace('hardwaretype','address') + "']");
              address_field.off('change');

              if ('remote' === this.value || 'remote-dimmer' === this.value) {
                address_field.on('change',function(){
                    parse_remote_data('switch',this.value);
                });
              }

            }).val(null).trigger('change');
            $.get($('form').attr('action'),function(data){
              $.each(data.switches, function(index,power_switch) {
                // Clone empty switch row....
                add_switch_row(power_switch.id,
                               power_switch.hardwaretype,
                               power_switch.address,
                               power_switch.name,
                               power_switch.power_wattage,
                               power_switch.water_flow,
                               power_switch.dimmer_duration,
                               power_switch.dimmer_on_duration,
                               power_switch.dimmer_on_percentage,
                               power_switch.dimmer_off_duration,
                               power_switch.dimmer_off_percentage);
                update_power_switch(power_switch.id,power_switch);
              });
              reload_reload_theme();
            });
          });
        </script>
% include('inc/page_footer.tpl')
