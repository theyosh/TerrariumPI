% include('inc/page_header.tpl')
        <div class="row documentation">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="" data-example-id="togglable-tabs" role="tabpanel">
              <ul class="nav nav-tabs bar_tabs" id="info_tablist" role="tablist">
                <li class="active" role="presentation">
                  <a aria-expanded="true" data-toggle="tab" href="#info-tab-terrariumpi" id="info_tab_terrariumpi" role="tab">{{_('TerrariumPI %s') % version,}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#info-tab-software" id="info_tab_software" role="tab">{{_('Used software')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#info-tab-contact" id="info_tab_contact" role="tab">{{_('Contact')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#info-tab-example" id="info_tab_example" role="tab">{{_('Example setup')}}</a>
                </li>
              </ul>
              <div class="tab-content" id="info_content">
                <div aria-labelledby="info_tab_terrariumpi" class="tab-pane fade active in" id="info-tab-terrariumpi" role="tabpanel">
                  <h2>{{_('TerrariumPI %s') % version,}}</h2>
                  <p>{{_('Use TerrariumPI to automate your own reptile environment. The software can handle a combination of multiple temperature and humidity sensors and relay switches to control a closed environment.')}}</p>
                  <img src="static/images/documentation/dashboard.png" alt="Dashboard screenshot" class="img-thumbnail" style="width:60%"/>
                </div>
                <div aria-labelledby="info_tab_software" class="tab-pane fade" id="info-tab-software" role="tabpanel">
                  <h2>{{_('Used software')}}</h2>
                  <p>{{!_('TerrariumPI is mainly written in Python version 2.7. The web interface is a bootstrap 3 template. It can be downloaded from %s.') % ('<a href="https://github.com/theyosh/TerrariumPI" target="_blank" title="' + _('Download TerrariumPI on Github') + '">Github</a>')}}</p>
                  <div class="col-xs-9">
                    <!-- Tab panes -->
                    <div class="tab-content">
                      <div class="tab-pane active" id="info-tab-software-python">
                        <h4>{{_('Python modules')}}</h4>
                        <p>{{_('The following external Python libraries are used')}}</p>
                        <strong>{{_('Raspbian OS')}}</strong>
                        <ul>
                          <li><strong>Bottle</strong> http://bottlepy.org/</li>
                          <li><strong>OW</strong> http://owfs.sourceforge.net/owpython.html</li>
                          <li><strong>RPi.GPIO</strong> https://pypi.python.org/pypi/RPi.GPIO</li>
                          <li><strong>PiCamera</strong> https://pypi.python.org/pypi/picamera/</li>
                          <li><strong>psutil</strong> https://pypi.python.org/pypi/psutil/</li>
                          <li><strong>OpenCV</strong> https://pypi.python.org/pypi/opencv-python</li>
                        </ul>
                        <strong>{{_('PIP')}}</strong>
                        <ul>
                          <li><strong>gevent</strong> https://pypi.python.org/pypi/gevent</li>
                          <li><strong>untangle</strong> https://pypi.python.org/pypi/untangle</li>
                          <li><strong>uptime</strong> https://pypi.python.org/pypi/uptime</li>
                          <li><strong>bottle_websocket</strong> https://pypi.python.org/pypi/bottle-websocket</li>
                          <li><strong>pylibftdi</strong> https://pypi.python.org/pypi/pylibftdi</li>
                        </ul>
                        <strong>{{_('Source')}}</strong>
                        <ul>
                          <li><strong>Adafruit DHT</strong> https://github.com/adafruit/Adafruit_Python_DHT</li>
                        </ul>
                      </div>
                      <div class="tab-pane" id="info-tab-software-webinterface">
                        <h4>{{_('Web interface')}}</h4>
                        <p>{{_('Gentellela Admin is a free to use Bootstrap admin template. This template uses the default Bootstrap 3 styles along with a variety of powerful jQuery plugins and tools to create a powerful framework for creating admin panels or back-end dashboards.')}}</p>
                        <p>{{_('Theme uses several libraries for charts, calendar, form validation, wizard style interface, off-canvas navigation menu, text forms, date range, upload area, form autocomplete, range slider, progress bars, notifications and much more.')}}</p>
                        <p>{{_('We would love to see how you use this awesome admin template. You can notify us about your site, app or service by tweeting to @colorlib. Once the list will grown long enough we will write a post similar to this to showcase the best examples.')}}</p>
                        <p><a href="https://github.com/puikinsh/gentelella" target="_blank">Gentelella</a> - Bootstrap Admin Template by Colorlib</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-xs-3">
                    <!-- required for floating -->
                    <!-- Nav tabs -->
                    <ul class="nav nav-tabs tabs-right">
                      <li class="active">
                        <a data-toggle="tab" href="#info-tab-software-python" title="{{_('Python modules')}}">{{_('Python modules')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#info-tab-software-webinterface" title="{{_('Web interface')}}">{{_('Web interface')}}</a>
                      </li>
                    </ul>
                  </div>
                </div>
                <div aria-labelledby="info_tab_contact" class="tab-pane fade" id="info-tab-contact" role="tabpanel">
                  <h2>{{_('Contact')}}</h2>
                  <p>{{!_('Questions or problems? Contact me at %s or open an issue on %s.') % ('<a href="mailto:terrariumpi@theyosh.nl">terrariumpi@theyosh.nl</a>', '<a href="https://github.com/theyosh/TerrariumPI" target="_blank" title="' + _('Download TerrariumPI on Github') + '">Github</a>')}}</p>
                  <h2>{{_('Feature request')}}</h2>
                  <p>{{!_('Missing something? Drop a feature request on %s and we will see what can be done.') % ('<a href="htt</a>ps://github.com/theyosh/TerrariumPI" target="_blank" title="' + _('Download TerrariumPI on Github') + '">Github</a>')}}</p>
                  <h2>{{_('Copyright')}}</h2>
                  <p>&copy; Copyright 2015 - 2017</p>
                </div>
                <div aria-labelledby="info_tab_example" class="tab-pane fade" id="info-tab-example" role="tabpanel">
                  <h2>{{_('Example setup')}}</h2>
                  <p>{{_('Here are some photos how you can use it.')}}</p>
                  <a href="static/images/photos/20170704_163655.jpg" data-fancybox="gallery"><img src="static/images/photos/20170704_163655.jpg" class="thumbnail alignleft" alt="test"/></a>
                  <a href="static/images/photos/20170704_163822.jpg" data-fancybox="gallery"><img src="static/images/photos/20170704_163822.jpg" class="thumbnail alignleft" /></a>
                  <a href="static/images/photos/20170704_163845.jpg" data-fancybox="gallery"><img src="static/images/photos/20170704_163845.jpg" class="thumbnail alignleft" /></a>
                  <a href="static/images/photos/20170704_164213.jpg" data-fancybox="gallery"><img src="static/images/photos/20170704_164213.jpg" class="thumbnail alignleft" /></a>
                  <a href="static/images/photos/20170704_164800.jpg" data-fancybox="gallery"><img src="static/images/photos/20170704_164800.jpg" class="thumbnail alignleft" /></a>
                  <a href="static/images/photos/20170704_165605.jpg" data-fancybox="gallery"><img src="static/images/photos/20170704_165605.jpg" class="thumbnail alignleft"/></a>
                  <a href="static/images/photos/20170704_165617.jpg" data-fancybox="gallery"><img src="static/images/photos/20170704_165617.jpg" class="thumbnail alignleft"/></a>
                  <a href="static/images/photos/20170704_165637.jpg" data-fancybox="gallery"><img src="static/images/photos/20170704_165637.jpg" class="thumbnail alignleft"/></a>
                  <a href="static/images/photos/20170704_172443.jpg" data-fancybox="gallery"><img src="static/images/photos/20170704_172443.jpg" class="thumbnail alignleft"/></a>
                  <a href="static/images/photos/20170704_173437.jpg" data-fancybox="gallery"><img src="static/images/photos/20170704_173437.jpg" class="thumbnail alignleft"/></a>
                  <a href="static/images/photos/20170704_174156.jpg" data-fancybox="gallery"><img src="static/images/photos/20170704_174156.jpg" class="thumbnail alignleft"/></a>
                  <a href="static/images/photos/20170704_174223.jpg" data-fancybox="gallery"><img src="static/images/photos/20170704_174223.jpg" class="thumbnail alignleft"/></a>
                  <a href="static/images/photos/20170704_201329.jpg" data-fancybox="gallery"><img src="static/images/photos/20170704_201329.jpg" class="thumbnail alignleft"/></a>
                  <a href="static/images/photos/20170706_113413.jpg" data-fancybox="gallery"><img src="static/images/photos/20170706_113413.jpg" class="thumbnail alignleft"/></a>
                  <a href="static/images/photos/20170706_113426.jpg" data-fancybox="gallery"><img src="static/images/photos/20170706_113426.jpg" class="thumbnail alignleft"/></a>
                  <a href="static/images/photos/20170706_194921.jpg" data-fancybox="gallery"><img src="static/images/photos/20170706_194921.jpg" class="thumbnail alignleft"/></a>
                  <a href="static/images/photos/20170706_195141.jpg" data-fancybox="gallery"><img src="static/images/photos/20170706_195141.jpg" class="thumbnail alignleft"/></a>
                  <a href="static/images/photos/20170707_105830.jpg" data-fancybox="gallery"><img src="static/images/photos/20170707_105830.jpg" class="thumbnail alignleft"/></a>
                  <a href="static/images/photos/DistanceSensor1.jpg" data-fancybox="gallery"><img src="static/images/photos/DistanceSensor1.jpg" class="thumbnail alignleft"/></a>
                  <a href="static/images/photos/DistanceSensor2.jpg" data-fancybox="gallery"><img src="static/images/photos/DistanceSensor2.jpg" class="thumbnail alignleft"/></a>
                  <a href="static/images/photos/DistanceSensor5.jpg" data-fancybox="gallery"><img src="static/images/photos/DistanceSensor5.jpg" class="thumbnail alignleft"/></a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <script type="text/javascript">
          $("[data-fancybox]").fancybox({
            // Options will go here
          });
        </script>
% include('inc/page_footer.tpl')
