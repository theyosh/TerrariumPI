% include('inc/page_header.tpl')
        <form action="/api/config/sensors" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
          % for item in range(0,amount_of_sensors):
          <div class="row sensor">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 id="deviceid"><span class="sensor_{{item}}_icon"></span> Sensor {{item+1}}<small></small></h2>
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
                  <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                    <label for="sensor_{{item}}_address">Address</label> <input class="form-control" name="sensor_{{item}}_address" placeholder="Address" readonly="readonly" type="text"> <input class="form-control" name="sensor_{{item}}_id" placeholder="ID" readonly="readonly" type="hidden">
                  </div>
                  <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                    <label for="sensor_{{item}}_name">Name</label> <input class="form-control" name="sensor_{{item}}_name" placeholder="Name" type="text">
                  </div>
                  <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                    <label for="sensor_{{item}}_alarm_min">Alarm min</label> <input class="form-control" name="sensor_{{item}}_alarm_min" placeholder="Limit min" type="text">
                  </div>
                  <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                    <label for="sensor_{{item}}_alarm_max">Alarm max</label> <input class="form-control" name="sensor_{{item}}_alarm_max" placeholder="Limit max" type="text">
                  </div>
                  <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                    <label for="sensor_{{item}}_min">Limix min</label> <input class="form-control" name="sensor_{{item}}_min" placeholder="Limit min" type="text">
                  </div>
                  <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                    <label for="sensor_{{item}}_max">Limix max</label> <input class="form-control" name="sensor_{{item}}_max" placeholder="Limit max" type="text">
                  </div>
                  <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                    <label for="sensor_{{item}}_current">Current</label> <input class="form-control" name="sensor_{{item}}_current" placeholder="Current" readonly="readonly" type="text">
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
        <script type="text/javascript">
          $(document).ready(function() {
            $.get($('form').attr('action'),function(data){
              $.each(data.sensors, function(index,sensor) {
                $(Object.keys(sensor)).each(function(index2,key){
                  if ('type' == key ) {
                    $('span.sensor_' + index + '_icon').html('<span class="glyphicon glyphicon-' + (sensor[key] == 'temperature' ? 'fire' : 'tint') + '" aria-hidden="true"><\/span>')
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
