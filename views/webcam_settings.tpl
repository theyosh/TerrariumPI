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
            <p>{{_('Here you can setup the webcams that are used. Per webcam fill in the following fields:')}}</p>
            <ul>
              <li>
                <strong>{{_('ID')}}</strong>: {{translations.get_translation('webcam_field_id')}}
              </li>
              <li>
                <strong>{{_('Name')}}</strong>: {{translations.get_translation('webcam_field_name')}}
              </li>
              <li>
                <strong>{{_('Location')}}</strong>: {{ translations.get_translation('webcam_field_location') % ('rpicam','/dev/video0','https://source.mywebcam.com/stream')}}
              </li>
              <li>
                <strong>{{_('Picture rotation')}}</strong>: {{translations.get_translation('webcam_field_rotation')}}
              </li>
            </ul>
          </div>
        </div>
        <form action="/api/config/webcams" class="form-horizontal form-label-left" data-parsley-validate="" id="webcam_settings_form" method="put" name="webcam_settings_form">
          % for item in range(0,amount_of_webcams+1):
          <div class="row">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2><span class="title">{{_('Webcam')}}</span> <small>new</small></h2>
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
                  <div class="col-md-8 col-sm-8 col-xs-12 form-group">
                    <label for="webcam_{{item}}_id">{{_('ID')}} <span class="required">*</span></label>
                    <input class="form-control" name="webcam_{{item}}_id" placeholder="{{_('ID')}}" readonly="readonly" type="text">
                  </div>
                  <div class="col-md-4 col-sm-4 col-xs-12 form-group pull-right">
                    <label for="webcam_{{item}}_location">{{_('Preview')}}</label>
                    <div class="webcam_preview"><img id="webcam_{{item}}_preview" src="static/images/webcam_offline.png"></div>
                  </div>
                  <div class="col-md-8 col-sm-8 col-xs-12 form-group">
                    <label for="webcam_{{item}}_name">{{_('Name')}} <span class="required">*</span></label>
                    <input class="form-control" name="webcam_{{item}}_name" placeholder="{{_('Name')}}" type="text">
                  </div>
                  <div class="col-md-8 col-sm-8 col-xs-12 form-group">
                    <label for="webcam_{{item}}_location">{{_('Location')}} <span class="required">*</span></label>
                    <input class="form-control" name="webcam_{{item}}_location" onchange="update_webcam_preview(this.name.split('_')[1],this.value)" placeholder="{{_('Location')}}" type="text">
                  </div>
                  <div class="col-md-8 col-sm-8 col-xs-12 form-group">
                    <label for="webcam_{{item}}_rotation">{{_('Picture rotation')}} <span class="required">*</span></label>
                    <div class="form-group">
                      <select class="form-control" name="webcam_{{item}}_rotation" tabindex="-1" placeholder="{{_('Select an option')}}">
                        <option value="0">0 {{_('degrees')}}</option>
                        <option value="90">90 {{_('degrees')}}</option>
                        <option value="180">180 {{_('degrees')}}</option>
                        <option value="270">270 {{_('degrees')}}</option>
                        <option value="H">{{_('Flip Horizontal')}}</option>
                        <option value="V">{{_('Flip Vertical')}}</option>
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
                  <button class="btn btn-success" type="submit">{{_('Submit')}}</button>
                </div>
              </div>
            </div>
          </div>
        </form>
        <script type="text/javascript">
          $(document).ready(function() {
            var selector = $("select");
            selector.select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            });
            selector.on('change',function() {
              var id = this.name.split('_')[1];
              $('img#webcam_' + id + '_preview').removeClass('webcam_90 webcam_180 webcam_270 webcam_H webcam_V').addClass('webcam_' + this.value);
            });

            $.get($('form').attr('action'),function(data) {
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
