{% if page.device_url %}
[More information ...]({{ page.device_url }})
{% endif %}

## Setup

{% if page.device_auto_detect %}

### Auto detect

This relay will be auto detected during startup or added by 'Scan relays' in the menu.
{% endif %}

In order to use the **{{ page.device_title | default: page.title }}** use the following settings:

### Mandatory

Hardware
: {{ page.device_hardware | default: page.title }}

Address
: {{ page.device_address }}

{% if page.dimmer_frequency %}

### Calibration

This is only available for dimmers.

Dimmer frequency in Hz
: Default frequency: {{ page.dimmer_frequency }} Hz

{% endif %}

Other settings can be found at the [relay setup]({% link _tabs/setup.md %}#relays) information
