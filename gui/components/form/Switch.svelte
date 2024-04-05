<script>
import FormGroup from './FormGroup.svelte';
import { getRandomString } from '../../helpers/string-helpers';

export let name;
export let id = name + getRandomString(6); // Create a unique ID
export let label = null;

export let value = null;

export let required = null;
export let readonly = false;
export let help = null;
export let invalid = null;
export let disabled = false;

export let horizontal = null;

let checkbox;

$: {
  if (checkbox) {
    // Update the switch state
    checkbox.checked = value === true || value === 'true' || value === 1 || value === 'on';
  }
}
</script>

<FormGroup {id} {label} {required} {help} {invalid} {horizontal} class="{$$props.class || ''}">
  <div class="switch">
    <input type="checkbox" class="switch" {id} {name} {readonly} {disabled} checked="{value}" bind:this="{checkbox}" />
    <label for="{id}" class="mt-1"></label>
  </div>
</FormGroup>
