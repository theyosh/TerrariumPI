<script context="module">
  let current;
</script>

<script>
  import { isDay } from '../../stores/terrariumpi';

  export let src;

  let audio;
  let paused = true;

  const stopOthers = () => {
    if (current && current !== audio) current.pause();
    current = audio;
  };
</script>

<audio bind:this="{audio}" bind:paused="{paused}" on:play="{stopOthers}" controls preload="none" class="d-none" src="{src}"></audio>
<button class="btn btn-sm" class:btn-light="{$isDay}" class:btn-dark="{!$isDay}" on:click="{paused ? audio.play() : audio.pause()}">
  <i
    class="fas"
    class:fa-play-circle="{paused}"
    class:fa-stop-circle="{!paused}"
    class:text-success="{paused}"
    class:text-primary="{!paused}"></i>
</button>
