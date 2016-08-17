% include('inc/page_header.tpl')
            <form id="" data-parsley-validate class="form-horizontal form-label-left" method="put" action="/api/config/sensors">
            % for item in range(0,amount_of_sensors):
              <div class="row sensor">
                <div class="col-md-12 col-sm-12 col-xs-12">
                  <div class="x_panel">
                    <div class="x_title">
                      <h2 id="deviceid"><span class="sensor_{{item}}_icon"></span> Sensor {{item+1}}<small></small></h2>
                      <ul class="nav navbar-right panel_toolbox">
                        <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                        </li>
                        <li><a class="close-link"><i class="fa fa-close"></i></a>
                        </li>
                      </ul>
                      <div class="clearfix"></div>
                    </div>
                    <div class="x_content">
                      <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                        <label for="sensor_{{item}}_address">Address</label>
                        <input type="text" placeholder="Address" class="form-control" name="sensor_{{item}}_address" readonly="readonly">
                        <input type="hidden" placeholder="ID" class="form-control" name="sensor_{{item}}_id" readonly="readonly">
                      </div>
                      <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                        <label for="sensor_{{item}}_name">Name</label>
                        <input type="text" placeholder="Name" class="form-control" name="sensor_{{item}}_name">
                      </div>
                      <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                         <label for="sensor_{{item}}_alarm_min">Alarm min</label>
                        <input type="text" placeholder="Limit min" class="form-control" name="sensor_{{item}}_alarm_min">
                      </div>
                      <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                        <label for="sensor_{{item}}_alarm_max">Alarm max</label>
                        <input type="text" placeholder="Limit max" class="form-control" name="sensor_{{item}}_alarm_max">
                      </div>
                      <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                        <label for="sensor_{{item}}_min">Limix min</label>
                        <input type="text" placeholder="Limit min" class="form-control" name="sensor_{{item}}_min">
                      </div>
                      <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                        <label for="sensor_{{item}}_max">Limix max</label>
                        <input type="text" placeholder="Limit max" class="form-control" name="sensor_{{item}}_max">
                      </div>
                      <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                        <label for="sensor_{{item}}_current">Current</label>
                        <input type="text" placeholder="Current" class="form-control" name="sensor_{{item}}_current" readonly="readonly">
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
            <script type="text/javascript">
              $(document).ready(function() {
                $.get($('form').attr('action'),function(data){
                  $.each(data.sensors, function(index,sensor) {
                    $(Object.keys(sensor)).each(function(index2,key){
                        if ('type' == key ) {
                          $('span.sensor_' + index + '_icon').html('<span class="glyphicon glyphicon-' + (sensor[key] == 'temperature' ? 'fire' : 'tint') + '" aria-hidden="true"></span>')
                                                              .attr('title',sensor[key] + ' sensor');
                        } else {
                          $('input[name="sensor_' + index + '_' + key + '"]').val(sensor[key]);
                        }
                    });
                  });
                });
              });
            </script>
% include('inc/page_footer.tpl')
