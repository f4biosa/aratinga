from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

from .models import Theme

## Path (relative to BASE_DIR) where theme ZIPs are extracted
ARATINGA_THEME_PATH = "themes"


@register_setting(icon="view")
class ThemeSettings(BaseSiteSetting):
    theme = models.ForeignKey(
        Theme,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Active theme"),
    )

    panels = [FieldPanel("theme")]

    class Meta:
        verbose_name = _("Theme")
        verbose_name_plural = _("Themes")
