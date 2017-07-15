% include('inc/page_header.tpl')
        <div class="x_panel">
          <div class="x_title">
            <h2><span class="glyphicon glyphicon-info-sign" aria-hidden="true" title="{{_('Information')}}"></span> {{_('Help')}}<small></small></h2>
            <ul class="nav navbar-right panel_toolbox">
              <li>
                <a class="collapse-link"><i class="fa fa-chevron-down"></i></a>
              </li>
              <li>
                <a class="close-link"><i class="fa fa-close" title="{{_('Close')}}"></i></a>
              </li>
            </ul>
            <div class="clearfix"></div>
          </div>
          <div class="x_content" style="display:none">
            <p>{{_('Here you can configure your webcams.')}}</p>
            <ul>
              <li>
                <strong>{{_('Location')}}</strong>: {{!translations.get_translation('webcam_field_location')}}
                <ul>
                  <li><strong>{{_('RPICam')}}:</strong> rpicam</li>
                  <li><strong>{{_('V4L')}}:</strong> /dev/videoX</li>
                  <li><strong>{{_('Remote source')}}:</strong> http://source.web.cam/stream</li>
                </ul>
              </li>
              <li>
                <strong>{{_('Name')}}</strong>: {{translations.get_translation('webcam_field_name')}}
              </li>
              <li>
                <strong>{{_('Picture rotation')}}</strong>: {{translations.get_translation('webcam_field_rotation')}}
              </li>
              <li>
                <strong>{{_('Preview')}}</strong>: {{translations.get_translation('webcam_field_preview')}}
              </li>
            </ul>
          </div>
        </div>
        <form action="/api/config/webcams" class="form-horizontal form-label-left" data-parsley-validate="" id="webcam_settings_form" method="put" name="webcam_settings_form">
          <div class="row submit">
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
        <div class="modal fade new-webcam-form" tabindex="-1" role="dialog" aria-hidden="true">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">
                  <span aria-hidden="true">×</span>
                </button>
                <h4 class="modal-title" id="myModalLabel">{{_('Add new webcam')}}</h4>
              </div>
              <div class="modal-body">
                <div class="row webcam">
                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="x_panel">
                      <div class="x_title" style="display: none">
                        <h2><span class="webcam_[nr]_icon"></span> {{_('Webcam')}} <small>{{_('new')}}</small></h2>
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
                        <div class="col-md-4 col-sm-4 col-xs-12 form-group pull-right">
                          <label for="webcam_[nr]_location">{{_('Preview')}}</label>
                          <div class="webcam_preview"><img id="webcam_[nr]_preview" src="static/images/webcam_offline.png"></div>
                        </div>
                        <div class="col-md-8 col-sm-8 col-xs-12 form-group">
                          <label for="webcam_[nr]_location">{{_('Location')}} <span class="required">*</span></label>
                          <input class="form-control" name="webcam_[nr]_location" placeholder="{{_('Location')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('webcam_field_location')}}">
                          <input class="form-control" name="webcam_[nr]_id" placeholder="{{_('ID')}}" readonly="readonly" type="hidden">
                        </div>
                        <div class="col-md-8 col-sm-8 col-xs-12 form-group">
                          <label for="webcam_[nr]_name">{{_('Name')}}</label>
                          <input class="form-control" name="webcam_[nr]_name" placeholder="{{_('Name')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('webcam_field_name')}}">
                        </div>
                        <div class="col-md-8 col-sm-8 col-xs-12 form-group">
                          <label for="webcam_[nr]_rotation">{{_('Picture rotation')}}</label>
                          <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{translations.get_translation('webcam_field_rotation')}}">
                            <select class="form-control" name="webcam_[nr]_rotation" tabindex="-1" placeholder="{{_('Select an option')}}">
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
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">{{_('Close')}}</button>
                <button type="button" class="btn btn-primary" onclick="add_webcam()" >{{_('Add')}}</button>
              </div>
            </div>
          </div>
        </div>
        <script type="text/javascript">
          $(document).ready(function() {
            $('.page-title').append('<div class="title_right"><h3><button type="button" class="btn btn-primary alignright" data-toggle="modal" data-target=".new-webcam-form"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button></h3> </div>');
            $("select").select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            });
            $.get($('form').attr('action'),function(data){
              $.each(data.webcams, function(index,webcam) {
                // Clone empty webcam row....
                add_webcam_row(webcam.id,
                               webcam.location,
                               webcam.name,
                               webcam.rotation,
                               webcam.preview);
              });
              reload_reload_theme();
            });
          });
        </script>
% include('inc/page_footer.tpl')
