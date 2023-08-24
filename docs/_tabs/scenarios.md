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

<h2 id="timer-wizard">Timer wizard</h2>
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
<script defer src="/TerrariumPI/assets/js/timerGraph.js" ></script>



<h2 id="dependencies">Dependencies</h2>
<p>There are multiple dependencies levels. Here we describe all the different dependencies that are possible to use.</p>

<h3 id="dependencies-general">General dependencies</h3>
<p>There are <strong>2</strong> <a href="/TerrariumPI/setup/#other-areas" title="Area setup page">basic dependencies</a>. When you choose something other than <code class="language-plaintext highlighter-rouge">Ignore</code>, then the selected option will be enforced.</p>
<img src="/assets/img/General_dependencies.webp" alt="Example general dependencies">
<p>
 These are:
<ol>
<li>Light status

<ul>
<li>On</li>
<li>Off</li>
<li>Ignore</li>
</ul>

</li>
<li>Door status
<ul>
<li>Closed</li>
<li>Open</li>
<li>Ignore</li>
</ul>

</li>
</ol>
In the above example we have a raining area setup which will toggle the relays 'Mister' and 'Sprayer' when the humidity is to low. But, there are 2 dependencies selected and active.
</p>
<p>
- In this case, the <strong><a href="/TerrariumPI/setup/#main-lights" title="Main lights setting page">main</a></strong> lights needs to be on, so it is day, and the water of the sprayer can vaporize.
<br />
- And the door needs to be closed. So you are sure that when you are working in the terrarium, and the door is open, you will not get wet.
</p>

<h3 id="dependencies-area">Area dependency</h3>
<img src="/assets/img/Area_dependecies.webp" alt="Example area dependency">
<p>
Here you can select other areas on which this area depends on. If the depending area is in an alarm state, this area will not toggle on, or if already on, toggle off.
</p>
<p>
For example you have a water tank area and a humidity area where you use a sprayer. When the water tank is (near) empty the low alarm of the water tank will go on, and this humidity area will then not toggle on.
<br />
This will protect the water sprayer against running hot/dry when there is no water.
</p>

<h3 id="dependencies-relay">Relay dependency</h3>
<p>
With relay dependencies you can make extra complex logic. A possibility is to 'share' a relay between two areas. As the basic rule is that <strong>a relay can only be used once</strong>. In order to 'share' a relay between the areas you need to create <strong>a new third area</strong>. In the third area you can select a timer window to toggle the 'shared' relay on. And select the relays used in the other two areas as dependening relays. And choice that <code class="language-plaintext highlighter-rouge">at least one on</code> dependency mode.
<br />
This way the relay in the third area will only go on when one of the selected relays of other areas are on.
</p>
<p>
When you select depending relays, you also need to select the dependency mode.
There are <strong>3</strong> dependency modes:
</p>
<ol>
<li>All on</li>
<li>At least one on</li>
<li>None on</li>
</ol>

<img src="/assets/img/Relay_dependencies.webp" alt="Example relay dependency">
<p>
In the example above we have selected an area which is controlling a fan. This will clear the air in the terrarium and should be running when there is either the rain relay is toggled on or the mister relay is toggled on. In this case, those relays are in different areas with different logic.
The fan should be on based on a timer from 08:00 till 20:00 hours. This is a 12 hour on time.
<br/>
But with the selected dependency relays, this area will only go on when on of the two selected relays is on. And when there is no depending relay is on, the power of this area will also shut down. So the fan will only be running when either the mister is running, or the sprayer is running.
</p>
<p>
You can also use the 'Power on time' and 'Settle time' values to fine tune.
</p>