"""
Create or customize your page models here.
"""

from aratinga.models import AratingaPage, AratingaArticlePage, AratingaArticleIndexPage, AratingaWebPage
from django.utils.translation import gettext_lazy as _


class DefaultPage(AratingaPage):
    class Meta:
        verbose_name = _("Default Page")
        ordering = ["-first_published_at"]

    template = "pages/page.html"
    search_template = "pages/page.search.html"
    search_filterable = True


class ArticlePage(AratingaArticlePage):
    """
    Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = _("Article")
        ordering = ["-first_published_at"]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["website.ArticleIndexPage"]

    template = "pages/article_page.html"
    search_template = "pages/article_page.search.html"
    search_filterable = True


class ArticleIndexPage(AratingaArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta:
        verbose_name = _("Article List Page")

    # Only allow ArticlePages beneath this page.
    subpage_types = ["website.ArticlePage"]

    template = "pages/article_index_page.html"
    search_filterable = True

    def get_index_children(self):
        return ArticlePage.objects.child_of(self).live().order_by(
            self.index_order_by or "-date_display"
        )


class WebPage(AratingaWebPage):
    """
    General use page with featureful streamfield.
    """

    class Meta:
        verbose_name = _("Web Page")

    template = "pages/web_page.html"
    search_filterable = True

    def get_context(self, request):
        context = super().get_context(request)
        last_pages = list(AratingaPage.objects.all()[:12])
        context["last_pages"] = last_pages[:6]
        context["last_pages_without_image"] = last_pages[6:]
        return context
