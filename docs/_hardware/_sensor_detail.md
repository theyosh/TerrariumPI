{% if page.device_url %}
[More information ...]({{ page.device_url }})
{% endif %}

## Setup

{% if page.device_auto_detect %}

### Auto detect

This sensor will be auto detected during startup or added by 'Scan sensors' in the menu.
{% endif %}

In order to use the **{{ page.device_title | default: page.title }}** use the following settings:

### Mandatory

Hardware
: {{ page.device_hardware | default: page.title }}

Types
{% assign types = page.device_types | sort_natural | join: ", " %}
: {{types}}

Address
: {{ page.device_address }} {%if page.device_power_management %}This sensor does support ([**power management**]({% link _tabs/hardware.md %}#power-saving))
 {% endif %}

Other settings can be found at the [sensor setup]({% link _tabs/setup.md %}#sensors) information
