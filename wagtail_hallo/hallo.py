import json

from collections import OrderedDict

from django.forms import Media, widgets
from django.utils.functional import cached_property

from wagtail.admin.edit_handlers import RichTextFieldPanel
from wagtail.admin.rich_text.converters.editor_html import EditorHTMLConverter
from wagtail.admin.staticfiles import versioned_static
from wagtail.core.rich_text import features
from wagtail.core.telepath import register
from wagtail.core.widget_adapters import WidgetAdapter

from .plugins import CORE_HALLO_PLUGINS


class HalloRichTextArea(widgets.Textarea):
    template_name = "wagtail_hallo/widgets/hallo_rich_text_area.html"

    # this class's constructor accepts a 'features' kwarg
    accepts_features = True

    def get_panel(self):
        return RichTextFieldPanel

    def __init__(self, *args, **kwargs):
        self.options = kwargs.pop("options", None)

        self.features = kwargs.pop("features", None)
        if self.features is None:
            self.features = features.get_default_features()

        self.converter = EditorHTMLConverter(self.features)

        # construct a list of plugin objects, by querying the feature registry
        # and keeping the non-null responses from get_editor_plugin
        self.plugins = CORE_HALLO_PLUGINS + list(
            filter(
                None,
                [
                    features.get_editor_plugin("hallo", feature_name)
                    for feature_name in self.features
                ],
            )
        )
        self.plugins.sort(key=lambda plugin: plugin.order)

        super().__init__(*args, **kwargs)

    def format_value(self, value):
        # Convert database rich text representation to the format required by
        # the input field
        value = super().format_value(value)

        if value is None:
            return None

        return self.converter.from_database_format(value)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        if self.options is not None and "plugins" in self.options:
            # explicit 'plugins' config passed in options, so use that
            plugin_data = self.options["plugins"]
        else:
            plugin_data = OrderedDict()
            for plugin in self.plugins:
                plugin.construct_plugins_list(plugin_data)
        context["widget"]["plugins_json"] = json.dumps(plugin_data)

        return context

    def value_from_datadict(self, data, files, name):
        original_value = super().value_from_datadict(data, files, name)
        if original_value is None:
            return None
        return self.converter.to_database_format(original_value)

    @cached_property
    def media(self):
        media = Media(
            js=[
                versioned_static("js/vendor/hallo.js"),
                versioned_static("js/hallo-editor.js"),
                versioned_static("js/hallo-telepath.js"),
            ],
            css={"all": [versioned_static("css/hallo.css")]},
        )

        for plugin in self.plugins:
            media += plugin.media

        return media


class HalloRichTextAreaAdapter(WidgetAdapter):
    js_constructor = "wagtail.widgets.HalloRichTextArea"


register(HalloRichTextAreaAdapter(), HalloRichTextArea)
