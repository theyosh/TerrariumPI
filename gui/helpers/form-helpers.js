// https://stackoverflow.com/a/2553032 (Slightly adjusted to support multiple select field names and values, and number/float values)
export const formToJSON = (form) => {
  let rv, obj, elements, element, index, names, nameIndex, value;

  rv = {};
  elements = form.elements;
  for (index = 0; index < elements.length; ++index) {
    element = elements[index];
    if (element.disabled) {
      continue;
    }
    let name = element.name.replace(/\[\]/gm, '');
    if (name) {
      if (element.multiple && element.multiple === true) {
        value = [];
        for (let item of element.selectedOptions) {
          value.push(item.value);
        }
      } else if (element.type === 'checkbox') {
        value = element.checked && element.value ? (!isNaN(parseFloat(element.value)) ? parseFloat(element.value) : element.value) : element.checked;
      } else if (element.type === 'number') {
        value = !isNaN(parseFloat(element.value)) ? parseFloat(element.value) : 0;
      } else if (element.value !== '' && (element.value[0] === '+' || element.value[0] === '-')) {
        value = element.value
      } else {
        value = element.value !== '' && !element.value.startsWith('0x') && !isNaN(parseFloat(element.value)) ? parseFloat(element.value) : element.value;
      }

      if (value === 'true') {
        value = true;
      } else if (value === 'false') {
        value = false;
      }
      names = name.split('.');
      obj = rv;
      for (nameIndex = 0; nameIndex < names.length; ++nameIndex) {
        name = names[nameIndex];
        if (nameIndex === names.length - 1) {
          obj[name] = value;
        } else {
          obj = obj[name] = obj[name] || (!isNaN(names[nameIndex + 1]) ? [] : {});
        }
      }
    }
  }
  return rv;
};

export const invalid_form_fields = (form) => {
  let fields = [];
  form.querySelectorAll(':invalid').forEach((item) => {
    fields.push(form.querySelector('label[for="' + item.id + '"]').textContent.replace(/\*/gm, ''));
  });
  return fields;
};