% include('inc/page_header.tpl')
            <div class="row">
              <div class="col-md-12 col-sm-12 col-xs-12">
                <div class="x_panel">
                  <div class="x_title">
                    <h2 id="deviceid">Device type <small>[..]</small></h2>
                    <ul class="nav navbar-right panel_toolbox">
                      <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                      </li>
                      <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false"><i class="fa fa-wrench"></i></a>
                        <ul class="dropdown-menu" role="menu">
                          <li><a href="#">Settings 1</a>
                          </li>
                          <li><a href="#">Settings 2</a>
                          </li>
                        </ul>
                      </li>
                      <li><a class="close-link"><i class="fa fa-close"></i></a>
                      </li>
                    </ul>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                    <br />
                    <form id="demo-form2" data-parsley-validate class="form-horizontal form-label-left" method="put" action="/api/config/switches">
                      <div class="row">
                        <div class="form-group">
                          <label class="control-label col-md-2 col-sm-3 col-xs-12" for="first-name">Amount of switches <span class="required">*</span></label>
                          <div class="col-md-8 col-sm-8 col-xs-12">
                            <div class="form-group">
                              <select class="amount_of_switches form-control" tabindex="-1" name="amount_of_switches">
                                <option></option>
                                % for item in range(0,max_swithes):
                                <option value="{{item+1}}">{{item+1}}</option>
                                % end
                              </select>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="row">
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                        </div>
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                          <strong>ID</strong>
                        </div>
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                          <strong>Name</strong>
                        </div>
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                          <strong>Power usage in Watt</strong>
                        </div>
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                          <strong>Water usage in liters/minute</strong>
                        </div>
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                          <strong>Action</strong>
                        </div>
                      </div>
                      % for item in range(1,max_swithes+1):
                      <div class="row switch">
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                          <label class="control-label col-md-8 col-sm-12 col-xs-12" for="first-name">Switch {{item}} <span class="required">*</span></label>
                          <input type="hidden" placeholder="nr" class="form-control" name="switch_{{item}}_nr" readonly="readonly">
                        </div>
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                          <input type="text" placeholder="ID" class="form-control" name="switch_{{item}}_id" readonly="readonly">
                        </div>
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                          <input type="text" placeholder="Name" class="form-control" name="switch_{{item}}_name">
                        </div>
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                          <input type="text" placeholder="Power usage" class="form-control" name="switch_{{item}}_power_wattage">
                        </div>
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                          <input type="text" placeholder="Water usage" class="form-control" name="switch_{{item}}_water_flow">
                        </div>
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                          <div class="form-group">
                            <div class="col-md-9 col-sm-9 col-xs-12">
                              <div class="">
                                <label>
                                  <input type="checkbox" class="js-switch" name="switch_{{item}}_state"/>
                                </label>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      % end
                      <div class="ln_solid"></div>
                      <div class="form-group">
                        <div class="col-md-6 col-sm-6 col-xs-12 col-md-offset-5">
                          <button type="submit" class="btn btn-success">Submit</button>
                        </div>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>

            <!-- Select2 -->
            <style>
              .row.switch {
                display: none;
              }
            </style>

            <script type="text/javascript">

              $(document).ready(function() {
                var selector = $(".amount_of_switches");
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
                    var nr = powerswitch.nr;
                    $(Object.keys(powerswitch)).each(function(index,key){
                        if ('state' == key ) {
                          $('input[name="switch_' + powerswitch.nr + '_' + key + '"]').attr('checked',(powerswitch[key] ? 'checked' : ''));
                          $('input[name="switch_' + powerswitch.nr + '_' + key + '"]').on('change',function(){
                            websocket_message({'type':'toggle_switch', 'data' : {'nr': nr, 'state' : this.checked}});
                          });
                        } else {
                          $('input[name="switch_' + powerswitch.nr + '_' + key + '"]').val(powerswitch[key]);
                        }
                    });
                  });
                  selector.val(data.switches.length);
                  selector.trigger('change');
                });

              });
            </script>
% include('inc/page_footer.tpl')
