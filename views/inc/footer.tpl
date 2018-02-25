      </div>
    </div>
    <footer>
      <div class="pull-right">
        {{device}} - {{title}} - <a href="https://terrarium.theyosh.nl" title="{{_('Terrarium home automation v. %s' % version)}}" target="_blank">{{_('Terrarium home automation v. %s' % version)}}</a> - <a href="https://github.com/theyosh/TerrariumPI" target="_blank" title="{{_('Download TerrariumPI on Github')}}">{{_('Github')}}</a>
      </div>
      <div class="clearfix"></div>
    </footer><!-- /footer content -->
  </div>
  <!-- gauge.js -->
  <script type="text/javascript" src="/static/js/gauge.min.js"></script>
  <!-- Skycons -->
  <script type="text/javascript" src="/gentelella/vendors/skycons/skycons.js"></script>
  <!-- Flot -->
  <script type="text/javascript" src="/gentelella/vendors/Flot/jquery.flot.js"></script>
  <script type="text/javascript" src="/gentelella/vendors/Flot/jquery.flot.time.js"></script>
  <script type="text/javascript" src="/gentelella/vendors/Flot/jquery.flot.resize.js"></script>
  <script type="text/javascript" src="/gentelella/vendors/flot.curvedlines/curvedLines.js"></script>
  <!-- Momentjs -->
  <script type="text/javascript" src="/gentelella/vendors/moment/min/moment-with-locales.min.js"></script>
  <!-- bootstrap-progressbar -->
  <script type="text/javascript" src="/gentelella/vendors/bootstrap-progressbar/bootstrap-progressbar.min.js"></script>
  <!-- NProgress -->
  <script type="text/javascript" src="/gentelella/vendors/nprogress/nprogress.js"></script>
  <!-- select2 -->
  <script type="text/javascript" src="/gentelella/vendors/select2/dist/js/select2.full.min.js"></script>
  <!-- FastClick -->
  <script type="text/javascript" src="/gentelella/vendors/fastclick/lib/fastclick.js"></script>
  <!-- jQuery Knob -->
  <script type="text/javascript" src="/gentelella/vendors/jquery-knob/dist/jquery.knob.min.js"></script>
  <!-- PNotify -->
  <script type="text/javascript" src="/gentelella/vendors/pnotify/dist/pnotify.js"></script>
  <script type="text/javascript" src="/gentelella/vendors/pnotify/dist/pnotify.buttons.js"></script>
  <script type="text/javascript" src="/gentelella/vendors/pnotify/dist/pnotify.nonblock.js"></script>
  <!-- Leaflet -->
  <script type="text/javascript" src="/static/leaflet/leaflet.js"></script>
  <script type="text/javascript" src="/static/Leaflet.loading/src/Control.Loading.js"></script>
  <script type="text/javascript" src="/static/Leaflet.fullscreen/dist/Leaflet.fullscreen.min.js"></script>
  <!-- bootstrap-wysiwyg -->
  <script type="text/javascript" src="/gentelella/vendors/bootstrap-wysiwyg/js/bootstrap-wysiwyg.min.js"></script>
  <script type="text/javascript" src="/gentelella/vendors/jquery.hotkeys/jquery.hotkeys.js"></script>
  <script type="text/javascript" src="/gentelella/vendors/google-code-prettify/src/prettify.js"></script>
  <!-- Fancybox -->
  <script type="text/javascript" src="/static/fancybox/dist/jquery.fancybox.min.js"></script>
  <!-- jQuery fullscreen -->
  <script type="text/javascript" src="/static/js/jquery.fullscreen-min.js"></script>
  <!-- Dropzone.js -->
  <script type="text/javascript" src="/gentelella/vendors/dropzone/dist/min/dropzone.min.js"></script>
  <!-- DataTables -->
  <script type="text/javascript" src="/gentelella/vendors/datatables.net/js/jquery.dataTables.min.js"></script>
  <script type="text/javascript" src="/gentelella/vendors/datatables.net-bs/js/dataTables.bootstrap.min.js"></script>
  <script type="text/javascript" src="/gentelella/vendors/datatables.net-responsive/js/dataTables.responsive.min.js"></script>
  <script type="text/javascript" src="/gentelella/vendors/datatables.net-responsive-bs/js/responsive.bootstrap.js"></script>
  <!-- Switchery -->
  <script type="text/javascript" src="/gentelella/vendors/switchery/dist/switchery.min.js"></script>
  <!-- Load the terrariumPI JS script-->
  <script type="text/javascript" src="/static/js/terrariumpi.js"></script>
  <script type="text/javascript">
    globals.current_version = '{{version}}';
    globals.temperature_indicator = '{{temperature_indicator}}';
    globals.distance_indicator = '{{distance_indicator}}';
    globals.language = '{{lang}}';
  </script>
</body>
</html>
