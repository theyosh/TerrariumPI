% include('inc/page_header.tpl')
        <div class="row jumbotron">
          <div class="col-md-12 col-sm-12 col-xs-12">
              <h1>{{_('No sensors available')}}</h1>
          </div>
        </div>
        <div class="row sensor">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2 class="temperature"><span aria-hidden="true" class="glyphicon glyphicon-fire"></span> {{_('Temperature sensor')}} <span class="title">{{_('new')}}</span> <span class="small">...</span> <span class="badge bg-red" title="{{_('warning')}}">{{_('warning')}}</span> <span class="badge bg-orange" title="{{_('error')}}">{{_('error')}}</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">{{_('excl. avg')}}</span></h2>
                <h2 class="humidity"><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> {{_('Humidity sensor')}} <span class="title">{{_('new')}}</span> <span class="small">...</span> <span class="badge bg-red" title="{{_('warning')}}">{{_('warning')}}</span> <span class="badge bg-orange" title="{{_('error')}}">{{_('error')}}</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">{{_('excl. avg')}}</span></h2>
                <h2 class="moisture"><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> {{_('Moisture sensor')}} <span class="title">{{_('new')}}</span> <span class="small">...</span> <span class="badge bg-red" title="{{_('warning')}}">{{_('warning')}}</span> <span class="badge bg-orange" title="{{_('error')}}">{{_('error')}}</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">{{_('excl. avg')}}</span></h2>
                <h2 class="conductivity"><span aria-hidden="true" class="glyphicon glyphicon-oil"></span> {{_('Conductivity sensor')}} <span class="title">{{_('new')}}</span> <span class="small">...</span> <span class="badge bg-red" title="{{_('warning')}}">{{_('warning')}}</span> <span class="badge bg-orange" title="{{_('error')}}">{{_('error')}}</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">{{_('excl. avg')}}</span></h2>
                <h2 class="distance"><span aria-hidden="true" class="glyphicon glyphicon-signal"></span> {{_('Distance sensor')}} <span class="title">{{_('new')}}</span> <span class="small">...</span> <span class="badge bg-red" title="{{_('warning')}}">{{_('warning')}}</span> <span class="badge bg-orange" title="{{_('error')}}">{{_('error')}}</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">{{_('excl. avg')}}</span></h2>
                <h2 class="ph"><span aria-hidden="true" class="glyphicon glyphicon-scale"></span> {{_('pH sensor')}} <span class="title">{{_('new')}}</span> <span class="small">...</span> <span class="badge bg-red" title="{{_('warning')}}">{{_('warning')}}</span> <span class="badge bg-orange" title="{{_('error')}}">{{_('error')}}</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">{{_('excl. avg')}}</span></h2>
                <h2 class="light uva uvb uvi"><span aria-hidden="true" class="glyphicon glyphicon-adjust"></span> {{_('Light sensor')}} <span class="title">{{_('new')}}</span> <span class="small">...</span> <span class="badge bg-red" title="{{_('warning')}}">{{_('warning')}}</span> <span class="badge bg-orange" title="{{_('error')}}">{{_('error')}}</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">{{_('excl. avg')}}</span></h2>
                <h2 class="fertility"><span aria-hidden="true" class="glyphicon glyphicon-grain"></span> {{_('Fertility sensor')}} <span class="title">{{_('new')}}</span> <span class="small">...</span> <span class="badge bg-red" title="{{_('warning')}}">{{_('warning')}}</span> <span class="badge bg-orange" title="{{_('error')}}">{{_('error')}}</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">{{_('excl. avg')}}</span></h2>
                <h2 class="co2"><span aria-hidden="true" class="glyphicon glyphicon-tree-conifer"></span> {{_('CO2 sensor')}} <span class="title">{{_('new')}}</span> <span class="small">...</span> <span class="badge bg-red" title="{{_('warning')}}">{{_('warning')}}</span> <span class="badge bg-orange" title="{{_('error')}}">{{_('error')}}</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">{{_('excl. avg')}}</span></h2>
                <h2 class="volume"><span aria-hidden="true" class="glyphicon glyphicon-signal"></span> {{_('Volume sensor')}} <span class="title">{{_('new')}}</span> <span class="small">...</span> <span class="badge bg-red" title="{{_('warning')}}">{{_('warning')}}</span> <span class="badge bg-orange" title="{{_('error')}}">{{_('error')}}</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">{{_('excl. avg')}}</span></h2>
                <ul class="nav navbar-right panel_toolbox">
                  <li>
                    <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                  </li>
                  <li class="dropdown">
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-calendar" title="{{_('Period')}}"></i></a>
                    <ul class="dropdown-menu period" role="menu">
                      <li>
                        <a href="javascript:;" >{{_('Day')}}</a>
                      </li>
                      <li>
                        <a href="javascript:;" >{{_('Week')}}</a>
                      </li>
                      <li>
                        <a href="javascript:;" >{{_('Month')}}</a>
                      </li>
                      <li>
                        <a href="javascript:;" >{{_('Year')}}</a>
                      </li>
                    </ul>
                  </li>
                  <li class="dropdown">
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-wrench" title="{{_('Options')}}"></i></a>
                    <ul class="dropdown-menu" role="menu">
                      <li>
                        <a href="javascript:;" onclick="menu_click('sensor_settings.html')">{{_('Settings')}}</a>
                      </li>
                      <li>
                        <a href="javascript:;" class="export">{{_('Export data')}}</a>
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
                  <div class="sidebar-widget text-center">
                    <canvas class="gauge"></canvas>
                    <div class="goal-wrapper">
                      <span class="gauge-value">...</span> <span class="gauge-indicator"></span>
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
        <script type="text/javascript">
          $(document).ready(function() {
            source_row = $('div.row.sensor').html();
            $('div.row.sensor').remove();

            var sensor_types = '{{sensor_type}}'.split(',');
            $.each(sensor_types,function(counter,sensor_type){
              $.get('/api/sensors/' + sensor_type,function(json_data) {
                $.each(sortByKey(json_data.sensors,'name'),function(index,sensor_data){
                  add_sensor_status_row(sensor_data);
                  update_sensor(sensor_data);
                  sensor_gauge('sensor_' + sensor_data.id, sensor_data);
                  load_history_graph('sensor_' + sensor_data.id,sensor_type + (sensor_type == 'light' && sensor_data.firmware === undefined ? '_percentage' : '') ,'/api/history/sensors/' + sensor_data.id);
                });
                $('div.row.jumbotron').toggle($('div.row.sensor:visible').length == 0);
                reload_reload_theme();
              });
            });
          });
        </script>
% include('inc/page_footer.tpl')
