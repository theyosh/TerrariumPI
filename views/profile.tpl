% include('inc/page_header.tpl')
            <div class="row">
              <div class="col-md-12 col-sm-12 col-xs-12">
                <div class="x_panel">
                  <div class="x_title">
                    <h2>{{_('Profile')}} <small>{{_('Overview')}}</small></h2>
                    <ul class="nav navbar-right panel_toolbox">
                      <li>
                        <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                      </li>
                      <li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false"><i class="fa fa-wrench"></i></a>
                        <ul class="dropdown-menu" role="menu">
                          <li>
                            <a href="#" onclick="edit_profile()">{{_('Edit')}}</a>
                          </li>
                        </ul>
                      </li>
                      <li><a class="close-link"><i class="fa fa-close"></i></a>
                      </li>
                    </ul>
                    <div class="clearfix"></div>
                  </div>
                  <div class="x_content">
                    <form id="profile" action="/api/config/profile" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
                      <div class="col-md-3 col-sm-3 col-xs-12 profile_left">
                        <div class="profile_img">
                          <div id="crop-avatar">
                            <img class="img-responsive avatar-view" src="{{person_image}}" alt="{{_('Avatar')}}" >
                            <span title="{{_('Click to change image')}}" class="glyphicon glyphicon-import" aria-hidden="true" style="margin: 0.2em;position: absolute;font-size: 2em;" onclick="uploadProfileImage()"> </span>
                          </div>
                        </div>
                        <h3 class="profile_name">{{person_name}}</h3>
                        <ul class="list-unstyled user_data">
                          <li>
                            <i class="fa fa-map-marker user-profile-icon"></i>
                            <span class="profile_location">...</span>
                          </li>
                          <li>
                            <i class="fa fa-briefcase user-profile-icon"></i>
                            <span class="profile_type">...</span>
                          </li>
                          <li class="m-top-xs">
                            <i class="fa fa-external-link user-profile-icon"></i>
                            <span class="profile_moreinfo">...</span>
                          </li>
                        </ul>
                      </div>
                      <div class="col-md-9 col-sm-9 col-xs-12">
                        <div class="profile_title">
                          <div class="col-md-6">
                            <h2>{{_('General information')}}</h2>
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-2 col-sm-2 col-xs-12" for="name">{{_('Name')}} </label>
                          <div class="col-md-8 col-sm-8 col-xs-12">
                            <span class="text">{{person_name}}</span>
                            <input class="form-control" name="name" placeholder="{{_('Name')}}" value="{{person_name}}" type="text" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('profile_name')}}">
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-2 col-sm-2 col-xs-12" for="type">{{_('Type')}} </label>
                          <div class="col-md-8 col-sm-8 col-xs-12">
                            <span class="text"></span>
                            <input class="form-control" name="type" placeholder="{{_('Type')}}" value="" type="text" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('profile_type')}}">
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-2 col-sm-2 col-xs-12" for="gender">{{_('Gender')}} </label>
                          <div class="col-md-8 col-sm-8 col-xs-12">
                            <span class="text"></span>
                            <input class="form-control" name="gender" placeholder="{{_('Gender')}}" value="" type="text" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('profile_gender')}}">
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-2 col-sm-2 col-xs-12" for="age">{{_('Age')}} </label>
                          <div class="col-md-8 col-sm-8 col-xs-12">
                            <span class="text"></span>
                            <div class="col-md-12 xdisplay_inputx form-group has-feedback" style="margin-left: -8px;">
                              <input type="text" class="form-control has-feedback-left" name="age" placeholder="{{_('Age')}}" aria-describedby="inputSuccess2Status2" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('profile_age')}}">
                              <span class="fa fa-calendar-o form-control-feedback left" aria-hidden="true"></span>
                              <span id="inputSuccess2Status2" class="sr-only">(success)</span>
                            </div>
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-2 col-sm-2 col-xs-12" for="species">{{_('Species')}} </label>
                          <div class="col-md-8 col-sm-8 col-xs-12">
                            <span class="text"></span>
                            <input class="form-control" name="species" placeholder="{{_('Species')}}" value="" type="text" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('profile_species')}}">
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-2 col-sm-2 col-xs-12" for="latin">{{_('Latin name')}} </label>
                          <div class="col-md-8 col-sm-8 col-xs-12">
                            <span class="text"></span>
                            <input class="form-control" name="latin" placeholder="{{_('Latin name')}}" value="" type="text" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('profile_latin_name')}}">
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-2 col-sm-2 col-xs-12" for="description">{{_('Description')}} </label>
                          <div class="col-md-10 col-sm-10 col-xs-12">
                            <span class="text pidescription"></span>
                            <div class="btn-toolbar editor" data-role="editor-toolbar" data-target="#editor-one">
                              <div class="btn-group">
                                <a class="btn dropdown-toggle" data-toggle="dropdown" title="Font"><i class="fa fa-font"></i><b class="caret"></b></a>
                                <ul class="dropdown-menu">
                                </ul>
                              </div>
                              <div class="btn-group">
                                <a class="btn dropdown-toggle" data-toggle="dropdown" title="Font Size"><i class="fa fa-text-height"></i>&nbsp;<b class="caret"></b></a>
                                <ul class="dropdown-menu">
                                  <li>
                                    <a data-edit="fontSize 5">
                                      <p style="font-size:17px">Huge</p>
                                    </a>
                                  </li>
                                  <li>
                                    <a data-edit="fontSize 3">
                                      <p style="font-size:14px">Normal</p>
                                    </a>
                                  </li>
                                  <li>
                                    <a data-edit="fontSize 1">
                                      <p style="font-size:11px">Small</p>
                                    </a>
                                  </li>
                                </ul>
                              </div>
                              <div class="btn-group">
                                <a class="btn" data-edit="bold" title="Bold (Ctrl/Cmd+B)"><i class="fa fa-bold"></i></a>
                                <a class="btn" data-edit="italic" title="Italic (Ctrl/Cmd+I)"><i class="fa fa-italic"></i></a>
                                <a class="btn" data-edit="strikethrough" title="Strikethrough"><i class="fa fa-strikethrough"></i></a>
                                <a class="btn" data-edit="underline" title="Underline (Ctrl/Cmd+U)"><i class="fa fa-underline"></i></a>
                              </div>
                              <div class="btn-group">
                                <a class="btn" data-edit="insertunorderedlist" title="Bullet list"><i class="fa fa-list-ul"></i></a>
                                <a class="btn" data-edit="insertorderedlist" title="Number list"><i class="fa fa-list-ol"></i></a>
                                <a class="btn" data-edit="outdent" title="Reduce indent (Shift+Tab)"><i class="fa fa-dedent"></i></a>
                                <a class="btn" data-edit="indent" title="Indent (Tab)"><i class="fa fa-indent"></i></a>
                              </div>
                              <div class="btn-group">
                                <a class="btn" data-edit="justifyleft" title="Align Left (Ctrl/Cmd+L)"><i class="fa fa-align-left"></i></a>
                                <a class="btn" data-edit="justifycenter" title="Center (Ctrl/Cmd+E)"><i class="fa fa-align-center"></i></a>
                                <a class="btn" data-edit="justifyright" title="Align Right (Ctrl/Cmd+R)"><i class="fa fa-align-right"></i></a>
                                <a class="btn" data-edit="justifyfull" title="Justify (Ctrl/Cmd+J)"><i class="fa fa-align-justify"></i></a>
                              </div>
                              <div class="btn-group">
                                <a class="btn dropdown-toggle" data-toggle="dropdown" title="Hyperlink"><i class="fa fa-link"></i></a>
                                <div class="dropdown-menu input-append">
                                  <input class="span2" placeholder="URL" type="text" data-edit="createLink" />
                                  <button class="btn" type="button">Add</button>
                                </div>
                                <a class="btn" data-edit="unlink" title="Remove Hyperlink"><i class="fa fa-cut"></i></a>
                              </div>
                              <div class="btn-group">
                                <a class="btn" title="Insert picture (or just drag & drop)" id="pictureBtn"><i class="fa fa-picture-o"></i></a>
                                <input type="file" data-role="magic-overlay" data-target="#pictureBtn" data-edit="insertImage" />
                              </div>
                              <div class="btn-group">
                                <a class="btn" data-edit="undo" title="Undo (Ctrl/Cmd+Z)"><i class="fa fa-undo"></i></a>
                                <a class="btn" data-edit="redo" title="Redo (Ctrl/Cmd+Y)"><i class="fa fa-repeat"></i></a>
                              </div>
                            </div>
                            <div id="editor-one" class="editor-wrapper"></div>
                            <input type="hidden" name="description">
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="control-label col-md-2 col-sm-2 col-xs-12" for="moreinfo">{{_('More information')}} </label>
                          <div class="col-md-8 col-sm-8 col-xs-12">
                            <span class="text"></span>
                            <input class="form-control" name="moreinfo" placeholder="{{_('More information')}}" value="" type="text" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('profile_more_information')}}">
                          </div>
                        </div>
                        <div class="form-group submit">
                          <div class="col-md-10 col-sm-10 col-xs-12 text-center">
                            <button class="btn btn-success" type="submit">{{_('Submit')}}</button>
                          </div>
                        </div>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>
            <script>
              $(document).ready(function() {
                $('#editor-one').on('change',function(){
                  $('input[name="description"]').val(this.innerHTML);
                });
                $.get($('form').attr('action').replace('/config/','/'),function(data){
                  $.each(Object.keys(data), function(index,key){
                    var field = $('input[name="' + key + '"]');
                    if (field.length == 1) {
                      if (key == 'age') {
                        var date = moment.unix(data[key]);
                        if (date.isValid()) {
                          field.val(date.format('L'));
                          field.parents('.form-group').find('span.text').text(
                            date.format('L') + ', ' + moment.duration(moment.now() - date).humanize()
                          );
                        }
                      } else if (key == 'moreinfo') {
                        field.val(data[key]);
                        field.parents('.form-group').find('span.text').html('<a href="' + data[key] + '" target="_blank" title="More information">' + data[key] + '</a>');
                      } else if (key == 'description') {
                        field.val(data[key]);
                        $('#editor-one').html(data[key]);
                        field.parents('.form-group').find('span.text').html(data[key]);
                      } else {
                        field.val(data[key]);
                        field.parents('.form-group').find('span.text').text(data[key]);
                      }
                    }
                    if (key === 'name') {
                      $('h3.profile_name').text(data[key]);
                    } else if (key === 'type') {
                      $('span.profile_type').text(data[key]);
                    } else if (key === 'moreinfo') {
                      var re = /https?:\/\/([^\/]+)\/.*/g;
                      var moreinfoname = 'More info';
                      if ((matches = re.exec(data[key])) !== null) {
                        moreinfoname = matches[1];
                      }
                      $('span.profile_moreinfo').html('<a href="' + data[key] + '" target="_blank" title="More information">' + moreinfoname + '</a>');
                    } else if (key === 'image') {
                      $('img.avatar-view').attr('src',data[key]);
                    }
                  });
                  // Add fanycbox to images
                  $('span.text.pidescription img').wrap(function(){
                    return $('<a>').attr({'href': $(this).attr('src'), 'data-fancybox':'gallery'})
                  });
                });
                $.get('/api/weather',function(data){
                  $('span.profile_location').text(data.city.city + ', ' + data.city.country);
                });
              });
            </script>
% include('inc/page_footer.tpl')
