        <div class="col-md-3 left_col menu_fixed">
          <div class="left_col scroll-view">
            <div class="navbar nav_title" style="border: 0;">
              <a href="/" class="site_title"><i class="fa fa-paw"></i> <span>{{title}}</span></a>
            </div>
            <div class="clearfix"></div>
            <!-- menu profile quick info -->
            <div class="profile">
              <div class="profile_pic">
                <img src="{{person_image}}" alt="..." class="img-circle profile_img">
              </div>
              <div class="profile_info">
                <span>Welcome,</span>
                <h2>{{person_name}}</h2>
              </div>
            </div>
            <!-- /menu profile quick info -->
            <br />
            <!-- sidebar menu -->
            <div id="sidebar-menu" class="main_menu_side hidden-print main_menu">
              <div class="menu_section">
                <h3>General</h3>
                <ul class="nav side-menu">
                  <li><a href="dashboard.html" title="Home"><i class="fa fa-home"></i> Home</a>
                  </li>
                  <li>
                    <a><i class="fa fa-cloud"></i> Weather <span class="fa fa-chevron-down"></span></a>
                    <ul class="nav child_menu">
                      <li><a href="weather_forecast.html">Forecast</a></li>
                      <li><a href="weather_settings.html">Settings</a></li>
                    </ul>
                  </li>
                  <li>
                    <a><i class="fa fa-tint"></i> Sensors <span class="fa fa-chevron-down"></span></a>
                    <ul class="nav child_menu">
                      <li><a href="sensor_temperature.html">Temperature</a></li>
                      <li><a href="sensor_humidity.html">Humidity</a></li>
                      <li><a href="sensor_settings.html">Settings</a></li>
                    </ul>
                  </li>
                  <li>
                    <a><i class="fa fa-flash"></i> Switches <span class="fa fa-chevron-down"></span></a>
                    <ul class="nav child_menu">
                      <li><a href="switch_status.html">Status</a></li>
                      <li><a href="switch_settings.html">Settings</a></li>
                    </ul>
                  </li>
                  <li>
                    <a><i class="fa fa-video-camera"></i> Webcam <span class="fa fa-chevron-down"></span></a>
                    <ul class="nav child_menu">
                      <li><a href="webcam.html">Show</a></li>
                      <li><a href="webcam_settings.html">Settings</a></li>
                    </ul>
                  </li>
                  <li>
                    <a><i class="fa fa-lightbulb-o"></i> System <span class="fa fa-chevron-down"></span></a>
                    <ul class="nav child_menu">
                      <li><a href="environment.html">Environment</a></li>
                      <li><a href="system_settings.html">Settings</a></li>
                    </ul>
                  </li>
                </ul>
              </div>
              <div class="menu_section">
                <h3>About</h3>
                <ul class="nav side-menu">
                  <li>
                    <a><i class="fa fa-info"></i> Help <span class="fa fa-chevron-down"></span></a>
                    <ul class="nav child_menu">
                      <li><a href="info.html">Info</a></li>
                      <li><a href="usage.html">Usage</a></li>
                      <li><a href="software.html">Software</a></li>
                      <li><a href="hardware.html">Hardware</a></li>
                      <li><a href="contact.html">Contact</a></li>
                    </ul>
                  </li>
                </ul>
              </div>
            </div>
            <!-- /sidebar menu -->
            <!-- /menu footer buttons -->
            <div class="sidebar-footer hidden-small">
              <a data-toggle="tooltip" data-placement="top" title="Settings">
              <span class="glyphicon glyphicon-cog" aria-hidden="true"></span>
              </a>
              <a onclick="$(document).fullScreen(true);" data-toggle="tooltip" data-placement="top" title="FullScreen">
              <span class="glyphicon glyphicon-fullscreen" aria-hidden="true"></span>
              </a>
              <a data-toggle="tooltip" data-placement="top" title="Lock">
              <span class="glyphicon glyphicon-eye-close" aria-hidden="true"></span>
              </a>
              <a data-toggle="tooltip" data-placement="top" title="Logout">
              <span class="glyphicon glyphicon-off" aria-hidden="true"></span>
              </a>
            </div>
            <!-- /menu footer buttons -->
          </div>
        </div>
        <!-- top navigation -->
        <div class="top_nav">
          <div class="nav_menu">
            <nav class="" role="navigation">
              <div class="nav toggle">
                <a id="menu_toggle"><i class="fa fa-bars"></i></a>
              </div>
              <ul class="nav navbar-nav navbar-right">
                <li role="presentation" class="">
                  <div class="dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
                    <span class="glyphicon glyphicon-time" aria-hidden="true"></span> <span id="system_time">date/time</span>
                  </div>
                </li>
                <li role="presentation" class="dropdown">
                  <a href="javascript:;" class="dropdown-toggle info-number" data-toggle="dropdown" aria-expanded="false" id="door_indicator">
                  <i class="fa fa-lock green"></i> <span>Door closed</span>
                  </a>
                  <ul id="door_messages" class="dropdown-menu list-unstyled msg_list" role="menu">
                    <li class="no_message">
                      <div class="text-center">
                        <a>
                        <strong>No messages</strong>
                        </a>
                      </div>
                    </li>
                  </ul>
                </li>
                <li role="presentation" class="dropdown">
                  <a href="javascript:;" class="dropdown-toggle info-number" data-toggle="dropdown" aria-expanded="false" id="online_indicator">
                  <i class="fa fa-exclamation-triangle red"></i> <span>Offline</span>
                  </a>
                  <ul id="online_messages" class="dropdown-menu list-unstyled msg_list" role="menu">
                    <li class="no_message">
                      <div class="text-center">
                        <a>
                        <strong>No messages</strong>
                        </a>
                      </div>
                    </li>
                  </ul>
                </li>
              </ul>
            </nav>
          </div>
        </div>
        <!-- /top navigation -->
        <!-- page content -->
        <div class="right_col" role="main">
