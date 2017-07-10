% include('inc/page_header.tpl')
        <div class="x_panel">
          <div class="x_title">
            <h2><span class="glyphicon glyphicon-info-sign" aria-hidden="true" title="{{_('Information')}}"></span> {{_('Help')}}<small></small></h2>
            <ul class="nav navbar-right panel_toolbox">
              <li>
                <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
              </li>
              <li>
                <a class="close-link"><i class="fa fa-close" title="{{_('Close')}}"></i></a>
              </li>
            </ul>
            <div class="clearfix"></div>
          </div>
          <div class="x_content">
            <p>{{_('Here you can configure the weather settings. Currently only data from https://yr.no is supported:')}}</p>
            <ul>
              <li>
                <strong>{{_('Location')}}</strong>: {{_('Holds the full url of the XML source.')}}
              </li>
              <li>
                <strong>{{_('Wind speed')}}</strong>: {{_('Holds the wind speed indicator.')}}
              </li>
              <li>
                <strong>{{_('Temperature')}}</strong>: {{_('Holds the temperature indicator.')}}
              </li>
            </ul>
          </div>
        </div>
        <form action="/api/config/weather" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
          <div class="row">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 id="deviceid">{{_('Weather')}} <small>...</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="location">{{_('Location')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" id="location" name="location" required="required" type="text" placeholder="{{_('Location')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Enter the full url to the weather data source. For now only YR.no is supported')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="windspeed">{{_('Wind speed')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Choose the windspeed indicator. The software will recalculate to the chosen indicator')}}">
                        <select class="form-control" name="windspeed" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option>
                            </option>
                          <option value="ms">
                            {{_('m/s')}}
                          </option>
                          <option value="kmh">
                            {{_('km/h')}}
                          </option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature">{{_('Temperature')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{_('Choose the temperature indicator. The software will recalulate to the chosen indicator')}}">
                        <select class="form-control" name="temperature" tabindex="-1" placeholder="{{_('Select an option')}}">
                          <option>
                            </option>
                          <option value="C">
                            C
                          </option>
                          <option value="F">
                            F
                          </option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div class="ln_solid"></div>
                  <div class="form-group">
                    <div class="col-md-11 col-sm-11 col-xs-12 text-center">
                      <button class="btn btn-success" type="submit">{{_('Submit')}}</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </form>
        <script type="text/javascript">
          $(document).ready(function() {
            var windspeed_selector = $("select[name='windspeed']").select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            });

            var temperature_selector = $("select[name='temperature']").select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            });

            $.get($('form').attr('action'),function(data){
              $('h2 small').text(data.type);
              $('input[name="location"]').val(data.location);

              windspeed_selector.val(data.windspeed);
              windspeed_selector.trigger('change');
              temperature_selector.val(data.temperature);
              temperature_selector.trigger('change');
            });
          });
        </script>
% include('inc/page_footer.tpl')
