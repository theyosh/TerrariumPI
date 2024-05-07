<style>
  i.password-eye {
    cursor: pointer;
    float: right;
    margin: -1.7rem 0.5rem auto auto;
    position: relative;
  }
</style>

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

  const originalType = type;
</script>

<FormGroup {id} {label} {required} {help} {invalid} {horizontal} class="{$$props.class || ''}">
  <input
    {type}
    {id}
    {name}
    {placeholder}
    {value}
    {required}
    {readonly}
    {disabled}
    {min}
    {max}
    {step}
    class="form-control"
  />
  {#if originalType == 'password'}
    <i
      class="password-eye far"
      aria-hidden="true"
      class:fa-eye-slash="{type == 'password'}"
      class:fa-eye="{type == 'text'}"
      on:click="{() => (type = type === 'password' ? 'text' : 'password')}"
    ></i>
  {/if}
</FormGroup>
