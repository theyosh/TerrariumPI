{% if page.device_url %}
[More information ...]({{ page.device_url }})
{% endif %}
## Setup

{% if page.device_auto_detect %}
### Auto detect
This relay will be auto detected during startup
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
: {{ page.device_address }}

Name
: The name of the relay

Alarm min
: The ammount of power that is used when on or at full power (dimmer)

Alarm max
: The ammount of water that is used when on or at full power (dimmer) in Liter/Gallon per minute

Limit min
: The current state of the relay. Value 0 is off, 100 is full on, or a value between 0 - 100 (dimmer)

Limit max
: The current state of the relay. Value 0 is off, 100 is full on, or a value between 0 - 100 (dimmer)

Max diff
: The current state of the relay. Value 0 is off, 100 is full on, or a value between 0 - 100 (dimmer)

Exclude average
: The current state of the relay. Value 0 is off, 100 is full on, or a value between 0 - 100 (dimmer)

### Optional
Offset
: The frequency of wicht the dimmer is working on. Default {{ page.dimmer_frequency }}
