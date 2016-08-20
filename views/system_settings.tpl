% include('inc/page_header.tpl')
        <div class="row">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2 id="deviceid">TerrariumPI <small>[..]</small></h2>
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
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="host">IP or hostname <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <input class="form-control" id="location" name="host" required="required" type="text">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="port">Port number <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <input class="form-control" id="location" name="port" required="required" type="text">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="power_usage">Pi power usage in W <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <input class="form-control" id="location" name="power_usage" required="required" type="text">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="gpio_door_pin">Door GPIO pin <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <input class="form-control" id="location" name="gpio_door_pin" required="required" type="text">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="1wire_port">1-Wire / OWFS port <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <input class="form-control" id="location" name="1wire_port" required="required" type="text">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="loglevel">Loglevel <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <input class="form-control" id="location" name="loglevel" required="required" type="text" value="3">
                    </div>
                  </div>
                  <div class="ln_solid"></div>
                  <div class="form-group">
                    <div class="col-md-11 col-sm-11 col-xs-12 text-center">
                      <button class="btn btn-success" type="submit">Submit</button>
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
              $.each(Object.keys(data), function(key,value){
                $('input[name="' + value + '"]').val(data[value]);
              });
            });
          });
        </script>
% include('inc/page_footer.tpl')
