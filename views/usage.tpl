% include('inc/page_header.tpl')
        <div class="row documentation">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="" data-example-id="togglable-tabs" role="tabpanel">
              <ul class="nav nav-tabs bar_tabs" id="usage_tablist" role="tablist">
                <li class="active" role="presentation">
                  <a aria-expanded="true" data-toggle="tab" href="#usage-tab-dashboard" id="usage_tab_dashboard" role="tab"><i class="fa fa-home"></i> {{_('Home')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#usage-tab-weather" id="usage_tab_weather" role="tab"><i class="fa fa-cloud"></i> {{_('Weather')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#usage-tab-profile" id="usage_tab_profile" role="tab"><i class="fa fa-cloud"></i> {{_('Profile')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#usage-tab-sensors" id="usage_tab_sensors" role="tab"><i class="fa fa-tint"></i> {{_('Sensors')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#usage-tab-switches" id="usage_tab_switches" role="tab"><i class="fa fa-flash"></i> {{_('Switches')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#usage-tab-doors" id="usage_tab_doors" role="tab"><i class="fa fa-lock"></i> {{_('Doors')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#usage-tab-webcam" id="usage_tab_webcam" role="tab"><i class="fa fa-video-camera"></i> {{_('Webcam')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#usage-tab-audio" id="usage_tab_audio" role="tab"><i class="fa fa-music"></i> {{_('Audio')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#usage-tab-environment" id="usage_tab_system" role="tab"><i class="fa fa-lightbulb-o"></i> {{_('Environment')}}</a>
                </li>
              </ul>
              <div class="tab-content" id="usage_content">
                <div aria-labelledby="usage_tab_dashboard" class="tab-pane fade active in" id="usage-tab-dashboard" role="tabpanel">
                  % include('inc/usage_dashboard.tpl')
                </div>
                <div aria-labelledby="usage_tab_weather" class="tab-pane fade" id="usage-tab-weather" role="tabpanel">
                  % include('inc/usage_weather.tpl')
                </div>
                <div aria-labelledby="usage_tab_profile" class="tab-pane fade" id="usage-tab-profile" role="tabpanel">
                  % include('inc/usage_profile.tpl')
                </div>
                <div aria-labelledby="usage_tab_sensors" class="tab-pane fade" id="usage-tab-sensors" role="tabpanel">
                  % include('inc/usage_sensors.tpl')
                </div>
                <div aria-labelledby="usage_tab_switches" class="tab-pane fade" id="usage-tab-switches" role="tabpanel">
                  % include('inc/usage_switches.tpl')
                </div>
                <div aria-labelledby="usage_tab_doors" class="tab-pane fade" id="usage-tab-doors" role="tabpanel">
                  % include('inc/usage_doors.tpl')
                </div>
                <div aria-labelledby="usage_tab_audio" class="tab-pane fade" id="usage-tab-audio" role="tabpanel">
                  % include('inc/usage_audio.tpl')
                </div>
                <div aria-labelledby="usage_tab_webcam" class="tab-pane fade" id="usage-tab-webcam" role="tabpanel">
                  % include('inc/usage_webcams.tpl')
                </div>
                <div aria-labelledby="usage_tab_environment" class="tab-pane fade" id="usage-tab-environment" role="tabpanel">
                  % include('inc/usage_environment.tpl')
                </div>
              </div>
            </div>
          </div>
        </div>
        <script type="text/javascript">
          $('ul.nav.nav-tabs.tabs-right a').hover(
              function() {
                $($(this).attr('href').replace('usage-tab','screenshot').replace(/-/g,'_')).addClass('hover');
              },
              function() {
                $($(this).attr('href').replace('usage-tab','screenshot').replace(/-/g,'_')).removeClass('hover');
              }
          );

          $('div.interactive_screenshot div.click_area').on('click',function(){
            var link = $(this).attr('id').replace('screenshot','usage-tab').replace(/_/g,'-');
            $('ul.nav.nav-tabs.tabs-right a[href="#' + link + '"]').click();
          });
        </script>
% include('inc/page_footer.tpl')
