<script>
  import bsCustomFileInput from 'bs-custom-file-input';
  import { onMount } from 'svelte';
  import { _ } from 'svelte-i18n';

  import FormGroup from './FormGroup.svelte';
  import { getRandomString } from '../../helpers/string-helpers';

  export let name;
  export let label;

  export let id = name + getRandomString(6); // Create a unique ID when not entered manual
  export let placeholder = null;
  export let value;

  export let required = null;
  export let readonly = null;

  export let help = null;
  export let invalid = null;
  export let accept = null;
  export let horizontal = null;

  let filename_placeholder;
  let deleteFile = false;

  value = value || placeholder;
  onMount(() => {
    bsCustomFileInput.init();
    return () => {
      bsCustomFileInput.destroy();
    };
  });

  $: {
    if (filename_placeholder && value) {
      filename_placeholder.textContent = value;
    }
  }
</script>

<FormGroup
  id="{id}"
  label="{label}"
  required="{required}"
  help="{help}"
  invalid="{invalid}"
  horizontal="{horizontal}"
  class="{$$props.class || ''}">
  <div class="input-group">
    <div class="custom-file">
      <input type="hidden" name="{name}" />
      <input type="checkbox" name="{`delete_${name}`}" value="true" checked="{deleteFile}" class="d-none" />
      <input
        type="file"
        name="file_{name}"
        accept="{accept}"
        id="{id}"
        required="{required}"
        readonly="{readonly}"
        class="custom-file-input"
        on:change="{() => {
          deleteFile = false;
        }}" />
      <label class="custom-file-label" for="{id}" bind:this="{filename_placeholder}">{value}</label>
    </div>
    <div class="input-group-append">
      <span class="input-group-text">
        <button
          type="button"
          class="btn btn-sm"
          on:click="{() => {
            deleteFile = !deleteFile;
          }}">
          <i class="fas fa-trash-alt" class:text-danger="{deleteFile}"></i>
        </button>
      </span>
    </div>
  </div>
</FormGroup>

<style>
  .input-group-text {
    padding: 0px;
  }

  :global(.dark-mode .input-group-text i.fas) {
    color: white;
  }
</style>
