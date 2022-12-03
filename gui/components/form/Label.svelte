<script>
  export let id;
  export let label = null;
  export let required = false;
</script>

<label for="{id}" class="col col-form-label text-truncate"
>{label}{#if required === true}<span class="required text-danger ml-1">*</span>{/if}</label>
