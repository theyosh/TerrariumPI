% include('inc/page_header.tpl')
        <div class="row jumbotron">
          <div class="col-md-12 col-sm-12 col-xs-12">
              <h1>{{_('No sensors available')}}</h1>
          </div>
        </div>
        <div class="row sensor col-md-3 col-sm-6 col-xs-12">
          <div class="col-md-3 col-sm-6 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2 class="temperature"><span aria-hidden="true" class="glyphicon glyphicon-fire"></span> <span class="title"></span> <span class="small">...</span> <span class="badge bg-red">!</span> <span class="badge bg-orange">!</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">!</span></h2>
                <h2 class="humidity"><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> <span class="title"></span> <span class="small">...</span> <span class="badge bg-red">!</span> <span class="badge bg-orange">!</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">!</span></h2>
                <h2 class="moisture"><span aria-hidden="true" class="glyphicon glyphicon-tint"></span> <span class="title"></span> <span class="small">...</span> <span class="badge bg-red">!</span> <span class="badge bg-orange">!</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">!</span></h2>
                <h2 class="conductivity"><span aria-hidden="true" class="glyphicon glyphicon-oil"></span> <span class="title"></span> <span class="small">...</span> <span class="badge bg-red">!</span> <span class="badge bg-orange">!</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">!</span></h2>
                <h2 class="distance"><span aria-hidden="true" class="glyphicon glyphicon-signal"></span> <span class="title"></span> <span class="small">...</span> <span class="badge bg-red">!</span> <span class="badge bg-orange">!</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">!</span></h2>
                <h2 class="ph"><span aria-hidden="true" class="glyphicon glyphicon-scale"></span> <span class="title"></span> <span class="small">...</span> <span class="badge bg-red">!</span> <span class="badge bg-orange">!</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">!</span></h2>
                <h2 class="light uva uvb uvi"><span aria-hidden="true" class="glyphicon glyphicon-adjust"></span> <span class="title"></span> <span class="small">...</span> <span class="badge bg-red">!</span> <span class="badge bg-orange">!</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">!</span></h2>
                <h2 class="fertility"><span aria-hidden="true" class="glyphicon glyphicon-grain"></span> <span class="title"></span> <span class="small">...</span> <span class="badge bg-red">!</span> <span class="badge bg-orange">!</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">!</span></h2>
                <h2 class="co2"><span aria-hidden="true" class="glyphicon glyphicon-tree-conifer"></span> <span class="title"></span> <span class="small">...</span> <span class="badge bg-red">!</span> <span class="badge bg-orange">!</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">!</span></h2>
                <h2 class="volume"><span aria-hidden="true" class="glyphicon glyphicon-signal"></span> <span class="title"></span> <span class="small">...</span> <span class="badge bg-red">!</span> <span class="badge bg-orange">!</span> <span class="badge bg-blue" title="{{_('Excluded from average calculation')}}">!</span></h2>
                <div class="clearfix"></div>
              </div>
              <div class="x_content" >
                <div class="col-md-12 col-sm-12 col-xs-12">
                  <div class="sidebar-widget text-center">
                    <canvas class="gauge"></canvas>
                    <div class="goal-wrapper">
                      <span class="gauge-value">...</span> <span class="gauge-indicator"></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <style>
          .x_panel {
            padding-left: 0px;
            padding-right: 0px;
            overflow: hidden;
          }
        </style>
        <script type="text/javascript">
          $(document).ready(function() {
            source_row = $('div.row.sensor').html();
            $('div.row.sensor').remove();

            $.get('/api/sensors',function(json_data) {
              $.each(sortByKey(json_data.sensors,'name'),function(index,sensor_data){
                add_sensor_status_row(sensor_data);
                update_sensor(sensor_data);
                sensor_gauge('sensor_' + sensor_data.id, sensor_data);
              });
              $('div.row.jumbotron').toggle($('div.row.sensor:visible').length == 0);
              $('div.row.sensor').removeClass('row');
              reload_reload_theme();
            });
          });
        </script>
% include('inc/page_footer.tpl')
