% include('inc/page_header.tpl')
        <div class="x_panel help">
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
          <div class="x_content">
            <p>{{_('Here you can configure your webcams.')}} {{!_('Required fields are marked with \'%s\'.') % ('<span class="required">*</span>',)}}</p>
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
                <strong>{{_('Resolution')}}</strong>: {{translations.get_translation('webcam_field_resolution')}}
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
        <div class="modal fade add-form" tabindex="-1" role="dialog" aria-hidden="true">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">
                  <span aria-hidden="true">×</span>
                </button>
                <h4 class="modal-title">{{_('Add new webcam')}}</h4>
              </div>
              <div class="modal-body">
                <div class="row webcam">
                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="x_panel">
                      <div class="x_title">
                        <h2><span aria-hidden="true" class="glyphicon glyphicon-facetime-video"></span> {{_('Webcam')}} <span class="title">{{_('new')}}</span></h2>
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
                          <label for="webcam_[nr]_location">{{_('Location')}}</label>
                          <input class="form-control" name="webcam_[nr]_location" placeholder="{{_('Location')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('webcam_field_location')}}">
                          <input class="form-control" name="webcam_[nr]_id" placeholder="{{_('ID')}}" readonly="readonly" type="hidden">
                        </div>
                        <div class="col-md-8 col-sm-8 col-xs-12 form-group">
                          <label for="webcam_[nr]_name">{{_('Name')}}</label>
                          <input class="form-control" name="webcam_[nr]_name" placeholder="{{_('Name')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('webcam_field_name')}}">
                        </div>
                        <div class="col-md-4 col-sm-4 col-xs-12 form-group">
                          <label for="webcam_[nr]_resolution">{{_('Resolution')}}</label>
                          <div class="form-group">
                            <div class="col-md-6 col-sm-6 col-xs-12" style="padding-left: 0px;padding-right: 0px">
                              <input class="form-control" name="webcam_[nr]_resolution_width" placeholder="{{_('Width')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" pattern="[0-9]+" data-original-title="{{translations.get_translation('webcam_field_resolution_width')}}">
                            </div>
                            <div class="col-md-6 col-sm-6 col-xs-12" style="padding-left: 0px;padding-right: 0px">
                              <input class="form-control" name="webcam_[nr]_resolution_height" placeholder="{{_('Height')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" pattern="[0-9]+"  data-original-title="{{translations.get_translation('webcam_field_resolution_height')}}">
                            </div>
                          </div>
                        </div>
                        <div class="col-md-4 col-sm-4 col-xs-12 form-group">
                          <label for="webcam_[nr]_rotation">{{_('Picture rotation')}}</label>
                          <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{translations.get_translation('webcam_field_rotation')}}">
                            <select class="form-control" name="webcam_[nr]_rotation" tabindex="-1" placeholder="{{_('Select an option')}}">
                              <option value="">{{_('Select an option')}}</option>
                              <option value="0">0 {{_('degrees')}}</option>
                              <option value="90">90 {{_('degrees')}}</option>
                              <option value="180">180 {{_('degrees')}}</option>
                              <option value="270">270 {{_('degrees')}}</option>
                              <option value="H">{{_('Flip Horizontal')}}</option>
                              <option value="V">{{_('Flip Vertical')}}</option>
                            </select>
                          </div>
                        </div>
                        <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                          <label for="webcam_[nr]_archive">{{_('Archive')}}</label>
                          <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{translations.get_translation('webcam_field_archive')}}">
                            <select class="form-control" name="webcam_[nr]_archive" tabindex="-1" placeholder="{{_('Select an option')}}">
                              <option value="">{{_('Select an option')}}</option>
                              <option value="disabled">{{_('Disabled')}}</option>
                              <option value="motion">{{_('Motion')}}</option>
                              <option value="60">{{_('1 minute')}}</option>
                              <option value="300">{{_('5 minutes')}}</option>
                              <option value="900">{{_('15 minutes')}}</option>
                              <option value="1800">{{_('30 minutes')}}</option>
                              <option value="3600">{{_('1 hour')}}</option>
                              <option value="10800">{{_('3 hours')}}</option>
                              <option value="21600">{{_('6 hours')}}</option>
                              <option value="43200">{{_('12 hours')}}</option>
                              <option value="86400">{{_('1 day')}}</option>
                            </select>
                          </div>
                        </div>
                        <div class="col-md-3 col-sm-3 col-xs-6 form-group">
                          <label for="webcam_[nr]_archivelight">{{_('Archive light state')}}</label>
                          <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{translations.get_translation('webcam_field_archive_light')}}">
                            <select class="form-control" name="webcam_[nr]_archivelight" tabindex="-1" placeholder="{{_('Select an option')}}">
                              <option value="">{{_('Select an option')}}</option>
                              <option value="ignore">{{_('Ignore')}}</option>
                              <option value="on">{{_('When on')}}</option>
                              <option value="off">{{_('When off')}}</option>
                            </select>
                          </div>
                        </div>
                        <div class="col-md-3 col-sm-3 col-xs-6 form-group">
                          <label for="webcam_[nr]_archivedoor">{{_('Archive door state')}}</label>
                          <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{translations.get_translation('webcam_field_archive_door')}}">
                            <select class="form-control" name="webcam_[nr]_archivedoor" tabindex="-1" placeholder="{{_('Select an option')}}">
                              <option value="">{{_('Select an option')}}</option>
                              <option value="ignore">{{_('Ignore')}}</option>
                              <option value="open">{{_('When open')}}</option>
                              <option value="closed">{{_('When closed')}}</option>
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
                <button type="button" class="btn btn-primary">{{_('Add')}}</button>
              </div>
            </div>
          </div>
        </div>
        <script type="text/javascript">
          $(document).ready(function() {
            // Create add button
            init_form_settings('webcam');

            $('select').select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            });

            $.get($('form').attr('action'),function(json_data){
              $.each(sortByKey(json_data.webcams,'name'), function(index,webcam_data) {
                add_webcam_setting_row(webcam_data);
                update_webcam(webcam_data);
              });
              reload_reload_theme();
            });
          });
        </script>
% include('inc/page_footer.tpl')
