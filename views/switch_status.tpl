% include('inc/page_header.tpl')
        <div class="row jumbotron">
          <div class="col-md-12 col-sm-12 col-xs-12">
              <h1>{{_('No switches available')}}</h1>
          </div>
        </div>
        <div class="row switch">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2><span aria-hidden="true" class="glyphicon glyphicon-flash"></span>{{_('Switch')}} <span class="title"></span>
                <span class="badge bg-red manual_mode">{{_('in manual mode')}}</span>
                <span class="small current_usage"></span>
                <span class="small total_usage"></span></h2>
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
                      <li>
                        <a href="javascript:;" >{{_('Last replacement')}}</a>
                      </li>
                    </ul>
                  </li>
                  <li class="dropdown">
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-wrench" title="{{_('Options')}}"></i></a>
                    <ul class="dropdown-menu" role="menu">
                      <li>
                        <a href="javascript:;" onclick="menu_click('switch_settings.html')">{{_('Settings')}}</a>
                      </li>
                      <li>
                        <a href="javascript:;" class="manual_mode">{{_('Manual mode')}}</a>
                      </li>
                      <li>
                        <a href="javascript:;" class="export">{{_('Export data')}}</a>
                      </li>
                      <li>
                        <a href="javascript:;" class="replace_hardware" onclick="replace_hardware(this)" >{{_('Replace hardware')}}</a>
                      </li>
                    </ul>
                  </li>
                  <li>
                    <a class="close-link"><i class="fa fa-close" title="{{_('Close')}}"></i></a>
                  </li>
                </ul>
                <div class="clearfix"></div>
              </div>
              <div class="x_content">
                <div class="col-md-3 col-sm-4 col-xs-12">
                  <div class="power_switch big">
                    <span aria-hidden="true" class="glyphicon glyphicon-off" title="{{_('Toggle power switch')}}"></span>
                  </div>
                </div>
                <div class="col-md-9 col-sm-8 col-xs-12">
                  <div class="history_graph loading"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal fade add-form" tabindex="-1" role="dialog" aria-hidden="true">
          <form action="/api/config/switches/hardware" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
            <div class="modal-dialog modal-lg">
              <div class="modal-content">
                <div class="modal-header">
                  <button type="button" class="close" data-dismiss="modal">
                    <span aria-hidden="true">×</span>
                  </button>
                  <h4 class="modal-title">{{_('Replace hardware')}}</h4>
                </div>
                <div class="modal-body">
                  <div class="row">
                    <div class="col-md-12 col-sm-12 col-xs-12">
                      <div class="x_panel">
                        <div class="x_title">
                          <h2><span aria-hidden="true" class="glyphicon glyphicon-flash"></span> {{_('Switch')}} <span class="title">...</span></h2>
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
                            <div class="col-md-6 col-sm-6 col-xs-6 form-group">
                              <label for="switch_device">{{_('With new device')}}</label>
                              <input class="form-control" name="switch_device" placeholder="{{_('With new device')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_new_device')}}">
                              <input class="form-control" name="switch_id" placeholder="{{_('ID')}}" readonly="readonly" type="hidden">
                            </div>
                            <div class="col-md-6 col-sm-6 col-xs-12 form-group">
                              <label for="switch_reminder" style="padding-left: 0.6em;">{{_('Remind in')}}</label>
                              <div class="form-group">
                                <div class="col-md-4 col-sm-4 col-xs-4">
                                  <input class="form-control" name="switch_reminder_amount" placeholder="{{_('Amount')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" pattern="[0-9]+" data-original-title="{{translations.get_translation('switch_reminder_amount')}}">
                                </div>
                                <div class="col-md-8 col-sm-8 col-xs-8">
                                  <select class="form-control" name="switch_reminder_period" tabindex="-1" placeholder="{{_('Select an option')}}" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('switch_reminder_period')}}">
                                    <option value="">{{_('Select an option')}}</option>
                                    <option value="days">{{_('Days')}}</option>
                                    <option value="weeks">{{_('Weeks')}}</option>
                                    <option value="months">{{_('Months')}}</option>
                                    <option value="years">{{_('Years')}}</option>
                                  </select>
                                </div>
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
                  <button class="btn btn-success" type="submit">{{_('Replace')}}</button>
                </div>
              </div>
            </div>
          </form>
        </div>
        <script type="text/javascript">
          function replace_hardware(obj) {
            var obj = $(obj).parents('.row.switch');
            var id = obj.attr('id').replace('powerswitch_','');
            var name = obj.find('h2 span.title').text();

            var modalWindow = $('.add-form');
            modalWindow.find('input[name="switch_id"]').val(id);
            modalWindow.find('h2 span.title').text(name);
            modalWindow.find('span.required').remove();
            modalWindow.find('.form-group:has([required="required"]) > label').append('<span class="required"> *</span>');
            modalWindow.find('select').select2({
              placeholder: '{{_('Select an option')}}',
              allowClear: false,
              minimumResultsForSearch: Infinity
            });
            modalWindow.modal('show');
          }

          $(document).ready(function() {
            source_row = $('div.row.switch').html();
            $('div.row.switch').remove();

            $.get('/api/switches',function(json_data) {
              $('div.row.jumbotron').toggle(json_data.switches.length == 0);
              $.each(sortByKey(json_data.switches,'name'),function(index,switch_data){
                add_power_switch_status_row(switch_data);
                update_power_switch(switch_data);
                load_history_graph('powerswitch_' + switch_data.id,'switch','/api/history/switches/' + switch_data.id);
              });
              reload_reload_theme();
            });
          });
        </script>
% include('inc/page_footer.tpl')
