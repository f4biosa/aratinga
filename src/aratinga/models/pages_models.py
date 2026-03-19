"""
Base and abstract pages used in Aratinga.
"""

from django.conf import settings
from typing import cast

from django.db import models
from django.db.models import Field
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.fields import StreamField
from wagtail.models import Page, PageBase, PageQuerySet
from wagtail.search import index
from wagtail.utils.decorators import cached_classmethod

from aratinga.blocks import COMPONENT_STREAMBLOCKS, CONTENT_STREAMBLOCKS
from aratinga.models.snippets_models import Template
from aratinga.settings import cms_settings
from aratinga.widgets import ClassifierSelectWidget

CMS_PAGE_MODELS = []


def get_page_models():
    return CMS_PAGE_MODELS


class AratingaPageMeta(PageBase):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        if not cls._meta.abstract:  # type: ignore[union-attr]
            CMS_PAGE_MODELS.append(cls)


class AratingaTag(TaggedItemBase):
    class Meta(TaggedItemBase.Meta):
        verbose_name = _("Aratinga Tag")

    content_object = ParentalKey("aratinga.AratingaPage", related_name="tagged_items")


class AratingaPage(Page, metaclass=AratingaPageMeta):
    """
    General use page with templating functionality.
    All pages should inherit from this.
    """

    class Meta(Page.Meta):
        verbose_name = _("Aratinga Page")

    # Do not allow this page type to be created in wagtail admin
    is_creatable = False

    # Subclasses can override these fields to enable custom
    # ordering based on specific subpage fields.
    index_order_by_default = ""
    index_order_by_choices = (
        ("", _("Default Ordering")),
        ("-first_published_at", _("Date first published, newest to oldest")),
        ("first_published_at", _("Date first published, oldest to newest")),
        ("-last_published_at", _("Date updated, newest to oldest")),
        ("last_published_at", _("Date updated, oldest to newest")),
        ("title", _("Title, alphabetical")),
        ("-title", _("Title, reverse alphabetical")),
    )

    index_order_by = models.CharField(
        max_length=255,
        choices=index_order_by_choices,
        default=index_order_by_default,
        blank=True,
        verbose_name=_("Order child pages by"),
        help_text=_("Child pages will then be sorted by this attribute."),
    )

    def children(self):
        order = self.index_order_by or "-first_published_at"
        qs: PageQuerySet = self.get_children()  # type: ignore[assignment]
        return qs.specific().live().order_by(order)

    def get_index_children(self):
        """
        Returns the live child pages to be shown in index/list views,
        ordered by ``index_order_by``.  Override in subclasses to filter
        or annotate the queryset (e.g. to a specific page type).
        """
        return self.children()

    ###############
    # Layout fields
    ###############

    custom_template = models.CharField(
        blank=True, max_length=255, choices=None, verbose_name=_("Template")
    )

    ###############
    # Classify
    ###############

    classifier_terms = ParentalManyToManyField(
        "aratinga.ClassifierTerm",
        blank=True,
        verbose_name=_("Classifiers"),
        help_text=_(
            "Categorize and group pages together with classifiers. "
            "Used to organize and filter pages across the site."
        ),
    )
    tags = ClusterTaggableManager(
        through=AratingaTag,
        blank=True,
        verbose_name=_("Tags"),
        help_text=_("Used to organize pages across the site."),
    )

    ###############
    # Panels
    ###############

    classify_panels = [
        FieldPanel("classifier_terms", widget=ClassifierSelectWidget()),
        FieldPanel("tags"),
    ]

    def __init__(self, *args, **kwargs):
        """
        Inject custom choices and defaults into the form fields
        to enable customization by subclasses.
        """
        super().__init__(*args, **kwargs)
        klassname = self.__class__.__name__.lower()

        cast(Field, self._meta.get_field("index_order_by")).choices = self.index_order_by_choices
        if not self.pk:
            self.index_order_by = self.index_order_by_default

    @cached_classmethod
    def get_edit_handler(cls):
        """
        Override to "lazy load" the panels overridden by subclasses.
        """
        panels = [
            ObjectList(
                cls.content_panels,
                heading=_("Content"),
            ),
            ObjectList(cls.classify_panels, heading=_("Classify")),
            ObjectList(cls.promote_panels, heading=_("Promote")),
        ]

        edit_handler = TabbedInterface(panels)
        return edit_handler.bind_to_model(cls)


###############################################################################
# Abstract pages providing pre-built common website functionality, suitable for subclassing.
# These are abstract so subclasses can override fields if desired.
###############################################################################


class AratingaWebPage(AratingaPage):
    """
    Provides a body and body-related functionality.
    This is abstract so that subclasses can override the body StreamField.
    """

    class Meta(AratingaPage.Meta):
        verbose_name = _("Aratinga Web Page")
        abstract = True

    template = "pages/web_page.html"

    # Child pages should override based on what blocks they want in the body.
    # Default is LAYOUT_STREAMBLOCKS which is the fullest editor experience.
    body = StreamField(
        COMPONENT_STREAMBLOCKS,
        verbose_name=_("Body"),
        null=True,
        blank=True,
        use_json_field=True,

    )

    # Search fields
    search_fields = AratingaPage.search_fields + [index.SearchField("body")]

    # Panels
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    @property
    def body_preview(self):
        """
        A shortened version of the body without HTML tags.
        """
        # add spaces between tags for legibility
        body = str(self.body).replace(">", "> ")
        # strip tags
        body = strip_tags(body)
        # truncate and add ellipses
        preview = body[:200] + "..." if len(body) > 200 else body
        return mark_safe(preview)


class AratingaArticlePage(AratingaPage):
    """
    Article, suitable for news or blog content.
    """

    class Meta(AratingaPage.Meta):
        verbose_name = _("Aratinga Article")
        abstract = True

    template = "pages/article_page.html"
    search_template = "pages/article_page.search.html"

    related_show_default = True

    caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Caption"),
    )

    # Override body to provide simpler content
    body = StreamField(
        CONTENT_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Author"),
    )
    author_display = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Display author as"),
        help_text=_("Override how the author’s name displays on this article."),
    )
    date_display = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Display publish date"),
    )

    search_fields = AratingaPage.search_fields + [
        index.SearchField("body"),
        index.SearchField("caption", boost=2),
        index.FilterField("author"),
        index.FilterField("author_display"),
        index.FilterField("date_display"),
    ]

    content_panels = [
        FieldPanel("title"),
        FieldPanel("caption"),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("author"),
                FieldPanel("author_display"),
                FieldPanel("date_display"),
            ],
            _("Publication Info"),
        ),
    ]


class AratingaArticleIndexPage(AratingaPage):
    """
    Shows a list of article sub-pages.
    """

    class Meta(AratingaPage.Meta):
        verbose_name = _("Aratinga Article Index Page")
        abstract = True

    template = "pages/article_index_page.html"

    index_show_subpages_default = True

    index_order_by_default = "-last_published_at"
    index_order_by_choices = (
        ("-last_published_at", _("Date first published, newest to oldest")),
    ) + AratingaWebPage.index_order_by_choices

    show_images = models.BooleanField(
        default=True,
        verbose_name=_("Show images"),
    )
    show_captions = models.BooleanField(
        default=True,
    )
    show_meta = models.BooleanField(
        default=True,
        verbose_name=_("Show author and date info"),
    )
    show_preview_text = models.BooleanField(
        default=True,
        verbose_name=_("Show preview text"),
    )


class TemplatePage(AratingaPage):
    """
    Page whose body is rendered from a stored Template snippet.
    Inherits classifiers, tags, and custom template selection from AratingaPage.
    """

    snippet_template = models.ForeignKey(
        Template,
        on_delete=models.SET_NULL,
        related_name="pages",
        null=True,
        blank=True,
        verbose_name=_("Template snippet"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("snippet_template"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["page_title"] = self.title
        if self.snippet_template:
            context["custom_content"] = self.snippet_template.render(context)
        return context

    class Meta(AratingaPage.Meta):
        verbose_name = _("Template Page")
        verbose_name_plural = _("Template Pages")
