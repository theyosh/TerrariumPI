% include('inc/page_header.tpl')
        <div class="row switch">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2><span aria-hidden="true" class="glyphicon glyphicon-flash"></span>{{_('Switch')}} <span class="title"></span>
                <small class="current_usage"></small> <small class="total_usage"></small></h2>
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
                        <a href="javascript:;" onclick="menu_click('switch_settings.html')">{{_('Settings')}}</a>
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
                  <div class="power_switch big">
                    <span aria-hidden="true" class="glyphicon glyphicon-off" title="{{_('Toggle power switch')}}"></span>
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
            source_row = $('div.row.switch').html();
            $('div.row.switch').remove();

            $.get('/api/switches',function(json_data) {
              $.each(json_data.switches,function(index,powerswitch_data){
                add_power_switch_status_row(powerswitch_data);
                update_power_switch(powerswitch_data);
                load_history_graph('powerswitch_' + powerswitch_data.id,'switch','/api/history/switches/' + powerswitch_data.id);
              });
              reload_reload_theme();
            });
          });
        </script>
% include('inc/page_footer.tpl')
