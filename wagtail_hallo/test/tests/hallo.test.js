describe('Hallo editor', () => {
  it('should not have hallo in the window by default', () => {
    expect(window.makeHalloRichTextEditable).toBeUndefined();
  });

  it('should add hallo to the window when imported', () => {
    // eslint-disable-next-line global-require
    window.$ = require('jquery'); // note: this is the dev dependency NOT the static file used in Wagtail
    // eslint-disable-next-line global-require
    require('../../static/js/hallo-editor.js');
    expect(window.makeHalloRichTextEditable).toBeInstanceOf(Function);
  });
});
