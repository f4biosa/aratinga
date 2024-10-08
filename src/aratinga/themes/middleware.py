from django.core.exceptions import ImproperlyConfigured
from wagtail.models import Site

from aratinga.themes.settings import ThemeSettings
from aratinga.themes.thread import set_theme


class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        site = Site.find_for_request(request)

        if site is None:
            raise ImproperlyConfigured("Site not found!")

        theme_settings = ThemeSettings.for_site(site)
        theme = theme_settings.theme

        if theme is not None:
            set_theme(theme)

        response = self.get_response(request)
        return response