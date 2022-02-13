import unittest
from bs4 import BeautifulSoup

from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from wagtail.core.blocks import RichTextBlock
from wagtail.core.models import Page, get_page_models
from wagtail.core.rich_text import features as feature_registry

from wagtail_hallo.hallo import HalloRichTextArea
from .utils import TestUtils


class BaseRichTextEditHandlerTestCase(TestCase):
    def _clear_edit_handler_cache(self):
        """
        These tests generate new EditHandlers with different settings. The
        cached edit handlers should be cleared before and after each test run
        to ensure that no changes leak through to other tests.
        """
        from wagtail_hallo.test.models import (
            HalloTestPage,
        )

        rich_text_block = (
            HalloTestPage.get_edit_handler()
            .get_form_class()
            .base_fields["body_stream"]
            .block.child_blocks["paragraph"]
        )
        if hasattr(rich_text_block, "field"):
            del rich_text_block.field

        for page_class in get_page_models():
            page_class.get_edit_handler.cache_clear()

    def setUp(self):
        super().setUp()
        self._clear_edit_handler_cache()

    def tearDown(self):
        self._clear_edit_handler_cache()
        super().tearDown()


class TestHalloRichText(BaseRichTextEditHandlerTestCase, TestUtils):
    fixtures = ["test.json"]

    def setUp(self):
        super().setUp()

        # Find root page
        self.root_page = Page.objects.get(pk=2)

        self.login()

    def test_default_editor_in_rich_text_field(self):
        response = self.client.get(
            reverse(
                "wagtailadmin_pages:add",
                args=("wagtail_hallo_test", "hallotestpage", self.root_page.id),
            )
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Check that hallo (default editor now) initialisation is applied
        self.assertContains(response, 'makeHalloRichTextEditable("id_body",')

        # check that media for the default hallo features (but not others) is being imported
        self.assertContains(response, "js/hallo-plugins/hallo-wagtaildoclink.js")
        self.assertNotContains(response, "testapp/js/hallo-blockquote.js")


class TestHalloJsHeadingOrder(BaseRichTextEditHandlerTestCase, TestUtils):
    def test_heading_order(self):
        # Using the `register_rich_text_features` doesn't work here,
        # probably because the features have already been scanned at that point.
        # Extending the registry directly instead.
        feature_registry.default_features.extend(["h1", "h5", "h6"])

        widget = HalloRichTextArea()
        html = widget.render("the_name", "<p>the value</p>", attrs={"id": "the_id"})

        expected_options = '"halloheadings": {"formatBlocks": ["p", "h1", "h2", "h3", "h4", "h5", "h6"]}'
        self.assertIn(expected_options, html)


class TestWidgetWhitelisting(TestCase, TestUtils):
    def test_default_whitelist(self):
        widget = HalloRichTextArea()

        # when no feature list is specified, accept elements that are part of the default set
        # (which includes h2)
        result = widget.value_from_datadict(
            {
                "body": "<h2>heading</h2><script>script</script><blockquote>blockquote</blockquote>"
            },
            {},
            "body",
        )
        self.assertEqual(result, "<h2>heading</h2>scriptblockquote")

    def test_custom_whitelist(self):
        widget = HalloRichTextArea(features=["h1", "bold", "somethingijustmadeup"])
        # accept elements that are represented in the feature list
        result = widget.value_from_datadict(
            {
                "body": "<h1>h1</h1> <h2>h2</h2> <script>script</script> <p><b>bold</b> <i>italic</i></p> <blockquote>blockquote</blockquote>"
            },
            {},
            "body",
        )
        self.assertEqual(
            result, "<h1>h1</h1> h2 script <p><b>bold</b> italic</p> blockquote"
        )

    def test_link_conversion_with_default_whitelist(self):
        widget = HalloRichTextArea()

        result = widget.value_from_datadict(
            {
                "body": '<p>a <a href="/foo" data-linktype="page" data-id="123">page</a>, <a href="/foo" data-linktype="squirrel" data-id="234">a squirrel</a> and a <a href="/foo" data-linktype="document" data-id="345">document</a></p>'
            },
            {},
            "body",
        )
        self.assertHTMLEqual(
            result,
            '<p>a <a linktype="page" id="123">page</a>, a squirrel and a <a linktype="document" id="345">document</a></p>',
        )

    def test_link_conversion_with_custom_whitelist(self):
        widget = HalloRichTextArea(
            features=["h1", "bold", "link", "somethingijustmadeup"]
        )

        result = widget.value_from_datadict(
            {
                "body": '<p>a <a href="/foo" data-linktype="page" data-id="123">page</a>, <a href="/foo" data-linktype="squirrel" data-id="234">a squirrel</a> and a <a href="/foo" data-linktype="document" data-id="345">document</a></p>'
            },
            {},
            "body",
        )
        self.assertHTMLEqual(
            result,
            '<p>a <a linktype="page" id="123">page</a>, a squirrel and a document</p>',
        )

    def test_embed_conversion_with_default_whitelist(self):
        widget = HalloRichTextArea()

        result = widget.value_from_datadict(
            {
                "body": '<p>image <img src="foo" data-embedtype="image" data-id="123" data-format="left" data-alt="test alt" /> embed <span data-embedtype="media" data-url="https://www.youtube.com/watch?v=vwyuB8QKzBI">blah</span> badger <span data-embedtype="badger" data-colour="black-and-white">badger</span></p>'
            },
            {},
            "body",
        )
        self.assertHTMLEqual(
            result,
            '<p>image <embed embedtype="image" id="123" format="left" alt="test alt" /> embed <embed embedtype="media" url="https://www.youtube.com/watch?v=vwyuB8QKzBI" /> badger </p>',
        )

    def test_embed_conversion_with_custom_whitelist(self):
        widget = HalloRichTextArea(
            features=["h1", "bold", "image", "somethingijustmadeup"]
        )

        result = widget.value_from_datadict(
            {
                "body": '<p>image <img src="foo" data-embedtype="image" data-id="123" data-format="left" data-alt="test alt" /> embed <span data-embedtype="media" data-url="https://www.youtube.com/watch?v=vwyuB8QKzBI">blah</span></p>'
            },
            {},
            "body",
        )
        self.assertHTMLEqual(
            result,
            '<p>image <embed embedtype="image" id="123" format="left" alt="test alt" /> embed </p>',
        )


class TestWidgetRendering(TestCase, TestUtils):
    fixtures = ["test.json"]

    def test_default_features(self):
        widget = HalloRichTextArea()

        result = widget.render(
            "foo",
            '<p>a <a linktype="page" id="3">page</a> and a <a linktype="document" id="1">document</a></p>',
            {"id": "id_foo"},
        )
        soup = BeautifulSoup(result, "html.parser")
        result_value = soup.textarea.string

        self.assertHTMLEqual(
            result_value,
            '<p>a <a data-linktype="page" data-id="3" data-parent-id="2" href="/events/">page</a> and a <a data-linktype="document" data-id="1" href="/documents/1/test.pdf">document</a></p>',
        )

    def test_custom_features(self):
        widget = HalloRichTextArea(features=["h1", "link", "somethingijustmadeup"])

        result = widget.render(
            "foo",
            '<p>a <a linktype="page" id="3">page</a> and a <a linktype="document" id="1">document</a></p>',
            {"id": "id_foo"},
        )
        soup = BeautifulSoup(result, "html.parser")
        result_value = soup.textarea.string

        self.assertHTMLEqual(
            result_value,
            '<p>a <a data-linktype="page" data-id="3" data-parent-id="2" href="/events/">page</a> and a <a>document</a></p>',
        )


@override_settings(
    WAGTAILADMIN_RICH_TEXT_EDITORS={
        "hallo": {
            "WIDGET": "wagtail_hallo.hallo.HalloRichTextArea",
            "OPTIONS": {
                "plugins": {
                    "halloheadings": {"formatBlocks": ["p", "h2"]},
                }
            },
        },
    }
)
class TestHalloJsWithCustomPluginOptions(BaseRichTextEditHandlerTestCase, TestUtils):
    def setUp(self):
        super().setUp()

        # Find root page
        self.root_page = Page.objects.get(id=2)

        self.login()

    def test_custom_editor_in_rich_text_field(self):
        response = self.client.get(
            reverse(
                "wagtailadmin_pages:add",
                args=("wagtail_hallo_test", "hallotestpage", self.root_page.id),
            )
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Check that the custom plugin options are being passed in the hallo initialiser
        self.assertContains(
            response,
            'makeHalloRichTextEditable("id_body", {"halloheadings": {"formatBlocks": ["p", "h2"]}});',
        )

    @unittest.skip("TODO - Telepath")
    def test_custom_editor_in_rich_text_block(self):
        block = RichTextBlock(editor="custom")

        form_html = block.render_form(block.to_python("<p>hello</p>"), "body")

        # Check that the custom plugin options are being passed in the hallo initialiser
        self.assertIn(
            'makeHalloRichTextEditable("body", {"halloheadings": {"formatBlocks": ["p", "h2"]}});',
            form_html,
        )


class TestHalloJsWithFeaturesKwarg(BaseRichTextEditHandlerTestCase, TestUtils):
    def setUp(self):
        super().setUp()

        # Find root page
        self.root_page = Page.objects.get(id=2)

        self.login()

    def test_features_list_on_rich_text_field(self):
        response = self.client.get(
            reverse(
                "wagtailadmin_pages:add",
                args=(
                    "wagtail_hallo_test",
                    "richtextfieldwithfeaturespage",
                    self.root_page.id,
                ),
            )
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Check that the custom plugin options are being passed in the hallo initialiser
        self.assertContains(response, '"halloquotation":')
        self.assertContains(response, '"hallowagtailembeds":')
        self.assertNotContains(response, '"hallolists":')
        self.assertNotContains(response, '"hallowagtailimage":')

        # check that media (js/css) from the features is being imported
        self.assertContains(response, "testapp/js/hallo-quotation.js")
        self.assertContains(response, "testapp/css/hallo-quotation.css")

        # check that we're NOT importing media for the default features we're not using
        self.assertNotContains(
            response, "wagtaildocs/js/hallo-plugins/hallo-wagtaildoclink.js"
        )

    @unittest.skip("TODO - Telepath")
    def test_features_list_on_rich_text_block(self):
        block = RichTextBlock(features=["quotation", "embed", "made-up-feature"])

        form_html = block.render_form(block.to_python("<p>hello</p>"), "body")

        # Check that the custom plugin options are being passed in the hallo initialiser
        self.assertIn('"halloquotation":', form_html)
        self.assertIn('"hallowagtailembeds":', form_html)
        self.assertNotIn('"hallolists":', form_html)
        self.assertNotIn('"hallowagtailimage":', form_html)

        # check that media (js/css) from the features is being imported
        media_html = str(block.media)
        self.assertIn("testapp/js/hallo-quotation.js", media_html)
        self.assertIn("testapp/css/hallo-quotation.css", media_html)
        # check that we're NOT importing media for the default features we're not using
        self.assertNotIn(
            "wagtaildocs/js/hallo-plugins/hallo-wagtaildoclink.js", media_html
        )


@override_settings(
    WAGTAILADMIN_RICH_TEXT_EDITORS={
        "hallo": {
            "WIDGET": "wagtail_hallo.hallo.HalloRichTextArea",
            "OPTIONS": {"features": ["quotation", "image"]},
        }
    }
)
class TestHalloJsWithCustomFeatureOptions(BaseRichTextEditHandlerTestCase, TestUtils):
    def setUp(self):
        super().setUp()

        # Find root page
        self.root_page = Page.objects.get(id=2)

        self.login()

    def test_custom_features_option_on_rich_text_field(self):
        response = self.client.get(
            reverse(
                "wagtailadmin_pages:add",
                args=("wagtail_hallo_test", "hallotestpage", self.root_page.id),
            )
        )

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Check that the custom plugin options are being passed in the hallo initialiser
        self.assertContains(response, '"halloquotation":')
        self.assertContains(response, '"hallowagtailimage":')
        self.assertNotContains(response, '"hallolists":')
        self.assertNotContains(response, '"hallowagtailembeds":')

        # a 'features' list passed on the RichTextField (as we do in richtextfieldwithfeaturespage)
        # should override the list in OPTIONS
        response = self.client.get(
            reverse(
                "wagtailadmin_pages:add",
                args=(
                    "wagtail_hallo_test",
                    "richtextfieldwithfeaturespage",
                    self.root_page.id,
                ),
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"halloquotation":')
        self.assertContains(response, '"hallowagtailembeds":')
        self.assertNotContains(response, '"hallolists":')
        self.assertNotContains(response, '"hallowagtailimage":')

        # check that media (js/css) from the features is being imported
        self.assertContains(response, "testapp/js/hallo-quotation.js")
        self.assertContains(response, "testapp/css/hallo-quotation.css")

        # check that we're NOT importing media for the default features we're not using
        self.assertNotContains(
            response, "wagtaildocs/js/hallo-plugins/hallo-wagtaildoclink.js"
        )

    @unittest.skip("TODO - Telepath")
    def test_custom_features_option_on_rich_text_block(self):
        block = RichTextBlock(editor="custom")

        form_html = block.render_form(block.to_python("<p>hello</p>"), "body")

        # Check that the custom plugin options are being passed in the hallo initialiser
        self.assertIn('"halloquotation":', form_html)
        self.assertIn('"hallowagtailimage":', form_html)
        self.assertNotIn('"hallowagtailembeds":', form_html)
        self.assertNotIn('"hallolists":', form_html)

        # a 'features' list passed on the RichTextBlock
        # should override the list in OPTIONS
        block = RichTextBlock(editor="custom", features=["quotation", "embed"])

        form_html = block.render_form(block.to_python("<p>hello</p>"), "body")

        self.assertIn('"halloquotation":', form_html)
        self.assertIn('"hallowagtailembeds":', form_html)
        self.assertNotIn('"hallowagtailimage":', form_html)
        self.assertNotIn('"hallolists":', form_html)

        # check that media (js/css) from the features is being imported
        media_html = str(block.media)
        self.assertIn("testapp/js/hallo-quotation.js", media_html)
        self.assertIn("testapp/css/hallo-quotation.css", media_html)
        # check that we're NOT importing media for the default features we're not using
        self.assertNotIn(
            "wagtaildocs/js/hallo-plugins/hallo-wagtaildoclink.js", media_html
        )
