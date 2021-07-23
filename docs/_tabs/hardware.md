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
{% unless sensor.relative_path contains "index" %}

  <h2>
    <a href="{{ site.baseurl }}{{ sensor.url }}">
      {{ sensor.title }} - {{ sensor.measures }}
    </a>
  </h2>
  <!-- <p>{{ sensor.content | markdownify }}</p> -->

{% endunless %}
{% endif %}
{% endfor %}