import $ from 'jquery';
import 'bootstrap';

if (typeof $.fn.popover === 'undefined' || $.fn.popover.Constructor.VERSION.split('.').shift() !== '4') {
  throw new Error('Bootstrap Confirmation 4 requires Bootstrap Popover 4');
}

const Popover = $.fn.popover.Constructor;

export default Popover;
