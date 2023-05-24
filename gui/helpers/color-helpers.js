export const get_template_color = (classname, transparency, hexformat) => {
  const hex = d => Number(d).toString(16).padStart(2, '0');

  const span = jQuery('<span>').addClass('d-none').addClass(classname).text('test').appendTo(jQuery('body')); // Need to append to body to make the color rendering work. Else we do not have a color
  let color = span.css('color') || span.css('backgroundColor');
  // Remove the span now we have the color
  span.remove();

  if (transparency) {
    color = color.replace(/rgb\(/gm, 'rgba(');
    color = color.replace(/\)/gm, ',' + transparency + ')');
  }

  if (hexformat) {
    const regex = /rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)/gm;
    color = regex.exec(color);
    color = '#' + hex(color[1]) + hex(color[2]) + hex(color[3]);
  }
  return color;
};

export const autoDarkmode = (isDark) => {
  const body = document.querySelector('body');
  if (isDark && !body.classList.contains('dark-mode')) {
    body.classList.add('dark-mode');
  } else if (!isDark && body.classList.contains('dark-mode')) {
    body.classList.remove('dark-mode');
  }
};