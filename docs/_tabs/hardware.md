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
  <h2>
    <a href="/TerrariumPI/{{ sensor.url }}">
      {{ sensor.title }} - {sensor.relative_path}
    </a>
  </h2>
  <p>{{ sensor.content | markdownify }}</p>
{% endfor %}