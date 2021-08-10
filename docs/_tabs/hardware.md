---
title: Hardware
icon: fas fa-tools
order: 3
layout: post
toc: true
---

Help
----
On every form popup you have a small question mark <i class="far fa-question-circle" aria-hidden="true"></i> next to the form title. Click on it to get more information about the form fields.

Relays
------
![New relay form](/assets/img/Add_Relay_Form.png)
_Popup form for adding and updating relays. - Calibration is only available for dimmers_

{% assign relays = site.hardware | where_exp: "relay", "relay.tags contains 'relay'" %}

We currently support <strong>{{ relays | size}}</strong> types of relays:
<br />

{% for relay in relays %}
  <h3>
    <a href="{{ relay.url | relative_url }}">{{ relay.title }}</a>

  {% if relay.tags contains 'dimmer' %}
    <img src="../assets/img/dimmer_icon.png" title="Relay is a dimmer" alt="Relay is a dimmer" style="height: 20px" class="ml-xl-3">
  {% endif %}

  </h3>
{% endfor %}


Sensors
------

{% assign sensors = site.hardware | where_exp: "sensor", "sensor.tags contains 'sensor'" %}

We currently support <strong>{{ sensors | size}}</strong> types of sensors:
<br />

{% for sensor in sensors %}
  <h3>
    <a href="{{ sensor.url | relative_url }}">{{ sensor.title }}</a>
  </h3>
{% endfor %}
