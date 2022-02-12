from wagtail.core import hooks
from wagtail_hallo.plugins import HalloPlugin


# register 'quotation' as a rich text feature supported by a hallo.js plugin
@hooks.register("register_rich_text_features")
def register_quotation_feature(features):
    features.register_editor_plugin(
        "hallo",
        "quotation",
        HalloPlugin(
            name="halloquotation",
            js=["testapp/js/hallo-quotation.js"],
            css={"all": ["testapp/css/hallo-quotation.css"]},
        ),
    )
