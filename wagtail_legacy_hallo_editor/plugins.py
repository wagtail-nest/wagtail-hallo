from django.forms import Media

from wagtail.admin.staticfiles import versioned_static


class HalloPlugin:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", None)
        self.options = kwargs.get("options", {})
        self.js = kwargs.get("js", [])
        self.css = kwargs.get("css", {})
        self.order = kwargs.get("order", 100)

    def construct_plugins_list(self, plugins):
        if self.name is not None:
            plugins[self.name] = self.options

    @property
    def media(self):
        js = [versioned_static(js_file) for js_file in self.js]
        css = {}
        for media_type, css_files in self.css.items():
            css[media_type] = [versioned_static(css_file) for css_file in css_files]

        return Media(js=js, css=css)


class HalloFormatPlugin(HalloPlugin):
    def __init__(self, **kwargs):
        kwargs.setdefault("name", "halloformat")
        kwargs.setdefault("order", 10)
        self.format_name = kwargs["format_name"]
        super().__init__(**kwargs)

    def construct_plugins_list(self, plugins):
        plugins.setdefault(
            self.name,
            {
                "formattings": {
                    "bold": False,
                    "italic": False,
                    "strikeThrough": False,
                    "underline": False,
                }
            },
        )
        plugins[self.name]["formattings"][self.format_name] = True


class HalloHeadingPlugin(HalloPlugin):
    default_order = 20

    def __init__(self, **kwargs):
        kwargs.setdefault("name", "halloheadings")
        kwargs.setdefault("order", self.default_order)
        self.element = kwargs.pop("element")
        super().__init__(**kwargs)

    def construct_plugins_list(self, plugins):
        plugins.setdefault(self.name, {"formatBlocks": []})
        plugins[self.name]["formatBlocks"].append(self.element)


class HalloListPlugin(HalloPlugin):
    def __init__(self, **kwargs):
        kwargs.setdefault("name", "hallolists")
        kwargs.setdefault("order", 40)
        self.list_type = kwargs["list_type"]
        super().__init__(**kwargs)

    def construct_plugins_list(self, plugins):
        plugins.setdefault(self.name, {"lists": {"ordered": False, "unordered": False}})
        plugins[self.name]["lists"][self.list_type] = True


class HalloRequireParagraphsPlugin(HalloPlugin):
    @property
    def media(self):
        return (
            Media(
                js=[
                    versioned_static("js/hallo-plugins/hallo-requireparagraphs.js"),
                ]
            )
            + super().media
        )


# Plugins which are always imported, and cannot be enabled/disabled via 'features'
CORE_HALLO_PLUGINS = [
    HalloPlugin(name="halloreundo", order=50),
    HalloRequireParagraphsPlugin(name="hallorequireparagraphs"),
    HalloHeadingPlugin(element="p"),
]
