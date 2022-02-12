'use strict';

// original source - https://github.com/wagtail/wagtail/blob/stable/2.16.x/wagtail/embeds/static_src/wagtailembeds/js/hallo-plugins/hallo-wagtailembeds.js

(function () {
  // hallo-wagtailembeds
  $.widget('IKS.hallowagtailembeds', {
    options: {
      uuid: '',
      editable: null,
    },
    populateToolbar: function (toolbar) {
      var button;
      var widget;

      widget = this;
      button = $('<span class="' + this.widgetName + '"></span>');
      button.hallobutton({
        uuid: this.options.uuid,
        editable: this.options.editable,
        label: 'Embed',
        icon: 'icon-media',
        command: null,
      });

      toolbar.append(button);

      return button.on('click', function (event) {
        var insertionPoint;
        var lastSelection;

        lastSelection = widget.options.editable.getSelection();
        insertionPoint = $(lastSelection.endContainer)
          .parentsUntil('[data-hallo-editor]')
          .last();

        return ModalWorkflow({
          url: window.chooserUrls.embedsChooser,
          onload: global.EMBED_CHOOSER_MODAL_ONLOAD_HANDLERS,
          responses: {
            embedChosen: function (embedData) {
              var elem;

              elem = $(embedData).get(0);
              lastSelection.insertNode(elem);
              if (elem.getAttribute('contenteditable') === 'false') {
                insertRichTextDeleteControl(elem);
              }

              return widget.options.editable.element.trigger('change');
            },
          },
        });
      });
    },
  });
})();
