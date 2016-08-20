% include('inc/page_header.tpl')
            % for item in range(0,amount_of_sensors):
            <div class="row sensor">
              <div class="col-md-12 col-sm-12 col-xs-12">
                <div class="x_panel">
                  <div class="x_title">
                    <h2><span class="glyphicon glyphicon-fire" aria-hidden="true"></span> <span class="title">{{sensor_type.title()}}</span> <small class="data_update">live...</small> <span class="badge bg-red" style="display:none;">warning</span></h2>
                    <ul class="nav navbar-right panel_toolbox">
                      <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                      </li>
                      <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false"><i class="fa fa-wrench"></i></a>
                        <ul class="dropdown-menu" role="menu">
                          <li><a href="#" onclick="menu_click('sensor_settings.html')">Settings</a> </li>
                        </ul>
                      </li>
                      <li><a class="close-link"><i class="fa fa-close"></i></a>
                      </li>
                    </ul>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                    <div class="col-md-3 col-sm-4 col-xs-12">
                      <div class="sidebar-widget">
                        <canvas class="gauge"></canvas>
                        <div class="goal-wrapper">
                          <span class="gauge-value pull-left">...</span>
                          <span class="gauge-value pull-left"> {{sensor_indicator}}</span>
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
                  // Reset the gauges, due to reloading the main content
                  globals.gauges = [];
                  var rows = $('div.row.sensor');
                  $.each(data.sensors, function(index,sensor) {
                  // Add an id to the row when first run
                    if ($(rows[index]).attr('id') === undefined) {
                      var row = $(rows[index]).attr('id','sensor_' + sensor.id);
                      row.find('canvas').attr('id','gauge_canvas_' + sensor.id);
                      row.find('div.goal-wrapper > span:first').attr('id','gauge_text_' + sensor.id);
                      row.find('div.history_graph').attr('id','history_graph_' + sensor.id);
                    }
                    sensor_gauge(sensor.id, sensor);
                  });
                  update_sensor_history('{{sensor_type}}');
                });
              });
            </script>
% include('inc/page_footer.tpl')
