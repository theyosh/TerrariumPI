                  <div class="col-xs-9">
                    <!-- Tab panes -->
                    <div class="tab-content">
                      <div class="tab-pane active" id="usage-tab-webcams-list">
                        <div class="interactive_screenshot">
                          <div id="screenshot_webcams_title" class="click_area" title="{{_('Title')}}"></div>
                          <div id="screenshot_webcams_zoom" class="click_area" title="{{_('Zoom')}}"></div>
                          <div id="screenshot_webcams_fullscreen" class="click_area" title="{{_('Full screen')}}"></div>
                          <img src="static/images/documentation/webcam_overview.png" alt="{{_('Webcam overview screenshot')}}" />
                        </div>
                      </div>
                      <div class="tab-pane" id="usage-tab-webcams-title">
                        <h3 class="lead">{{_('Title')}}</h3>
                        <p>{{_('Per webcam the title holds shows some values and options.')}}</p>
                        <div class="x_panel">
                          <div class="x_title">
                            <h2>
                              <span aria-hidden="true" class="glyphicon glyphicon-lock"></span>
                              <span class="title">{{_('Webcam')}} '{{_('Name')}}'</span>
                            </h2>
                            <ul class="nav navbar-right panel_toolbox">
                              <li>
                                <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                              </li>
                              <li class="dropdown">
                                <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-calendar" title="{{_('Period')}}"></i></a>
                                <ul class="dropdown-menu period" role="menu">
                                  <li>
                                    <a href="javascript:;" >{{_('Day')}}</a>
                                  </li>
                                  <li>
                                    <a href="javascript:;" >{{_('Week')}}</a>
                                  </li>
                                  <li>
                                    <a href="javascript:;" >{{_('Month')}}</a>
                                  </li>
                                  <li>
                                    <a href="javascript:;" >{{_('Year')}}</a>
                                  </li>
                                </ul>
                              </li>
                              <li class="dropdown">
                                <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-wrench" title="{{_('Options')}}"></i></a>
                                <ul class="dropdown-menu" role="menu">
                                  <li>
                                    <a href="javascript:;">{{_('Settings')}}</a>
                                  </li>
                                </ul>
                              </li>
                              <li>
                                <a class="close-link" href="javascript:;"><i class="fa fa-close" title="{{_('Close')}}"></i></a>
                              </li>
                            </ul>
                            <div class="clearfix"></div>
                          </div>
                        </div>
                        <h4>{{_('Left side')}} <small>({{_('values')}})</small></h4>
                        <ul>
                          <li>{{_('The configured name')}}</li>
                        </ul>
                        <h4>{{_('Right side')}} <small>({{_('Options')}})</small></h4>
                        <ul>
                          <li><i class="fa fa-chevron-up"></i>: {{_('Show or hide the door')}}</li>
                          <li><i class="fa fa-calendar" title="{{_('Period')}}"></i>: {{_('Select history graph period')}}</li>
                          <li><i class="fa fa-wrench" title="{{_('Options')}}"></i>: {{_('Options menu')}}</li>
                          <li><i class="fa fa-close" title="{{_('Close')}}"></i>: {{_('Close')}}</li>
                        </ul>
                      </div>
                      <div class="tab-pane" id="usage-tab-webcams-zoom">
                        <h3 class="lead">{{_('Zoom')}}</h3>
                        <p>{{_('Use the zooming control to zoom in and out.')}}</p>
                        <h4>{{_('Controls')}}</h4>
                        <ul>
                          <li><img src="static/images/documentation/webcam_zoom_icon.png" style="height: 3em" />: {{_('Zooming control')}}</li>
                          <li><img src="static/images/documentation/webcam_zoom_icon_min.png" style="height: 3em" />: {{_('Zoom at minimum level')}}</li>
                          <li><img src="static/images/documentation/webcam_zoom_icon_max.png" style="height: 3em" />: {{_('Zoom at maximum level')}}</li>
                        </ul>
                      </div>
                      <div class="tab-pane" id="usage-tab-webcams-fullscreen">
                        <h3 class="lead">{{_('Full screen')}}</h3>
                        <p>{{_('Use the full screen control to toggle full screen on or off.')}}</p>
                        <h4>{{_('Controls')}}</h4>
                        <ul>
                          <li><img src="static/images/documentation/webcam_fullscreen_icon.png" style="height: 3em" />: {{_('Full screen control')}}</li>
                        </ul>
                      </div>
                      <div class="tab-pane" id="usage-tab-webcams-settings">
                        <h3 class="lead">{{_('Settings')}}</h3>
                        <p>{{!_('On the webcam settings page you can configure all needed webcams. Click on %s button to add a new webcam. And empty form like below is shown and has to be filled in. Make sure the right values are filled in. All fields with a %s are required.') % ('<button type="button" class="btn btn-primary"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button>','<span class="required">*</span>',)}}</p>
                        <div class="row">
                          <div class="col-md-12 col-sm-12 col-xs-12">
                            <div class="x_panel">
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
                  </div>
                  <div class="col-xs-3">
                    <!-- required for floating -->
                    <!-- Nav tabs -->
                    <ul class="nav nav-tabs tabs-right">
                      <li class="active">
                        <a data-toggle="tab" href="#usage-tab-webcams-list" title="{{_('Overview')}}">{{_('Overview')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-webcams-title" title="{{_('Title')}}">{{_('Title')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-webcams-zoom" title="{{_('Zoom')}}">{{_('Zoom')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-webcams-fullscreen" title="{{_('Full screen')}}">{{_('Full screen')}}</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#usage-tab-webcams-settings" title="{{_('Settings')}}">{{_('Settings')}}</a>
                      </li>
                    </ul>
                  </div>
