% include('inc/page_header.tpl')
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



              $.each(json_data.webcams,function(index,webcam_data){
                initWebcam(webcam_data);



                //add_power_switch_status_row(switch_data);
                //update_power_switch(switch_data);



                //load_history_graph('powerswitch_' + switch_data.id,'switch','/api/history/switches/' + switch_data.id);
              });
              reload_reload_theme();
            });
          });
          /*

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
          */

        </script>
% include('inc/page_footer.tpl')
