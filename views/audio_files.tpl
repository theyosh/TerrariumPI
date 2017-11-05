% include('inc/page_header.tpl')
        <div class="x_panel">
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
          <div class="x_content" style="display:none">
            <p>{{_('Here you can upload your audio files.')}} {{_('Open the dropzone multiple file uploader to upload new audio files.')}}</p>
          </div>
        </div>
        <div class="row">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2>{{_('Dropzone multiple file uploader')}}</h2>
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
              <div class="x_content" style="display:none">
                <p>{{_('Drag multiple files to the box below for multi upload or click to select files.')}}</p>
                <form action="/api/audio/file" class="dropzone"></form>
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <div class="x_panel">
              <div class="x_title">
                <h2>{{_('Existing audio files')}}</h2>
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
                <table id="datatable-responsive" class="table table-striped table-bordered dt-responsive nowrap" cellspacing="0" width="100%">
                    <thead>
                      <tr>
                        <th></th>
                        <th>{{_('Action')}}</th>
                        <th>{{_('File')}}</th>
                        <th>{{_('Size')}}</th>
                        <th>{{_('Upload')}}</th>
                        <th>{{_('Duration')}}</th>
                        <th>{{_('Name')}}</th>
                        <th>{{_('Album')}}</th>
                        <th>{{_('Type')}}</th>
                        <th>{{_('Bitrate')}}</th>
                        <th>{{_('Channels')}}</th>
                        <th>{{_('Frequency')}}</th>
                      </tr>
                    </thead>
                </table>
              </div>
            </div>
          </div>
        </div>
        <script type="text/javascript">
          $(document).ready(function() {
            $('.dropzone').dropzone({ url: this.action,
                                      withCredentials: true,
                                      init: function() {
                                        this.on("success", function(file,response) {
                                          new PNotify({
                                            type: (response.ok ? 'success' : 'error'),
                                            title: response.title,
                                            text: response.message,
                                            nonblock: {
                                              nonblock: true
                                            },
                                            delay: 3000,
                                            mouse_reset: false,
                                            //addclass: 'dark',
                                            styling: 'bootstrap3',
                                            hide: true,
                                          });
                                        });
                                      }
                                    });
            $('#datatable-responsive').DataTable({
              processing: true,
              order: [[ 2, 'asc' ]],
              ajax: {
                url: '/api/audio/files',
                dataSrc: 'audiofiles'
              },
              columns: [
                { data: null, render: function(value) {return '';}, orderable: false },
                { data: 'id', render: function(value,type,data) {return '<span class="glyphicon glyphicon-trash" aria-hidden="true" onclick="delete_audio_file(\'' + value + '\',\'' + data.name + '\')" title="Delete file ' + data.name + '"></span> <span class="glyphicon glyphicon-play" aria-hidden="true"></span>';} },
                { data: 'name' },
                { data: 'size',          render: function(value) {return formatBytes(value);}},
                { data: 'uploaddate',    render: function(value) {return moment(value * 1000).format('LLL');}},
                { data: 'trackduration', render: function(value) {return moment.duration(value*1000).humanize();}},
                { data: 'trackname' },
                { data: 'trackalbum' },
                { data: 'extension' },
                { data: 'trackbitrate' },
                { data: 'trackchannels' },
                { data: 'trackfrequency' }
              ]
            });
          });
        </script>
% include('inc/page_footer.tpl')
