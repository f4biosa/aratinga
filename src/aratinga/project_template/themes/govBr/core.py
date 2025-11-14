from django.conf import settings

GOVBRDS_DEFAULTS = {}

def get_govbrds_setting(name, default=None):
    """
    Read a setting.

    Lookup order is:

    1. Django settings
    2. `django-govbrds` defaults
    3. Given default value
    """
    govbrds_settings = getattr(settings, "GOVBRDS", {})
    return govbrds_settings.get(name, GOVBRDS_DEFAULTS.get(name, default))