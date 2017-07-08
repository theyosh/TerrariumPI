% include('inc/page_header.tpl')
% icon = 'fire' if sensor_type == 'temperature' else 'tint'
        % for item in range(0,amount_of_sensors):
        <div class="row sensor">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2>
                  <span aria-hidden="true" class="glyphicon glyphicon-{{icon}}"></span>
                  <span class="title">{{_(sensor_type.capitalize())}}</span>
                  <small>...</small>
                  <span class="badge bg-red" style="display:none;">{{_('warning')}}</span>
                </h2>
                <ul class="nav navbar-right panel_toolbox">
                  <li>
                    <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                  </li>
                  <li class="dropdown">
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-calendar" title="{{_('Period')}}"></i></a>
                    <ul class="dropdown-menu period" role="menu">
                      <li>
                        <a href="javascript:;" >{{_('day')}}</a>
                      </li>
                      <li>
                        <a href="javascript:;" >{{_('week')}}</a>
                      </li>
                      <li>
                        <a href="javascript:;" >{{_('month')}}</a>
                      </li>
                      <li>
                        <a href="javascript:;" >{{_('year')}}</a>
                      </li>
                    </ul>
                  </li>
                  <li class="dropdown">
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-wrench" title="{{_('Options')}}"></i></a>
                    <ul class="dropdown-menu" role="menu">
                      <li>
                        <a href="javascript:;" onclick="menu_click('sensor_settings.html')">{{_('Settings')}}</a>
                      </li>
                    </ul>
                  </li>
                  <li>
                    <a class="close-link"><i class="fa fa-close" title="{{_('Close')}}"></i></a>
                  </li>
                </ul>
                <div class="clearfix"></div>
              </div>
              <div class="x_content">
                <div class="col-md-3 col-sm-4 col-xs-12">
                  <div class="sidebar-widget">
                    <canvas class="gauge"></canvas>
                    <div class="goal-wrapper">
                      <span class="gauge-value pull-left">...</span> <span class="gauge-value pull-left">{{sensor_indicator}}</span>
                    </div>
                  </div>
                </div>
                <div class="col-md-9 col-sm-8 col-xs-12">
                  <div class="history_graph loading"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        % end
        <script type="text/javascript">
          $(document).ready(function() {
            $.get('/api/sensors/{{sensor_type}}',function(data){
              var rows = $('div.row.sensor');
              $.each(data.sensors, function(index,sensor) {
                // Add an id to the row when first run
                $(rows[index]).attr('id',sensor.id);
                sensor_gauge(sensor.id, sensor);
                load_history_graph(sensor.id,'{{sensor_type}}','/api/history/sensors/' + sensor.id);
              });
            });
          });
        </script>
% include('inc/page_footer.tpl')
