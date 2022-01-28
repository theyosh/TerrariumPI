**Webcam type:** {{ page.device_type }}

{% if page.device_url %}
[More information ...]({{ page.device_url }})
{% endif %}

## Setup

In order to use the **{{ page.device_title | default: page.title }}** use the following settings:

### Mandatory

Hardware
: {{ page.device_hardware | default: page.title }}

Address
: {{ page.device_address }}

Other settings can be found at the [webcam setup]({% link _tabs/setup.md %}#webcams) information
