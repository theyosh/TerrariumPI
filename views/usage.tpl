% include('inc/page_header.tpl')
        <div class="row documentation">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="" data-example-id="togglable-tabs" role="tabpanel">
              <ul class="nav nav-tabs bar_tabs" id="usage_tablist" role="tablist">
                <li class="active" role="presentation">
                  <a aria-expanded="true" data-toggle="tab" href="#usage-tab-dashboard" id="usage_tab_dashboard" role="tab">{{_('Home')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#usage-tab-weather" id="usage_tab_weather" role="tab">{{_('Weather')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#usage-tab-sensors" id="usage_tab_sensors" role="tab">{{_('Sensors')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#usage-tab-switches" id="usage_tab_switches" role="tab">{{_('Switches')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#usage-tab-doors" id="usage_tab_doors" role="tab">{{_('Doors')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#usage-tab-webcam" id="usage_tab_webcam" role="tab">{{_('Webcam')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#usage-tab-system" id="usage_tab_system" role="tab">{{_('System')}}</a>
                </li>
              </ul>
              <div class="tab-content" id="usage_content">
                <div aria-labelledby="usage_tab_dashboard" class="tab-pane fade active in" id="usage-tab-dashboard" role="tabpanel">
                  % include('inc/usage_dashboard.tpl')
                </div>
                <div aria-labelledby="usage_tab_weather" class="tab-pane fade" id="usage-tab-weather" role="tabpanel">
                  % include('inc/usage_weather.tpl')
                </div>
                <div aria-labelledby="usage_tab_sensors" class="tab-pane fade" id="usage-tab-sensors" role="tabpanel">
                  <h1>{{_('Sensors')}}</h1>
                  <p></p>
                </div>
                <div aria-labelledby="usage_tab_switches" class="tab-pane fade" id="usage-tab-switches" role="tabpanel">
                  <h1>{{_('Switches')}}</h1>
                  <p></p>
                </div>
                <div aria-labelledby="usage_tab_doors" class="tab-pane fade" id="usage-tab-doors" role="tabpanel">
                  <h1>{{_('Doors')}}</h1>
                  <p></p>
                </div>
                <div aria-labelledby="usage_tab_webcam" class="tab-pane fade" id="usage-tab-webcam" role="tabpanel">
                  <h1>{{_('Webcam')}}</h1>
                  <p></p>
                </div>
                <div aria-labelledby="usage_tab_system" class="tab-pane fade" id="usage-tab-system" role="tabpanel">
                  <h1>{{_('System')}}</h1>
                  <p></p>
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
