# Re-export the CMS search view so this app's URL conf stays independent
# while benefiting from all CMS features (pagination from SiteSettings,
# page-type filtering, MySQL backend workaround, etc.)
from aratinga.views import search  # noqa: F401
