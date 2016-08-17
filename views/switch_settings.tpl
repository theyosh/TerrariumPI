% include('inc/page_header.tpl')
            <form id="demo-form2" data-parsley-validate class="form-horizontal form-label-left" method="put" action="/api/config/switches">
            <div class="row">
              <div class="col-md-12 col-sm-12 col-xs-12">
                <div class="x_panel">
                  <div class="x_title">
                    <h2 id="deviceid">Device type <small>[..]</small></h2>
                    <ul class="nav navbar-right panel_toolbox">
                      <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                      </li>
                      <li><a class="close-link"><i class="fa fa-close"></i></a>
                      </li>
                    </ul>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                    <div class="form-group">
                      <label class="control-label col-md-2 col-sm-4 col-xs-12" for="amount_of_switches">Amount of switches <span class="required">*</span></label>
                      <div class="col-md-8 col-sm-6 col-xs-12">
                        <div class="form-group">
                          <select class="form-control" tabindex="-1" name="amount_of_switches">
                            <option></option>
                            % for item in range(0,max_swithes):
                              <option value="{{item+1}}">{{item+1}}</option>
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
                      <span class="glyphicon glyphicon-off" aria-hidden="true" onclick="toggleSwitch($(this).parent().attr('id'));"></span>
                    </div>
                    <h2>Switch {{item+1}}<small></small></h2>
                    <ul class="nav navbar-right panel_toolbox">
                      <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                      </li>
                      <li><a class="close-link"><i class="fa fa-close"></i></a>
                      </li>
                    </ul>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                    <div class="col-md-3 col-sm-6 col-xs-12 form-group">
                      <label for="switch_{{item}}_id">ID</label>
                      <input type="text" placeholder="ID" class="form-control" name="switch_{{item}}_id" readonly="readonly">
                    </div>
                    <div class="col-md-3 col-sm-6 col-xs-12 form-group">
                      <label for="switch_{{item}}_name">Name</label>
                      <input type="text" placeholder="Name" class="form-control" name="switch_{{item}}_name">
                    </div>
                    <div class="col-md-3 col-sm-6 col-xs-12 form-group">
                      <label for="switch_{{item}}_power_wattage">Power usage in Watt</label>
                      <input type="text" placeholder="Power usage" class="form-control" name="switch_{{item}}_power_wattage">
                    </div>
                    <div class="col-md-3 col-sm-6 col-xs-12 form-group">
                      <label for="switch_{{item}}_water_flow">Water usage in liters/minute</label>
                      <input type="text" placeholder="Water usage" class="form-control" name="switch_{{item}}_water_flow">
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
                      <button type="submit" class="btn btn-success">Submit</button>
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
                  $('h2#deviceid').html('Powerswitch board: ' + data.switchboard_device + ' (' + data.switchboard_type + ') <small>' + data.switchboard_id + '</small>')
                  $.each(data.switches, function(index,powerswitch) {
                    $('.switch_' + index + '_state').attr('id','switch_' + powerswitch['id']);
                    $(Object.keys(powerswitch)).each(function(counter,key){
                      if ('state' != key ) {
                        $('input[name="switch_' + index + '_' + key + '"]').val(powerswitch[key]);
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
