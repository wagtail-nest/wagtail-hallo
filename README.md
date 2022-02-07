# Wagtail Hallo - Rich Text Editor

This is the legacy rich text editor for the Wagtail CMS. Based on [Hallo.js](http://hallojs.org/).

**As of [Wagtail 2.0, the hallo.js editor is deprecated](https://docs.wagtail.org/en/stable/releases/2.0.html#new-rich-text-editor).**

**Status** This package should be compatible with Wagtail 2.17 and earlier versions, however, it will no longer receive bug fixes or be actively maintained. Pull requests will be accepted and if maintainers wish to support this outside of the Core Wagtail team please raise an Issue to discuss this.

## Major risks of using this package

- Please be aware of the [known hallo.js issues](https://github.com/wagtail/wagtail/issues?q=is%3Aissue+hallo+is%3Aclosed+label%3A%22status%3AWon%27t+Fix%22) should you want to keep using it.
- Hallo’s has inappropriate handling of HTML and editor input – it is not reliable, has browser-specific inconsistent behavior, is not a good user experience and is not accessible.
- This package is a source of security concerns (XSS injections, not CSP compatible) and allows injection of undesirable content or formatting (e.g. images in headings, or headings in lists).
- There is no guarantee that this package will be compatible with Wagtail beyond the supported versions listed above.

## Installing the Hallo Editor

- Important: Requires jQuery and jQueryUI - which are not included and may not always be included with Wagtail.
- `pip install wagtail-hallo`
- Add `'wagtail_hallo'` to your settings.py `INSTALLED_APPS`
- **INSTRUCTIONS NEEDED FOR PACKAGE HERE**

To use hallo.js on Wagtail 2.x, add the following to your settings:

```python
WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'hallo': {
        'WIDGET': 'wagtail_hallo.hallo.HalloRichTextArea'
    }
}
```

## Using the Hallo Editor in `RichTextField`

```python
# models.py
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

class MyHalloPage(Page):
    body = RichTextField(editor='hallo')

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
    ]
```

<!-- prettier-ignore-start -->
```html
{% extends "base.html" %}
{% load wagtailcore_tags wagtailimages_tags %}

{% block content %}
    {% include "base/include/header.html" %}
    <div class="container">
        <div class="row">
            <div class="col-md-7">{{ page.body|richtext }}</div>
        </div>
    </div>
{% endblock content %}
```
<!-- prettier-ignore-end -->

## Using the Hallo Editor in `StreamField` via `RichTextBlock`

```python
# models.py
from wagtail.core.models import Page
from wagtail.core.blocks import CharBlock, RichTextBlock
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField

class MyOtherHalloPage(Page):
    body = StreamField([
        ('heading', CharBlock(form_classname="full title")),
        ('paragraph', RichTextBlock(editor='hallo')),
    ], blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
```

<!-- prettier-ignore-start -->
```html
{% extends "base.html" %}
{% load wagtailcore_tags wagtailimages_tags %}

{% block content %}
    {% include "base/include/header.html" %}
    <div class="container">
        <div class="row">
            <div class="col-md-7">{{ page.body }}</div>
        </div>
    </div>
{% endblock content %}
```
<!-- prettier-ignore-end -->

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

## Development instructions

- Check out this repo locally `git clone git@github.com:wagtail/wagtail-hallo.git`

### TEMPORARY INSTRUCTIONS

- While this package is in development, use these instructions instead.
- You will need to clone the repo into a folder accessible via your virtual env `git clone git@github.com:lb-/wagtail-hallo.git`
- Your local Wagtail repo that is used for development must be checked out at `https://github.com/lb-/wagtail/tree/feature/hallo-editor-removal`
- **Important**: Delete the built static assets at `wagtail/admin/static` and then run the Wagtail build pipeline `nvm use` then `npm run build` - this is required so that validation can be done without the styles/JS provided by Wagtail and only the ones provided by the new package.

### Python (Django / Wagtail)

- `pip3 install -e ../path/to/wagtail-hallo/` -> this installs the package locally as [editable](https://pip.pypa.io/en/stable/cli/pip_install/#editable-installs)
- Ensure `'wagtail_hallo'` is added to your settings.py `INSTALLED_APPS`
- You will need to have a test application (e.g. Bakery Demo) and have a Page model to work with, along with a template.
  - see `test/testapp/models.py` for a reference model
  - see `test/testapp/templates/hallo_test_page.html` for a reference template
- After creating the model, remember to run `python manage.py makemigrations` and `python manage.py migrate`
- Run tests `python testmanage.py test` **WIP - not functional as yet**
- Run linting `flake8 wagtail_hallo`
- Run formatting `black wagtail_hallo`

### JavaScript & CSS (Frontend)

Currently the frontend tooling is based on Node & NPM and is only used to format and check code, this repository intentionally does not use any build tools and as such JavaScript and CSS must be written without that requirement.

- `nvm use` - Ensures you are on the right node version
- `npm install --no-save` - Install NPM packages
- `npm run fix` - Parses through JS/CSS files to fix anything it can
- `npm run lint` - Runs linting
- `npm run format` - Runs Prettier formatting on most files (non-Python)
- `npm test` - Runs tests (Jest)
- `npm run preflight` - Runs all the linting/formatting/jest checks and must be done before committing code

### Release checklist

- [ ] Update `tox.ini` & `setup.py` with new supported Wagtail, Python or Django versions
- [ ] Update changelog
