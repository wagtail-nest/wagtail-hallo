# Wagtail Legacy Hallo Editor

The legacy rich text editor for the Wagtail CMS. Based on [Hallo.js](http://hallojs.org/).

**As of [Wagtail 2.0, the hallo.js editor is deprecated](https://docs.wagtail.io/en/stable/releases/2.0.html).** it will no longer receive bug fixes.

Please be aware of the `known hallo.js issues <https://github.com/wagtail/wagtail/issues?q=is%3Aissue+is%3Aclosed+hallo+label%3A%22component%3ARich+text%22+label%3Atype%3ABug+label%3A%22status%3AWont+Fix%22>`\_ should you want to keep using it.

## Installing the Hallo Editor

- Important: Requires jQuery and jQueryUI - which are not included and may not always be included with Wagtail.
- **INSTRUCTIONS NEEDED FOR PACKAGE HERE**

## Using the Hallo Editor

To use hallo.js on Wagtail 2.x, add the following to your settings:

```python
    WAGTAILADMIN_RICH_TEXT_EDITORS = {
        'legacy': {
            'WIDGET': 'wagtail.admin.rich_text.HalloRichTextArea'
        }
    }
```

```python
# models.py
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

class HalloPage(Page):
    body = RichTextField(editor='legacy')

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
    ]
```

## Extending the Hallo Editor

The legacy hallo.js editor’s functionality can be extended through plugins. For information on developing custom `hallo.js` plugins, see the project's page: https://github.com/bergie/hallo

Once the plugin has been created, it should be registered through the feature registry's `register_editor_plugin(editor, feature_name, plugin)` method. For a `hallo.js` plugin, the `editor` parameter should always be `'hallo'`.

A plugin `halloblockquote`, implemented in `myapp/js/hallo-blockquote.js`, that adds support for the `<blockquote>` tag, would be registered under the feature name `block-quote` as follows:

```python
    from wagtail.admin.rich_text import HalloPlugin
    from wagtail.core import hooks

    @hooks.register('register_rich_text_features')
    def register_embed_feature(features):
        features.register_editor_plugin(
            'hallo', 'block-quote',
            HalloPlugin(
                name='halloblockquote',
                js=['myapp/js/hallo-blockquote.js'],
            )
        )
```

The constructor for `HalloPlugin` accepts the following keyword arguments:

- `name` - the plugin name as defined in the JavaScript code. `hallo.js` plugin names are prefixed with the `"IKS."` namespace, but the name passed here should be without the prefix.
- `options` - a dictionary (or other JSON-serialisable object) of options to be passed to the JavaScript plugin code on initialisation
- `js` - a list of JavaScript files to be imported for this plugin, defined in the same way as a [Django form media](django:topics/forms/media) definition
- `css` - a dictionary of CSS files to be imported for this plugin, defined in the same way as a [Django form media](django:topics/forms/media) definition
- `order` - an index number (default 100) specifying the order in which plugins should be listed, which in turn determines the order buttons will appear in the toolbar

When writing the front-end code for the plugin, Wagtail’s Hallo implementation offers two extension points:

- In JavaScript, use the `[data-hallo-editor]` attribute selector to target the editor, eg. `var editor = document.querySelector('[data-hallo-editor]');`.
- In CSS, use the `.halloeditor` class selector.

## Whitelisting rich text elements

After extending the editor to support a new HTML element, you'll need to add it to the whitelist of permitted elements - Wagtail's standard behaviour is to strip out unrecognised elements, to prevent editors from inserting styles and scripts (either deliberately, or inadvertently through copy-and-paste) that the developer didn't account for.

Elements can be added to the whitelist through the feature registry's `register_converter_rule(converter, feature_name, ruleset)` method. When the `hallo.js` editor is in use, the `converter` parameter should always be `'editorhtml'`.

The following code will add the `<blockquote>` element to the whitelist whenever the `block-quote` feature is active:

```python

    from wagtail.admin.rich_text.converters.editor_html import WhitelistRule
    from wagtail.core.whitelist import allow_without_attributes

    @hooks.register('register_rich_text_features')
    def register_blockquote_feature(features):
        features.register_converter_rule('editorhtml', 'block-quote', [
            WhitelistRule('blockquote', allow_without_attributes),
        ])
```

`WhitelistRule` is passed the element name, and a callable which will perform some kind of manipulation of the element whenever it is encountered. This callable receives the element as a [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) Tag object.

The `wagtail.core.whitelist` module provides a few helper functions to assist in defining these handlers: `allow_without_attributes`, a handler which preserves the element but strips out all of its attributes, and `attribute_rule` which accepts a dict specifying how to handle each attribute, and returns a handler function. This dict will map attribute names to either True (indicating that the attribute should be kept), False (indicating that it should be dropped), or a callable (which takes the initial attribute value and returns either a final value for the attribute, or None to drop the attribute).

## Developing Instructions

- Check out this repo locally.

## Python / Django

-

### Frontend

Currently the frontend tooling is based on Node & NPM and is only used to format and check code, this repository intentionally does not use any build tools and as such JavaScript and CSS must be written without that requirement.

- `nvm use` - Ensures you are on the right node version
- `npm install --no-save` - Install NPM packages
- `npm run fix` - Parses through JS/CSS files to fix anything it can
- `npm run lint` - Runs linting
- `npm run format` - Runs Prettier formatting on most files (non-Python)
- `npm run preflight` - Runs all the linting/formatting checks and must be done before committing code
