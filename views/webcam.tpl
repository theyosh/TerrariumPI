% include('inc/page_header.tpl')
        <div class="row jumbotron">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <h1>{{_('No webcams available')}}</h1>
          </div>
        </div>
        <div class="row webcam">
          <div class="col-md-4 col-sm-6 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2><span aria-hidden="true" class="glyphicon glyphicon-facetime-video"></span> {{_('Webcam')}} <span class="title"></span></h2>
                <ul class="nav navbar-right panel_toolbox">
                  <li>
                    <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                  </li>
                  <li class="dropdown">
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-wrench" title="{{_('Options')}}"></i></a>
                    <ul class="dropdown-menu" role="menu">
                      <li>
                        <a href="javascript:;" onclick="menu_click('webcam_settings.html')">{{_('Settings')}}</a>
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
                <div class="webcam_player"></div>
              </div>
            </div>
          </div>
        </div>
        <script type="text/javascript">
          $(document).ready(function() {
            source_row = $('div.row.webcam').html();
            // Do not remove it, but clean it
            $('div.row.webcam').html('');

            $.get('/api/webcams',function(json_data) {
              $('div.row.jumbotron').toggle(json_data.webcams.length == 0);
              $.each(sortByKey(json_data.webcams,'name'),function(index,webcam_data){
                initWebcam(webcam_data);
              });
              reload_reload_theme();
            });
          });
        </script>
% include('inc/page_footer.tpl')
