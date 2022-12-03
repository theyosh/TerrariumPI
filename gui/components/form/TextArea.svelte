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
  export let rows = null;

  export let horizontal = null;
</script>

<FormGroup
  id="{id}"
  label="{label}"
  required="{required}"
  help="{help}"
  invalid="{invalid}"
  horizontal="{horizontal}"
  class="{$$props.class || ''}">
  <textarea id="{id}" name="{name}" placeholder="{placeholder}" rows="{rows}" readonly="{readonly}" class="form-control">{value}</textarea>
</FormGroup>
