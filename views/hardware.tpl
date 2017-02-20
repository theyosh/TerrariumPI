% include('inc/page_header.tpl')
        <div class="row">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="" data-example-id="togglable-tabs" role="tabpanel">
              <ul class="nav nav-tabs bar_tabs" id="myTab" role="tablist">
                <li class="active" role="presentation">
                  <a aria-expanded="true" data-toggle="tab" href="#pi" id="pi-tab" role="tab">Raspberry PI</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#sensors" id="sensors-tab" role="tab">1 Wire</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#switches" id="switches-tab2" role="tab">Switches</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#webcam" id="webcam-tab2" role="tab">Webcams</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#door" id="door-tab2" role="tab">Door sensor</a>
                </li>
                <li class="" role="presentation">
                  <a aria-expanded="false" data-toggle="tab" href="#water" id="water-tab2" role="tab">Water sprayer</a>
                </li>
              </ul>
              <p>Here you can see the hardware that is used in TerrariumPI</p>
              <div class="tab-content" id="myTabContent">
                <div aria-labelledby="pi-tab" class="tab-pane fade active in" id="pi" role="tabpanel">
                  <p class="lead">Raspberry Pi</p>
                  <p>The Raspberry Pi is a credit-card sized computer that plugs into your TV and a keyboard. It is a capable little computer which can be used in electronics projects, and for many of the things that your desktop PC does, like spreadsheets, word-processing and games. It also plays high-definition video. We want to see it being used by kids all over the world to learn programming. <a href="http://www.raspberrypi.org/" target="_blank" title="Raspberry PI">http://www.raspberrypi.org/</a></p>
                </div>
                <div aria-labelledby="sensors-tab" class="tab-pane fade" id="sensors" role="tabpanel">
                  <div class="col-xs-9">
                    <!-- Tab panes -->
                    <div class="tab-content">
                      <div class="tab-pane active" id="1w_adapter">
                        <p class="lead">RPI2 I2C to 1-Wire Host Adapter for Raspberry Pi</p>
                        <p>This module provides an easy way to connect 1-Wire devices to your Raspberry Pi without using up one of the USB ports. It is based around a DS2482-100 I2C to 1-Wire IC. <a href="http://www.sheepwalkelectronics.co.uk/product_info.php?cPath=22&products_id=30" target="_blank" title="RPI2 I2C to 1-Wire Host Adapter for Raspberry Pi">http://www.sheepwalkelectronics.co.uk/product_info.php?cPath=22&products_id=30</a></p>
                      </div>
                      <div class="tab-pane" id="1w_temperature">
                        <p class="lead">SWE0 Temperature Sensor</p>
                        <p>A simple temperature sensor consisting of a DS18B20 sensors on 2m of cable with an RJ45 plug on the other end.<br>
                        Wired for parasitic or external power (see options below).<br>
                        Unsure which power option to choose? See the SWE0 Information page linked below for further information. <a href="http://www.sheepwalkelectronics.co.uk/product_info.php?cPath=23&products_id=52" target="_blank" title="SWE0 Temperature Sensor">http://www.sheepwalkelectronics.co.uk/product_info.php?cPath=23&products_id=52</a></p>
                      </div>
                      <div class="tab-pane" id="1w_humidity">
                        <p class="lead">SWE3 Humidity Sensor Module</p>
                        <p>This is a humidity sensor module based on a Honeywell HIH-4031 humidity sensor interfaced to the 1-Wire bus with a Maxim DS2438Z IC.</p>
                        <p>After several customer requests this module is now designed with 3 extra screw terminals connected directly to pins on the DS2438Z allowing you to use it as a general purpose 0-10V DC ADC. The assembled module and kit are now available omitting the HIH-4031 sensor and resistor R1 if you wish to use the module as such. <a href="http://www.sheepwalkelectronics.co.uk/product_info.php?cPath=23&products_id=55" target="_blank" title="SWE3 Humidity Sensor Module">http://www.sheepwalkelectronics.co.uk/product_info.php?cPath=23&products_id=55</a></p>
                      </div>
                      <div class="tab-pane" id="1w_hub">
                        <p class="lead">SWE2b Sensor Connection Module</p>
                        <p>This is a simple PCB with two RJ45 sockets and 6 sets of screw terminals connected in parallel to allow you to easily connect SWE0a sensors into your 1-Wire network. <a href="http://www.sheepwalkelectronics.co.uk/product_info.php?cPath=23&products_id=64" target="_blank" title="SWE2b Sensor Connection Module">http://www.sheepwalkelectronics.co.uk/product_info.php?cPath=23&products_id=64</a></p>
                      </div>
                    </div>
                  </div>
                  <div class="col-xs-3">
                    <!-- required for floating -->
                    <!-- Nav tabs -->
                    <ul class="nav nav-tabs tabs-right">
                      <li class="active">
                        <a data-toggle="tab" href="#1w_adapter">Host adapter</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#1w_temperature">Temperature</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#1w_humidity">Humidity</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#1w_hub">Hub</a>
                      </li>
                    </ul>
                  </div>
                </div>
                <div aria-labelledby="switches-tab" class="tab-pane fade" id="switches" role="tabpanel">
                  <p class="lead">USB Four(4) Relay Output Module,Board for Home Automation</p>
                  <p>This is Four Channel relay board controlled by computer USB port. The usb relay board is with 4 SPDT relays rated up to 10A each. You may control devices 220V / 120V (up to 4) directly with one such relay unit. It is fully powered by the computer USB port. Suitable for home automation applications, hobby projects, industrial automation. The free software allows to control relays manually, create timers (weekly and calendar) and multivibrators, use date and time for alarms or control from command line. We provide software examples in Labview, .NET, Java, Borland C++. <a href="http://www.denkovi.com/usb-relay-board-four-channels-for-home-automation" target="_blank" title="USB Four(4) Relay Output Module,Board for Home Automation">http://www.denkovi.com/usb-relay-board-four-channels-for-home-automation</a></p>
                  <p>Alternatively: <a href="http://sigma-shop.com/product/75/usb-4-relay-board-rs232-serial-controlled-pcb.html" target="_blank" title="USB 4 Relay Board - RS232 Serial controlled, PCB">http://sigma-shop.com/product/75/usb-4-relay-board-rs232-serial-controlled-pcb.html</a></p>
                </div>
                <div aria-labelledby="webcam-tab" class="tab-pane fade" id="webcam" role="tabpanel">
                  <div class="col-xs-9">
                    <!-- Tab panes -->
                    <div class="tab-content">
                      <div class="tab-pane active" id="webcam_rpi">
                        <p class="lead">Raspberry PI Camera</p>
                        <p><a href="http://www.raspberrypi.org/camera" target="_blank" title="Raspberry PI Camera">http://www.raspberrypi.org/camera</a></p>
                      </div>
                      <div class="tab-pane" id="webcam_usb">
                        <p class="lead">USB Webcam</p>
                        <p>Any USB webcam will work</p>
                      </div>
                      <div class="tab-pane" id="webcam_online">
                        <p class="lead">Online Webcam</p>
                        <p>Any online camera that provides a (simple) HTTP support</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-xs-3">
                    <!-- required for floating -->
                    <!-- Nav tabs -->
                    <ul class="nav nav-tabs tabs-right">
                      <li class="active">
                        <a data-toggle="tab" href="#webcam_rpi">PiCam</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#webcam_usb">USB</a>
                      </li>
                      <li>
                        <a data-toggle="tab" href="#webcam_online">Online</a>
                      </li>
                    </ul>
                  </div>
                </div>
                <div aria-labelledby="door-tab" class="tab-pane fade" id="door" role="tabpanel">
                  <p class="lead">Magnetic contact switch</p>
                  <p>This sensor is essentially a reed switch, encased in an ABS plastic shell. Normally the reed is 'open' (no connection between the two wires). The other half is a magnet. When the magnet is less than 13mm (0.5") away, the reed switch closes. They're often used to detect when a door or drawer is open, which is why they have mounting tabs and screws. You can also pick up some double-sided foam tape from a hardware store to mount these, that works well without needing screws.<br>
                  <br>
                  <a href="https://www.adafruit.com/products/375" target="_blank">More info</a></p>
                </div>
                <div aria-labelledby="water-tab" class="tab-pane fade" id="water" role="tabpanel">
                  <p class="lead">Jewel spray starters set</p>
                  <p><a href="http://allinone-ict.mooo.com/jewelsprayv3/pages/bakery/basis-systeem-65-liter-4.php" target="_blank" title="Jewel spray starters set">Read more</a></p>
                </div>
              </div>
            </div>
          </div>
        </div>
% include('inc/page_footer.tpl')
