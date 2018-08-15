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
            <p>{{_('Here you can configure your audio playlists.')}} {{_('Make sure you do not overlap playlists in time!')}} {{!_('When you have a %s type switch added the audio player will not work. More information can be found here: %s.') % ('<strong>pwm-dimmer</strong>','<a href="http://www.raspberry-projects.com/pi/programming-in-c/pwm/using-the-pwm-pin" target="_blank">http://www.raspberry-projects.com/pi/programming-in-c/pwm/using-the-pwm-pin</a>')}} {{!_('Required fields are marked with \'%s\'.') % ('<span class="required">*</span>',)}}</p>
            <ul>
              <li>
                <strong>{{_('Name')}}</strong>: {{!translations.get_translation('audio_playlist_field_name')}}
              </li>
              <li>
                <strong>{{_('Start')}}</strong>: {{translations.get_translation('audio_playlist_field_start')}}
              </li>
              <li>
                <strong>{{_('Stop')}}</strong>: {{translations.get_translation('audio_playlist_field_stop')}}
              </li>
              <li>
                <strong>{{_('Volume')}}</strong>: {{translations.get_translation('audio_playlist_field_volume')}}
              </li>
              <li>
                <strong>{{_('Repeat')}}</strong>: {{translations.get_translation('audio_playlist_field_repeat')}}
              </li>
              <li>
                <strong>{{_('Shuffle')}}</strong>: {{translations.get_translation('audio_playlist_field_shuffle')}}
              </li>
              <li>
                <strong>{{_('Files')}}</strong>: {{translations.get_translation('audio_playlist_field_files')}}
              </li>
            </ul>
          </div>
        </div>
        <form action="/api/config/audio" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
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
                <h4 class="modal-title">{{_('Add new audio playlist')}}</h4>
              </div>
              <div class="modal-body">
                <div class="row playlist">
                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="x_panel">
                      <div class="x_title">
                        <h2><span aria-hidden="true" class="glyphicon glyphicon-music"></span> {{_('Audio playlist')}} <span class="title">{{_('new')}}</span> <small>...</small></h2>
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
                        <div class="row">
                          <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                            <label for="playlist_[nr]_name">{{_('Name')}}</label>
                            <input class="form-control" name="playlist_[nr]_name" placeholder="{{_('Name')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('audio_playlist_field_name')}}">
                            <input class="form-control" name="playlist_[nr]_id" placeholder="{{_('ID')}}" readonly="readonly" type="hidden">
                          </div>
                          <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                            <label for="playlist_[nr]_start">{{_('Start')}}</label>
                            <input class="form-control" name="playlist_[nr]_start" placeholder="{{_('Start')}}" required="required" type="text" pattern="[0-9:]+" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('audio_playlist_field_start')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                            <label for="playlist_[nr]_stop">{{_('Stop')}}</label>
                            <input class="form-control" name="playlist_[nr]_stop" placeholder="{{_('Stop')}}" required="required" type="text" pattern="[0-9:]+"  data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('audio_playlist_field_stop')}}">
                          </div>
                          <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                            <label for="playlist_[nr]_volume">{{_('Volume')}}</label>
                            <input class="form-control" name="playlist_[nr]_volume" placeholder="{{_('Volume')}}" required="required" type="text" pattern="[0-9]+"  data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('audio_playlist_field_volume')}}" />
                          </div>
                          <div class="col-md-1 col-sm-1 col-xs-12 form-group" style="text-align: center">
                            <label for="playlist_[nr]_repeat" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('audio_playlist_field_repeat')}}">{{_('Repeat')}}</label><br />
                            <input type="checkbox" name="playlist_[nr]_repeat" class="js-switch" value="0" />
                          </div>
                          <div class="col-md-1 col-sm-1 col-xs-12 form-group" style="text-align: center">
                            <label for="playlist_[nr]_shuffle" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('audio_playlist_field_shuffle')}}">{{_('Shuffle')}}</label><br />
                            <input type="checkbox" name="playlist_[nr]_shuffle" class="js-switch" value="0" />
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-md-12 col-sm-12 col-xs-12 form-group">
                            <label for="playlist_[nr]_files">{{_('Files')}}</label>
                            <div class="form-group" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('audio_playlist_field_files')}}">
                              <select class="form-control" multiple="multiple" name="playlist_[nr]_files" tabindex="-1" placeholder="{{_('Select an option')}}">
                                <option value="">{{_('Select an option')}}</option>
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
        <script type="text/javascript">
          $(document).ready(function() {
            init_form_settings('playlist');

            $.get('/api/audio/files',function(data){
              var select_boxes = $('select[name="playlist_[nr]_files"]');
              $.each(data.audiofiles,function (index,audiofile){
                select_boxes.append($('<option>').attr({'value':audiofile.id}).text(audiofile.name));
              });

              source_row = $('.modal-body div.row.playlist').html();

              $('select[name="playlist_[nr]_files"]').select2({
                placeholder: '{{_('Select an option')}}',
                allowClear: false,
                minimumResultsForSearch: Infinity
              });

              $('.add-form .js-switch').each(function(index,html_element){
                var switchery = new Switchery(html_element);
                html_element.onchange = function() {
                  this.value = this.checked;
                };
              });

              $.get($('form').attr('action'),function(json_data){
                $.each(sortByKey(json_data.playlists,'name'), function(index,playlist_data) {
                  add_audio_playlist_setting_row(playlist_data);
                  update_audio_playlist(playlist_data);
                });
                reload_reload_theme();
              });
            });
          });
        </script>
% include('inc/page_footer.tpl')
