from django.test import SimpleTestCase

from wagtail_hallo.plugins import HalloPlugin


class TestHalloPlugin(SimpleTestCase):
    def test_versioned_static_media(self):
        plugin = HalloPlugin(
            js=["wagtailadmin/js/vendor/hallo.js"],
            css={
                "all": ["wagtailadmin/css/panels/hallo.css"],
            },
        )
        media_html = str(plugin.media)
        self.assertRegex(media_html, r"hallo.js\?v=(\w+)")
        self.assertRegex(media_html, r"hallo.css\?v=(\w+)")
