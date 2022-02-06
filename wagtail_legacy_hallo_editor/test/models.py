from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page


class HalloTestPage(Page):
    body = RichTextField(editor="legacy", blank=True)

    body_stream = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="full title")),
            ("paragraph", blocks.RichTextBlock(editor="legacy")),
        ]
    )

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
        StreamFieldPanel("body_stream"),
    ]
