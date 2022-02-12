from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.blocks import CharBlock, RichTextBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page


class HalloTestPage(Page):
    body = RichTextField(editor="hallo", blank=True)

    body_stream = StreamField(
        [
            ("heading", CharBlock(form_classname="full title")),
            ("paragraph", RichTextBlock(editor="hallo")),
        ]
    )

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
        StreamFieldPanel("body_stream"),
    ]


class RichTextFieldWithFeaturesPage(Page):
    body = RichTextField(
        editor="hallo", features=["quotation", "embed", "made-up-feature"]
    )

    content_panels = [
        FieldPanel("title", classname="full title"),
        FieldPanel("body"),
    ]
