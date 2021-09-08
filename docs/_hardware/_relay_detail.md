{% if page.device_url %}
[More information ...]({{ page.device_url }})
{% endif %}
## Setup

{% if page.device_auto_detect %}
### Auto detect
This relay will be auto detected during startup or added by 'Scan relays' in the menu.
{% endif %}

In order to use the **{{ page.device_title | default: page.title }}** use the following settings:

### Mandantory

Hardware
: {{ page.device_type }}

Address
: {{ page.device_address }}

Name
: The name of the relay

Wattage
: The ammount of power that is used when on or at full power (dimmer)

Water flow
: The ammount of water that is used when on or at full power (dimmer) in Liter/Gallon per minute

Current
: The current state of the relay. Value 0 is off, 100 is full on, or a value between 0 - 100 (dimmer)

{% if page.tags contains 'dimmer' %}
### Optional
{% if page.dimmer_frequency %}
Dimmer frequency in Hz
: The frequency of wicht the dimmer is working on. Default {{ page.dimmer_frequency }}
{% endif %}

Max power in %
: The max power the dimmer is allowed to use. Default 100

Dimmer offset in %
: An offset value that is reduced from the actual value. Default 0
{% endif %}