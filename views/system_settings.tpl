% include('inc/page_header.tpl')
        <div class="x_panel">
          <div class="x_title">
            <h2><span class="glyphicon glyphicon-info-sign" aria-hidden="true" title="{{_('Information')}}"></span> {{_('Help')}}<small></small></h2>
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
            <p>{{_('Here you can adjust the basic system. Hover above the settings to get more information. Or go to the help section.')}}</p>
          </div>
        </div>
        <div class="row">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2 id="deviceid">{{_('TerrariumPI')}} <small>...</small></h2>
                <ul class="nav navbar-right panel_toolbox">
                  <li>
                    <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                  </li>
                </ul>
                <div class="clearfix"></div>
              </div>
              <div class="x_content">
                <form action="/api/config/system" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="active_language">{{_('Language')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Choose your interface language')}}">
                        <select class="form-control" required="required" name="active_language" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option></option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="admin">{{_('Admin name')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="admin" required="required" type="text" placeholder="{{_('Admin name')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the username which can make changes (Administrator).')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="port">{{_('New admin password')}} </label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="new_password" type="password" placeholder="{{_('New admin password')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the new password for the administration user. Leaving empty will not change the password!')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="port">{{_('Current admin password')}} </label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="cur_password" type="password" placeholder="{{_('Current admin password')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Confirm the newly choosen password.')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="power_usage">{{_('Pi power usage in W')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="power_usage" required="required" type="text" placeholder="{{_('Pi power usage in W')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the amount of power in Wattage that the Raspberry PI uses including all USB equipment')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="host">{{_('Power price')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="power_price" required="required" type="text" placeholder="{{_('Power price')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the amount of euro/dollar per 1 kW/h (1 Kilowatt per hour).')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="port">{{_('Water price')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="water_price" required="required" type="text" placeholder="{{_('Water price')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the amount of euro/dollar per 1000 liters water.')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="host">{{_('IP or hostname')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="host" required="required" type="text" placeholder="{{_('IP or hostname')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the hostname or IP address on which the software will listen for connections. Enter 0.0.0.0 for all adresses to bind to.')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="port">{{_('Port number')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="port" required="required" type="text" placeholder="{{_('Port number')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the portnumber on which the software is listening for connections')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="owfs_port">{{_('OWFS server port')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="owfs_port" required="required" type="text" placeholder="{{_('OWFS server port')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the port number on which the OWFS software is running. Default is 4304. Make sure the service OWServer is running.')}}">
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
            </div>
          </div>
        </div>
        <script type="text/javascript">
          $(document).ready(function() {
            $.get($('form').attr('action'),function(data){
              var language_selector = $("select[name='active_language']");
              language_selector.select2({
                placeholder: '{{_('Select an option')}}',
                allowClear: false,
                minimumResultsForSearch: Infinity
              });
              $.each(data.available_languages.split(','),function(index,value){
                language_selector.append($('<option>').attr({'value':value}).text(value));
              });
              language_selector.val(data.active_language).trigger('change');
              delete data.available_languages;
              delete data.active_language;
              $.each(Object.keys(data), function(key,value){
                $('input[name="' + value + '"]').val(data[value]);
              });
            });
          });
        </script>
% include('inc/page_footer.tpl')
