<script>
  import 'trumbowyg';
  import 'trumbowyg/dist/plugins/base64/trumbowyg.base64.min.js';
  import 'trumbowyg/dist/plugins/colors/trumbowyg.colors.min.js';
  import 'trumbowyg/dist/plugins/emoji/trumbowyg.emoji.min.js';
  import 'trumbowyg/dist/plugins/fontfamily/trumbowyg.fontfamily.min.js';
  import 'trumbowyg/dist/plugins/pasteimage/trumbowyg.pasteimage.min.js';
  import 'trumbowyg/dist/plugins/table/trumbowyg.table.min.js';
  import 'trumbowyg/dist/plugins/indent/trumbowyg.indent.min.js';

  import 'trumbowyg/dist/ui/trumbowyg.min.css';
  import 'trumbowyg/dist/plugins/colors/ui/trumbowyg.colors.min.css';
  import 'trumbowyg/dist/plugins/emoji/ui/trumbowyg.emoji.min.css';
  import 'trumbowyg/dist/plugins/table/ui/trumbowyg.table.min.css';

  import { onMount } from 'svelte';

  import FormGroup from './FormGroup.svelte';
  import { getRandomString } from '../../helpers/string-helpers';
  import { isDay } from '../../stores/terrariumpi';

  export let name;
  export let id = name + getRandomString(6); // Create a unique ID
  export let label = null;
  export let placeholder = label;

  export let value = null;

  export let required = null;
  export let readonly = false;
  export let help = null;
  export let invalid = null;

  export let horizontal = null;

  let wysiwyg = null;

  onMount(() => {
    jQuery(wysiwyg).trumbowyg({
      btnsDef: {
        // Create a new dropdown
        image: {
          dropdown: ['insertImage', 'base64'],
          ico: 'insertImage',
        },

        alignment: {
          dropdown: ['justifyLeft', 'justifyCenter', 'justifyRight', 'justifyFull', 'indent', 'outdent'],
          ico: 'justifyLeft',
        },
      },

      btns: [
        ['viewHTML'],
        ['undo', 'redo'], // Only supported in Blink browsers
        ['formatting'],
        ['strong', 'em', 'del'],
        ['superscript', 'subscript'],
        ['fontfamily'],
        ['foreColor', 'backColor'],
        ['link'],
        ['image'],
        ['table'],
        ['alignment'],
        ['unorderedList', 'orderedList'],
        ['removeformat'],
        ['fullscreen'],
      ],

      svgPath: 'css/icons.svg',
      imageWidthModalEdit: true,
    });
    return () => {
      jQuery(wysiwyg).trumbowyg('destroy');
    };
  });

  $: if (wysiwyg) {
    if (value && value !== '') {
      jQuery(wysiwyg).trumbowyg('html', value);
    } else {
      jQuery(wysiwyg).trumbowyg('empty');
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
  <div class:trumbowyg-dark="{!$isDay}">
    <textarea id="{id}" name="{name}" placeholder="{placeholder}" readonly="{readonly}" bind:this="{wysiwyg}"></textarea>
  </div>
</FormGroup>
