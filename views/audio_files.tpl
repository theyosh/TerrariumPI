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
            <p>{{_('Here you can upload and manange your audio files.')}} {{_('Open the dropzone multiple file uploader to upload new audio files.')}} {{!_('In the existing audio files list you can see which files are uploaded. By clicking on the trashbin (%s) icon you can delete the file.') % ('<span class="glyphicon glyphicon-trash" aria-hidden="true"></span>',)}}</p>
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
                    <a class="collapse-link"><i class="fa fa-chevron-up"></i></a>
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
                        <th>{{_('Filename')}}</th>
                        <th>{{_('Size')}}</th>
                        <th>{{_('Upload date')}}</th>
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
        <div class="modal fade preview_player" tabindex="-1" role="dialog" aria-hidden="true">
          <div class="modal-dialog modal-sm">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close" onclick="stop_player()">
                  <span aria-hidden="true">×</span>
                </button>
                <h4 class="modal-title">{{_('Preview player')}}</h4>
              </div>
              <div class="modal-body">
                <h4>...</h4>
                <p>...</p>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal" onclick="stop_player()">Close</button>
              </div>
            </div>
          </div>
        </div>
        <script type="text/javascript">
          function stop_player() {
            $('.modal.fade.preview_player .modal-body p').html('')
          }
          $(document).ready(function() {
            $('.dropzone').dropzone({ url: this.action,
                                      withCredentials: true,
                                      acceptedFiles: '.mp3,.ogg,.m4a,.oga',
                                      dictDefaultMessage: '{{_('Drop files here to upload')}}',
                                      dictFallbackMessage: '{{_('Press browse button to select files')}}',
                                      dictFallbackText: null,
                                      dictFileTooBig: '{{_('File is to big. Filesize {{filesize}} is more then max {{maxFilesize}}')}}',
                                      dictInvalidFileType: '{{_('Invalid filetype')}}',
                                      dictResponseError: '{{_('Server could not process the upload. Error code {{statusCode}}')}}',
                                      init: function() {
                                        this.on("success", function(file,response) {
                                          if (response.ok) {
                                            ok_notification_bubble(response.title,response.message);
                                          } else {
                                            error_notification_bubble(response.title,response.message);
                                          }

                                        });
                                      }
                                    });

            $('#datatable-responsive').DataTable({
              language: {
                url: dataTableTranslations[$('html').attr('lang')],
              },
              processing: true,
              order: [[ 2, 'asc' ]],
              ajax: {
                url: '/api/audio/files',
                dataSrc: 'audiofiles'
              },
              columns: [
                { data: null, render: function(value) {return '';}, orderable: false },
                { data: 'id', render: function(value,type,data) {return '<span class="glyphicon glyphicon-trash" aria-hidden="true" onclick="delete_audio_file(\'' + value + '\',\'' + data.name + '\')" title="{{_('Delete file')}} ' + data.name + '"></span> <span class="glyphicon glyphicon-play" aria-hidden="true" data-toggle="modal" data-target=".preview_player" onclick="preview_audio_file(\'' + value + '\',\'' + data.name + '\')" title="{{_('Preview file')}} ' + data.name + '"></span>';} },
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
