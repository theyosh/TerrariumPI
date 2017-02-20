% include('inc/page_header.tpl')
        <div class="row">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="" data-example-id="togglable-tabs" role="tabpanel">
              <ul class="nav nav-tabs bar_tabs" id="myTab" role="tablist">
                <li class="active" role="presentation">
                  <a aria-expanded="true" data-toggle="tab" href="#tab_terrariumpi" id="terrariumpi-tab" role="tab">TerrariumPI</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#tab_usage" id="usage-tab" role="tab">Usage</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#tab_contact" id="contact-tab" role="tab">Contact</a>
                </li>
              </ul>
              <div class="tab-content" id="myTabContent">
                <div aria-labelledby="terrariumpi-tab" class="tab-pane fade active in" id="tab_terrariumpi" role="tabpanel">
                  <h1>TerrariumPI</h1>
                  <p>Use TerrariumPI to automate your own reptile environment</p>
                </div>
                <div aria-labelledby="usage-tab" class="tab-pane fade" id="tab_usage" role="tabpanel">
                  <p>This software is able to use temperature and humidity sensors. Together with power switches it is possible to regulate your terrarium.
                  
                  </p>
                
                </div>
                <div aria-labelledby="contact-tab" class="tab-pane fade" id="tab_contact" role="tabpanel">
                  <p>Questions or problems? Contact me at <a href="mailto:terrariumpi@theyosh.nl">terrariumpi@theyosh.nl</a></p>
                
                </div>
              </div>
            </div>
          </div>
        </div>
% include('inc/page_footer.tpl')
