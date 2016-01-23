function showAboutWindow() {
  var aboutMenu = jQuery('<div>').load('about.html', function() {
    aboutWindow.find('#tabs').jqxTabs({
      width: '100%'
    });
  });

  var aboutWindow = jQuery('<div>').attr('id', 'aboutForm').css({
      'display': 'none',
      'position': 'fixed'
    })
    .append(jQuery('<div>')
      .append(jQuery('<span>').addClass('icon about'))
      .append('About ' + document.title));

  aboutWindow.append(jQuery('<div>')
    .append(jQuery('<div>')
      .append(aboutMenu)));

  aboutWindow.jqxWindow({
    minHeight: 400,
    minWidth: 650,
    resizable: false,
    isModal: true,
    modalOpacity: 0.3,
  });
  aboutWindow.jqxWindow('open');

  aboutWindow.on('close', function(event) {
    aboutWindow.jqxWindow('destroy');
  });
}

function showLoginForm() {
  if (loggedin == true) {
    showLoginUpdateForm();
  } else {
    var loginWindow = jQuery('<div>').attr('id', 'loginForm').css({
        'display': 'none',
        'position': 'fixed'
      })
      .append(jQuery('<div>')
        .append(jQuery('<span>').addClass('icon authentication'))
        .append('Authenticate'));

    loginWindow.append(jQuery('<div>')
      .append(jQuery('<div>')
        .append('Username:')
        .append(jQuery('<input>').attr({
          'type': 'text'
        }).addClass('username').jqxInput({
          placeHolder: "Enter username",
          height: 25,
          width: 200,
          minLength: 1,
        }))
        .append('<br>')
        .append('Password:')
        .append(jQuery('<input>').attr({
          'type': 'password'
        }).addClass('password').jqxInput({
          placeHolder: "Enter password",
          height: 25,
          width: 200,
          minLength: 1,
        })))
      .append(jQuery('<div>').css({
          'float': 'right',
          'margin-top': '15px'
        })
        .append(jQuery('<input>').attr({
          'type': 'button',
          'value': 'OK'
        }).addClass('ok'))
        .append(jQuery('<input>').attr({
          'type': 'button',
          'value': 'Cancel'
        }).addClass('cancel'))));

    loginWindow.jqxWindow({
      maxHeight: 600,
      maxWidth: 850,
      minHeight: 30,
      minWidth: 250,
      resizable: false,
      isModal: true,
      modalOpacity: 0.3,
      okButton: loginWindow.find('.ok').jqxButton({
        width: '65px'
      }),
      cancelButton: loginWindow.find('.cancel').jqxButton({
        width: '65px'
      }),
    });
    loginWindow.jqxWindow('open');
    loginWindow.find('.username').focus();
    loginWindow.on('close', function(event) {
      if (event.args.dialogResult.OK) {
        var user = jQuery('#loginForm .username').val();
        var pass = jQuery('#loginForm .password').val();
        if (user != '' && pass != '') doLogin(user, pass);
      }
      loginWindow.jqxWindow('destroy');
    });

  }
}

function showLoginUpdateForm() {
  var loginWindow = jQuery('<div>').attr('id', 'loginForm').css({
      'display': 'none',
      'position': 'fixed'
    })
    .append(jQuery('<div>')
      .append(jQuery('<span>').addClass('icon authentication'))
      .append('Update authentication'));

  loginWindow.append(jQuery('<div>')
    .append(jQuery('<div>')
      .append('New username:')
      .append(jQuery('<input>').attr({
        'type': 'text'
      }).addClass('username').jqxInput({
        placeHolder: "Enter new username",
        height: 25,
        width: 200,
        minLength: 1,
      }))
      .append('<br>')
      .append('New password:')
      .append(jQuery('<input>').attr({
        'type': 'password'
      }).addClass('password1').jqxInput({
        placeHolder: "Enter new password",
        height: 25,
        width: 200,
        minLength: 1,
      }))
      .append('<br>')
      .append('New password (repeat):')
      .append(jQuery('<input>').attr({
        'type': 'password'
      }).addClass('password2').jqxInput({
        placeHolder: "Enter new password (repeat)",
        height: 25,
        width: 200,
        minLength: 1,
      })))

    .append(jQuery('<div>').css({
        'float': 'right',
        'margin-top': '15px'
      })
      .append(jQuery('<input>').attr({
        'type': 'button',
        'value': 'OK'
      }).addClass('ok'))
      .append(jQuery('<input>').attr({
        'type': 'button',
        'value': 'Cancel'
      }).addClass('cancel'))));

  loginWindow.jqxWindow({
    maxHeight: 600,
    maxWidth: 850,
    minHeight: 30,
    minWidth: 250,
    resizable: false,
    isModal: true,
    modalOpacity: 0.3,
    okButton: loginWindow.find('.ok').jqxButton({
      width: '65px'
    }),
    cancelButton: loginWindow.find('.cancel').jqxButton({
      width: '65px'
    }),
  });
  loginWindow.jqxWindow('open');
  jQuery('input[type=password].password1').passStrengthify();

  loginWindow.find('.username').focus();
  loginWindow.on('close', function(event) {
    if (event.args.dialogResult.OK) {
      var user = jQuery('#loginForm .username').val();
      var pass1 = jQuery('#loginForm .password1').val();
      var pass2 = jQuery('#loginForm .password1').val();
      if (user != '' && pass1 != '' && pass2 != '' && pass1 == pass2) updateLogin(user, pass1, pass2);
    }
    loginWindow.jqxWindow('destroy');
  });
}

function updateLogin(username, password1, password2) {
  var data = {
    username: username,
    password1: password1,
    password2: password2
  };
  jQuery.ajax({
    type: 'POST',
    url: '/auth/update',
    dataType: 'json',
    data: data
  }).done(function(result) {
    if (result.value == true) {
      showMessage('ok', 'Authentication', 'User authentication is updated');
    } else {
      showMessage('error', 'Authentication', 'User authentication update failed');
    }
  }).fail(function(result) {
    showMessage('error', 'Authentication', 'User authentication update failed');
  });
}

function doLogin(user, password) {
  jQuery.ajax({
    type: 'POST',
    url: '/auth/login',
    dataType: 'json',
    username: user,
    password: password
  }).done(function(result) {
    if (result.value == true) {
      loginOK();
    } else {
      loginError();
    }
  }).fail(function(result) {
    loginError();
  });
}

function loginOK() {
  loggedin = true;
  showMessage('ok', 'Authentication', 'User is authenticated');
  jQuery('.icon.authentication').removeClass('loggedout').addClass('loggedin');

  jQuery('.environment .icon:not(.alarm):not(.chart)').addClass('pointer');
  jQuery('.weatherLocation').addClass('pointer');
  jQuery('div.switch').addClass('pointer');

  jQuery('#system .icon.addwebcam').removeClass('inactive').addClass('pointer');
  jQuery('#system .icon.addwebcam').attr('title', 'Add a new webcam').bind('click', function() {
    addWebCamForm();
  });

  jQuery('tr[id^="env_"]').each(function(index) {
    var environmentPart = jQuery(this).attr('id').split('_')[1];
    jQuery(this).find('.icon').each(function(index) {
      var part = 'unknown'
      if (jQuery(this).hasClass('enabled')) {
        part = 'engine';
      } else if (jQuery(this).hasClass('trigger')) {
        part = 'trigger';
      } else if (jQuery(this).hasClass('running')) {
        part = 'current';
      } else if (jQuery(this).hasClass('options')) {
        part = 'options';
        jQuery(this).removeClass('inactive');
        jQuery(this).attr('title', 'Options (logged in)');
      }
      if (part == 'options') {
        if (environmentPart == 'lights') {
          jQuery(this).bind('click', function() {
            showEnvironmentLightsSettingsForm()
          });
        } else if (environmentPart == 'heater') {
          jQuery(this).bind('click', function() {
            showEnvironmentHeaterSettingsForm()
          });
        } else if (environmentPart == 'humidity') {
          jQuery(this).bind('click', function() {
            showEnvironmentHumiditySettingsForm()
          });
        }

      } else {
        jQuery(this).addClass('pointer').bind('click', function() {
          jQuery.ajax({
            url: '/environment/' + environmentPart + '/toggle/' + part,
            dataType: 'json'
          }).done(function(result) {
            updateEnvironment();
          });
        });
      }
    });
  });
}

function loginError() {
  loggedin = false;
  jQuery('.environment .edit').removeClass('edit');
  jQuery('.environment .icon.setup').addClass('edit');
  showMessage('error', 'Authentication', 'Authentication failed');
}

function showMessage(type, title, message) {
  jQuery('body').jqxTooltip({
    position: 'bottom',
    content: '<div class="message-' + type + '"><b>' + title + '</b><br />' + message + '</div>',
    showArrow: false,
    showDelay: 3000,
    disabled: false,
    width: '20em',
    top: '45%',
    name: 'message',
  }).bind('close', function() {
    jQuery(this).jqxTooltip('destroy');
  });

  jQuery('body').jqxTooltip('open');
}

function showEditForm(title, fields, post, callback) {
  if (callback == '' || callback == undefined) {
    callback = null;
  }
  var editWindow = jQuery('<div>').attr('id', 'editForm').css({
      'display': 'none',
      'position': 'fixed'
    })
    .append(jQuery('<div>')
      .append(jQuery('<span>').addClass('icon options'))
      .append('Edit ' + title));

  var fieldsCanvas = jQuery('<div>').css({
    'float': 'left',
    'width': '100%'
  });
  fieldsCanvas.append(jQuery('<input>').attr({
    'type': 'hidden',
    'value': post,
    'id': 'post'
  }));

  jQuery.each(fields, function(i, data) {
    if (data.type != 'radio' && data.type != 'hidden') {
      fieldsCanvas.append(data.label + ':');
    }
    var formElement = null;

    var fieldType = 'text';
    switch (data.type) {
      case 'radio':
        if (fieldsCanvas.find('div#radio_' + data.name).length == 0) {
          formElement = jQuery('<input>').attr({
            'id': data.name,
            'type': 'hidden',
            'value': data.value
          });
          fieldsCanvas.append(data.label + ':');
          fieldsCanvas.append(jQuery('<div>').attr({
            'id': 'radio_' + data.name
          }).css({
            'float': 'right'
          }));
          fieldsCanvas.append('<br />');
        }
        fieldsCanvas.find('div#radio_' + data.name).append(jQuery('<button>').attr({
          'id': data.value,
          'value': data.value,
          'readonly': data.readonly || false
        }));
        fieldsCanvas.find('div#radio_' + data.name).jqxButtonGroup({
          mode: 'radio'
        });
        break;
      case 'hidden':
        formElement = jQuery('<input>').attr({
          'id': data.name,
          'type': 'hidden',
          'value': data.value
        });
        break;
      case 'list':
        fieldsCanvas.append(jQuery('<input>').attr({
          'id': data.name,
          'type': 'hidden',
          'value': data.value
        }));
        formElement = jQuery('<div>').attr({
          'id': 'list_' + data.name
        }).css({
          'float': 'right'
        });
        break;
      case 'number':
      case 'text':
        fieldType = 'text';
        formElement = jQuery('<input>').attr({
            'id': data.name,
            'type': fieldType,
            'value': data.value,
            'readonly': data.readonly || false
          })
          .jqxInput({
            placeHolder: data.help,
            height: 25,
            width: 250,
            minLength: 1,
          });
        break;
      case 'dropdown':
        formElement = jQuery('<div>').jqxDropDownList({
          source: data.values,
          displayMember: 'name',
          valueMember: 'value',
          selectedIndex: 0,
          width: '100',
          autoDropDownHeight: true
        }).css({
          'float': 'right'
        });
        jQuery(formElement).find('input').attr({
          'id': data.name
        });
        break;
      case 'switch':
        formElement = jQuery('<div>').attr({
            'id': data.name,
            'type': fieldType,
            'value': data.value,
            'readonly': data.readonly || false
          }).css({
            'float': 'right'
          })
          .jqxSwitchButton({
            height: 20,
            width: 50,
            checked: data.value
          });
        break;
    }
    fieldsCanvas.append(formElement);
    if (data.type != 'radio' && data.type != 'hidden') {
      fieldsCanvas.append('<br />');
    }
  });

  editWindow.append(jQuery('<div>')
    .append(fieldsCanvas).append(jQuery('<div>').css({
        'float': 'right',
        'margin-top': '15px'
      })
      .append(jQuery('<input>').attr({
        'type': 'button',
        'value': 'OK'
      }).addClass('ok'))
      .append(jQuery('<input>').attr({
        'type': 'button',
        'value': 'Cancel'
      }).addClass('cancel'))));

  editWindow.jqxWindow({
    maxHeight: 600,
    maxWidth: 900,
    minHeight: 30,
    minWidth: 550,
    resizable: false,
    isModal: true,
    modalOpacity: 0.3,
    okButton: editWindow.find('.ok').jqxButton({
      width: '65px'
    }),
    cancelButton: editWindow.find('.cancel').jqxButton({
      width: '65px'
    }),
  });
  editWindow.jqxWindow('open');
  editWindow.on('close', {
    post_url: post,
    callback_function: callback
  }, function(event) {
    if (event.args.dialogResult.OK) {
      data = {};
      jQuery('input').each(function() {
        if (jQuery(this).attr('id') != undefined && jQuery(this).attr('id') != 'undefined' && jQuery(this).attr('id') != '' && jQuery(this).attr('id') != 'post' && jQuery(this).attr('id').indexOf('jqxWidget') == -1) {
          data[jQuery(this).attr('id')] = jQuery(this).val();
        }
      })

      jQuery('.jqx-switchbutton').each(function() {
        if (!jQuery(this).attr('readonly')) {
          data[jQuery(this).attr('id')] = jQuery(this).val();
        }
      })

      jQuery.ajax({
        type: 'POST',
        url: event.data.post_url,
        dataType: 'json',
        data: data
      }).done(function(result) {
        if (result.value === true) {
          switch (event.data.post_url) {
            case '/weather/save':
              showMessage('ok', 'Edit OK', 'Updated weather url:<br />' + data.xmlsource);
              break;
            case '/environment/lights/settings/save':
              showMessage('ok', 'Edit OK', 'The light environment settings are saved!');
              break;

          }
          if (event.data.callback_function != null) eval(event.data.callback_function);

          if (data.xmlsource !== undefined) {

          } else {
            showMessage('ok', 'Edit OK', 'Updated sensor:<br />' + data.name);
          }
        } else {
          showMessage('error', 'Edit Error', 'Error updating the XML source :<br />' + data.xmlsource);
        }
      }).fail(function(result) {
        showMessage('error', 'Edit Error', 'Error updating data. No connection with the terrarium server');
      });
    }
    editWindow.jqxWindow('destroy');
  });
}

function timeFormat(duration) {
  duration = moment.duration(duration);
  var value = '';
  if (duration.days() > 0 || value != '') {
    value += duration.days() + ' days, ';
  }
  if (duration.hours() > 0 || value != '') {
    value += duration.hours() + ' hours, ';
  }
  if (duration.minutes() > 0 || value != '') {
    value += duration.minutes() + ' minutes, ';
  }
  if (duration.seconds() > 0 || value != '') {
    value += duration.seconds() + ' seconds, ';
  }
  return value.substr(0, value.trim().length - 1);
}


var powerHistoryData = {};
function showPowerHistoryGraph(id, title, type) {
  powerHistoryData = {'datafields':[{name: 'timestamp',type: 'date'},{name: 'sRPI', type:'int'}],'dataLines':[ {dataField: 'sRPI', displayText: 'Raspberry PI'}]};
  jQuery.get('/switch/list', function(data) {
    jQuery.each(data.value, function(index, obj) {
      powerHistoryData['dataLines'].push({dataField: 's' + obj.id, displayText: obj.name});
      powerHistoryData['datafields'].push({name: 's' + obj.id, type: 'int'});
    });
    showGraph(id, title, type);
  });
}

function showGraph(id, title, type) {
  if (jQuery('#graphWindow').length == 1) {
    jQuery('#graphWindow').jqxWindow('destroy');
  }
  var grahWindow = jQuery('<div>').attr('id', 'graphWindow').css({
      'display': 'none',
      'position': 'fixed'
    })
    .append(jQuery('<div>')
      .append(jQuery('<span>').addClass('icon graph'))
      .append('Graph ' + title + ' (' + type + ')'));

  var fieldsCanvas = jQuery('<div>').attr('id', 'rrdgraph').css({
    'width': '100%',
    'height': '90%',
    'text-align': 'center'
  });

  grahWindow.append(jQuery('<div>')
    .append(fieldsCanvas)
    .append(jQuery('<div>').css({
        'float': 'right',
        'margin-top': '15px'
      })
      .append(jQuery('<input>').attr({
        'type': 'button',
        'value': 'day'
      }).jqxButton({
        width: '65px'
      }).bind('click', {
        id: id,
        title: title,
        type: type,
        period: 'day'
      }, function(event) {
        loadGraph(event.data.id, event.data.title, event.data.type, event.data.period)
      }))
      .append(jQuery('<input>').attr({
        'type': 'button',
        'value': 'week'
      }).jqxButton({
        width: '65px'
      }).bind('click', {
        id: id,
        title: title,
        type: type,
        period: 'week'
      }, function(event) {
        loadGraph(event.data.id, event.data.title, event.data.type, event.data.period)
      }))
      .append(jQuery('<input>').attr({
        'type': 'button',
        'value': 'month'
      }).jqxButton({
        width: '65px'
      }).bind('click', {
        id: id,
        title: title,
        type: type,
        period: 'month'
      }, function(event) {
        loadGraph(event.data.id, event.data.title, event.data.type, event.data.period)
      }))
      .append(jQuery('<input>').attr({
        'type': 'button',
        'value': 'year'
      }).jqxButton({
        width: '65px'
      }).bind('click', {
        id: id,
        title: title,
        type: type,
        period: 'year'
      }, function(event) {
        loadGraph(event.data.id, event.data.title, event.data.type, event.data.period)
      }))
      .append(jQuery('<input>').attr({
        'type': 'button',
        'value': 'close'
      }).addClass('cancel').jqxButton({
        width: '65px'
      }))
    ));

  grahWindow.jqxWindow({
    maxHeight: 500,
    maxWidth: 800,
    minHeight: 500,
    minWidth: 800,
    resizable: false,
    draggable: true,
    cancelButton: grahWindow.find('.cancel').jqxButton({
      width: '65px'
    }),
  });
  grahWindow.jqxWindow('open');
  grahWindow.on('close', function(event) {
    grahWindow.jqxWindow('destroy');
  });

  setTimeout(function() {
    loadGraph(id, title, type, 'day');
  }, 500);
}

function loadGraph(id, title, type, period) {
  $('#rrdgraph').html('<br /><br /><br />Loading...');

  var graphTitle = (type == 'temperature' ? 'Temperature' : 'Humidity') + ' sensor ' + title;
  var graphDescription = (type == 'temperature' ? 'Temperature in degrees' : 'Humidity in percentage');
  var graphToolTipsuffix = (type == 'temperature' ? 'C' : '%');
  var graphType = 'spline';

  var dataLines = [{
    dataField: 'current',
    displayText: 'Current ' + (type == 'temperature' ? 'temperature' : 'humidity'),
    lineColor: 'orange',
    fillColor: 'orange',
    lineWidth: 2
  }, {
    dataField: 'low',
    displayText: 'Low ' + (type == 'temperature' ? 'temperature' : 'humidity'),
    lineColor: 'green',
    fillColor: 'green',
    lineWidth: 2
  }];

  if (jQuery.inArray(type,['temperature','humidity','environment_humidity']) > -1) { // Exclude switches
    dataLines.push({
      dataField: 'high',
      displayText: 'High ' + (type == 'temperature' ? 'temperature' : 'humidity'),
      lineColor: 'red',
      fillColor: 'red',
      lineWidth: 2
    });
  }

  // Exlude powerswitches and weather temperature (Nasty hack)
  if (jQuery.inArray(type,['temperature','humidity','environment_humidity']) > -1 && title.indexOf('Weather in city:') == -1) {
    dataLines.push({
      dataField: 'limitlow',
      displayText: 'Limit low ' + (type == 'temperature' ? 'temperature' : 'humidity'),
      lineColor: 'darkgreen',
      fillColor: 'darkgreen',
      lineWidth: 2
    });
    dataLines.push({
      dataField: 'limithigh',
      displayText: 'Limit high ' + (type == 'temperature' ? 'temperature' : 'humidity'),
      lineColor: 'darkred',
      fillColor: 'darkred',
      lineWidth: 2
    });
  }

  if (type == 'power') {
    dataLines[0].displayText = 'Switch On';
    dataLines[1].displayText = 'Switch Off';
    graphTitle = 'Power switch ' + title;
  } else if (title.indexOf('Weather in city:') == -1) {
    graphTitle = 'Weater ' + title;
  }

  var source = {
    datatype: "json",
    datafields: [{
        name: 'high',
        type: 'float'
      }, {
        name: 'limithigh',
        type: 'float'
      }, {
        name: 'timestamp',
        type: 'date'
      }, {
        name: 'current',
        type: 'float'
      }, {
        name: 'low',
        type: 'float'
      }, {
        name: 'limitlow',
        type: 'float'
      },
    ],
    url: '/rrd/' + id + '/get/' + period,
    root: 'value'
  };

  var baseUnitValue = 'minute';
  var dateFormatxAxis = 'HH:mm';
  var periodDays = 1;
  var unitInterval = 30;

  switch (period) {
    case 'day':
      baseUnitValue = 'minute';
      dateFormatxAxis = 'HH:mm';
      periodDays = 1;
      unitInterval = 60;
      break;
    case 'week':
      baseUnitValue = 'hour';
      dateFormatxAxis = 'ddd dd@HH:mm';
      periodDays = 7;
      unitInterval = 6;
      break;
    case 'month':
      baseUnitValue = 'hour';
      dateFormatxAxis = 'dd MMM@HH:mm';
      periodDays = 31;
      unitInterval = 24;
      break;
    case 'year':
      baseUnitValue = 'day';
      dateFormatxAxis = 'ddd dd-MMM-yyyy';
      periodDays = 365;
      unitInterval = 7;
      break;
  }

  graphTitle += ' period: ' + moment().subtract(periodDays, 'days').format('ll') + ' - ' + moment().format('ll');

  if (type == 'wattage') {
    // Big hack! To leazy to fix nicely
    graphTitle = 'Power usage for day ' + moment().format('ll');
    graphType = 'stackedcolumn';
    graphDescription = 'Power usage in Watt';
    graphToolTipsuffix = 'W';
    source['datafields'] = powerHistoryData['datafields'];
    dataLines = powerHistoryData['dataLines'];
    source['url'] = '/system/wattage/graph';
  }

  var dataAdapter = new $.jqx.dataAdapter(source, {
    autoBind: true,
    async: false,
    downloadComplete: function() {},
    loadComplete: function() {},
    loadError: function(jqXHR, status, error) {
      alert('Error loading "' + status + '" : ' + error);
    },
  });

  // prepare jqxChart settings
  var settings = {
    title: graphTitle,
    description: '',
    showBorderLine: false,
    backgroundColor: 'transparent',
    showLegend: true,
    padding: {
      left: 0,
      top: 0,
      right: 0,
      bottom: 0
    },
    titlePadding: {
      left: 0,
      top: 0,
      right: 0,
      bottom: 0
    },
    source: dataAdapter,
    categoryAxis: {
      type: 'date',
      baseUnit: baseUnitValue,
      dataField: 'timestamp',
//      text: 'Time',
      textRotationAngle: -45,
      textRotationPoint: 'topright',
      textOffset: {
        x: 0,
        y: (baseUnitValue == 'minute' ? -20 : -35)
      },
      dateFormat: dateFormatxAxis,
      showTickMarks: true,
      tickMarksColor: '#E0E0E0',
      unitInterval: unitInterval,
      showGridLines: true,
      gridLinesColor: '#E0E0E0',
    },
    seriesGroups: [{
      type: graphType,
      columnsGapPercent: 0,
      seriesGapPercent: 0,
      toolTipFormatFunction: function(value, itemIndex, serie, group, xAxisValue, xAxis) {
        return moment(xAxisValue).format('dddd D MMMM YYYY [at] HH:mm') + '<br />' +
               serie.displayText + ': ' + value + graphToolTipsuffix;
      },
      valueAxis: {
        displayValueAxis: true,
        description: graphDescription,
        showTickMarks: true,
        tickMarksColor: '#E0E0E0',
        unitInterval: 5,
        gridLinesColor: '#E0E0E0',
      },
      series: dataLines
    }]
  };
  jQuery('#rrdgraph').jqxChart(settings);
}

function updateFavicon() {
  var currentFavicon = jQuery('link[rel=icon]').attr('href');
  var newFavicon = null;
  if (jQuery('.icon.webserver.enabled.error').length == 1) {
    var img = jQuery('.icon.webserver.enabled.error').css('background-image').substr(5);
    newFavicon = img.substr(0, img.length - 2);
  } else {
    newFavicon = (jQuery('#environment .alarm.on').length > 0 ? 'images/icons/alarm.png' : 'images/icons/enabled.png')
  }
  if (currentFavicon != newFavicon) {
    jQuery('link[rel=icon]').replaceWith(jQuery('link[rel=icon]').clone().attr('href', newFavicon));
  }

  setTimeout(function() {
    updateFavicon();
  }, 10000);
}

function updater(object) {
  jQuery('#' + object + ' span.updater').css({
    opacity: 0.0,
    visibility: "visible"
  }).animate({
    opacity: 1.0
  }, 500).animate({
    opacity: 0
  }, 500);
}

var loggedin = false;
jQuery(document).ready(function() {
  // Overrule the system and environment update timeout in seconds
  //environmentTimerTimeOut = 60;
  //systemTimerTimeOut = 60;
  //watherTimerTimeOut = 120;

  // Set the value weatherMaxStars to zero (0) to disable the stars
  //weatherMaxStars = 15;

  // Overrule the timeout for updating the switches. Default is 30 seconds
  //switchTimerTimeOut = 15;

  // Overrule the timeout for updating the sensors. Default is 30 seconds
  // sensorTimerTimeOut = 15;

  loadSystem();
  loadEnvironment();

  loadWeather();
  loadSensors();
  loadSwitches();
  loadWebcams();
  updateFavicon();

  jQuery('body').waitForImages(function() {
    jQuery('.loading').remove();
    jQuery('body').css('overflow', 'auto');
  }, function(loaded, count, success) {
    jQuery('.loading span').text('Loading ...  (' + loaded + '/' + count + ')');
  }, true);
});
