% include('inc/page_header.tpl')
            % for item in range(0,amount_of_switches):
            <div class="row switch">
              <div class="col-md-12 col-sm-12 col-xs-12">
                <div class="x_panel">
                  <div class="x_title">
                    <h2><span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <span class="title">Switch</span> <small class="data_update">live...</small> <span class="badge bg-red" style="display:none;">warning</span></h2>
                    <ul class="nav navbar-right panel_toolbox">
                      <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                      </li>
                      <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false"><i class="fa fa-wrench"></i></a>
                        <ul class="dropdown-menu" role="menu">
                          <li><a href="#" onclick="menu_click('switch_settings.html')">Settings</a> </li>
                        </ul>
                      </li>
                      <li><a class="close-link"><i class="fa fa-close"></i></a>
                      </li>
                    </ul>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                    <div class="col-md-3 col-sm-4 col-xs-12">
                      <div class="power_switch big">
                        <span class="glyphicon glyphicon-off" aria-hidden="true" onclick="toggleSwitch($(this).parents('div.row.switch').attr('id'))"></span>
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
                    $('div.row.switch').each(function(index,power_switch_div){
                       $(power_switch_div).attr('id','switch_' + data.switches[index].id);
                       $(power_switch_div).find('div.history_graph').attr('id','history_graph_' + data.switches[index].id);
                       update_power_switch(data.switches[index].id,data.switches[index]);
                    });
                    update_switch_history();
                 });
              });
            </script>
% include('inc/page_footer.tpl')
