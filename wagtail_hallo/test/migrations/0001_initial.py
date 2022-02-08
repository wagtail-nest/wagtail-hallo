from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0062_comment_models_and_pagesubscription"),
    ]

    operations = [
        migrations.CreateModel(
            name="HalloTestPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("body", wagtail.core.fields.RichTextField(blank=True)),
                (
                    "body_stream",
                    wagtail.core.fields.StreamField(
                        [
                            (
                                "heading",
                                wagtail.core.blocks.CharBlock(
                                    form_classname="full title"
                                ),
                            ),
                            (
                                "paragraph",
                                wagtail.core.blocks.RichTextBlock(editor="hallo"),
                            ),
                        ]
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
