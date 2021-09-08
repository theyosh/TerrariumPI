{% if page.device_url %}
[More information ...]({{ page.device_url }})
{% endif %}
## Setup

{% if page.device_auto_detect %}
### Auto detect
This sensor will be auto detected during startup or added by 'Scan sensors' in the menu.
{% endif %}

In order to use the **{{ page.device_title | default: page.title }}** use the following settings:

### Mandantory

Hardware
: {{ page.device_hardware }}

Types
{% for type in page.device_types %}
: {{ type }}
{% endfor %}

Address
: {{ page.device_address }} {%if page.device_power_management %}This sensor does support ([power management]({{ 'hardware' | relative_url}}#power-saving))
 {% endif %}

Name
: The name of the sensor

Alarm min
: The lower alarm value. When the sensor gets below this value, the **low** alarm will be triggered

Alarm max
: The high alarm value. When the sensor gets higher then this value, the **hight** alarm will be triggered

Limit min
: The minimun value that is valid for this sensor. Values measured below this value will be ignored.

Limit max
: The maximum value that is valid for this sensor. Values measured higher then this value will be ignored.

Max diff
: The maximum difference between two measurements that is valid. Enter **0** to disable.

Exclude average
: Exclude this sensor from the average calculation and graphs on the dashboard.

### Optional
Offset
: The the value to add or subtract from the sensor reading.
