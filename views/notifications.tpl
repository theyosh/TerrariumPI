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
            <p>{{_('Enter the values per service that you want to use. Per service are all fields required, except mail port and mail authentication values.')}}</p>
            <p>{{_('Select per message the service to send the notification. You can have everything per email, and important ones per pushover or telegram.')}}</p>
            <p>{{_('Use %rawdata% to get all the possible replacement values. Then create your own message with variables like %now% and %current%. This can be done in either the title and message.')}}</p>
            <p>{{_('Make sure you submit the form after making changes!')}}</p>
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
                    <input class="form-control" name="email_receiver" placeholder="{{_('Receiver email')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_email_receiver')}}">
                  </div>
                  <div class="col-md-2 col-sm-3 col-xs-12 form-group">
                    <label for="email_server">{{_('SMTP server')}}</label>
                    <input class="form-control" name="email_server" placeholder="{{_('SMTP server')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_email_server')}}">
                  </div>
                  <div class="col-md-2 col-sm-3 col-xs-12 form-group">
                    <label for="email_server">{{_('SMTP server port')}}</label>
                    <input class="form-control" name="email_serverport" placeholder="{{_('SMTP server port')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_email_serverport')}}">
                  </div>
                  <div class="col-md-2 col-sm-3 col-xs-12 form-group">
                    <label for="email_to">{{_('SMTP username')}}</label>
                    <input class="form-control" name="email_username" placeholder="{{_('SMTP username')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_email_email_username')}}">
                  </div>
                  <div class="col-md-2 col-sm-3 col-xs-12 form-group">
                    <label for="email_to">{{_('SMTP password')}}</label>
                    <input class="form-control" name="email_password" placeholder="{{_('SMTP password')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_email_email_password')}}">
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row" id="notifications_display">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2><i class="fa fa-newspaper-o"></i> {{_('Display')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="col-md-4 col-sm-4 col-xs-12 form-group">
                    <label for="display_hardwaretype">{{_('Hardware')}}</label>
                    <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('notification_display_hardwaretype')}}">
                      <select class="form-control" name="display_hardwaretype" tabindex="-1" placeholder="{{_('Select an option')}}">
                      </select>
                    </div>
                  </div>
                  <div class="col-md-4 col-sm-4 col-xs-12 form-group">
                    <label for="display_address">{{_('Address')}}</label>
                    <input class="form-control" name="display_address" placeholder="{{_('Address')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_display_address')}}">
                  </div>
                  <div class="col-md-4 col-sm-4 col-xs-12 form-group">
                    <label for="display_title">{{_('Title')}}</label>
                    <div class="form-group" data-toggle="tooltip" data-placement="right" title="" data-original-title="{{translations.get_translation('notification_display_title')}}">
                      <select class="form-control" name="display_title" tabindex="-1" placeholder="{{_('Select an option')}}">
                        <option value="true">{{_('Enabled')}}</option>
                        <option value="false">{{_('Disabled')}}</option>
                      </select>
                    </div>
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
                  <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                    <label for="email_to">{{_('Consumer key')}}</label>
                    <input class="form-control" name="twitter_consumer_key" placeholder="{{_('Receiver email')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_twitter_consumer_key')}}">
                  </div>
                  <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                    <label for="email_server">{{_('Consumer secret')}}</label>
                    <input class="form-control" name="twitter_consumer_secret" placeholder="{{_('Consumer secret')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_twitter_consumer_secret')}}">
                  </div>
                  <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                    <label for="email_server">{{_('Access token')}}</label>
                    <input class="form-control" name="twitter_access_token" placeholder="{{_('Access token')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_twitter_access_token')}}">
                  </div>
                  <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                    <label for="email_to">{{_('Access token secret')}}</label>
                    <input class="form-control" name="twitter_access_token_secret" placeholder="{{_('Access token secret')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_twitter_access_token_secret')}}">
                  </div>
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
                  <div class="col-md-6 col-sm-6 col-xs-12 form-group">
                    <label for="email_to">{{_('API Token')}}</label>
                    <input class="form-control" name="pushover_api_token" placeholder="{{_('API Token')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_pushover_api_token')}}">
                  </div>
                  <div class="col-md-6 col-sm-6 col-xs-12 form-group">
                    <label for="email_server">{{_('User key')}}</label>
                    <input class="form-control" name="pushover_user_key" placeholder="{{_('User key')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_pushover_user_key')}}">
                  </div>
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
                  <div class="col-md-4 col-sm-4 col-xs-12 form-group">
                    <label for="email_to">{{_('Bot Token')}}</label>
                    <input class="form-control" name="telegram_bot_token" placeholder="{{_('Bot Token')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_telegram_bot_token')}}">
                  </div>
                  <div class="col-md-4 col-sm-4 col-xs-12 form-group">
                    <label for="email_server">{{_('Username')}}</label>
                    <input class="form-control" name="telegram_userid" placeholder="{{_('Username')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_telegram_username')}}">
                  </div>
                  <div class="col-md-4 col-sm-4 col-xs-12 form-group">
                    <label for="email_server">{{_('Proxy')}}</label>
                    <input class="form-control" name="telegram_proxy" placeholder="{{_('Proxy')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_telegram_proxy')}}">
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row" id="notifications_webhook">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <div class="x_panel">
                <div class="x_title">
                  <h2><i class="fa fa-cloud-upload"></i> {{_('Webhook')}} <small class="data_update">{{_('Settings')}}</small></h2>
                  <ul class="nav navbar-right panel_toolbox">
                    <li>
                      <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
                    </li>
                  </ul>
                  <div class="clearfix"></div>
                </div>
                <div class="x_content">
                  <div class="col-md-12 col-sm-12 col-xs-12 form-group">
                    <label for="email_to">{{_('Full post url')}}</label>
                    <input class="form-control" name="webhook_address" placeholder="{{_('Full post url')}}" type="text" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="{{translations.get_translation('notification_webhook_address')}}">
                  </div>
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
                    <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                      <label>{{_('Trigger')}}</label>
                    </div>
                    <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                      <label>{{_('Title')}}</label>
                    </div>
                    <div class="col-md-4 col-sm-4 col-xs-12 form-group">
                      <label>{{_('Message')}}</label>
                    </div>
                    <div class="col-md-2 col-sm-2 col-xs-12 form-group">
                      <label>{{_('Service')}}</label>
                    </div>
                  </div>
                  % for message in notifications.get_messages():
                  <div class="row">
                    <div class="col-md-3 col-sm-3 col-xs-12 form-group">
                      {{message['id'].replace('_',' ').capitalize()}}
                    </div>
                    <div class="col-md-3 col-sm-2 col-xs-12 form-group">
                      <input class="form-control" name="{{message['id']}}_title"  value="{{message['title']}}" placeholder="{{_('Title')}}" type="text">
                    </div>
                    <div class="col-md-4 col-sm-6 col-xs-12 form-group">
                      <textarea required="required" class="form-control" name="{{message['id']}}_message" ></textarea>
                    </div>
                    <div class="col-md-2 col-sm-2 col-xs-12 form-group notification_services text-center" >
                      <input type="hidden" name="{{message['id']}}_services" value="">
                      <label>
                        <i class="fa fa-send orange disabled" id="{{message['id']}}_services_email" title="{{_('Email')}}"></i>
                      </label>
                      <label>
                        <i class="fa fa-twitter blue disabled" id="{{message['id']}}_services_twitter" title="{{_('Twitter')}}"></i>
                      </label>
                      <label>
                        <i class="fa fa-pinterest blue disabled" id="{{message['id']}}_services_pushover" title="{{_('Pushover')}}"></i>
                      </label>
                      <label>
                        <i class="fa fa-send blue disabled" id="{{message['id']}}_services_telegram" title="{{_('Telegram')}}"></i>
                      </label>
                      <label>
                        <i class="fa fa-newspaper-o disabled" id="{{message['id']}}_services_display" title="{{_('Display')}}"></i>
                      </label>
                      <label>
                        <i class="fa fa-cloud-upload disabled" id="{{message['id']}}_services_webhook" title="{{_('Webhook')}}"></i>
                      </label>
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
          function toggleService(id) {
            // Toggle icon
            $('#' + id).toggleClass('disabled');

            id = id.split('_');
            var type = id.pop()
            var hidden_field_id = id.join('_');

            // Update hidden field
            var field = $('input[name="' + hidden_field_id + '"]');
            if ($('#' + hidden_field_id + '_' + type).hasClass('disabled')) {
              field.val(field.val().replace(type + ',','').replace(',' + type, '').replace(type,''));
            } else {
              if (field.val().indexOf(type) == -1) {
                field.val(field.val() + (field.val() == '' ? '' : ',') + type);
              }
            }
          }

          $(document).ready(function() {
            init_form_settings('notifications');

            $('div.notification_services i.fa').on('click',function(event){
              toggleService(this.id)
            });

            $("select").select2({
                placeholder: '{{_('Select an option')}}',
                allowClear: false,
                minimumResultsForSearch: Infinity
            });

            $('div#notifications_telegram input[name="telegram_bot_token"]').on('change',function() {
              if (this.value != '') {
                $.get('https://api.telegram.org/bot' + this.value + '/getMe', function(data){
                  if (data.ok) {
                    var link = $('div#notifications_telegram small.data_update a');
                    if (link.length == 0) {
                      link = $('<a>').attr({'target':'_blank','href':'#'}).css('margin-left' , '0.6em');
                      $('div#notifications_telegram small.data_update').append(link);
                    }
                    link.attr({'title':data.result.first_name,'href':'http://t.me/' + data.result.username}).text('Telegram Bot: ' + data.result.first_name);
                  } else {
                    $('div#notifications_telegram small.data_update a').remove();
                  }
                }).fail(function() {
                    $('div#notifications_telegram small.data_update a').remove();
                });
              } else {
                $('div#notifications_telegram small.data_update a').remove();
              }
            });

            $.get($('form').attr('action'),function(data){
              $.each(data.notifications,function(part,partdata) {
                switch (part) {
                  case 'email':
                  case 'display':
                    $.each(partdata.supported,function(key,value){
                      $('select[name="display_hardwaretype"]').append($('<option>').val(value).text(value));
                    });
                    $('select[name="display_hardwaretype"]').sortSelect();
                  case 'twitter':
                  case 'pushover':
                  case 'telegram':
                  case 'webhook':
                    $.each(partdata,function(key,value){
                      var config_field = $('form [name="' + part + '_' + key + '"]');
                      if (config_field.length >= 1) {
                        switch (config_field.prop('type').toLowerCase()) {
                          case 'text':
                          case 'select-one':
                          case 'select-multiple':
                            config_field.val(value + '').trigger('change');
                            break;
                        }
                      }
                    });
                    break;

                  case 'messages':
                    $.each(partdata,function(key,value){
                      $.each(value,function(index,data){
                        var config_field = $('form [name="' + value.id + '_' + index + '"]');
                        if (config_field.length >= 1) {
                          switch (config_field.prop('type').toLowerCase()) {
                            case 'text':
                            case 'textarea':
                              config_field.val(data);
                              break;

                            case 'hidden':
                              $.each(data.split(','),function(counter,service){
                                toggleService(value.id + '_services_' + service);
                              });
                              break;

                          case 'select-one':
                          case 'select-multiple':
                            config_field.val(data[value]).trigger('change');
                            break;
                          }
                        }
                      });
                    });
                    break;
                }
              });
            });
          });
        </script>
% include('inc/page_footer.tpl')
