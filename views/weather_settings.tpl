% include('inc/page_header.tpl')
            <div class="row">
              <div class="col-md-12 col-sm-12 col-xs-12">
                <div class="x_panel">
                  <div class="x_title">
                    <h2 id="deviceid">Weather <small>[..]</small></h2>
                    <ul class="nav navbar-right panel_toolbox">
                      <li><a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                      </li>
                      <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false"><i class="fa fa-wrench"></i></a>
                        <ul class="dropdown-menu" role="menu">
                          <li><a href="#">Settings 1</a>
                          </li>
                          <li><a href="#">Settings 2</a>
                          </li>
                        </ul>
                      </li>
                      <li><a class="close-link"><i class="fa fa-close"></i></a>
                      </li>
                    </ul>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                    <br />
                    <form id="demo-form2" data-parsley-validate class="form-horizontal form-label-left" method="put" action="/api/config/weather">
                      <div class="row">
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12" for="location">Location <span class="required">*</span></label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <input type="text" id="location" name="location" required="required" class="form-control col-md-7 col-xs-12">
                          </div>
                        </div>
                      </div>
                      <div class="row">
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12" for="windspeed">Wind speed <span class="required">*</span></label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <div class="form-group">
                              <select class="form-control" tabindex="-1" name="windspeed">
                                <option></option>
                                <option value="ms">m/s</option>
                                <option value="kmh">km/h</option>
                              </select>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="row">
                        <div class="form-group">
                          <label class="control-label col-md-3 col-sm-3 col-xs-12" for="temperature">Temperature <span class="required">*</span></label>
                          <div class="col-md-6 col-sm-6 col-xs-12">
                            <div class="form-group">
                              <select class="form-control" tabindex="-1" name="temperature">
                                <option></option>
                                <option value="C">C</option>
                                <option value="F">F</option>
                              </select>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="ln_solid"></div>
                      <div class="form-group">
                        <div class="col-md-6 col-sm-6 col-xs-12 col-md-offset-5">
                          <button type="submit" class="btn btn-success">Submit</button>
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
                  //console.log(data);
                  $('input[name="location"]').val(data.location);


                  windspeed_selector.val(data.windspeed);
                  windspeed_selector.trigger('change');
                  temperature_selector.val(data.temperature);
                  temperature_selector.trigger('change');
                });
              });
            </script>
% include('inc/page_footer.tpl')
