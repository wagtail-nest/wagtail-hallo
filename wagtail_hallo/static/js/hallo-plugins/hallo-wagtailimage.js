'use strict';

// original source - https://github.com/wagtail/wagtail/blob/stable/2.16.x/wagtail/images/static_src/wagtailimages/js/hallo-plugins/hallo-wagtailimage.js

(function () {
  // hallo-wagtailimage
  $.widget('IKS.hallowagtailimage', {
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
        label: 'Images',
        icon: 'icon-image',
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
          url: window.chooserUrls.imageChooser + '?select_format=true',
          onload: IMAGE_CHOOSER_MODAL_ONLOAD_HANDLERS,
          responses: {
            imageChosen: function (imageData) {
              var elem;

              elem = $(imageData.html).get(0);
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
