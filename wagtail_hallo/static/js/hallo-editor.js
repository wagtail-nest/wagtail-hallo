'use strict';

// original source - https://github.com/wagtail/wagtail/blob/stable/2.16.x/client/src/entrypoints/admin/hallo-bootstrap.js

(function () {
  window.halloPlugins = {};

  function registerHalloPlugin(name, opts) {
    /* Obsolete - used on Wagtail <1.12 to register plugins for the hallo.js editor.
    Defined here so that third-party plugins can continue to call it to provide Wagtail <1.12
    compatibility, without throwing an error on later versions. */
  }

  window.registerHalloPlugin = registerHalloPlugin;

  function setupLinkTooltips(elem) {
    elem.tooltip({
      animation: false,
      title: function title() {
        return $(this).attr('href');
      },
      trigger: 'hover',
      placement: 'bottom',
      selector: 'a',
    });
  }

  window.setupLinkTooltips = setupLinkTooltips;

  function makeHalloRichTextEditable(id, plugins) {
    var removeStylingPending = false;
    var input = $('#' + id);
    var editor = $('<div class="halloeditor" data-hallo-editor></div>').html(
      input.val(),
    );
    var closestObj = input.closest('.object');

    editor.insertBefore(input);
    input.hide();

    function removeStyling() {
      /* Strip the 'style' attribute from spans that have no other attributes.
      (we don't remove the span entirely as that messes with the cursor position,
      and spans will be removed anyway by our whitelisting)
      */
      $('span[style]', editor)
        .filter(function () {
          return this.attributes.length === 1;
        })
        .removeAttr('style');
      removeStylingPending = false;
    }
    /* Workaround for faulty change-detection in hallo */

    function setModified() {
      var hallo = editor.data('IKS-hallo');

      if (hallo) {
        hallo.setModified();
      }
    }

    editor
      .hallo({
        toolbar: 'halloToolbarFixed',
        toolbarCssClass: closestObj.hasClass('full') ? 'full' : '',

        /* use the passed-in plugins arg */
        plugins: plugins,
      })
      .on('hallomodified', function (event, data) {
        input.val(data.content);

        if (!removeStylingPending) {
          setTimeout(removeStyling, 100);
          removeStylingPending = true;
        }
      })
      .on('paste drop', function () {
        setTimeout(function () {
          removeStyling();
          setModified();
        }, 1);
        /* Animate the fields open when you click into them. */
      })
      .on('halloactivated', function (event) {
        $(event.target).addClass('expanded', 200, function () {
          /* Hallo's toolbar will reposition itself on the scroll event.
        This is useful since animating the fields can cause it to be
        positioned badly initially. */
          $(window).trigger('scroll');
        });
      })
      .on('hallodeactivated', function (event) {
        $(event.target).removeClass('expanded', 200, function () {
          $(window).trigger('scroll');
        });
      });
    setupLinkTooltips(editor);
  }

  window.makeHalloRichTextEditable = makeHalloRichTextEditable;

  function insertRichTextDeleteControl(elem) {
    var anchor = $(
      '<a class="icon icon-cross text-replace halloembed__delete">Delete</a>',
    );
    $(elem).addClass('halloembed').prepend(anchor);
    anchor.on('click', function () {
      var widget = $(elem).parent('[data-hallo-editor]').data('IKS-hallo');
      $(elem).fadeOut(function () {
        $(elem).remove();

        if (widget !== undefined && widget.options.editable) {
          widget.element.trigger('change');
        }
      });
    });
  }

  window.insertRichTextDeleteControl = insertRichTextDeleteControl;
  $(function () {
    $('[data-hallo-editor] [contenteditable="false"]').each(function () {
      insertRichTextDeleteControl(this);
    });
  });
})();
