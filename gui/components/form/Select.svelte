<script>
  import { onMount, createEventDispatcher } from 'svelte';

  import { template_sensor_type_icon } from '../../helpers/icon-helpers';
  import { getRandomString } from '../../helpers/string-helpers';
  import FormGroup from './FormGroup.svelte';
  import { arrIdentical } from '../../helpers/number-helpers';

  export let name;
  export let id = name + getRandomString(6); // Create a unique ID
  export let label = null;
  export let placeholder = label;

  export let value = null;
  export let options = [];

  export let multiple = false;
  export let required = null;
  export let readonly = false;
  export let help = null;
  export let invalid = null;

  export let horizontal = null;
  export let sort = false;
  export let disabled = null;

  if (multiple) name += '[]';

  const dispatch = createEventDispatcher();

  const changeAction = (data) => {
    dispatch('change', data);
  };

  const iconFormat = (state) => {
    if (!state.id || state.id === '') {
      return state.text;
    }

    let icon = false;
    if ((icon = template_sensor_type_icon(state.id))) {
      let span = document.createElement('span');
      span.innerHTML = '<i class="mr-1 fa-fw ' + icon + '"></i> ' + state.text;
      return span;
    }

    return state.text;
  };

  let old_value;
  const updateValue = (new_value, force) => {
    force = force || false;
    try {
      let update = false;

      if (multiple) {
        update = !arrIdentical(old_value, new_value);
      } else {
        update = old_value !== new_value;
      }

      if (select && (force || update)) {
        old_value = value;
        // Again some strange race condition with select2
        setTimeout(() => {
          if (select) {
            select.val(value).trigger('change.select2');
          }
        }, 10);
      }
    } catch {}
  };

  let old_options = [];
  const updateOptions = (options, force) => {
    if (
      options &&
      (!arrIdentical(
        options.map((item) => {
          return item.value + item.disabled;
        }),
        old_options.map((item) => {
          return item.value + item.disabled;
        })
      ) ||
        force)
    ) {
      let selected = select?.val() ?? [];
      if (sort) {
        options.sort((a, b) => {
          a = a.text.toLowerCase();
          b = b.text.toLowerCase();
          if (a < b) return -1;
          else if (a > b) return 1;
        });
      }

      if (select) {
        select.find('option').remove();
        if (!multiple) {
          select.append(new Option('', '', false, false));
        }

        options.map((item) => {
          let option = new Option(item.text, item.value, false, selected.indexOf(item.value) !== -1);
          option.disabled = item.disabled ?? false;
          select.append(option);
        });

        old_options = options;
      }
    }
  };

  let select;
  let old_data;
  onMount(() => {
    select = jQuery(select);
    select
      .select2({
        placeholder: `${placeholder}`,
        dropdownParent: select.parents('form'),
        minimumResultsForSearch: 10,
        templateResult: iconFormat,
        templateSelection: iconFormat,
      })
      .on('change.select2', (event) => {
        let data = select.select2('data').map((item) => {
          return item.id;
        });
        if (!multiple) {
          data = data.length === 0 ? null : data[0];
        }

        let update = multiple ? !arrIdentical(old_data, data) : old_data !== data;
        if (update) {
          changeAction(data);
        }
      });

    if (options) {
      // This is needed if the select is used/generated in a if statement
      updateOptions(options, true);
    }

    if (value) {
      // This is needed if the select is used/generated in a if statement
      updateValue(value, true);
    }

    // Destroy select2 when unmounted
    return () => {
      if (select) {
        select.select2('destroy');
        select.off('change.select2');
      }
    };
  });

  // Listen to value updates
  $: updateValue(value);

  // Listen to options change
  $: updateOptions(options);

  // Update readonly state, so that when false, it will not be added to the select
  $: readonly = readonly === true ? true : null;
</script>

<FormGroup
  id="{id}"
  label="{label}"
  required="{required}"
  help="{help}"
  invalid="{invalid}"
  horizontal="{horizontal}"
  class="{$$props.class || ''}">
  <select
    id="{id}"
    name="{name}"
    required="{required}"
    multiple="{multiple}"
    readonly="{readonly}"
    disabled="{disabled}"
    class="custom-select select2"
    bind:this="{select}">
    <!-- generate the options with javascript else it cannot dynamically update -->
  </select>
  <slot />
</FormGroup>
