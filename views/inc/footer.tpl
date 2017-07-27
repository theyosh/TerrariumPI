      </div>
    </div>
    <footer>
      <div class="pull-right">
        {{title}} - <a href="https://terrarium.theyosh.nl" title="{{_('Terrarium home automation v. %s' % version)}}" target="_blank">{{_('Terrarium home automation v. %s' % version)}}</a> - <a href="https://github.com/theyosh/TerrariumPI" target="_blank" title="{{_('Download TerrariumPI on Github')}}">{{_('Github')}}</a>
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
  <script type="text/javascript" src="/gentelella/vendors/bootstrap-progressbar/bootstrap-progressbar.min.js"></script>
  <!-- NProgress -->
  <script type="text/javascript" src="/gentelella/vendors/nprogress/nprogress.js"></script>
  <script type="text/javascript" src="/gentelella/vendors/select2/dist/js/select2.full.min.js"></script>
  <!-- FastClick -->
  <script type="text/javascript" src="/gentelella/vendors/fastclick/lib/fastclick.js"></script>
  <!-- PNotify -->
  <script type="text/javascript" src="/gentelella/vendors/pnotify/dist/pnotify.js"></script>
  <script type="text/javascript" src="/gentelella/vendors/pnotify/dist/pnotify.buttons.js"></script>
  <script type="text/javascript" src="/gentelella/vendors/pnotify/dist/pnotify.nonblock.js"></script>
  <!-- Leaflet -->
  <script type="text/javascript" src="/static/leaflet/leaflet.js"></script>
  <script type="text/javascript" src="/static/leaflet.loading/src/Control.Loading.js"></script>
  <script type="text/javascript" src='/static/leaflet.fullscreen/dist/Leaflet.fullscreen.min.js'></script>



  <script type="text/javascript" src='/static/fancybox/dist/jquery.fancybox.min.js'></script>


  <!-- Load the terrariumPI JS script-->
  <script type="text/javascript" src="/static/js/jquery.fullscreen-min.js"></script>
  <!-- Load the terrariumPI JS script-->
  <script type="text/javascript" src="/static/js/terrariumpi.js"></script>
  <script type="text/javascript">
    globals.current_version = '{{version}}';
  </script>
</body>
</html>
