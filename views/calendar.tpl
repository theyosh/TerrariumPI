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
        <script type="text/javascript">
          $(document).ready(function() {
            $.get('api/system',function(data){

              if (data.external_calendar_url != '' && data.external_calendar_url != null) {
                $('div.x_content').html($('<iframe>').addClass('external_calendar').attr('src',data.external_calendar_url));
              } else {
                /*
                var date = new Date(),
                        d = date.getDate(),
                        m = date.getMonth(),
                        y = date.getFullYear(),
                        started,
                        categoryClass;
*/
                var calendar = $('div.x_content').fullCalendar({
                  header: {
                        left: 'prev,next today',
                        center: 'title',
                        right: 'month,agendaWeek,agendaDay,listMonth'
                  },
                  selectable: true,
                  selectHelper: true,
                  editable: true,

                  events: {
                    url: '/api/calendar/', // use the `url` property
                  },

                  /*
                  select: function(start, end, allDay) {
                        $('#fc_create').click();

                        started = start;
                        ended = end;

                        $(".antosubmit").on("click", function() {
                          var title = $("#title").val();
                          if (end) {
                                ended = end;
                          }

                          categoryClass = $("#event_type").val();

                          if (title) {
                                calendar.fullCalendar('renderEvent', {
                                        title: title,
                                        start: started,
                                        end: end,
                                        allDay: allDay
                                  },
                                  true // make the event "stick"
                                );
                          }

                          $('#title').val('');

                          calendar.fullCalendar('unselect');

                          $('.antoclose').click();

                          return false;
                        });
                  },
                  */

                  /*
                  eventClick: function(calEvent, jsEvent, view) {
                        $('#fc_edit').click();
                        $('#title2').val(calEvent.title);

                        categoryClass = $("#event_type").val();

                        $(".antosubmit2").on("click", function() {
                          calEvent.title = $("#title2").val();

                          calendar.fullCalendar('updateEvent', calEvent);
                          $('.antoclose2').click();
                        });

                        calendar.fullCalendar('unselect');
                  },

                  */


                });


                //calendar.fullCalendar('option', 'locale', 'fr');

              }
            });
            reload_reload_theme();
          });
        </script>
% include('inc/page_footer.tpl')
