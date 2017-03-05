% include('inc/page_header.tpl')
        <div class="row door">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2><span class="title">{{_('Door status')}}</span> <small>...</small> <span class="badge bg-red" style="display:none;">{{_('warning')}}</span></h2>
                <ul class="nav navbar-right panel_toolbox">
                  <li>
                    <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                  </li>
                  <li class="dropdown">
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-calendar"></i></a>
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
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-wrench"></i></a>
                    <ul class="dropdown-menu" role="menu">
                      <li>
                        <a href="javascript:;" onclick="menu_click('system_settings.html')">{{_('Settings')}}</a>
                      </li>
                    </ul>
                  </li>
                  <li>
                    <a class="close-link"><i class="fa fa-close"></i></a>
                  </li>
                </ul>
                <div class="clearfix"></div>
              </div>
              <div class="x_content">
                <div class="col-md-3 col-sm-4 col-xs-12">
                  <div class="sidebar-widget">
                    <i class="fa fa-lock"></i>
                  </div>
                </div>
                <div class="col-md-9 col-sm-8 col-xs-12">
                  <div class="history_graph loading"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row load">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2><span class="title">{{_('CPU Load')}}</span> <small>...</small> <span class="badge bg-red" style="display:none;">{{_('warning')}}</span></h2>
                <ul class="nav navbar-right panel_toolbox">
                  <li>
                    <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                  </li>
                  <li class="dropdown">
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-calendar"></i></a>
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
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-wrench"></i></a>
                    <ul class="dropdown-menu" role="menu">
                      <li>
                        <a href="javascript:;" onclick="menu_click('system_settings.html')">{{_('Settings')}}</a>
                      </li>
                    </ul>
                  </li>
                  <li>
                    <a class="close-link"><i class="fa fa-close"></i></a>
                  </li>
                </ul>
                <div class="clearfix"></div>
              </div>
              <div class="x_content">
                <div class="col-md-3 col-sm-4 col-xs-12">
                  <div class="sidebar-widget">
                    <canvas class="gauge"></canvas>
                    <div class="goal-wrapper">
                      <span class="gauge-value pull-left">...</span> <span class="gauge-value pull-left">%</span>
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
        <div class="row temperature">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2><span class="title">{{_('CPU Temperature')}}</span> <small>...</small> <span class="badge bg-red" style="display:none;">{{_('warning')}}</span></h2>
                <ul class="nav navbar-right panel_toolbox">
                  <li>
                    <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                  </li>
                  <li class="dropdown">
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-calendar"></i></a>
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
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-wrench"></i></a>
                    <ul class="dropdown-menu" role="menu">
                      <li>
                        <a href="javascript:;" onclick="menu_click('system_settings.html')">{{_('Settings')}}</a>
                      </li>
                    </ul>
                  </li>
                  <li>
                    <a class="close-link"><i class="fa fa-close"></i></a>
                  </li>
                </ul>
                <div class="clearfix"></div>
              </div>
              <div class="x_content">
                <div class="col-md-3 col-sm-4 col-xs-12">
                  <div class="sidebar-widget">
                    <canvas class="gauge"></canvas>
                    <div class="goal-wrapper">
                      <span class="gauge-value pull-left">...</span> <span class="gauge-value pull-left">°C</span>
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
        <div class="row memory">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2><span class="title">{{_('Memory usage')}}</span> <small>...</small> <span class="badge bg-red" style="display:none;">{{_('warning')}}</span></h2>
                <ul class="nav navbar-right panel_toolbox">
                  <li>
                    <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                  </li>
                  <li class="dropdown">
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-calendar"></i></a>
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
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-wrench"></i></a>
                    <ul class="dropdown-menu" role="menu">
                      <li>
                        <a href="javascript:;" onclick="menu_click('system_settings.html')">{{_('Settings')}}</a>
                      </li>
                    </ul>
                  </li>
                  <li>
                    <a class="close-link"><i class="fa fa-close"></i></a>
                  </li>
                </ul>
                <div class="clearfix"></div>
              </div>
              <div class="x_content">
                <div class="col-md-3 col-sm-4 col-xs-12">
                  <div class="sidebar-widget">
                    <canvas class="gauge"></canvas>
                    <div class="goal-wrapper">
                      <span class="gauge-value pull-left">...</span> <span class="gauge-value pull-left">MB</span>
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
        <div class="row uptime">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2><span class="title">{{_('Uptime')}}</span> <small class="data_update">...</small></h2>
                <ul class="nav navbar-right panel_toolbox">
                  <li>
                    <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                  </li>
                  <li class="dropdown">
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-calendar"></i></a>
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
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-wrench"></i></a>
                    <ul class="dropdown-menu" role="menu">
                      <li>
                        <a href="javascript:;" onclick="menu_click('system_settings.html')">{{_('Settings')}}</a>
                      </li>
                    </ul>
                  </li>
                  <li>
                    <a class="close-link"><i class="fa fa-close"></i></a>
                  </li>
                </ul>
                <div class="clearfix"></div>
              </div>
              <div class="x_content">
                <div class="col-md-12 col-sm-12 col-xs-12">
                  <div class="history_graph loading"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <script type="text/javascript">
          $(document).ready(function() {
            $.get('/api/door',function(data) {
              $.each(data, function (key,value) {
                var row = $('div.row.' + key).attr('id','system_' + key);
                $('h2 small', row).text((value === 'closed'  ? '{{_('closed')}}' : '{{_('open')}}' ));
                $('.sidebar-widget i.fa-lock',row).removeClass('red','green','closed','open')
                                                  .addClass(value + ' ' + (value === 'closed' ? 'green':'red'))
                                                  .attr({'title': (value === 'closed'  ? '{{_('Door is closed')}}' : '{{_('Door is open')}}' )});
                load_history_graph('system_' + key,key,'/api/history/' + key);
              });
            });
            $.get('/api/system',function(data) {
              $.each(data, function (key,value) {
                var row = $('div.row.' + key).attr('id','system_' + key);
                if (row.find('canvas').length == 1) {

                  gauge_data = {alarm: false, current : 0, alarm_min : 0, alarm_max: 0, min : 0, max : 0}
                  switch (key) {
                    case 'load':
                      gauge_data.current = value['load1'] * 100;
                      gauge_data.alarm_max = 80;
                      gauge_data.alarm_min = 0;
                      gauge_data.max = 100;
                      break;

                    case 'temperature':
                      gauge_data.current = value;
                      gauge_data.alarm_min = 30;
                      gauge_data.alarm_max = 60;
                      gauge_data.max = 80;
                      break;

                    case 'memory':
                      gauge_data.current = value['used'] / (1024 * 1024);
                      gauge_data.max = value['total'] / (1024 * 1024);
                      gauge_data.alarm_max = gauge_data.max * 0.9;
                      gauge_data.alarm_min = gauge_data.max * 0.1;
                      break;
                  }
                  gauge_data.alarm = gauge_data.current < gauge_data.alarm_min || gauge_data.current > gauge_data.alarm_max
                  sensor_gauge('system_' + key, gauge_data);
                }
                load_history_graph('system_' + key,'system_' + key,'/api/history/system/' + key);
              });
            });
          });
        </script>
% include('inc/page_footer.tpl')
