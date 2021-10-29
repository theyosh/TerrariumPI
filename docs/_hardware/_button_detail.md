{% if page.device_url %}
[More information ...]({{ page.device_url }})
{% endif %}
## Setup

In order to use the **{{ page.device_title | default: page.title }}** use the following settings:

### Mandantory

Hardware
: {{ page.device_hardware | default: page.title }}

Address
: {{ page.device_address }}

{% if page.calibration %}
### Calibration
This is only available for light sensors.

Capacitor value in µF
: Enter the value of the capacitor
{% endif %}
Other settings can be found at the [button setup]({% link _tabs/setup.md %}#doors--buttons) information