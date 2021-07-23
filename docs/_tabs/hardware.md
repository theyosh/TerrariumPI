---
title: Hardware
icon: fas fa-tools
order: 3
layout: post
---


Relays
======

Sensors
=======
All supported sensors 3
{% for sensor in site.hardware %}
{% if sensor.relative_path contains "sensor" %}

  <h2>
    <a href="{{ sensor.url }}">
      {{ sensor.title }} - {{ sensor.measures }}
    </a>
  </h2>
  <!-- <p>{{ sensor.content | markdownify }}</p> -->

{% endif %}
{% endfor %}