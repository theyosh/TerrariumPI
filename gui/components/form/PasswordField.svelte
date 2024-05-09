<script>
  import FormGroup from './FormGroup.svelte';
  import { getRandomString } from '../../helpers/string-helpers';

  export let name;
  export let id = name + getRandomString(6); // Create a unique ID
  export let label = null;
  export let placeholder = label;

  export let value = null;

  export let required = null;
  export let readonly = false;
  export let help = null;
  export let invalid = null;
  export let disabled = false;

  export let horizontal = null;

  let type = 'password';
</script>

<FormGroup {id} {label} {required} {help} {invalid} {horizontal} class="{$$props.class || ''}">
  <div class="input-group">
    <input {type} {id} {name} {placeholder} {value} {required} {readonly} {disabled} class="form-control" />
    <div class="input-group-append">
      <span class="input-group-text p-0">
        <button
          type="button"
          class="btn btn-sm btn-flat"
          on:click="{() => (type = type === 'password' ? 'text' : 'password')}"
        >
          <i
            class="password-eye fas"
            aria-hidden="true"
            class:fa-eye-slash="{type == 'password'}"
            class:fa-eye="{type == 'text'}"
          ></i>
        </button>
      </span>
    </div>
  </div>
</FormGroup>
