% include('inc/page_header.tpl')
        % for item in range(0,amount_of_switches):
        <div class="row switch">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2><span aria-hidden="true" class="glyphicon glyphicon-flash"></span> <span class="title">Switch</span> <small class="data_update">live...</small> <span class="badge bg-red" style="display:none;">warning</span></h2>
                <ul class="nav navbar-right panel_toolbox">
                  <li>
                    <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                  </li>
                  <li class="dropdown">
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="#" role="button"><i class="fa fa-wrench"></i></a>
                    <ul class="dropdown-menu" role="menu">
                      <li>
                        <a href="#" onclick="menu_click('switch_settings.html')">Settings</a>
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
                power_div = $(power_divs[value.nr-1]);
                power_div.attr('id','switch_' + value.id);
                power_div.find('div.history_graph').attr('id','history_graph_' + value.id);
                update_power_switch(value.id,value);
              });
              update_switch_history();
            });
          });
        </script>
% include('inc/page_footer.tpl')
