from wagtail.admin.panels import FieldPanel
from wagtail.blocks import CharBlock, RichTextBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page


class HalloTestPage(Page):
    body = RichTextField(editor="hallo", blank=True)

    body_stream = StreamField(
        [
            ("heading", CharBlock(form_classname="full title")),
            ("paragraph", RichTextBlock(editor="hallo")),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
        FieldPanel("body_stream"),
    ]


class RichTextFieldWithFeaturesPage(Page):
    body = RichTextField(
        editor="hallo", features=["quotation", "embed", "made-up-feature"]
    )

    content_panels = [
        FieldPanel("title", classname="full title"),
        FieldPanel("body"),
    ]
