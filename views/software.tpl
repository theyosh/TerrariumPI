% include('inc/page_header.tpl')
        <div class="row">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="" data-example-id="togglable-tabs" role="tabpanel">
              <ul class="nav nav-tabs bar_tabs" id="myTab" role="tablist">
                <li class="active" role="presentation">
                  <a aria-expanded="true" data-toggle="tab" href="#raspbian" id="raspbian-tab" role="tab">Raspbian</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#owfs" id="owfs-tab" role="tab">OWFS</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#python" id="python-tab2" role="tab">Python</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#webinterface" id="webinterface-tab2" role="tab">Webinterface</a>
                </li>
              </ul>
              <p>Here you can see the software that is used in TerrariumPI</p>
              <div class="tab-content" id="myTabContent">
                <div aria-labelledby="raspbian-tab" class="tab-pane fade active in" id="raspbian" role="tabpanel">
                  <p class="lead">Raspbian</p>
                  <p>The OS is Raspbian. Which is a Debian version for the Raspberry PI. <a href="http://www.raspbian.org/" target="_blank" title="Raspbian OS Website">http://www.raspbian.org/</a></p>
                </div>
                <div aria-labelledby="owfs-tab" class="tab-pane fade" id="owfs" role="tabpanel">
                  <p class="lead">OWFS 1-Wire File System</p>
                  <p>The OWFS 1-Wire File System software is used for reading out the 1-Wire temperatures and humidity sensors. <a href="http://owfs.org/" target="_blank" title="OWFS 1-Wire File System Website">http://owfs.org/</a></p>
                </div>
                <div aria-labelledby="python-tab" class="tab-pane fade" id="python" role="tabpanel">
                  <p class="lead">Python</p>
                  <p>The software is completely written in Python. It is tested on version 2.7. <a href="http://python.org/" target="_blank" title="Python Website">http://python.org/</a></p>
                  <div class="col-xs-9">
                    <!-- Tab panes -->
                    <div class="tab-content">
                      <div class="tab-pane active" id="python_bottle">
                        <p class="lead">Python module Bottle</p>
                        <p>Bottle: Python Web Framework. <a href="http://bottlepy.org/" target="_blank" title="Python module bottle">http://bottlepy.org/</a></p>
                      </div>
                      <div class="tab-pane" id="python_ow">
                        <p class="lead">Python module ow</p>
                        <p>Python module for reading from the OWFS software. <a href="http://packages.debian.org/search?keywords=python-ow" target="_blank" title="Python module ow">http://packages.debian.org/search?keywords=python-ow</a></p>
                      </div>
                      <div class="tab-pane" id="python_pylibftdi">
                        <p class="lead">Python module pylibftdi</p>
                        <p>pylibftdi is a minimal Pythonic interface to FTDI devices using libftdi. <a href="https://bitbucket.org/codedstructure/pylibftdi/" target="_blank" title="Python module pylibftdi">https://bitbucket.org/codedstructure/pylibftdi/</a></p>
                      </div>
                    </div>
                  </div>
                  <div class="col-xs-3">
                    <!-- required for floating -->
                    <!-- Nav tabs -->
                    <ul class="nav nav-tabs tabs-right">
                      <li class="active">
                        <a data-toggle="tab" href="#python_bottle">Bottle</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#python_ow">OW</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#python_pylibftdi">pylibftdi</a>
                      </li>
                    </ul>
                  </div>
                </div>
                <div aria-labelledby="webinterface-tab" class="tab-pane fade" id="webinterface" role="tabpanel">
                  <p class="lead">Webinterface</p>
                  <p>Gentellela Admin is a free to use Bootstrap admin template. This template uses the default Bootstrap 3 styles along with a variety of powerful jQuery plugins and tools to create a powerful framework for creating admin panels or back-end dashboards.</p>
                  <p>Theme uses several libraries for charts, calendar, form validation, wizard style interface, off-canvas navigation menu, text forms, date range, upload area, form autocomplete, range slider, progress bars, notifications and much more.</p>
                  <p>We would love to see how you use this awesome admin template. You can notify us about your site, app or service by tweeting to @colorlib. Once the list will grown long enough we will write a post similar to this to showcase the best examples.</p>
                  <p><a href="https://github.com/puikinsh/gentelella" target="_blank">Gentelella</a> - Bootstrap Admin Template by Colorlib</p>
                </div>
              </div>
            </div>
          </div>
        </div>
% include('inc/page_footer.tpl')
