% include('inc/page_header.tpl')
        <div class="row jumbotron">
          <div class="col-md-12 col-sm-12 col-xs-12">
              <h1>{{_('No doors available')}}</h1>
          </div>
        </div>
        <div class="row door">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2><span aria-hidden="true" class="glyphicon glyphicon-lock"></span> {{_('Door')}} <span class="title"></span> <small class="total_usage"></small></h2>
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
                        <a href="javascript:;" onclick="menu_click('door_settings.html')">{{_('Settings')}}</a>
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
                  <div class="door_status">
                    <i class="fa fa-lock" title="{{_('Door status')}}"></i>
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
            source_row = $('div.row.door').html();
            $('div.row.door').remove();

            $.get('/api/doors',function(json_data) {
              $('div.row.jumbotron').toggle(json_data.doors.length == 0);
              $.each(sortByKey(json_data.doors,'name'),function(index,door_data){
                add_door_status_row(door_data);
                update_door(door_data);
                load_history_graph('door_' + door_data.id,'door','/api/history/doors/' + door_data.id);
              });
              reload_reload_theme();
            });
          });
        </script>
% include('inc/page_footer.tpl')
