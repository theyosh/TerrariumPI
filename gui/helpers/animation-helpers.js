export const animate_footer_badge = (type, number) => {
  type = type || 'success';
  number = number || 1;

  const animation_badge = jQuery(`footer .badge.badge-${type}`);
  if (animation_badge.length === 0) {
    return;
  }

  if ('success' !== type) {
    number = animation_badge.text().trim();
    number = (number !== '' ? number : 0);
    number++;
    animation_badge.text(number);
  }

  animation_badge.stop(true);
  animation_badge.animate({
    opacity: 1,
  }, 50, function () {
    // Animation complete.
    animation_badge.animate({
      opacity: (number < 10 ? number : 10) / 10
    }, 150);
  });
};

let hourGlassTimer = null;
export const animateHourglass = () => {
  clearTimeout(hourGlassTimer);
  const icon = jQuery('i.hourglass-animation');
  if (icon.length === 0) {
    return;
  }
  const clearClasses = 'fa-hourglass-half fa-hourglass-end animate';
  icon.removeClass(clearClasses).addClass('fa-hourglass-end animate');
  hourGlassTimer = setTimeout(() => {
    icon.removeClass(clearClasses).addClass('fa-hourglass-half');
    hourGlassTimer = setTimeout(() => {
      icon.removeClass(clearClasses).addClass('fa-hourglass-end');
    }, 14 * 1000);
  }, 14 * 1000);
};