from bs4 import BeautifulSoup
from django.test import TestCase

from wagtail.admin.rich_text.converters.editor_html import EditorHTMLConverter


class TestDbWhitelisterMethods(TestCase):
    def setUp(self):
        self.whitelister = EditorHTMLConverter().whitelister

    def test_clean_tag_node(self):
        soup = BeautifulSoup('<a irrelevant="baz">foo</a>', "html5lib")
        tag = soup.a
        self.whitelister.clean_tag_node(soup, tag)
        self.assertEqual(str(tag), "<a>foo</a>")


class TestDbWhitelister(TestCase):
    def setUp(self):
        self.whitelister = EditorHTMLConverter().whitelister

    def assertHtmlEqual(self, str1, str2):
        """
        Assert that two HTML strings are equal at the DOM level
        (necessary because we can't guarantee the order that attributes are output in)
        """
        self.assertEqual(
            BeautifulSoup(str1, "html5lib"), BeautifulSoup(str2, "html5lib")
        )

    def test_page_link_is_rewritten(self):
        input_html = (
            '<p>Look at the <a data-linktype="page" data-id="2" href="/">lovely homepage</a>'
            ' of my <a href="http://wagtail.org/">Wagtail</a> site</p>'
        )
        output_html = self.whitelister.clean(input_html)
        expected = (
            '<p>Look at the <a linktype="page" id="2">lovely homepage</a>'
            ' of my <a href="http://wagtail.org/">Wagtail</a> site</p>'
        )
        self.assertHtmlEqual(expected, output_html)

    def test_div_conversion(self):
        # DIVs should be converted to P, and all whitelist / conversion rules still applied
        input_html = (
            '<p>before</p><div class="shiny">OMG <b>look</b> at this <blink>video</blink> of a kitten: '
            '<iframe data-embedtype="media" data-url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"'
            ' width="640" height="480"'
            ' src="//www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe></div><p>after</p>'
        )
        output_html = self.whitelister.clean(input_html)
        expected = (
            "<p>before</p><p>OMG <b>look</b> at this video of a kitten:"
            ' <embed embedtype="media" url="https://www.youtube.com/watch?v=dQw4w9WgXcQ" /></p><p>after</p>'
        )
        self.assertHtmlEqual(expected, output_html)

    def test_whitelist_with_feature_list(self):
        converter = EditorHTMLConverter(
            features=["h1", "bold", "link", "something_i_just_made_up"]
        )
        input_html = (
            "<h1>this heading is allowed</h1> <h2>but not this one</h2> "
            "<p><b>bold</b> <i>italic</i></p>"
            '<p><a href="http://torchbox.com">external link</a> <a data-linktype="page" data-id="2" href="/">internal link</a></p>'
        )
        output_html = converter.to_database_format(input_html)
        expected = (
            "<h1>this heading is allowed</h1> but not this one "
            "<p><b>bold</b> italic</p>"
            '<p><a href="http://torchbox.com">external link</a> <a linktype="page" id="2">internal link</a></p>'
        )
        self.assertHtmlEqual(expected, output_html)
