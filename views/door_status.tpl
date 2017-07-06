% include('inc/page_header.tpl')
        % for item in range(0,amount_of_doors):
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
                        <a href="javascript:;" onclick="menu_click('door_settings.html')">{{_('Settings')}}</a>
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
        % end
        <script type="text/javascript">
          $(document).ready(function() {
            $.get('/api/doors',function(data) {
              var rows = $('div.row.door');
              $.each(data.doors, function(index,door) {
                // Add an id to the row when first run
                $(rows[index]).attr('id',door.id);
                $('h2 span.title', rows[index]).text(door.name);
                $('h2 small', rows[index]).text((door.state === 'closed'  ? '{{_('closed')}}' : '{{_('open')}}' ));
                $('.sidebar-widget i.fa-lock',rows[index]).removeClass('red','green','closed','open')
                                                  .addClass(door.state + ' ' + (door.state === 'closed' ? 'green':'red'))
                                                  .attr({'title': (door.state === 'closed'  ? '{{_('Door is closed')}}' : '{{_('Door is open')}}' )});


                load_history_graph(door.id,'door','/api/history/doors/' + door.id);
              });
            });
          });
        </script>
% include('inc/page_footer.tpl')
