% include('inc/page_header.tpl')
        <div class="row calendar">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2><span aria-hidden="true" class="glyphicon glyphicon-calendar"></span> {{_('Calendar')}}</h2>
                <ul class="nav navbar-right panel_toolbox">
                  <li>
                    <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                  </li>
                  <li class="dropdown">
                    <a aria-expanded="false" class="dropdown-toggle" data-toggle="dropdown" href="javascript:;" role="button"><i class="fa fa-wrench" title="{{_('Options')}}"></i></a>
                    <ul class="dropdown-menu" role="menu">
                      <li>
                        <a href="/api/calendar/ical" target="_blank">{{_('iCal')}}</a>
                      </li>
                      <li>
                        <a href="javascript:;" onclick="menu_click('system_settings.html')">{{_('Settings')}}</a>
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
                <div class="row jumbotron">
                  <div class="col-md-12 col-sm-12 col-xs-12">
                    <h1>{{_('No calendar available')}}</h1>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal fade add-form" tabindex="-1" role="dialog" aria-hidden="true">
          <form id="new_item_form" action="/api/calendar" class="form-horizontal form-label-left" data-parsley-validate="" method="post">
            <div class="modal-dialog modal-lg">
              <div class="modal-content">
                <div class="modal-header">
                  <button type="button" class="close" data-dismiss="modal">
                    <span aria-hidden="true">×</span>
                  </button>
                  <h4 class="modal-title">{{_('New calendar item')}}</h4>
                </div>
                <div class="modal-body">
                  <div class="row">
                    <div class="col-md-10 col-sm-10 col-xs-12">
                      <div class="row">
                        <div class="col-md-12 col-sm-12 col-xs-12 form-group">
                          <input class="form-control" name="calendar_id" placeholder="{{_('ID')}}" readonly="readonly" type="hidden">
                          <label for="calendar_title">{{_('Title')}}</label>
                          <input class="form-control" name="calendar_title" placeholder="{{_('Calendar title')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('calendar_title')}}">
                        </div>
                      </div>
                      <div class="row">
                        <div class="col-md-12 col-sm-12 col-xs-12 form-group">
                          <label for="calendar_description">{{_('Description')}}</label>
                          <textarea class="form-control" name="calendar_description" placeholder="{{_('Calendar description')}}" required="required" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('calendar_description')}}"></textarea>     
                        </div>
                      </div>
                    </div>
                    <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                      <label for="calendar_date">{{_('Date')}}</label>
                      <input type="hidden" class="form-control" id="calendar_date"  name="calendar_date" >
                       <div id="calendar_date_picker"></div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-6 col-sm-6 col-xs-12">
                      </div>
                  </div>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-default" data-dismiss="modal">{{_('Close')}}</button>
                  <button class="btn btn-success" type="submit">{{_('Save')}}</button>
                </div>
              </div>
            </div>
          </form>
        </div>
        <script type="text/javascript">
          var modalWindow = null;      
          $(document).ready(function() {

            $('form#new_item_form').on('submit',function(event){
                event.preventDefault();
                modalWindow.modal('hide');
                // Reload the calendar page...
                setTimeout(function(){
                  load_page('calendar.html');                
                },1000);     
            });    
 
            $.get('api/system',function(data){
              if (data.external_calendar_url != '' && data.external_calendar_url != null) {
                $('div.x_content').html($('<iframe>').addClass('external_calendar').attr('src',data.external_calendar_url));
              } else {
                var calendar = $('div.x_content').fullCalendar({
                  header: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'month,agendaWeek,agendaDay,listMonth'
                  },
                  eventRender: function(eventObj, $el) {
                    $el.popover({
                       title: eventObj.title,
                       content: eventObj.description,
                       trigger: 'hover',
                       placement: 'top',
                       container: 'body'
                     });
                  },
                  selectable: true,
                  selectHelper: true,
                  editable: true,
                  events: {
                    url: '/api/calendar/'
                  },
                  select: function(start, end, allDay) {
                    calendar_item({start:start});
                  },              
                });
              }
            });
            reload_reload_theme();
          });
        </script>
% include('inc/page_footer.tpl')
