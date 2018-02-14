% include('inc/page_header.tpl')
        <div class="row logtail">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2><span class="title">{{_('Last update')}}</span> <small>...</small></h2>
                <ul class="nav navbar-right panel_toolbox">
                  <li>
                    <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                  </li>
                  <li class="dropdown">
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-wrench" title="{{_('Options')}}"></i></a>
                    <ul class="dropdown-menu" role="menu">
                      <li>
                        <a href="javascript:;" onclick="menu_click('system_settings.html')">{{_('Settings')}}</a>
                      </li>
                      <li>
                        <a href="/log/terrariumpi.log" target="_blank">{{_('Download')}}</a>
                      </li>
                    </ul>
                  </li>
                  <li>
                    <a class="close-link"><i class="fa fa-close" title="{{_('Close')}}"></i></a>
                  </li>
                </ul>
                <div class="clearfix"></div>
              </div>
              <div class="x_content"><pre></pre>
              </div>
            </div>
          </div>
        </div>
        <script type="text/javascript">
          $(document).ready(function() {
            // Read the last 100KB of logfile data
            $.ajax({
              url: 'log/terrariumpi.log',
              headers: {Range: "bytes=-102400"},
              success: function( data ) {
                var content = $('.x_content pre');
                // Data in wrong order. Need to reverse it.
                $.each(data.split("\n"),function(counter,line){
                  if ((line = line.trim()) != '') {
                    content.prepend(line + "\n");
                  }
                });
                reload_reload_theme();
              }
            });
          });
        </script>
% include('inc/page_footer.tpl')
