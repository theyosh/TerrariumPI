% include('inc/page_header.tpl')
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
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="active_language">{{_('Language')}} <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <div class="form-group">
                        <select class="form-control" required="required" name="active_language" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option></option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="host">{{_('IP or hostname')}} <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <input class="form-control" name="host" required="required" type="text" placeholder="{{_('IP or hostname')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="port">{{_('Port number')}} <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <input class="form-control" name="port" required="required" type="text" placeholder="{{_('Port number')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="admin">{{_('Admin name')}} <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <input class="form-control" name="admin" required="required" type="text" placeholder="{{_('Admin name')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="port">{{_('New admin password')}} </label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <input class="form-control" name="new_password" type="password" placeholder="{{_('New admin password')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="port">{{_('Current admin password')}} </label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <input class="form-control" name="cur_password" type="password" placeholder="{{_('Current admin password')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="power_usage">{{_('Pi power usage in W')}} <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <input class="form-control" name="power_usage" required="required" type="text" placeholder="{{_('Pi power usage in W')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="gpio_door_pin">{{_('Door GPIO pin')}} <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <input class="form-control" name="gpio_door_pin" required="required" type="text" placeholder="{{_('Door GPIO pin')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="1wire_port">{{_('1-Wire / OWFS port')}} <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <input class="form-control" name="1wire_port" required="required" type="text" placeholder="{{_('1-Wire / OWFS port')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="loglevel">{{_('Loglevel')}} <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <input class="form-control" name="loglevel" required="required" type="text" value="3" placeholder="{{_('Loglevel')}}">
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
