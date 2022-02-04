from django.urls import path, include
from django.views.i18n import JavaScriptCatalog

from wagtail.core import hooks


@hooks.register("register_admin_urls")
def register_admin_urls():
    urls = [
        path('jsi18n/', JavaScriptCatalog.as_view(packages=['wagtail_legacy_hallo_editor']), name='javascript_catalog'),

        # Add your other URLs here, and they will appear under `/admin/legacy_hallo_editor/`
        # Note: you do not need to check for authentication in views added here, Wagtail does this for you!
    ]

    return [
        path(
            "legacy_hallo_editor/",
            include(
                (urls, "wagtail_legacy_hallo_editor"),
                namespace="wagtail_legacy_hallo_editor",
            ),
        )
    ]
