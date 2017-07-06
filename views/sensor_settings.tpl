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
            <p>{{_('Enter per sensor the values. The icon in front of the sensors shows if it is a humidity or temperature sensor. The address and current fields are readonly. The fields are:')}}</p>
            <ul>
              <li>
                <strong>{{_('Address')}}</strong>: {{_('Shows the 1-wire address of the sensor. (readonly)')}}
              </li>
              <li>
                <strong>{{_('Name')}}</strong>: {{_('Holds the name of the sensor.')}}
              </li>
              <li>
                <strong>{{_('Alarm min')}}</strong>: {{_('Holds the lower limit of the sensor. When below this value, alarms will trigger. Like humidity gets to low, it will trigger the spraying system.')}}
              </li>
              <li>
                <strong>{{_('Alarm max')}}</strong>: {{_('Holds the maximum limit of the sensor. When above this value, it will show alarms to indicate but no triggers.')}}
              </li>
              <li>
                <strong>{{_('Limit min')}}</strong>: {{_('Holds the lowest value that should be used in the graphs.')}}
              </li>
              <li>
                <strong>{{_('Limit max')}}</strong>: {{_('Holds the maximum value that should be used in the graphs.')}}
              </li>
              <li>
                <strong>{{_('Current')}}</strong>: {{_('Shows the current value in temperature or humidity.')}}
              </li>
            </ul>
          </div>
        </div>
        <form action="/api/config/sensors" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
          % for item in range(0,amount_of_sensors):
          <div class="row sensor">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2><span class="sensor_{{item}}_icon"></span> {{_('Sensor')}} {{item+1}}<small></small></h2>
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
                  <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                    <label for="sensor_{{item}}_address">{{_('Address')}}</label> <input class="form-control" name="sensor_{{item}}_address" placeholder="{{_('Address')}}" readonly="readonly" type="text"> <input class="form-control" name="sensor_{{item}}_id" placeholder="ID" readonly="readonly" type="hidden">
                  </div>
                  <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                    <label for="sensor_{{item}}_name">{{_('Name')}}</label> <input class="form-control" name="sensor_{{item}}_name" placeholder="{{_('Name')}}" type="text">
                  </div>
                  <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                    <label for="sensor_{{item}}_alarm_min">{{_('Alarm min')}}</label> <input class="form-control" name="sensor_{{item}}_alarm_min" placeholder="{{_('Limit min')}}" type="text">
                  </div>
                  <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                    <label for="sensor_{{item}}_alarm_max">{{_('Alarm max')}}</label> <input class="form-control" name="sensor_{{item}}_alarm_max" placeholder="{{_('Limit max')}}" type="text">
                  </div>
                  <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                    <label for="sensor_{{item}}_min">{{_('Limit min')}}</label> <input class="form-control" name="sensor_{{item}}_min" placeholder="{{_('Limit min')}}" type="text">
                  </div>
                  <div class="col-md-1 col-sm-1 col-xs-12 form-group">
                    <label for="sensor_{{item}}_max">{{_('Limit max')}}</label> <input class="form-control" name="sensor_{{item}}_max" placeholder="{{_('Limit max')}}" type="text">
                  </div>
                  <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                    <label for="sensor_{{item}}_current">{{_('Current')}}</label> <input class="form-control" name="sensor_{{item}}_current" placeholder="{{_('Current')}}" readonly="readonly" type="text">
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
                  <button class="btn btn-success" type="submit">{{_('Submit')}}</button>
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
                    $('span.sensor_' + index + '_icon').append(
                        $('<span>').addClass('glyphicon glyphicon-' + (sensor[key] == 'temperature' ? 'fire' : 'tint'))
                                   .attr({'aria-hidden':'true','title': capitalizeFirstLetter(sensor[key] + ' {{_('sensor')}}')})
                    );
                  } else {
                    $('input[name="sensor_' + index + '_' + key + '"]').val(sensor[key]);
                  }
                });
              });
            });
          });
        </script>
% include('inc/page_footer.tpl')
