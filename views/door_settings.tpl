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
                <strong>{{_('ID')}}</strong>: {{translations.get_translation('door_field_id')}}
              </li>
              <li>
                <strong>{{_('Name')}}</strong>: {{translations.get_translation('door_field_name')}}
              </li>
              <li>
                <strong>{{_('GPIO Pin')}}</strong>: {{translations.get_translation('door_field_gpio_pin')}}
              </li>
            </ul>
          </div>
        </div>
        <form action="/api/config/doors" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
          % for item in range(0,amount_of_doors+1):
          <div class="row">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2><span class="title">{{_('Door')}}</span> <small>new</small></h2>
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
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="door_{{item}}_id">{{_('ID')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="door_{{item}}_id" placeholder="{{_('ID')}}" readonly="readonly" type="text" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('door_field_id')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="door_{{item}}_name">{{_('Name')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="door_{{item}}_name" placeholder="{{_('Name')}}" type="text" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('door_field_name')}}">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-md-3 col-sm-3 col-xs-12" for="door_{{item}}_gpiopin">{{_('GPIO Pin')}} <span class="required">*</span></label>
                    <div class="col-md-7 col-sm-6 col-xs-10">
                      <input class="form-control" name="door_{{item}}_gpiopin" placeholder="{{_('GPIO Pin')}}" type="text" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('door_field_gpio_pin')}}">
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
            $.get($('form').attr('action'),function(data) {
              $.each(data.doors, function(index,door) {
                $(Object.keys(door)).each(function(index2,key){
                  $('input[name="door_' + index + '_' + key + '"]').val(door[key]);
                });
                $('input[name="door_' + index + '_name"]').parents('div.x_panel').find('h2 small').text(door.name);
              });
            });
          });
        </script>
% include('inc/page_footer.tpl')
