% include('inc/page_header.tpl')
        <form action="/api/config/webcams" class="form-horizontal form-label-left" data-parsley-validate="" id="switch_settigs_form" method="put" name="switch_settigs_form">
          % for item in range(0,amount_of_webcams+1):
          <div class="row">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2><span class="title">Webcam</span> <small>new</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                    <li>
                      <a class="close-link"><i class="fa fa-close"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="col-md-8 col-sm-8 col-xs-12 form-group">
                    <label for="webcam_{{item}}_id">ID<span class="required">*</span></label> <input class="form-control" name="webcam_{{item}}_id" placeholder="ID" readonly="readonly" type="text">
                  </div>
                  <div class="col-md-4 col-sm-4 col-xs-12 form-group pull-right">
                    <label for="webcam_{{item}}_location">Preview</label>
                    <div class="webcam_preview"><img id="webcam_{{item}}_preview" src="static/images/webcam_offline.png"></div>
                  </div>
                  <div class="col-md-8 col-sm-8 col-xs-12 form-group">
                    <label for="webcam_{{item}}_name">Name<span class="required">*</span></label> <input class="form-control" name="webcam_{{item}}_name" placeholder="Name" type="text">
                  </div>
                  <div class="col-md-8 col-sm-8 col-xs-12 form-group">
                    <label for="webcam_{{item}}_location">Location<span class="required">*</span></label> <input class="form-control" name="webcam_{{item}}_location" onchange="update_webcam_preview(this.name.split('_')[1],this.value)" placeholder="Location" type="text">
                  </div>
                  <div class="col-md-8 col-sm-8 col-xs-12 form-group">
                    <label for="webcam_{{item}}_rotation">Picture rotation<span class="required">*</span></label>
                    <div class="form-group">
                      <select class="form-control" name="webcam_{{item}}_rotation" tabindex="-1">
                        <option>
                          </option>
                        <option value="0">
                          0
                        </option>
                        <option value="90">
                          90
                        </option>
                        <option value="180">
                          180
                        </option>
                        <option value="270">
                          270
                        </option>
                        <option value="H">
                          Flip Horizontal
                        </option>
                        <option value="V">
                          Flip Vertical
                        </option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          % end
          <div class="row">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="ln_solid"></div>
              <div class="form-group">
                <div class="col-md-11 col-sm-11 col-xs-12 text-center">
                  <button class="btn btn-success" type="submit">Submit</button>
                </div>
              </div>
            </div>
          </div>
        </form>
        <script type="text/javascript">
          $(document).ready(function() {
            var selector = $("select");
            selector.select2({
              placeholder: "Select a number",
              allowClear: false,
              minimumResultsForSearch: Infinity
            });

            selector.on('change',function() {
              var id = this.name.split('_')[1];
              $('img#webcam_' + id + '_preview').removeClass('webcam_90 webcam_180 webcam_270 webcam_H webcam_V').addClass('webcam_' + this.value);
            });

            $.get('/api/config/webcams',function(data) {
              $.each(data.webcams, function(index,webcam) {
                $(Object.keys(webcam)).each(function(index2,key){
                  $('img#webcam_' + index + '_preview').parents('h2').find('small').text(webcam['last_update']);
                  if ('preview' == key) {
                    $('img#webcam_' + index + '_preview').attr('src',webcam[key]);
                  } else {
                    $('input[name="webcam_' + index + '_' + key + '"]').val(webcam[key]);
                    if (key == 'name') {
                      $('input[name="webcam_' + index + '_' + key + '"]').parents('div.x_panel').find('h2 small').text(webcam[key]);
                    }
                  }
                });
                $('select[name="webcam_' + index + '_rotation"]').val(webcam['rotation']);
                $('select[name="webcam_' + index + '_rotation"]').trigger('change');
              });
            });
          });
        </script>
% include('inc/page_footer.tpl')
