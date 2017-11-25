% include('inc/page_header.tpl')
        <div class="row documentation">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="" data-example-id="togglable-tabs" role="tabpanel">
              <ul class="nav nav-tabs bar_tabs" id="hardware_tablist" role="tablist">
                <li class="active" role="presentation">
                  <a aria-expanded="true" data-toggle="tab" href="#hardware-tab-hardware" id="hardware_tab_hardware" role="tab">{{_('Hardware')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#hardware-tab-raspberrypi" id="hardware_tab_raspberrypi" role="tab">{{_('Raspberry Pi')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#hardware-tab-sensors" id="hardware_tab_sensors" role="tab">{{_('Sensors')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#hardware-tab-switches" id="hardware_tab_switches" role="tab">{{_('Switches')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#hardware-tab-doors" id="hardware_tab_doors" role="tab">{{_('Doors')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#hardware-tab-webcams" id="hardware_tab_webcams" role="tab">{{_('Webcams')}}</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#hardware-tab-audio" id="hardware_tab_audio" role="tab">{{_('Audio')}}</a>
                </li>
              </ul>
              <div class="tab-content col-xs-9" id="hardware_content">
                <div aria-labelledby="hardware_tab_hardware" class="tab-pane fade active in" id="hardware-tab-hardware" role="tabpanel">
                  <h2>{{_('Hardware')}}</h2>
                  <p>{{_('Hover over the image below to read more about the supported hardware.')}}</p>
                  <div class="interactive_screenshot">
                    <div id="raspberrypi" class="click_area raspberrypi" title="{{_('Raspberry Pi')}}"></div>
                    <div id="bus_i2c" class="click_area" title="{{_('I2C bus')}}"></div>
                    <div id="bus_1wire" class="click_area" title="{{_('1Wire bus')}}"></div>
                    <div id="one_wire_temp_sensor1" class="click_area sensors" title="{{_('1Wire sensor 1')}}"></div>
                    <div id="one_wire_temp_sensor2" class="click_area sensors" title="{{_('1Wire sensor 2')}}"></div>
                    <div id="dht22_temp_humidity_sensor" class="click_area sensors" title="{{_('DHT22 temperature and humidity sensor')}}"></div>
                    <div id="USB_Relay" class="click_area switches" title="{{_('4 Ports USB relay board')}}"></div>
                    <div id="GPIO_Relay" class="click_area switches" title="{{_('4 Ports GPIO relay board')}}"></div>
                    <div id="GPIO_Door_sensor" class="click_area doors" title="{{_('GPIO Magnetic door sensor')}}"></div>
                    <div id="RPICam" class="click_area webcams" title="{{_('Raspberry Pi camera')}}"></div>
                    <img src="static/images/documentation/hardware_overview.jpg" alt="{{_('TerrariumPI test setup')}}" />
                  </div>
                </div>
                <div aria-labelledby="hardware_tab_raspberrypi" class="tab-pane fade" id="hardware-tab-raspberrypi" role="tabpanel">
                  <h2>{{_('Raspberry Pi')}}</h2>
                  <p>{{!_('TerrariumPI software is designed to run on a Raspberry Pi. It has been tested on a Raspberry Pi 2 and 3 with %s. Raspberry Pi Zero is not tested.') % ('<a href="https://www.raspberrypi.org/downloads/raspbian/" target="_blank">' + _('Raspbian OS') + '</a>')}}</p>
                  <p>{{_('The Raspberry Pi should have network connection and optionally SSH enabled for remote management. Also a strong power adapter is needed (+2Amps).')}}</p>
                  <img src="static/images/documentation/pi3specs.jpg" alt="{{_('Raspberry Pi 3 specifications')}}" class="img-thumbnail" />
                </div>
                <div aria-labelledby="hardware_tab_sensors" class="tab-pane fade" id="hardware-tab-sensors" role="tabpanel">
                  <h2>{{_('Sensors')}}</h2>
                  <p>{{_('TerrariumPI software has support for different kind of sensors. The following sensors below are tested with TerrariumPI software.')}}</p>
                  <div class="row">
                    <img src="static/images/documentation/ds1820-Raspberry-pi.png" alt="{{_('1Wire DS18B20 wiring scheme')}}" class="img-thumbnail alignright col-xs-3" />
                    <h4>{{_('1Wire')}}</h4>
                    <p>{{_('The 1wire bus will be scanned automatically during start up to load the connected and supported sensors. The DS18B20 sensors can share the GPIO pin by putting the sensors in parallel.')}}</p>
                    <p>{{_('Through the 1wire bus of the Raspberry Pi you can use the following hardware sensors')}}</p>
                    <ul>
                      <li><strong>{{_('DS18B20')}}</strong>: ...</li>
                    </ul>
                  </div>
                  <div class="row">
                    <img src="static/images/documentation/DHT_GPIO_schema.jpg" alt="{{_('DHT22 GPIO wiring scheme')}}" class="img-thumbnail alignright col-xs-3" />
                    <h4>{{_('GPIO')}}</h4>
                    <p>{{_('GPIO sensors has to added manually to TerrariumPI software. That can done in the web interface. The GPIO sensors cannot share GPIO pins. The DHT11 and DHT22 needs an extra resistor')}}</p>
                    <p>{{_('Through the GPIO bus of the Raspberry Pi you can use the following hardware sensors')}}</p>
                    <ul>
                      <li><strong>{{_('DHT11')}}</strong>: ...</li>
                      <li><strong>{{_('DHT22')}}</strong>: ...</li>
                      <li><strong>{{_('AM2302')}}</strong>: ...</li>
                    </ul>
                  </div>
                  <div class="row">
                    <img src="static/images/documentation/RPI2-1lg.jpg" alt="{{_('I2C bus adapter')}}" class="img-thumbnail alignright col-xs-3" />
                    <h4>{{_('OWFS')}}</h4>
                    <p>{{_('The OWFS server will be scanned automatically during start up to load the connected and supported sensors. There can be all kind of sensors connected to this server. All supported sensors will be shown.')}}</p>
                    <p>{{_('Through the I2C bus of the Raspberry Pi you can use the following hardware sensors with OWFS software')}}</p>
                    <ul>
                      <li><strong>{{_('DS18B20')}}</strong>: ...</li>
                      <li><strong>{{_('HIH400')}}</strong>: ...</li>
                    </ul>
                  </div>
                </div>
                <div aria-labelledby="hardware_tab_switches" class="tab-pane fade" id="hardware-tab-switches" role="tabpanel">
                  <h2>{{_('Switches')}}</h2>
                  <p>{{_('TerrariumPI software has support for different kind of relay boards. The following relay boards below are tested with TerrariumPI software.')}}</p>
                  <div class="row">
                    <img src="static/images/documentation/Raspberry_Pi_with_4_Channel_Relay_2.png" alt="{{_('GPIO relay board wiring scheme')}}" class="img-thumbnail alignright col-xs-3" />
                    <h4>{{_('GPIO')}}</h4>
                    <p>{{_('For every relay on the board there is need for a dedicated GPIO pin. For a 4 ports relay board there are 4 control GPIO pins and 2 pins for power and ground needed. This makes that it needs 6 GPIO pins in total.')}}</p>
                    <p>{{_('The following boards are tested')}}</p>
                    <ul>
                      <li><strong>{{_('VMA400')}}</strong>: ...</li>
                    </ul>
                  </div>
                  <div class="row">
                    <img src="static/images/documentation/variant_44_107.jpg" alt="{{_('USB Relay board')}}" class="img-thumbnail alignright col-xs-3" />
                    <h4>{{_('USB')}}</h4>
                    <p>{{_('The USB relay board does not need GPIO pins. It only needs one USB connection. The TerrariumPI software supports boards that are either running in Serial or BitBang. This is automatically detected when adding power switches.')}}</p>
                    <p>{{_('The following boards are tested')}}</p>
                    <ul>
                      <li><strong>{{_('Denkovi')}}</strong>: ...</li>
                    </ul>
                  </div>
                  <div class="row">
                    <img src="static/images/documentation/AC_Dimmer_MPDMv4_1_3_Kit_top_1.jpg.2560x2560_q85.jpg" alt="{{_('Universal AC MAINS Dimmer - MPDMv4.1')}}" class="img-thumbnail alignright col-xs-3" />
                    <h4>{{_('PWM')}}</h4>
                    <p>{{_('With PWM controlled boards it is possible to support dimming devices.')}}</p>
                    <p>{{_('The following boards are tested')}}</p>
                    <ul>
                      <li><strong>{{_('Nextevo')}}</strong>: <a href="https://www.tindie.com/products/nEXT_EVO1/universal-ac-mains-dimmer-mpdmv41/" target="blank">Universal AC MAINS Dimmer - MPDMv4.1 </a></li>
                    </ul>
                  </div>
                </div>
                <div aria-labelledby="hardware_tab_doors" class="tab-pane fade" id="hardware-tab-doors" role="tabpanel">
                  <img src="static/images/documentation/door_magnets.jpg" alt="Dashboard screenshot" class="img-thumbnail alignright col-xs-3" />
                  <h2>{{_('Doors')}}</h2>
                  <p>{{_('TerrariumPI software has support for magnetic door sensors. Only versions with two wires are supported. Connect one wire to the ground and the other wire to any GPIO pin that is free (except power and ground pins).')}}</p>
                </div>
                <div aria-labelledby="hardware_tab_webcams" class="tab-pane fade" id="hardware-tab-webcams" role="tabpanel">
                  <h2>{{_('Webcam')}}</h2>
                  <p>{{_('TerrariumPI software has support for different kind of cameras. The following cameras below are tested with TerrariumPI software.')}}</p>
                  <div class="row">
                    <img src="static/images/documentation/Pi-Camera-web.jpg" alt="{{_('Raspberry Pi 3 camera')}}" class="img-thumbnail alignright col-xs-3" />
                    <h4>{{_('RPICam')}}</h4>
                    <p>{{_('There are different Raspberry Pi cameras available. If the camera is Raspberry Pi compatible, it can be used with TerrariumPI software.')}}</p>
                  </div>
                  <div class="row">
                    <img src="static/images/documentation/webcam.jpg" alt="{{_('USB Webcam')}}" class="img-thumbnail alignright col-xs-3" />
                    <h4>{{_('USB')}}</h4>
                    <p>{{_('All kind of USB cameras can be used. Enter physical path of the device like /dev/videoX.')}}</p>
                  </div>
                </div>
                <div aria-labelledby="hardware_tab_audio" class="tab-pane fade" id="hardware-tab-audio" role="tabpanel">
                  <!-- <img src="static/images/documentation/door_magnets.jpg" alt="Dashboard screenshot" class="img-thumbnail alignright col-xs-3" /> -->
                  <h2>{{_('Audio')}}</h2>
                  <p></p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <script type="text/javascript">
          $('ul.nav.nav-tabs.bar_tabs a').hover(
              function() {
                $('.interactive_screenshot .' + $(this).attr('href').replace('#hardware-tab-','')).addClass('hover');
              },
              function() {
                $('.interactive_screenshot .' + $(this).attr('href').replace('#hardware-tab-','')).removeClass('hover');
              }
          );

          $('div.interactive_screenshot div.click_area').on('click',function(){
            var link = $(this).attr('class').replace('click_area ','hardware-tab-');
            $('ul.nav.nav-tabs.bar_tabs a[href="#' + link + '"]').click();
          });
        </script>
% include('inc/page_footer.tpl')
