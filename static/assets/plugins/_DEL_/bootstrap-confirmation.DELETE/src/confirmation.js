import $ from 'jquery';
import Popover from 'bootstrap/js/src/popover';

/**
 * ------------------------------------------------------------------------
 * Constants
 * ------------------------------------------------------------------------
 */

const NAME = 'confirmation';
const VERSION = '$VERSION';
const DATA_KEY = `bs.${NAME}`;
const EVENT_KEY = `.${DATA_KEY}`;
const JQUERY_NO_CONFLICT = $.fn[NAME];
const BTN_CLASS_BASE = 'h-100 d-flex align-items-center';
const BTN_CLASS_DEFAULT = 'btn btn-sm';

const DefaultType = {
  ...Popover.DefaultType,
  singleton           : 'boolean',
  popout              : 'boolean',
  copyAttributes      : '(string|array)',
  onConfirm           : 'function',
  onCancel            : 'function',
  btnOkClass          : 'string',
  btnOkLabel          : 'string',
  btnOkIconClass      : 'string',
  btnOkIconContent    : 'string',
  btnCancelClass      : 'string',
  btnCancelLabel      : 'string',
  btnCancelIconClass  : 'string',
  btnCancelIconContent: 'string',
  buttons             : 'array',
};

const Default = {
  ...Popover.Default,
  _attributes         : {},
  _selector           : null,
  placement           : 'top',
  title               : 'Are you sure?',
  trigger             : 'click',
  confirmationEvent   : undefined,
  content             : '',
  singleton           : false,
  popout              : false,
  copyAttributes      : 'href target',
  onConfirm           : $.noop,
  onCancel            : $.noop,
  btnOkClass          : `${BTN_CLASS_DEFAULT} btn-primary`,
  btnOkLabel          : 'Yes',
  btnOkIconClass      : '',
  btnOkIconContent    : '',
  btnCancelClass      : `${BTN_CLASS_DEFAULT} btn-secondary`,
  btnCancelLabel      : 'No',
  btnCancelIconClass  : '',
  btnCancelIconContent: '',
  buttons             : [],
  // @formatter:off
  template            : `
<div class="popover confirmation">
  <div class="arrow"></div>
  <h3 class="popover-header"></h3>
  <div class="popover-body">
    <p class="confirmation-content"></p>
    <div class="confirmation-buttons text-center">
      <div class="btn-group"></div>
    </div>
  </div>
</div>`,
  // @formatter:on
};

if (Default.whiteList) {
  Default.whiteList['*'].push('data-apply', 'data-dismiss');
}

const ClassName = {
  FADE: 'fade',
  SHOW: 'show',
};

const Selector = {
  TITLE  : '.popover-header',
  CONTENT: '.confirmation-content',
  BUTTONS: '.confirmation-buttons .btn-group',
};

const Keymap = {
  13: 'Enter',
  27: 'Escape',
  39: 'ArrowRight',
  40: 'ArrowDown',
};

const Event = {
  HIDE      : `hide${EVENT_KEY}`,
  HIDDEN    : `hidden${EVENT_KEY}`,
  SHOW      : `show${EVENT_KEY}`,
  SHOWN     : `shown${EVENT_KEY}`,
  INSERTED  : `inserted${EVENT_KEY}`,
  CLICK     : `click${EVENT_KEY}`,
  FOCUSIN   : `focusin${EVENT_KEY}`,
  FOCUSOUT  : `focusout${EVENT_KEY}`,
  MOUSEENTER: `mouseenter${EVENT_KEY}`,
  MOUSELEAVE: `mouseleave${EVENT_KEY}`,
  CONFIRMED : `confirmed${EVENT_KEY}`,
  CANCELED  : `canceled${EVENT_KEY}`,
  KEYUP     : `keyup${EVENT_KEY}`,
};

/**
 * ------------------------------------------------------------------------
 * Class Definition
 * ------------------------------------------------------------------------
 */

// keep track of the last openned confirmation for keyboard navigation
let activeConfirmation;

class Confirmation extends Popover {
  // Getters

  static get VERSION() {
    return VERSION;
  }

  static get Default() {
    return Default;
  }

  static get NAME() {
    return NAME;
  }

  static get DATA_KEY() {
    return DATA_KEY;
  }

  static get Event() {
    return Event;
  }

  static get EVENT_KEY() {
    return EVENT_KEY;
  }

  static get DefaultType() {
    return DefaultType;
  }

  // Constructor

  constructor(element, config) {
    super(element, config);

    if ((this.config.popout || this.config.singleton) && !this.config.rootSelector) {
      throw new Error('The rootSelector option is required to use popout and singleton features since jQuery 3.');
    }

    // keep trace of selectors
    this._isDelegate = false;

    if (config.selector) { // container of buttons
      config._selector = `${config.rootSelector} ${config.selector}`;
      this.config._selector = config._selector;
    }
    else if (config._selector) { // children of container
      this.config._selector = config._selector;
      this._isDelegate = true;
    }
    else { // standalone
      this.config._selector = config.rootSelector;
    }

    if (this.config.confirmationEvent === undefined) {
      this.config.confirmationEvent = this.config.trigger;
    }

    if (!this.config.selector) {
      this._copyAttributes();
    }

    this._setConfirmationListeners();
  }

  // Overrides

  isWithContent() {
    return true;
  }

  setContent() {
    const $tip = $(this.getTipElement());
    let content = this._getContent();

    if (typeof content === 'function') {
      content = content.call(this.element);
    }

    this.setElementContent($tip.find(Selector.TITLE), this.getTitle());

    $tip.find(Selector.CONTENT).toggle(!!content);
    if (content) {
      this.setElementContent($tip.find(Selector.CONTENT), content);
    }

    if (this.config.buttons.length > 0) {
      this._setButtons($tip, this.config.buttons);
    }
    else {
      this._setStandardButtons($tip);
    }

    $tip.removeClass(`${ClassName.FADE} ${ClassName.SHOW}`);

    this._setupKeyupEvent();
  }

  dispose() {
    $('body').off(`${Event.CLICK}.${this.uid}`);
    this.eventBody = false;
    this._cleanKeyupEvent();
    super.dispose();
  }

  hide(callback) {
    this._cleanKeyupEvent();
    super.hide(callback);
  }

  // Private

  /**
   * Copy the value of `copyAttributes` on the config object
   * @private
   */
  _copyAttributes() {
    this.config._attributes = {};
    if (this.config.copyAttributes) {
      if (typeof this.config.copyAttributes === 'string') {
        this.config.copyAttributes = this.config.copyAttributes.split(' ');
      }
    }
    else {
      this.config.copyAttributes = [];
    }

    this.config.copyAttributes.forEach((attr) => {
      this.config._attributes[attr] = $(this.element).attr(attr);
    });
  }

  /**
   * Custom event listeners for popouts and singletons
   * @private
   */
  _setConfirmationListeners() {
    const self = this;

    if (!this.config.selector) {
      // cancel original event
      $(this.element).on(this.config.trigger, (e, ack) => {
        if (!ack) {
          e.preventDefault();
          e.stopPropagation();
          e.stopImmediatePropagation();
        }
      });

      // manage singleton
      $(this.element).on(Event.SHOWN, function () {
        if (self.config.singleton) {
          // close all other popover already initialized
          $(self.config._selector).not($(this)).filter(function () {
            return $(this).data(DATA_KEY) !== undefined;
          }).confirmation('hide');
        }
      });
    }
    else {
      // cancel original event
      $(this.element).on(this.config.trigger, this.config.selector, (e, ack) => {
        if (!ack) {
          e.preventDefault();
          e.stopPropagation();
          e.stopImmediatePropagation();
        }
      });
    }

    if (!this._isDelegate) {
      // manage popout
      this.eventBody = false;
      this.uid = this.element.id || Confirmation.getUID(`${NAME}_group`);

      $(this.element).on(Event.SHOWN, () => {
        if (self.config.popout && !self.eventBody) {
          self.eventBody = $('body').on(`${Event.CLICK}.${self.uid}`, (e) => {
            if ($(self.config._selector).is(e.target) || $(self.config._selector).has(e.target).length > 0) {
              return;
            }
            // close all popover already initialized
            $(self.config._selector).filter(function () {
              return $(this).data(DATA_KEY) !== undefined;
            }).confirmation('hide');

            $('body').off(`${Event.CLICK}.${self.uid}`);
            self.eventBody = false;
          });
        }
      });
    }
  }

  /**
   * Init the standard ok/cancel buttons
   * @param $tip
   * @private
   */
  _setStandardButtons($tip) {
    const buttons = [
      {
        class      : this.config.btnOkClass,
        label      : this.config.btnOkLabel,
        iconClass  : this.config.btnOkIconClass,
        iconContent: this.config.btnOkIconContent,
        attr       : this.config._attributes,
      },
      {
        class      : this.config.btnCancelClass,
        label      : this.config.btnCancelLabel,
        iconClass  : this.config.btnCancelIconClass,
        iconContent: this.config.btnCancelIconContent,
        cancel     : true,
      },
    ];

    this._setButtons($tip, buttons);
  }

  /**
   * Init the buttons
   * @param $tip
   * @param buttons
   * @private
   */
  _setButtons($tip, buttons) {
    const self = this;
    const $group = $tip.find(Selector.BUTTONS).empty();

    buttons.forEach((button) => {
      const btn = $('<a href="#"></a>')
        .addClass(BTN_CLASS_BASE)
        .addClass(button.class || `${BTN_CLASS_DEFAULT} btn-secondary`)
        .html(button.label || '')
        .attr(button.attr || {});

      if (button.iconClass || button.iconContent) {
        btn.prepend($('<i></i>')
          .addClass(button.iconClass || '')
          .text(button.iconContent || ''));
      }

      btn.one('click', function (e) {
        if ($(this).attr('href') === '#') {
          e.preventDefault();
        }

        if (button.onClick) {
          button.onClick.call($(self.element));
        }

        if (button.cancel) {
          self.config.onCancel.call(self.element, button.value);
          $(self.element).trigger(Event.CANCELED, [button.value]);
        }
        else {
          self.config.onConfirm.call(self.element, button.value);
          $(self.element).trigger(Event.CONFIRMED, [button.value]);
          $(self.element).trigger(self.config.confirmationEvent, [true]);
        }

        self.hide();
      });

      $group.append(btn);
    });
  }

  /**
   * Install the keyboatd event handler
   * @private
   */
  _setupKeyupEvent() {
    activeConfirmation = this;
    $(window)
      .off(Event.KEYUP)
      .on(Event.KEYUP, this._onKeyup.bind(this));
  }

  /**
   * Remove the keyboard event handler
   * @private
   */
  _cleanKeyupEvent() {
    if (activeConfirmation === this) {
      activeConfirmation = undefined;
      $(window).off(Event.KEYUP);
    }
  }

  /**
   * Event handler for keyboard navigation
   * @param event
   * @private
   */
  _onKeyup(event) {
    if (!this.tip) {
      this._cleanKeyupEvent();
      return;
    }

    const $tip = $(this.getTipElement());
    const key = event.key || Keymap[event.keyCode || event.which];

    const $group = $tip.find(Selector.BUTTONS);
    const $active = $group.find('.active');
    let $next;

    switch (key) {
      case 'Escape':
        this.hide();
        break;

      case 'ArrowRight':
        if ($active.length && $active.next().length) {
          $next = $active.next();
        }
        else {
          $next = $group.children().first();
        }
        $active.removeClass('active');
        $next.addClass('active').focus();
        break;

      case 'ArrowLeft':
        if ($active.length && $active.prev().length) {
          $next = $active.prev();
        }
        else {
          $next = $group.children().last();
        }
        $active.removeClass('active');
        $next.addClass('active').focus();
        break;

      default:
        break;
    }
  }

  // Static

  /**
   * Generates an uui, copied from Bootrap's utils
   * @param {string} prefix
   * @returns {string}
   */
  static getUID(prefix) {
    let uid = prefix;
    do {
      // eslint-disable-next-line no-bitwise
      uid += ~~(Math.random() * 1000000); // "~~" acts like a faster Math.floor() here
    } while (document.getElementById(uid));
    return uid;
  }

  static _jQueryInterface(config) {
    return this.each(function () {
      let data = $(this).data(DATA_KEY);

      const _config = typeof config === 'object' ? config : {};
      _config.rootSelector = $(this).selector || _config.rootSelector; // this.selector removed in jQuery > 3

      if (!data && /destroy|hide/.test(config)) {
        return;
      }

      if (!data) {
        data = new Confirmation(this, _config);
        $(this).data(DATA_KEY, data);
      }

      if (typeof config === 'string') {
        if (typeof data[config] === 'undefined') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config]();
      }
    });
  }
}

/**
 * ------------------------------------------------------------------------
 * jQuery
 * ------------------------------------------------------------------------
 */

$.fn[NAME] = Confirmation._jQueryInterface;
$.fn[NAME].Constructor = Confirmation;
$.fn[NAME].noConflict = function () {
  $.fn[NAME] = JQUERY_NO_CONFLICT;
  return Confirmation._jQueryInterface;
};

export default Confirmation;
