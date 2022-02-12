'use strict';

// original source - https://github.com/wagtail/wagtail/blob/stable/2.16.x/client/src/entrypoints/admin/telepath/widgets.js

function _typeof(obj) {
  '@babel/helpers - typeof';

  return (
    (_typeof =
      typeof Symbol === 'function' && typeof Symbol.iterator === 'symbol'
        ? function (obj) {
            return typeof obj;
          }
        : function (obj) {
            return obj &&
              typeof Symbol === 'function' &&
              obj.constructor === Symbol &&
              obj !== Symbol.prototype
              ? 'symbol'
              : typeof obj;
          }),
    _typeof(obj)
  );
}

function _inherits(subClass, superClass) {
  if (typeof superClass !== 'function' && superClass !== null) {
    throw new TypeError('Super expression must either be null or a function');
  }
  subClass.prototype = Object.create(superClass && superClass.prototype, {
    constructor: { value: subClass, writable: true, configurable: true },
  });
  Object.defineProperty(subClass, 'prototype', { writable: false });
  if (superClass) _setPrototypeOf(subClass, superClass);
}

function _setPrototypeOf(o, p) {
  _setPrototypeOf =
    Object.setPrototypeOf ||
    function _setPrototypeOf(o, p) {
      o.__proto__ = p;
      return o;
    };
  return _setPrototypeOf(o, p);
}

function _createSuper(Derived) {
  var hasNativeReflectConstruct = _isNativeReflectConstruct();
  return function _createSuperInternal() {
    var Super = _getPrototypeOf(Derived);
    var result;
    if (hasNativeReflectConstruct) {
      var NewTarget = _getPrototypeOf(this).constructor;
      result = Reflect.construct(Super, arguments, NewTarget);
    } else {
      result = Super.apply(this, arguments);
    }
    return _possibleConstructorReturn(this, result);
  };
}

function _possibleConstructorReturn(self, call) {
  if (call && (_typeof(call) === 'object' || typeof call === 'function')) {
    return call;
  } else if (call !== void 0) {
    throw new TypeError(
      'Derived constructors may only return object or undefined',
    );
  }
  return _assertThisInitialized(self);
}

function _assertThisInitialized(self) {
  if (self === void 0) {
    throw new ReferenceError(
      "this hasn't been initialised - super() hasn't been called",
    );
  }
  return self;
}

function _isNativeReflectConstruct() {
  if (typeof Reflect === 'undefined' || !Reflect.construct) return false;
  if (Reflect.construct.sham) return false;
  if (typeof Proxy === 'function') return true;
  try {
    Boolean.prototype.valueOf.call(
      Reflect.construct(Boolean, [], function () {}),
    );
    return true;
  } catch (e) {
    return false;
  }
}

function _getPrototypeOf(o) {
  _getPrototypeOf = Object.setPrototypeOf
    ? Object.getPrototypeOf
    : function _getPrototypeOf(o) {
        return o.__proto__ || Object.getPrototypeOf(o);
      };
  return _getPrototypeOf(o);
}

function _defineProperty(obj, key, value) {
  if (key in obj) {
    Object.defineProperty(obj, key, {
      value: value,
      enumerable: true,
      configurable: true,
      writable: true,
    });
  } else {
    obj[key] = value;
  }
  return obj;
}

function _classCallCheck(instance, Constructor) {
  if (!(instance instanceof Constructor)) {
    throw new TypeError('Cannot call a class as a function');
  }
}

function _defineProperties(target, props) {
  for (var i = 0; i < props.length; i++) {
    var descriptor = props[i];
    descriptor.enumerable = descriptor.enumerable || false;
    descriptor.configurable = true;
    if ('value' in descriptor) descriptor.writable = true;
    Object.defineProperty(target, descriptor.key, descriptor);
  }
}

function _createClass(Constructor, protoProps, staticProps) {
  if (protoProps) _defineProperties(Constructor.prototype, protoProps);
  if (staticProps) _defineProperties(Constructor, staticProps);
  Object.defineProperty(Constructor, 'prototype', { writable: false });
  return Constructor;
}

var BoundWidget = /* #__PURE__ */ (function () {
  function BoundWidget(element, name, idForLabel, initialState) {
    _classCallCheck(this, BoundWidget);

    var selector = ':input[name="' + name + '"]';
    this.input = element.find(selector).addBack(selector); // find, including element itself

    this.idForLabel = idForLabel;
    this.setState(initialState);
  }

  _createClass(BoundWidget, [
    {
      key: 'getValue',
      value: function getValue() {
        return this.input.val();
      },
    },
    {
      key: 'getState',
      value: function getState() {
        return this.input.val();
      },
    },
    {
      key: 'setState',
      value: function setState(state) {
        this.input.val(state);
      },
    },
    {
      key: 'getTextLabel',
      value: function getTextLabel(opts) {
        var val = this.getValue();
        if (typeof val !== 'string') return null;
        var maxLength = opts && opts.maxLength;

        if (maxLength && val.length > maxLength) {
          return val.substring(0, maxLength - 1) + '…';
        }

        return val;
      },
    },
    {
      key: 'focus',
      value: function focus() {
        this.input.focus();
      },
    },
  ]);

  return BoundWidget;
})();

var Widget = /* #__PURE__ */ (function () {
  function Widget(html, idPattern) {
    _classCallCheck(this, Widget);

    _defineProperty(this, 'boundWidgetClass', BoundWidget);

    this.html = html;
    this.idPattern = idPattern;
  }

  _createClass(Widget, [
    {
      key: 'render',
      value: function render(placeholder, name, id, initialState) {
        var html = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);
        var idForLabel = this.idPattern.replace(/__ID__/g, id);
        var dom = $(html);
        $(placeholder).replaceWith(dom); // eslint-disable-next-line new-cap

        return new this.boundWidgetClass(dom, name, idForLabel, initialState);
      },
    },
  ]);

  return Widget;
})();

var BoundHalloRichTextArea = /* #__PURE__ */ (function (_BoundWidget) {
  _inherits(BoundHalloRichTextArea, _BoundWidget);

  var _super = _createSuper(BoundHalloRichTextArea);

  function BoundHalloRichTextArea() {
    _classCallCheck(this, BoundHalloRichTextArea);

    return _super.apply(this, arguments);
  }

  _createClass(BoundHalloRichTextArea, [
    {
      key: 'setState',
      value: function setState(state) {
        this.input.val(state);
        this.input.siblings('[data-hallo-editor]').html(state);
      },
    },
    {
      key: 'focus',
      value: function focus() {
        /* not implemented (leave blank so we don't try to focus the hidden field) */
      },
    },
  ]);

  return BoundHalloRichTextArea;
})(BoundWidget);

var HalloRichTextArea = /* #__PURE__ */ (function (_Widget) {
  _inherits(HalloRichTextArea, _Widget);

  var _super2 = _createSuper(HalloRichTextArea);

  function HalloRichTextArea() {
    var _this;

    _classCallCheck(this, HalloRichTextArea);

    for (
      var _len = arguments.length, args = new Array(_len), _key = 0;
      _key < _len;
      _key++
    ) {
      args[_key] = arguments[_key];
    }

    _this = _super2.call.apply(_super2, [this].concat(args));

    _defineProperty(
      _assertThisInitialized(_this),
      'boundWidgetClass',
      BoundHalloRichTextArea,
    );

    return _this;
  }

  return _createClass(HalloRichTextArea);
})(Widget);

window.telepath.register(
  'wagtail.widgets.HalloRichTextArea',
  HalloRichTextArea,
);
