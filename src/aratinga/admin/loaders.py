import os
from pathlib import Path
from aratinga.admin import settings
from django.template.loaders.filesystem import Loader as BaseLoader

from .thread import get_theme


class ThemeLoader(BaseLoader):
    """
    Theme template Loader class for serving optional themes per Aratinga site.
    """
    def get_dirs(self) -> list[str | Path]:
        dirs = super(ThemeLoader, self).get_dirs()
        theme = get_theme()
        theme_path = getattr(settings, 'ARATINGA_THEME_PATH', None)

        if theme:
            if theme_path:
                # Use the theme's absolute path directly when ARATINGA_THEME_PATH is set
                return [theme.theme_path]
            else:
                # Prepend theme subdirectory inside each configured DIRS entry
                return [os.path.join(str(d), theme.theme_path) for d in dirs]

        return list(dirs)