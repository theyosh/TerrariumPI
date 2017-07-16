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
            <p>{{_('Here you can configure your doors.')}} {{!_('Required fields are marked with \'%s\'.') % ('<span class="required">*</span>',)}}</p>
            <ul>
              <li>
                <strong>{{_('Hardware')}}</strong>: {{!translations.get_translation('door_field_hardware')}}
              </li>
              <li>
                <strong>{{_('Address')}}</strong>: {{translations.get_translation('door_field_address')}}
              </li>
              <li>
                <strong>{{_('Name')}}</strong>: {{translations.get_translation('door_field_name')}}
              </li>
            </ul>
          </div>
        </div>
        <form action="/api/config/doors" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
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
        <div class="modal fade new-door-form" tabindex="-1" role="dialog" aria-hidden="true">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal">
                  <span aria-hidden="true">×</span>
                </button>
                <h4 class="modal-title" id="myModalLabel">{{_('Add new door sensor')}}</h4>
              </div>
              <div class="modal-body">
                <div class="row door">
                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="x_panel">
                      <div class="x_title" style="display: none">
                        <h2><span class="door_[nr]_icon"></span> {{_('Door sensor')}} <small>{{_('new')}}</small></h2>
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
                        <div class="col-md-4 col-sm-4 col-xs-12 form-group">
                          <label for="door_[nr]_hardwaretype">{{_('Hardware')}} <span class="required">*</span></label>
                          <div class="form-group" data-toggle="tooltip" data-placement="top" title="" data-original-title="{{!translations.get_translation('door_field_hardware')}}">
                            <select class="form-control" name="door_[nr]_hardwaretype" tabindex="-1" placeholder="{{_('Select an option')}}" required="required">
                              <option value="gpio">{{_('GPIO')}}</option>
                            </select>
                          </div>
                        </div>
                        <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                          <label for="door_[nr]_address">{{_('Address')}}</label> <span class="required">*</span>
                          <input class="form-control" name="door_[nr]_address" placeholder="{{_('Address')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('door_field_address')}}">
                          <input class="form-control" name="door_[nr]_id" placeholder="{{_('ID')}}" readonly="readonly" type="hidden">
                        </div>
                        <div class="col-md-5 col-sm-5 col-xs-12 form-group">
                          <label for="door_[nr]_name">{{_('Name')}}</label> <span class="required">*</span>
                          <input class="form-control" name="door_[nr]_name" placeholder="{{_('Name')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('door_field_name')}}">
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">{{_('Close')}}</button>
                <button type="button" class="btn btn-primary" onclick="add_door()" >{{_('Add')}}</button>
              </div>
            </div>
          </div>
        </div>
        <script type="text/javascript">
          $(document).ready(function() {
            $('.page-title').append('<div class="title_right"><h3><button type="button" class="btn btn-primary alignright" data-toggle="modal" data-target=".new-door-form"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button></h3> </div>');
            $("select").select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            });
            $.get($('form').attr('action'),function(data){
              $.each(data.doors, function(index,door) {
                // Clone empty sensor row....
                add_door_row(door.id,
                             door.hardwaretype,
                             door.address,
                             door.name);
              });
              reload_reload_theme();
            });
          });
        </script>
% include('inc/page_footer.tpl')
