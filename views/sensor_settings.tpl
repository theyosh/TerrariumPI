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
                    <form id="demo-form2" data-parsley-validate class="form-horizontal form-label-left" method="put" action="/api/config/sensors">
                       <div class="row">
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                        </div>
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                          <strong>Address</strong>
                        </div>
                        <div class="col-md-1 col-sm-12 col-xs-12 form-group">
                          <strong>Type</strong>
                        </div>
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                          <strong>Name</strong>
                        </div>
                        <div class="col-md-1 col-sm-12 col-xs-12 form-group">
                          <strong>Alarm min</strong>
                        </div>
                        <div class="col-md-1 col-sm-12 col-xs-12 form-group">
                          <strong>Alarm max</strong>
                        </div>
                        <div class="col-md-1 col-sm-12 col-xs-12 form-group">
                          <strong>Limix min</strong>
                        </div>
                        <div class="col-md-1 col-sm-12 col-xs-12 form-group">
                          <strong>Limix max</strong>
                        </div>
                        <div class="col-md-1 col-sm-12 col-xs-12 form-group">
                          <strong>Current</strong>
                        </div>
                      </div>
                      % for item in range(0,amount_of_sensors):
                      <div class="row sensor">
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                          <label class="control-label col-md-8 col-sm-12 col-xs-12" for="first-name">Sensor {{item+1}} <span class="required">*</span></label>
                          <input type="hidden" placeholder="ID" class="form-control" name="sensor_{{item}}_id" readonly="readonly">
                        </div>
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                          <input type="text" placeholder="Address" class="form-control" name="sensor_{{item}}_address" readonly="readonly">
                        </div>
                        <div class="col-md-1 col-sm-12 col-xs-12 form-group">
                          <span class="sensor_{{item}}_icon"></span>
                        </div>
                        <div class="col-md-2 col-sm-12 col-xs-12 form-group">
                          <input type="text" placeholder="Name" class="form-control" name="sensor_{{item}}_name">
                        </div>
                        <div class="col-md-1 col-sm-12 col-xs-12 form-group">
                          <input type="text" placeholder="Limit min" class="form-control" name="sensor_{{item}}_alarm_min">
                        </div>
                        <div class="col-md-1 col-sm-12 col-xs-12 form-group">
                          <input type="text" placeholder="Limit max" class="form-control" name="sensor_{{item}}_alarm_max">
                        </div>
                        <div class="col-md-1 col-sm-12 col-xs-12 form-group">
                          <input type="text" placeholder="Limit min" class="form-control" name="sensor_{{item}}_min">
                        </div>
                        <div class="col-md-1 col-sm-12 col-xs-12 form-group">
                          <input type="text" placeholder="Limit max" class="form-control" name="sensor_{{item}}_max">
                        </div>
                        <div class="col-md-1 col-sm-12 col-xs-12 form-group">
                          <input type="text" placeholder="Current" class="form-control" name="sensor_{{item}}_current" readonly="readonly">
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

            <script type="text/javascript">
              $(document).ready(function() {
                $.get($('form').attr('action'),function(data){
                  //$('div.row.sensor:gt(' + (data.sensors.length-1) + ')').remove();
                  $.each(data.sensors, function(index,sensor) {
                    $(Object.keys(sensor)).each(function(index2,key){
                        if ('type' == key ) {
                          $('span.sensor_' + index + '_icon').html('<span class="glyphicon glyphicon-' + (sensor[key] == 'temperature' ? 'fire' : 'tint') + '" aria-hidden="true"></span>')
                                                              .attr('title',sensor[key])
                                                              .parent().css('paddingLeft','20px');
                        } else {
                          $('input[name="sensor_' + index + '_' + key + '"]').val(sensor[key]);
                        }
                    });
                  });
                });
              });
            </script>
% include('inc/page_footer.tpl')
