
import { get } from "svelte/store";

import { get_template_color } from "../helpers/color-helpers";
import { getCustomConfig } from "../config";
import { locale } from "../locale/i18n";
import { isDay } from "../stores/terrariumpi";

const settings = getCustomConfig();

/* jslint unparam: true */
export const graphDefaultOpts = {

  maintainAspectRatio: false,
  pointRadius: false,
  scales: {
    x: {
      adapters: {
        date: {
          locale: get(locale),
        }
      },
      type: 'time',
      time: {
        displayFormats: {
          minute: 'LLLL',
        },
        tooltipFormat: 'LLLL',
        unit: 'minute',
      },
      ticks: {
        color: function () {
          return get(isDay) ? '#6c757d' : '#adb5bd';
        },
      }
    },
    y: {
      position: 'left',
      display: true,
      min: 0,
      gridLines: {
        display: true,
      },
      ticks: {
        color: function () {
          return get(isDay) ? '#6c757d' : '#adb5bd';
        },
        callback: function (value, index, ticks) {
          let unit = null;
          this.chart.config._config.data.datasets.forEach(dataset => {
            if (dataset.yAxisID == this.id) {
              unit = dataset.graphType;
            }
          });
          switch (unit) {
            case 'magnetic':
              return (value === 0 ? 'closed' : 'open');

            case 'ldr':
              return (value === 0 ? 'dark' : 'light');

            case 'motion':
              return (value === 0 ? 'still' : 'motion');

            case 'remote':
              return (value === 0 ? 'off' : 'on');

            default:
              return value + ' ' + (unit != null ? settings.units[unit].value : '');
          }
        }
      }
    },
    y2: {
      position: 'right',
      display: false,
      min: 0,
      gridLines: {
        display: false,
      },
      ticks: {
        color: function () {
          return get(isDay) ? '#6c757d' : '#adb5bd';
        },
        callback: function (value, index, ticks) {
          let unit = null;
          this.chart.config._config.data.datasets.forEach(dataset => {
            if (dataset.yAxisID == this.id) {
              unit = dataset.graphType;
            }
          });
          switch (unit) {
            case 'magnetic':
              return (value === 0 ? 'closed' : 'open');

            case 'ldr':
              return (value === 0 ? 'dark' : 'light');

            case 'motion':
              return (value === 0 ? 'still' : 'motion');

            case 'remote':
              return (value === 0 ? 'off' : 'off');

            default:
              return value + ' ' + (unit != null ? settings.units[unit].value : '');
          }
        }
      }
    },
  },
  interaction: {
    mode: 'nearest'
  },
  plugins: {
    legend: {
      display: function (context) {
        return context.chart.legend.legendItems.length > 1;
      },
      labels: {
        color: function () {
          return get(isDay) ? '#6c757d' : '#adb5bd';
        },
      }
    },
    tooltip: {
      callbacks: {
        label: function (context) {
          let label = context.dataset.label || '';
          if (label != '') {
            label = ` ${label}: `;
          }
          switch (context.dataset.graphType) {
            case 'magnetic':
              label += (context.parsed.y === 0 ? 'closed' : 'open');
              break;

            case 'ldr':
              label += (context.parsed.y === 0 ? 'dark' : 'light');
              break;

            case 'motion':
              label += (context.parsed.y === 0 ? 'still' : 'motion');
              break;

            case 'remote':
              label += (context.parsed.y === 0 ? 'off' : 'on');
              break;

            default:
              label += context.formattedValue + ' ' + (settings.units[context.dataset.graphType] ? settings.units[context.dataset.graphType].value : '');
          }
          return label;
        }
      }
    }
  }
};
/* jslint unparam: false */

export const graphTypes = {
  alarm_min: {
    label: 'graph.alarm.min',
    colors: {
      line: get_template_color('text-info'),
      background: get_template_color('text-info', 0.7),
    }
  },
  alarm_max: {
    label: 'graph.alarm.max',
    colors: {
      line: get_template_color('text-danger'),
      background: get_template_color('text-danger', 0.7),
    }
  },
  value: {
    label: 'graph.current',
    colors: {
      line: get_template_color('text-success'),
      background: get_template_color('text-success', 0.7),
    }
  },
  wattage: {
    label: 'graph.wattage',
    colors: {
      line: get_template_color('text-success'),
      background: get_template_color('text-success', 0.7),
    }
  },
  flow: {
    label: 'graph.flow',
    colors: {
      line: get_template_color('text-info'),
      background: get_template_color('text-info', 0.7),
    }
  },

  magnetic: {
    label: 'graph.magnetic',
    colors: {
      line: get_template_color('text-success'),
      background: get_template_color('text-success', 0.7),
    }
  },
  ldr: {
    label: 'graph.ldr',
    colors: {
      line: get_template_color('text-success'),
      background: get_template_color('text-success', 0.7),
    }
  },
  motion: {
    label: 'graph.motion',
    colors: {
      line: get_template_color('text-success'),
      background: get_template_color('text-success', 0.7),
    }
  },
  remote: {
    label: 'graph.remote',
    colors: {
      line: get_template_color('text-success'),
      background: get_template_color('text-success', 0.7),
    }
  },
};
