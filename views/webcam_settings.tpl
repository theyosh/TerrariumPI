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
                  <li><strong>{{_('RPICam')}}:</strong> rpicam_live</li>
                  <li><strong>{{_('V4L')}}:</strong> /dev/videoX</li>
                  <li><strong>{{_('Remote source')}}:</strong> http://source.web.cam/stream.jpg</li>
                  <li><strong>{{_('Local source')}}:</strong> local://image.jpg</li>
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
                          <div class="webcam_preview webcam_player_preview"><img id="webcam_[nr]_preview" src="static/images/webcam_offline.png"></div>
                        </div>
                        <div class="col-md-8 col-sm-8 col-xs-12 form-group">
                          <label for="webcam_[nr]_location">{{_('Location')}}</label>
                          <input class="form-control" name="webcam_[nr]_location" placeholder="{{_('Location')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('webcam_field_location')}}">
                          <input class="form-control" name="webcam_[nr]_id" placeholder="{{_('ID')}}" readonly="readonly" type="hidden">
                          <input class="form-control" name="webcam_[nr]_realtimedata" placeholder="{{_('realtimedata')}}" readonly="readonly" type="hidden">
                        </div>
                        <div class="col-md-8 col-sm-8 col-xs-12 form-group">
                          <label for="webcam_[nr]_name">{{_('Name')}}</label>
                          <input class="form-control" name="webcam_[nr]_name" placeholder="{{_('Name')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('webcam_field_name')}}">
                        </div>
                        <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                          <label for="webcam_[nr]_resolution">{{_('Resolution')}}</label>
                          <div class="form-group">
                            <input class="form-control" name="webcam_[nr]_resolution_width" placeholder="{{_('Width')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" pattern="[0-9]+" data-original-title="{{translations.get_translation('webcam_field_resolution_width')}}">
                          </div>
                        </div>
                        <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                          <label for="webcam_[nr]_resolution" style="visibility:hidden"></label>
                          <div class="form-group">
                            <input class="form-control" name="webcam_[nr]_resolution_height" placeholder="{{_('Height')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" pattern="[0-9]+"  data-original-title="{{translations.get_translation('webcam_field_resolution_height')}}">
                          </div>
                        </div>
                        <div class="col-md-2 col-sm-2 col-xs-6 form-group rotation">
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
                        <div class="col-md-2 col-sm-2 col-xs-6 form-group awb">
                          <label for="webcam_[nr]_awb">{{_('White balance')}}</label>
                          <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{translations.get_translation('webcam_field_awb')}}">
                            <select class="form-control" name="webcam_[nr]_awb" tabindex="-1" placeholder="{{_('Select an option')}}">
                              <option value="">{{_('Select an option')}}</option>
                              <option value="off">{{_('off')}}</option>
                              <option value="auto">{{_('auto')}}</option>
                              <option value="sunlight">{{_('sunlight')}}</option>
                              <option value="cloudy">{{_('cloudy')}}</option>
                              <option value="shade">{{_('shade')}}</option>
                              <option value="tungsten">{{_('tungsten')}}</option>
                              <option value="fluorescent">{{_('fluorescent')}}</option>
                              <option value="incandescent">{{_('incandescent')}}</option>
                              <option value="flash">{{_('flash')}}</option>
                              <option value="horizon">{{_('horizon')}}</option>
                              <option value="greyworld">{{_('greyworld')}}</option>
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
                        <div class="motion_option" style="display:none;">
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="webcam_[nr]_motionboxes">{{_('Show motion boxes')}}</label>
                            <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{translations.get_translation('webcam_field_motion_boxes')}}">
                              <select class="form-control" name="webcam_[nr]_motionboxes" tabindex="-1" placeholder="{{_('Select an option')}}">
                                <option value="">{{_('Select an option')}}</option>
                                <option value="true">{{_('Enabled')}}</option>
                                <option value="false">{{_('Disabled')}}</option>
                              </select>
                            </div>
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="webcam_[nr]_motiondeltathreshold">{{_('Motion delta threshold')}}</label>
                            <div class="form-group">
                              <input class="form-control" name="webcam_[nr]_motiondeltathreshold" placeholder="{{_('Threshold')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" pattern="[0-9]+" data-original-title="{{translations.get_translation('webcam_field_motion_delta_threshold')}}">
                            </div>
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="webcam_[nr]_motionminarea">{{_('Motion minimum area')}}</label>
                            <div class="form-group">
                              <input class="form-control" name="webcam_[nr]_motionminarea" placeholder="{{_('Minimum area')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" pattern="[0-9]+" data-original-title="{{translations.get_translation('webcam_field_motion_min_area')}}">
                            </div>
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-6 form-group">
                            <label for="webcam_[nr]_motioncompareframe">{{_('Motion comparison frame')}}</label>
                            <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{translations.get_translation('webcam_field_motion_compare_frame')}}">
                              <select class="form-control" name="webcam_[nr]_motioncompareframe" tabindex="-1" placeholder="{{_('Select an option')}}">
                                <option value="">{{_('Select an option')}}</option>
                                <option value="last">{{_('Last frame')}}</option>
                                <option value="archived">{{_('Last archived frame')}}</option>
                              </select>
                            </div>
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
        <div class="modal fade realtime-data-form" tabindex="-1" role="dialog" aria-hidden="true">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">
                  <span aria-hidden="true">×</span>
                </button>
                <h4 class="modal-title">{{_('Select sensors')}}</h4>
              </div>
              <div class="modal-body">
                <div class="row">
                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="x_panel">
                      <div class="x_title">
                        <h2><span aria-hidden="true" class="glyphicon glyphicon-facetime-video"></span> {{_('Sensors')}}</h2>
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
                        <div class="col-md-12 col-sm-12 col-xs-12 form-group">
                          <div data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('webcam_realtime_sensors_list')}}">
                            <select class="form-control" multiple="multiple" name="webcam_realtime_sensors_list" tabindex="-1" placeholder="{{_('Select an option')}}">
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
                <button type="button" class="btn btn-primary" data-dismiss="modal" id="add_sensors">{{_('Save')}}</button>
                <button type="button" class="btn btn-warning" data-dismiss="modal" id="del_marker">{{_('DELETE')}}</button>
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
            }).on('change',function() {
              if (this.name.endsWith('_archive')) {
                $(this).parents('.x_content').find('.motion_option').toggle(('motion' === this.value));
              }
            }).on("select2:select", function (evt) {
                var element = evt.params.data.element;
                var $element = $(element);

                $element.detach();
                $(this).append($element);
                $(this).trigger("change");
              });

            $.get($('form').attr('action'),function(json_data){
              $.each(sortByKey(json_data.webcams,'name'), function(index,webcam_data) {
                add_webcam_setting_row(webcam_data);
                update_webcam(webcam_data);
                webcam_data.edit = true;
                initWebcam(webcam_data);
              });
              reload_reload_theme();
            });

            $.get('/api/sensors',function(data) {
              let pull_down = $('select[name="webcam_realtime_sensors_list"]');
              $.each(data.sensors,function (index,sensor){
                pull_down.append($('<option>').attr({'value':sensor.id}).text(sensor.type + ' ' + sensor.name + ' ' + (Math.round((sensor.current + Number.EPSILON) * 1000) / 1000) + ' ' + sensor.indicator));
              });
              pull_down.trigger('change');
            });
          });
        </script>
% include('inc/page_footer.tpl')
