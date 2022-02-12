'use strict';

// original source - https://github.com/wagtail/wagtail/blob/stable/2.16.x/client/src/entrypoints/admin/hallo-plugins/hallo-requireparagraphs.js

(function () {
  // hallo-requireparagraphs

  $.widget('IKS.hallorequireparagraphs', {
    options: {
      editable: null,
      uuid: '',
      blockElements: [
        'dd',
        'div',
        'dl',
        'figure',
        'form',
        'ul',
        'ol',
        'table',
        'p',
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',
      ],
    },
    cleanupContentClone(el) {
      // if the editable element contains no block-level elements wrap the contents in a <P>
      if (
        el.html().length &&
        !$(this.options.blockElements.toString(), el).length
      ) {
        this.options.editable.execute('formatBlock', 'p');
      }
    },
  });
})();
