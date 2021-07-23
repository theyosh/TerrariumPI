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
{% for sensor in site.hardware.sensor %}
  <h2>
    <a href="/TerrariumPI/{{ sensor.url }}">
      {{ sensor.title }}
    </a>
  </h2>
  <p>{{ sensor.content | markdownify }}</p>
{% endfor %}