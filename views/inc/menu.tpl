      <div class="col-md-3 left_col menu  ">
        <div class="left_col scroll-view">
          <div class="navbar nav_title" style="border: 0;">
            <a class="site_title" href="/"><i class="fa fa-paw"></i> <span>{{title}}</span></a>
          </div>
          <div class="clearfix"></div><!-- menu profile quick info -->
          <div class="profile">
            <div class="profile_pic"><img alt="..." class="img-circle profile_img" src="{{person_image}}"></div>
            <div class="profile_info">
              <span>{{_('Welcome')}},</span>
              <h2>{{person_name}}</h2>
            </div>
          </div><!-- /menu profile quick info -->
          <br>
          <!-- sidebar menu -->
          <div class="main_menu_side hidden-print main_menu" id="sidebar-menu">
            <div class="menu_section">
              <h3>{{_('General')}}</h3>
              <ul class="nav side-menu">
                <li class="active">
                  <a><i class="fa fa-home"></i> {{_('Home')}} <span class="fa fa-chevron-down"></span></a>
                  <ul class="nav child_menu" style="display:block">
                    <li>
                      <a href="dashboard.html">{{_('Dashboard')}}</a>
                    </li>
                    <li>
                      <a href="profile.html">{{_('Profile')}}</a>
                    </li>
                  </ul>
                </li>
                <li>
                  <a><i class="fa fa-cloud"></i> {{_('Weather')}} <span class="fa fa-chevron-down"></span></a>
                  <ul class="nav child_menu">
                    <li>
                      <a href="weather_forecast.html">{{_('Forecast')}}</a>
                    </li>
                    <li>
                      <a href="weather_settings.html">{{_('Settings')}}</a>
                    </li>
                  </ul>
                </li>
                <li>
                  <a><i class="fa fa-tint"></i> {{_('Sensors')}} <span class="fa fa-chevron-down"></span></a>
                  <ul class="nav child_menu">
                    <li>
                      <a href="sensor_temperature.html">{{_('Temperature')}}</a>
                    </li>
                    <li>
                      <a href="sensor_humidity.html">{{_('Humidity')}}</a>
                    </li>
                    <li>
                      <a href="sensor_settings.html">{{_('Settings')}}</a>
                    </li>
                  </ul>
                </li>
                <li>
                  <a><i class="fa fa-flash"></i> {{_('Switches')}} <span class="fa fa-chevron-down"></span></a>
                  <ul class="nav child_menu">
                    <li>
                      <a href="switch_status.html">{{_('Status')}}</a>
                    </li>
                    <li>
                      <a href="switch_settings.html">{{_('Settings')}}</a>
                    </li>
                  </ul>
                </li>
                <li>
                  <a><i class="fa fa-lock"></i> {{_('Doors')}} <span class="fa fa-chevron-down"></span></a>
                  <ul class="nav child_menu">
                    <li>
                      <a href="door_status.html">{{_('Status')}}</a>
                    </li>
                    <li>
                      <a href="door_settings.html">{{_('Settings')}}</a>
                    </li>
                  </ul>
                </li>
                <li>
                  <a><i class="fa fa-video-camera"></i> {{_('Webcam')}} <span class="fa fa-chevron-down"></span></a>
                  <ul class="nav child_menu">
                    <li>
                      <a href="webcam.html">{{_('Show')}}</a>
                    </li>
                    <li>
                      <a href="webcam_settings.html">{{_('Settings')}}</a>
                    </li>
                  </ul>
                </li>
                <li>
                  <a><i class="fa fa-lightbulb-o"></i> {{_('System')}} <span class="fa fa-chevron-down"></span></a>
                  <ul class="nav child_menu">
                    <li>
                      <a href="system_status.html">{{_('Status')}}</a>
                    </li>
                    <li>
                      <a href="system_environment.html">{{_('Environment')}}</a>
                    </li>
                    <li>
                      <a href="system_settings.html">{{_('Settings')}}</a>
                    </li>
                  </ul>
                </li>
              </ul>
            </div>
            <div class="menu_section">
              <h3>{{_('About')}}</h3>
              <ul class="nav side-menu">
                <li>
                  <a><i class="fa fa-info"></i> {{_('Help')}} <span class="fa fa-chevron-down"></span></a>
                  <ul class="nav child_menu">
                    <li>
                      <a href="info.html">{{_('Info')}}</a>
                    </li>
                    <li>
                      <a href="usage.html">{{_('Usage')}}</a>
                    </li>
                    <li>
                      <a href="hardware.html">{{_('Hardware')}}</a>
                    </li>
                  </ul>
                </li>
              </ul>
            </div>
          </div><!-- /sidebar menu -->
          <!-- /menu footer buttons -->
          <div class="sidebar-footer hidden-small">
            <a data-placement="top" data-toggle="tooltip" href="javascript:;" onclick="menu_click('system_settings.html');" title="{{_('Settings')}}"><span aria-hidden="true" class="glyphicon glyphicon-cog"></span><br />{{_('Settings')}}</a>
            <a data-placement="top" data-toggle="tooltip" href="javascript:;" onclick="$(document).fullScreen(true);" title="{{_('FullScreen')}}"><span aria-hidden="true" class="glyphicon glyphicon-fullscreen"></span><br />{{_('FullScreen')}}</a>
            <a data-placement="top" data-toggle="tooltip" title="{{_('Lock')}}"><span aria-hidden="true" class="glyphicon glyphicon-eye-close"></span><br />{{_('Lock')}}</a>
            <a data-placement="top" data-toggle="tooltip" title="{{_('Log out')}}"><span aria-hidden="true" class="glyphicon glyphicon-off"></span><br />{{_('Log out')}}</a>
          </div><!-- /menu footer buttons -->
        </div>
      </div><!-- top navigation -->
      <div class="top_nav">
        <div class="nav_menu">
          <nav class="" role="navigation">
            <div class="nav toggle">
              <a id="menu_toggle"><i class="fa fa-bars"></i></a>
            </div>
            <ul class="nav navbar-nav navbar-right">

              <li id="system_time" role="presentation">
                <i class="fa fa-clock-o"></i> <span >{{_('date/time')}}</span>
              </li>
              <li class="dropdown" role="presentation">
                <a aria-expanded="false" class="dropdown-toggle info-number" data-toggle="dropdown" href="javascript:;" id="door_indicator"><i class="fa fa-lock green"></i> <span>{{_('Door is closed')}}/{{_('Door is open')}}</span></a>
                <ul class="dropdown-menu list-unstyled msg_list" id="door_messages" role="menu">
                  <li class="no_message">
                    <div class="text-center">
                      <a><strong>{{_('No messages')}}</strong></a>
                    </div>
                  </li>
                </ul>
              </li>
              <li class="dropdown" role="presentation">
                <a aria-expanded="false" class="dropdown-toggle info-number" data-toggle="dropdown" href="javascript:;" id="online_indicator"><i class="fa fa-exclamation-triangle red"></i> <span>{{_('Online')}}/{{_('Offline')}}</span></a>
                <ul class="dropdown-menu list-unstyled msg_list" id="online_messages" role="menu">
                  <li class="no_message">
                    <div class="text-center">
                      <a><strong>{{_('No messages')}}</strong></a>
                    </div>
                  </li>
                </ul>
              </li>
            </ul>
          </nav>
        </div>
      </div><!-- /top navigation -->
      <!-- page content -->
      <div class="right_col" role="main" id="maincontent">
