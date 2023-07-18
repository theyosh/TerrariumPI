Chart.defaults.elements.line.borderWidth = 3;
Chart.defaults.elements.line.fill = true;
Chart.defaults.elements.line.stepped = true;
Chart.defaults.elements.point.radius = 0;

let timerGraph = null;

function showTimerGraph() {

  const graphData = {
    labels: null,
    datasets: []
  };

  let today = new Date();
  today = `${today.getFullYear()}-${today.getMonth() < 9 ? '0' : ''}${today.getMonth()+1}-${today.getDate()}T`;

  const begin_time = Date.parse( today + jQuery('input#begin_time').val() + ':00');
  let end_time   = Date.parse( today + jQuery('input#end_time').val() + ':00');

  let on_duration  = jQuery('input#on_duration').val();
  let off_duration = jQuery('input#off_duration').val();

  let running_time = jQuery('input#running_time').val();
  let settle_time  = jQuery('input#settle_time').val();

  if (begin_time && end_time) {

    if (begin_time == end_time) {
        end_time += 86400000;
    }

    on_duration  = (on_duration  == '' || on_duration  == 0) ? (end_time - begin_time)/60000 : on_duration;
    off_duration = off_duration == '' ? 0 : off_duration;

    on_duration  *= 60 * 1000;
    off_duration *= 60 * 1000;

    const dataSetTotal = {
      label: 'Operating window',
      borderColor: 'rgb(0,0,255)',
      backgroundColor: 'rgba(0,0,255,0.5)',
      order: 3,
      data: [
        { x : new Date(begin_time - (0.5 * 3600000)),
          y : 0 },
        { x :  new Date(begin_time),
          y : 3 },
        { x : new Date(end_time),
          y : 0 },
        { x : new Date(end_time + (0.5 * 3600000)),
          y : 0 }
      ]
    };

    const dataSetPeriod = {
      label: 'Timer period',
      data: [{
        x : new Date(begin_time - (0.5 * 3600000)),
        y : 0
      }],
      borderColor: 'rgb(0,255,0)',
      backgroundColor: 'rgba(0,255,0,0.5)',
      order: 2,
    };

    const dataSetRunning = {
      label: 'Running',
      data: [{
        x : new Date(begin_time - (0.5 * 3600000)),
        y : 0
      }],
      borderColor: 'rgb(255,0,0)',
      backgroundColor: 'rgba(255,0,0,0.5)',
      order: 1,
    };

    let period_start = begin_time;
    while (new Date(period_start + (on_duration)) <= new Date(end_time)) {
      let period_end   = period_start + on_duration;

      dataSetPeriod.data.push({
        x : new Date(period_start),
        y: 2
      });
      dataSetPeriod.data.push({
        x : new Date(period_start + on_duration),
        y: 0
      });
      dataSetPeriod.data.push({
        x : new Date(period_start + on_duration + off_duration),
        y: 0
      });

      settle_duration = settle_time  == '' ? 0 : settle_time;
      let run_duration    = (running_time == '' || running_time == 0 || settle_duration == 0) ? (period_end - period_start)/1000 : running_time;

      run_duration    *= 1000;
      settle_duration *= 1000;

      let run_start = period_start;
      while (new Date(run_start + (run_duration)) <= new Date(period_end)) {

        dataSetRunning.data.push({
          x : new Date(run_start),
          y: 1
        });
        dataSetRunning.data.push({
          x : new Date(run_start + run_duration),
          y: 0
        });
        dataSetRunning.data.push({
          x : new Date(run_start + run_duration + settle_duration),
          y: 0
        });
        run_start += (run_duration + settle_duration);
      }
      period_start += (on_duration + off_duration);
    }

    dataSetRunning.data.push({
      x : new Date(end_time + (0.5 * 3600000)),
      y : 0
    })

    dataSetPeriod.data.push({
      x : new Date(end_time + (0.5 * 3600000)),
      y : 0
    })

    graphData.datasets.push(dataSetTotal);
    graphData.datasets.push(dataSetPeriod);
    graphData.datasets.push(dataSetRunning);

    const config = {
      type: 'line',
      data: graphData,
      options: {
        responsive: true,
        plugins: {
          zoom: {
            pan: {
              enabled: true,
            },
            zoom: {
              wheel: {
                enabled: true,
              },
              pinch: {
                enabled: true
              },
              mode: 'xy',
            }
          },
          title: {
            display: true,
            text: 'TerrariumPI Timer display'
          }
        },
        scales: {
          x: {
            type: 'time',
            title: {
              display: true,
              text: 'Time of the day'
            }
          },
          y: {
            ticks: {
              stepSize: 1,
              display: false
            }
          }
        },
      },
    };

    if (timerGraph === null) {
      timerGraph = new Chart(
        document.getElementById('timeGraph'),
        config
      );
    } else {
      timerGraph.data = graphData
      timerGraph.update();
    }
  }
}
jQuery(function() {
  showTimerGraph();
  jQuery('input').on('change',showTimerGraph);
});