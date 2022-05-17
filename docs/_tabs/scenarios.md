---
title: Scenarios
icon: fas fa-mountain
order: 6

image:
  path: /assets/img/Scenery.webp
  src: /assets/img/Scenery.webp
  alt: Scenery header image
---
On this page you can find various information on how to setup areas and create scenarios.

<h2>Timer wizard</h2>
<p>Using the <code class="language-plaintext highlighter-rouge">weather</code> or <code class="language-plaintext highlighter-rouge">timer</code> mode in an area, you can set the following 6 fields. The minimal fields that needs to be entered are the <code class="language-plaintext highlighter-rouge">begin</code> and <code class="language-plaintext highlighter-rouge">end</code> time field. All other fields are optional. Using a value of '' or 0 will ignore the setting. Change some values in the form to see the outcome of the timer schedule.<p>
<p>The graph area in <span style="color:red">red</span> is the time the relay(s) are toggled on</p>
<p>And when you have selected <code class="language-plaintext highlighter-rouge">sensors</code>, used <code class="language-plaintext highlighter-rouge">light state</code> or <code class="language-plaintext highlighter-rouge">door state</code>, then the relay will only go on when that state is met during the on period in the red are of the graph.</p>
<table class="timertable">
  <tr>
    <th colspan="4" style="text-align:center">Operating window</th>
  </tr>
  <tr>
    <th>Begin time *</th><td><input type="time" id="begin_time" value="08:00"></td>
    <th>End time *</th><td><input type="time" id="end_time" value="20:00"></td>
  </tr>
  <tr>
    <td colspan="4">Enter the begin and end time off the operating window in which the relay(s) may operate</td>
  </tr>
  <tr>
    <th colspan="4" style="text-align:center">Timer periods</th>
  </tr>
  <tr>
    <th>On duration</th><td><input type="number" id="on_duration"></td>
    <th>Off duration</th><td><input type="number" id="off_duration"></td>
  </tr>
  <tr>
    <td colspan="4">Enter a duration in minutes where the relay(s) are toggled on and off. This will create timer(s)</td>
  </tr>
  <tr>
    <th colspan="4" style="text-align:center">Fine tuning</th>
  </tr>
  <tr>
    <th>Running time</th><td><input type="number" id="running_time"></td>
    <th>Settle time</th><td><input type="number" id="settle_time"></td>
  </tr>
  <tr>
    <td colspan="4">Enter a duration in seconds which the relay(s) are on and the settle timeout</td>
  </tr>
</table>
<canvas id="timeGraph" style="width: 100%; height: 300px;"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js@3.7.0/dist/chart.min.js" integrity="sha256-Y26AMvaIfrZ1EQU49pf6H4QzVTrOI8m9wQYKkftBt4s=" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/hammerjs@2.0.8/hammer.min.js" integrity="sha256-eVNjHw5UeU0jUqPPpZHAkU1z4U+QFBBY488WvueTm88=" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@1.2.0/dist/chartjs-plugin-zoom.min.js" integrity="sha256-23gWVYds+PNFbnldeTaY5stxoJ6j+5QmR/vGLWpNcOg=" crossorigin="anonymous"></script>
<script src="/TerrariumPI/assets/js/timerGraph.js" ></script>