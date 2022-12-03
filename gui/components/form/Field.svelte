<script>
  import FormGroup from './FormGroup.svelte';
  import { getRandomString } from '../../helpers/string-helpers';

  export let type;

  export let name;
  export let id = name + getRandomString(6); // Create a unique ID
  export let label = null;
  export let placeholder = label;

  export let value = null;
  export let min = null;
  export let max = null;
  export let step = null;

  export let required = null;
  export let readonly = false;
  export let help = null;
  export let invalid = null;
  export let disabled = false;

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
  <input
    type="{type}"
    id="{id}"
    name="{name}"
    placeholder="{placeholder}"
    value="{value}"
    {required}
    {readonly}
    {disabled}
    min="{min}"
    max="{max}"
    step="{step}"
    class="form-control" />
</FormGroup>
