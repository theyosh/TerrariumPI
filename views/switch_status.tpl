% include('inc/page_header.tpl')
        % for item in range(0,amount_of_switches):
        <div class="row switch">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2><span aria-hidden="true" class="glyphicon glyphicon-flash"></span> <span class="title">{{_('Switch')}}</span>
                <small class="data_update">...</small> <small class="total_usage">...</small></h2>
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
                        <a href="javascript:;" onclick="menu_click('switch_settings.html')">{{_('Settings')}}</a>
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
                    <span aria-hidden="true" class="glyphicon glyphicon-off" onclick="toggleSwitch($(this).parents('div.row.switch').attr('id'))"></span>
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
            $.get('/api/switches',function(data) {
              var power_divs = $('div.row.switch');
              $.each(data.switches,function(index,value){
                $(power_divs[index]).attr('id','switch_' + value.id).show()
                update_power_switch(value.id,value);
                load_history_graph('switch_' + value.id,'switch','/api/history/switches/' + value.id);
              });
              setContentHeight();
            });
          });
        </script>
% include('inc/page_footer.tpl')
