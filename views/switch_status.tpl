% include('inc/page_header.tpl')
            % for item in range(0,amount_of_switches):
            <div class="row switch">
               <div class="x_panel">
                 <div class="x_title">
                   <h2><span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <span class="title">Switch</span> <small class="data_update">live...</small> <span class="badge bg-red" style="display:none;">warning</span></h2>
                   <ul class="nav navbar-right panel_toolbox">
                     <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                     </li>
                     <li class="dropdown">
                       <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false"><i class="fa fa-wrench"></i></a>
                       <ul class="dropdown-menu" role="menu">
                         <li><a href="#">Settings 1</a>
                         </li>
                         <li><a href="#">Settings 2</a>
                         </li>
                       </ul>
                     </li>
                     <li><a class="close-link"><i class="fa fa-close"></i></a>
                     </li>
                   </ul>
                   <div class="clearfix"></div>
                 </div>
                 <div class="x_content">
                   <div class="col-md-4 col-sm-4 col-xs-12">
                     <div class="sidebar-widget">

                       <div class="power-switch" style="font-size: 4em; margin-top: 0.3em">

                          <span class="glyphicon glyphicon-off" aria-hidden="true"></span>

                        </div>


                     </div>
                   </div>
                   <div class="col-md-8 col-sm-8 col-xs-12">
                     <div class="history_graph loading" style="display:block!important;"> <!-- <span class="loading">loading ... <i class="fa fa-spin fa-spinner"></i></span> --> </div>
                   </div>
                 </div>
               </div>
             </div>

              % end

            <script type="text/javascript">
               $(document).ready(function() {
                  $.get('/api/switches',function(data){
                     var rows = $('div.row.switch');
                     $.each(data.switches, function(index,powerswitch) {
                        var power_switch_div = $('div.row.switch#switch_' + powerswitch.id);
                        if (power_switch_div.length == 0) {
                           power_switch_div = $(rows[index]).attr('id','switch_' + powerswitch.id);
                           power_switch_div.find('div.history_graph').attr('id','history_graph_' + powerswitch.id).css('height',power_switch_div.find('div.history_graph').parents('div.x_content').height() + 'px');
                        }
                        power_switch_div.find('h2 span.title').text('Switch ' + powerswitch.name);
                        power_switch_div.find('h2 small.data_update').text(powerswitch.power_wattage + 'W, ' + powerswitch.water_flow + 'L/m');
                        power_switch_div.find('span.glyphicon').removeClass('blue green').addClass((powerswitch.state ? 'green' : 'blue'));
                     });
                     update_switch_history();
                  });
               });

             function update_switch_history() {
                if ($('div.row.switch').length >= 0) {
                  $.getJSON('/api/history/switches',function(data){
                    $.each(data.switches, function(index,powerswitch) {
                     var graphdata = {power_wattage:[], water_flow: []}
                     var state_chage = -1

                     console.log('graph data:', powerswitch);
                     $.each(powerswitch.state, function (counter, status) {
                        if (!status[1]) {
                           powerswitch.power_wattage[counter][1] = 0;
                           powerswitch.water_flow[counter][1] = 0;
                        }

                        if (counter > 0 && state_chage != status[1]) {
                           // Copy previous object to get the right status with current timestamp
                           var copy = $.extend(true, {}, powerswitch.power_wattage[counter-1]);
                           copy[0] = status[0];
                           graphdata.power_wattage.push(copy);

                           var copy = $.extend(true, {}, powerswitch.water_flow[counter-1]);
                           copy[0] = status[0];
                           graphdata.water_flow.push(copy);

                           state_chage = status[1];
                        }

                        graphdata.power_wattage.push(powerswitch.power_wattage[counter]);
                        graphdata.water_flow.push(powerswitch.water_flow[counter]);

                        if (counter == powerswitch.state.length-1) {
                           // Add endpoint which is a copy of the last point, with current time
                           var copy = $.extend(true, {}, powerswitch.power_wattage[counter]);
                           copy[0] = (new Date()).getTime();
                           graphdata.power_wattage.push(copy);

                           var copy = $.extend(true, {}, powerswitch.water_flow[counter]);
                           copy[0] = (new Date()).getTime();
                           graphdata.water_flow.push(copy);
                        }
                     });
                      history_graph(index,graphdata, 'switch');
                    });
                    clearTimeout(globals['updatetimer']);
                    globals['updatetimer'] = setTimeout(function(){
                      update_switch_history();
                    }
                    , 1 * 60 * 1000)
                  });
                }
             }
            </script>
% include('inc/page_footer.tpl')
