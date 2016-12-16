% include('inc/page_header.tpl')
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
                <form action="/api/config/weather" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
                  <div class="form-group">
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="location">{{_('Location')}} <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <input class="form-control" id="location" name="location" required="required" type="text" placeholder="{{_('Location')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="windspeed">{{_('Wind speed')}} <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <div class="form-group">
                        <select class="form-control" name="windspeed" tabindex="-1">
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
                    <label class="control-label col-md-2 col-sm-2 col-xs-12" for="temperature">{{_('Temperature')}} <span class="required">*</span></label>
                    <div class="col-md-8 col-sm-8 col-xs-12">
                      <div class="form-group">
                        <select class="form-control" name="temperature" tabindex="-1">
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
                </form>
              </div>
            </div>
          </div>
        </div>
        <script type="text/javascript">
          $(document).ready(function() {
            var windspeed_selector = $("select[name='windspeed']").select2({
              placeholder: "Select a value",
              allowClear: false,
              minimumResultsForSearch: Infinity
            });

            var temperature_selector = $("select[name='temperature']").select2({
              placeholder: "Select a value",
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
