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
            <p>
            </p>
          </div>
        </div>
        <form action="/api/config/notifications" class="form-horizontal form-label-left" data-parsley-validate="" method="put">
          <div class="row" id="notifications_email">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 class="orange"><i class="fa fa-send"></i> {{_('Email')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">


                    <div class="col-md-2 col-sm-3 col-xs-12 form-group">
                      <label for="email_to">{{_('Receiver email')}}</label>
                      <input class="form-control" name="email_to" placeholder="{{_('Receiver email')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_email_to')}}">
                    </div>


                    <div class="col-md-2 col-sm-3 col-xs-12 form-group">
                      <label for="email_server">{{_('SMTP server')}}</label>
                      <input class="form-control" name="email_server" placeholder="{{_('SMTP srever')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_email_server')}}">
                    </div>

                    <div class="col-md-2 col-sm-3 col-xs-12 form-group">
                      <label for="email_to">{{_('SMTP username')}}</label>
                      <input class="form-control" name="email_server_username" placeholder="{{_('SMTP userame')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_email_email_server_username')}}">
                    </div>

                    <div class="col-md-2 col-sm-3 col-xs-12 form-group">
                      <label for="email_to">{{_('SMTP password')}}</label>
                      <input class="form-control" name="email_server_password" placeholder="{{_('SMTP password')}}" required="required" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_email_email_server_password')}}">
                    </div>



                </div>
              </div>
            </div>
          </div>

          <div class="row" id="notifications_twiter">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 class="blue"><i class="fa fa-twitter"></i> {{_('Twitter')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                </div>
              </div>
            </div>
          </div>

          <div class="row" id="notifications_pushover">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 class="blue"><i class="fa fa-pinterest"></i> {{_('Pushover')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                </div>
              </div>
            </div>
          </div>

          <div class="row" id="notifications_telegram">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 class="blue"><i class="fa fa-send"></i> {{_('Telegram')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                </div>
              </div>
            </div>
          </div>


          <div class="row" id="notifications_messages">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2 ><i class="fa fa-envelope"></i> {{_('Messages')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                   <div class="row">
                    <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                      <label>{{_('Enabled')}}</label>
                    </div>
                    <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                      <label>{{_('Trigger')}}</label>
                    </div>
                    <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                      <label>{{_('Message')}}</label>
                    </div>
                  </div>
% for message in notifications.get_messages():
                  <div class="row">
                    <div class="col-md-2 col-sm-3 col-xs-12 form-group">
                      <input type="checkbox" class="js-switch" id="{{message['id']}}" />
                    </div>

                    <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                      {{message['title']}}
                    </div>
                    <div class="col-md-7 col-sm-6 col-xs-12 form-group">
                      <textarea required="required" class="form-control" name="message" id="{{message['id']}}_message" >{{message['message']}}</textarea>
                    </div>
                  </div>
% end







                </div>
              </div>
            </div>
          </div>





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
        <script type="text/javascript">

var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch'));

elems.forEach(function(html) {
  var switchery = new Switchery(html);
});

        </script>
% include('inc/page_footer.tpl')
