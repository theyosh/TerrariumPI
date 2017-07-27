                  <div class="col-xs-9">
                    <!-- Tab panes -->
                    <div class="tab-content">
                      <div class="tab-pane active" id="usage-tab-system-settings">
                        <div class="x_panel">
                          <div class="x_content">
                            <div class="row">
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="active_language">{{_('Language')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_language')}}">
                                    <select class="form-control" required="required" name="active_language" tabindex="-1" placeholder="{{_('Select an option')}}">
                                    </select>
                                  </div>
                                </div>
                              </div>
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="admin">{{_('Admin name')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control" name="admin" required="required" type="text" placeholder="{{_('Admin name')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_admin')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="new_password">{{_('New admin password')}} </label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control" name="new_password" type="password" placeholder="{{_('New admin password')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_new_password')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="cur_password">{{_('Current admin password')}} </label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control" name="cur_password" type="password" placeholder="{{_('Current admin password')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_current_password')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="power_usage">{{_('Pi power usage in W')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control" name="power_usage" required="required" type="text" placeholder="{{_('Pi power usage in W')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_pi_power')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="power_price">{{_('Power price')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control" name="power_price" required="required" type="text" placeholder="{{_('Power price')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_power_price')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="water_price">{{_('Water price')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control" name="water_price" required="required" type="text" placeholder="{{_('Water price')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_water_price')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="host">{{_('IP or hostname')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control" name="host" required="required" type="text" placeholder="{{_('IP or hostname')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_hostname')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="port">{{_('Port number')}} <span class="required">*</span></label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control" name="port" required="required" type="text" placeholder="{{_('Port number')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_port_number')}}">
                                </div>
                              </div><br /><br />
                              <div class="form-group">
                                <label class="control-label col-md-3 col-sm-3 col-xs-12" for="owfs_port">{{_('OWFS server port')}} </label>
                                <div class="col-md-7 col-sm-6 col-xs-10">
                                  <input class="form-control" name="owfs_port" type="text" placeholder="{{_('OWFS server port')}}" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('system_field_owfs_port')}}">
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <ul>
                        <li>
                          <strong>{{_('Language')}}</strong>: {{!translations.get_translation('system_field_language')}}
                        </li>
                        <li>
                          <strong>{{_('Admin name')}}</strong>: {{!translations.get_translation('system_field_admin')}}
                        </li>
                        <li>
                          <strong>{{_('New admin password')}}</strong>: {{translations.get_translation('system_field_new_password')}}
                        </li>
                        <li>
                          <strong>{{_('Current admin password')}}</strong>: {{!translations.get_translation('system_field_current_password')}}
                        </li>
                        <li>
                          <strong>{{_('Pi power usage in W')}}</strong>: {{!translations.get_translation('system_field_pi_power')}}
                        </li>
                        <li>
                          <strong>{{_('Power price')}}</strong>: {{translations.get_translation('system_field_power_price')}}
                        </li>
                        <li>
                          <strong>{{_('Water price')}}</strong>: {{!translations.get_translation('system_field_water_price')}}
                        </li>
                        <li>
                          <strong>{{_('IP or hostname')}}</strong>: {{!translations.get_translation('system_field_hostname')}}
                        </li>
                        <li>
                          <strong>{{_('Port number')}}</strong>: {{translations.get_translation('system_field_port_number')}}
                        </li>
                        <li>
                          <strong>{{_('OWFS server port')}}</strong>: {{!translations.get_translation('system_field_owfs_port')}}
                        </li>
                      </ul>
                    </div>
                  </div>
                  <div class="col-xs-3">

                  </div>
