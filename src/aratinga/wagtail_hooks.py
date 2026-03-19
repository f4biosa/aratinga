from django.utils.html import format_html
from django.templatetags.static import static
from wagtail import hooks


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("wagtail/theme.css"))


@hooks.register("branding_logo")
def branding_logo(request):
    return format_html(
        '<img src="{}" alt="Aratinga CMS" style="width:auto;height:40px;">',
        static("images/aratinga.svg"),
    )


@hooks.register("branding_favicon")
def branding_favicon(request):
    return format_html('<link rel="shortcut icon" href="{}">', static("images/favicon.ico"))
