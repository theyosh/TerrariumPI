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
          });
        </script>
% include('inc/page_footer.tpl')
