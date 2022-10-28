from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail.admin.panels import FieldPanel
    from wagtail.blocks import CharBlock, RichTextBlock
    from wagtail.fields import RichTextField, StreamField
    from wagtail.models import Page
else:
    from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
    from wagtail.core.blocks import CharBlock, RichTextBlock
    from wagtail.core.fields import RichTextField, StreamField
    from wagtail.core.models import Page


class HalloTestPage(Page):
    body = RichTextField(editor="hallo", blank=True)

    if WAGTAIL_VERSION >= (3, 0):
        body_stream = StreamField(
            [
                ("heading", CharBlock(form_classname="full title")),
                ("paragraph", RichTextBlock(editor="hallo")),
            ],
            use_json_field=True,
        )
    else:
        body_stream = StreamField(
            [
                ("heading", CharBlock(form_classname="full title")),
                ("paragraph", RichTextBlock(editor="hallo")),
            ]
        )

    if WAGTAIL_VERSION >= (3, 0):
        content_panels = Page.content_panels + [
            FieldPanel("body", classname="full"),
            FieldPanel("body_stream"),
        ]
    else:
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
