      <div class="col-md-3 left_col menu  ">
        <div class="left_col scroll-view">
          <div class="navbar nav_title" style="border: 0;">
            <a class="site_title" href="/"><i class="fa fa-paw"></i> <span>{{title}}</span></a>
          </div>
          <div class="clearfix"></div><!-- menu profile quick info -->

          <div class="profile">
            <div class="profile_pic">
              <img src="/static/images/christmas_hat.png" class="christmashat">
              <img alt="{{person_name}}" class="img-circle profile_img" src="{{person_image}}">
            </div>
            <div class="profile_info">
              <span>{{_('Welcome')}},</span>
              <h2>{{person_name}}</h2>
            </div>
          </div><!-- /menu profile quick info -->
          <!-- sidebar menu -->
          <div class="main_menu_side hidden-print main_menu" id="sidebar-menu">
            <div class="menu_section">
              <h3>{{_('General')}}</h3>
              <ul class="nav side-menu">
                <li>
                  <a><i class="fa fa-home"></i> {{_('Home')}} <span class="fa fa-chevron-down"></span></a>
                  <ul class="nav child_menu">
                    <li>
                      <a href="dashboard.html">{{_('Dashboard')}}</a>
                    </li>
                    <li>
                      <a href="profile.html">{{_('Profile')}}</a>
                    </li>
                    <li>
                      <a href="weather.html">{{_('Weather')}}</a>
                    </li>
                    <li>
                      <a href="calendar.html">{{_('Calendar')}}</a>
                    </li>
                  </ul>
                </li>
                <li>
                  <a><i class="fa fa-tint"></i> {{_('Sensors')}} <span class="fa fa-chevron-down"></span></a>
                  <ul class="nav child_menu">
                    <li>
                      <a href="sensor_gauge_overview.html">{{_('All')}}</a>
                    </li>
                    <li>
                      <a href="sensor_temperature.html">{{_('Temperature')}}</a>
                    </li>
                    <li>
                      <a href="sensor_humidity.html">{{_('Humidity')}}</a>
                    </li>
                    <li>
                      <a href="sensor_moisture.html">{{_('Moisture')}}</a>
                    </li>
                    <li>
                      <a href="sensor_conductivity.html">{{_('Conductivity')}}</a>
                    </li>
                    <li>
                      <a href="sensor_distance.html">{{_('Distance')}}</a>
                    </li>
                    <li>
                      <a href="sensor_ph.html">{{_('pH')}}</a>
                    </li>
                    <li>
                      <a href="sensor_light.html">{{_('Light')}}</a>
                    </li>
                    <li>
                      <a href="sensor_fertility.html">{{_('Fertility')}}</a>
                    </li>
                    <li>
                      <a href="sensor_co2.html">{{_('CO2')}}</a>
                    </li>
                    <li>
                      <a href="sensor_volume.html">{{_('Volume')}}</a>
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
                  <a><i class="fa fa-music"></i> {{_('Audio')}} <span class="fa fa-chevron-down"></span></a>
                  <ul class="nav child_menu">
                    <!--
                    <li>
                      <a href="audio_status.html">{{_('Status')}}</a>
                    </li>
                    -->
                    <li>
                      <a href="audio_playlist.html">{{_('Playlist')}}</a>
                    </li>
                    <li>
                      <a href="audio_files.html">{{_('Files')}}</a>
                    </li>
                  </ul>
                </li>
                <li>
                  <a><i class="fa fa-cog"></i> {{_('System')}} <span class="fa fa-chevron-down"></span></a>
                  <ul class="nav child_menu">
                    <li>
                      <a href="system_status.html">{{_('Status')}}</a>
                    </li>
                    <li>
                      <a href="notifications.html">{{_('Notifications')}}</a>
                    </li>
                    <li>
                      <a href="system_environment.html">{{_('Environment')}}</a>
                    </li>
                    <li>
                      <a href="system_settings.html">{{_('Settings')}}</a>
                    </li>
                    <li>
                      <a href="system_log.html">{{_('Log')}}</a>
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
            <a data-placement="top" data-toggle="tooltip" href="javascript:;" onclick="$(document).fullScreen(true);" title="{{_('Full screen')}}"><span aria-hidden="true" class="glyphicon glyphicon-fullscreen"></span><br />{{_('FullScreen')}}</a>
            <a data-placement="top" data-toggle="tooltip" title="{{_('Lock')}}"><span aria-hidden="true" class="glyphicon glyphicon-eye-close"></span><br />{{_('Lock')}}</a>
            <a data-placement="top" data-toggle="tooltip" href="javascript:;" onclick="logout();" title="{{_('Log out')}}"><span aria-hidden="true" class="glyphicon glyphicon-off"></span><br />{{_('Log out')}}</a>
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
              <li role="presentation" id="system_time">
                <i class="fa fa-clock-o"></i> <span >{{_('date/time')}}</span>
              </li>
              <li class="dropdown" role="presentation" id="online_indicator">
                <a aria-expanded="false" class="dropdown-toggle info-number" data-toggle="dropdown" href="javascript:;">
                  <span class="online">
                    <i class="fa fa-check-circle-o green"></i> <span>{{_('Online')}}</span>
                  </span>
                  <span class="offline">
                    <i class="fa fa-exclamation-triangle red"></i> <span>{{_('Offline')}}</span>
                  </span>
                </a>
                <ul class="dropdown-menu list-unstyled msg_list" id="online_messages" role="menu">
                  <li class="no_message">
                    <div class="text-center">
                      <a><strong>{{_('No messages')}}</strong></a>
                    </div>
                  </li>
                </ul>
              </li>
              <li class="dropdown disabled" role="presentation" id="door_indicator">
                <a aria-expanded="false" class="dropdown-toggle info-number" data-toggle="dropdown" href="javascript:;">
                  <span class="disabled">
                    <i class="fa fa-lock orange"></i> <span>{{_('Disabled')}}</span>
                  </span>
                  <span class="closed">
                    <i class="fa fa-lock green"></i> <span>{{_('Door is closed')}}</span>
                  </span>
                  <span class="open">
                    <i class="fa fa-unlock red"></i> <span>{{_('Door is open')}}</span>
                  </span>
                </a>
                <ul class="dropdown-menu list-unstyled msg_list" id="door_messages" role="menu">
                  <li class="no_message">
                    <div class="text-center">
                      <a><strong>{{_('No messages')}}</strong></a>
                    </div>
                  </li>
                </ul>
              </li>
              <li class="dropdown" role="presentation" id="calendar">
                <a aria-expanded="false" class="dropdown-toggle info-number" data-toggle="dropdown" href="javascript:;">
                  <span class="online">
                    <i class="fa fa-calendar green"></i> <span>{{_('Calendar')}}</span>
                    <span class="badge bg-green hidden">0</span>
                  </span>
                </a>
                <ul class="dropdown-menu list-unstyled msg_list" id="calendar_messages" role="menu">
                  <li class="no_message">
                    <div class="text-center">
                      <a><strong>{{_('No events')}}</strong></a>
                    </div>
                  </li>
                </ul>
              </li>
              <li class="dropdown disabled" role="presentation" id="player_indicator">
                <a aria-expanded="false" class="dropdown-toggle info-number" data-toggle="dropdown" href="javascript:;">
                  <span class="running">
                    <i class="fa fa-play-circle-o green"></i> <span>{{_('Playing')}}</span>
                  </span>
                  <span class="stopped">
                    <i class="fa fa-play-circle-o red"></i> <span>{{_('Stopped')}}</span>
                  </span>
                  <span class="disabled">
                    <i class="fa fa-play-circle-o orange"></i> <span>{{_('Disabled')}}</span>
                  </span>
                </a>
                <ul class="dropdown-menu list-unstyled msg_list" id="player_messages" role="menu">
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
