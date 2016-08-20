% include('inc/page_header.tpl')
        <form action="/api/config/switches" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
          <div class="row">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 id="deviceid">Device type <small>[..]</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                    <li>
                      <a class="close-link"><i class="fa fa-close"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-2 col-sm-4 col-xs-12" for="amount_of_switches">Amount of switches <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-6 col-xs-12">
                      <div class="form-group">
                        <select class="form-control" name="amount_of_switches" tabindex="-1">
                          <option></option>
                          % for item in range(0,max_swithes):
                          <option value="{{item+1}}">
                            {{item+1}}
                          </option>
                          % end
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          % for item in range(0,max_swithes):
          <div class="row switch">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <div class="power_switch small switch_{{item}}_state">
                    <span aria-hidden="true" class="glyphicon glyphicon-off" onclick="toggleSwitch($(this).parent().attr('id'));"></span>
                  </div>
                  <h2>Switch {{item+1}}<small></small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                    <li>
                      <a class="close-link"><i class="fa fa-close"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="col-md-3 col-sm-6 col-xs-12 form-group">
                    <label for="switch_{{item}}_id">ID</label> <input class="form-control" name="switch_{{item}}_id" placeholder="ID" readonly="readonly" type="text">
                  </div>
                  <div class="col-md-3 col-sm-6 col-xs-12 form-group">
                    <label for="switch_{{item}}_name">Name</label> <input class="form-control" name="switch_{{item}}_name" placeholder="Name" type="text">
                  </div>
                  <div class="col-md-3 col-sm-6 col-xs-12 form-group">
                    <label for="switch_{{item}}_power_wattage">Power usage in Watt</label> <input class="form-control" name="switch_{{item}}_power_wattage" placeholder="Power usage" type="text">
                  </div>
                  <div class="col-md-3 col-sm-6 col-xs-12 form-group">
                    <label for="switch_{{item}}_water_flow">Water usage in liters/minute</label> <input class="form-control" name="switch_{{item}}_water_flow" placeholder="Water usage" type="text">
                  </div>
                </div>
              </div>
            </div>
          </div>
          % end
          <div class="row">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="ln_solid"></div>
              <div class="form-group">
                <div class="col-md-11 col-sm-11 col-xs-12 text-center">
                  <button class="btn btn-success" type="submit">Submit</button>
                </div>
              </div>
            </div>
          </div>
        </form>
        <style>
          .row.switch {
            display: none;
          }
        </style>
        <script type="text/javascript">
          $(document).ready(function() {
            var selector = $("select[name='amount_of_switches']");
            selector.select2({
              placeholder: "Select a number",
              allowClear: false,
              minimumResultsForSearch: Infinity
            });

            selector.on('change',function() {
              var amount = this.value;
              $('.row.switch').each(function(index,row) {
                if (index < amount) {
                  $(row).show();
                } else {
                  $(row).hide();
                }
              });
            });

            $.get($('form').attr('action'),function(data){
              $('h2#deviceid').html('Powerswitch board: ' + data.switchboard_device + ' (' + data.switchboard_type + ') <small>' + data.switchboard_id + '<\/small>')
              $.each(data.switches, function(index,powerswitch) {
                $('.switch_' + (powerswitch['nr']-1) + '_state').attr('id','switch_' + powerswitch['id']);
                $(Object.keys(powerswitch)).each(function(counter,key){
                  if ('state' != key ) {
                    $('input[name="switch_' + (powerswitch['nr']-1) + '_' + key + '"]').val(powerswitch[key]);
                  }
                });
                update_power_switch(powerswitch['id'],powerswitch);
              });
              selector.val(data.switches.length);
              selector.trigger('change');
            });
          });
        </script>
% include('inc/page_footer.tpl')
