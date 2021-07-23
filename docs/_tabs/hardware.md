---
title: Hardware
icon: fas fa-tools
order: 3
---


Relays
======

Sensors
=======
All supported sensors
{% for sensor in site.hardware.sensor %}
  <h2>
    <a href="{{ sensor.url }}">
      {{ sensor.name }} - {{ sensor.position }}
    </a>
  </h2>
  <p>{{ sensor.content | markdownify }}</p>
{% endfor %}