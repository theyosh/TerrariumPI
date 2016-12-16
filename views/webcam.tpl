% include('inc/page_header.tpl')
        <div class="row">
          % for item in range(0,amount_of_webcams):
          <div class="col-md-4 col-sm-6 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2><span class="title">{{_('Webcam')}}</span> <small>...</small></h2>
                <ul class="nav navbar-right panel_toolbox">
                  <li>
                    <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                  </li>
                  <li class="dropdown">
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="#" role="button"><i class="fa fa-wrench"></i></a>
                    <ul class="dropdown-menu" role="menu">
                      <li>
                        <a href="#" onclick="menu_click('webcam_settings.html')">{{_('Settings')}}</a>
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
                <div class="webcam"></div>
              </div>
            </div>
          </div>
          % end
        </div>
        <script type="text/javascript">
          $(document).ready(function() {
            $.get('/api/webcams',function(data) {
              globals.webcams = [];
              var webcams = $('div.webcam');
              $.each(data.webcams, function(index,value){
                if ($(webcams[index]).attr('id') === undefined) {
                  $(webcams[index]).attr('id','webcam_' + value.id).height($(webcams[index]).width());
                }
                initWebcam(value.id, value.name, value.max_zoom);
              });
            });
          });
        </script>
% include('inc/page_footer.tpl')
