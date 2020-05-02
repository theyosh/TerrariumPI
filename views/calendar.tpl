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
                    <div class="col-md-8 col-sm-8 col-xs-12">
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
                          <span class="text description"></span>
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
                          <div id="editor-one" class="editor-wrapper" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('calendar_description')}}"></div>
                          <input type="hidden" name="calendar_description">
                        </div>
                      </div>
                    </div>
                    <div class="col-md-4 col-sm-4 col-xs-12 form-group">
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

            $('#editor-one').on('change',function(){
              $('input[name="calendar_description"]').val(this.innerHTML);
            });

            $('form#new_item_form').on('submit',function(event){
                event.preventDefault();
                // Date range picker is including enddate, where ical is excluding it. So we add an extra dat here.... :? :(
                var enddate = moment($(this).find('input[name="daterangepicker_end"]').val(),'L').add(1, 'days')
                $(this).find('input[name="daterangepicker_end"]').val(enddate.format('L'))
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
                       content: eventObj.description + '<br /><strong>{{_('Duration')}}:</strong> ' + moment.duration(eventObj.end - eventObj.start).humanize(),
                       html: true,
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
                  select: function(start, end, jsEvent, view) {
                    calendar_item({start: start, end: end.subtract(1, 'days')});
                  },
                  eventClick: function(calEvent, jsEvent, view) {
                    // Here we go 1 day back for the date range picker. As the date range picker is inclusive the end date, where as the ical is exclusive end date
                    if (calEvent.end === null) {
                      calEvent.end = calEvent.start;
                    }
                    calendar_item({id: calEvent.id, start: calEvent.start, end: calEvent.end.subtract(1, 'days'), title: calEvent.title, description: calEvent.description});
                  }
                });
              }
            });
            reload_reload_theme();
          });
        </script>
% include('inc/page_footer.tpl')
