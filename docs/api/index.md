# API Reference

Complete API documentation for Aratinga CMS.

## Blocks API

### BaseBlock

Base class for all blocks in Aratinga.

```python
from aratinga.blocks.base_blocks import BaseBlock

class MyBlock(BaseBlock):
    """Custom block"""
    pass
```

**Features**:
- Consistent block structure
- Template rendering
- Translation support

### HTML Blocks

Simple, non-nested blocks for content:

```python
from aratinga.blocks.html_blocks import (
    RichTextBlock,
    ButtonBlock,
    ImageBlock,
    ImageLinkBlock,
    EmbedVideoBlock,
    QuoteBlock,
    DownloadBlock,
    EmbedGoogleMapBlock,
    PageListBlock,
    PagePreviewBlock,
    TableBlock,
)
```

### Content Blocks

Complex content patterns:

```python
from aratinga.blocks.content_blocks import (
    CardBlock,
    CarouselBlock,
    ImageGalleryBlock,
)
```

### Layout Blocks

Structural blocks:

```python
from aratinga.blocks.layout_blocks import (
    GridBlock,
    CardGridBlock,
)
```

### Section Blocks

Full-width sections:

```python
from aratinga.blocks.section_blocks import (
    HeroBlock,
    PromoBlock,
    FeaturedSectionBlock,
)
```

### Block Collections

Pre-configured block sets:

```python
from aratinga.blocks import (
    HTML_STREAMBLOCKS,      # Basic HTML elements
    CONTENT_STREAMBLOCKS,   # HTML + Content blocks
    LAYOUT_STREAMBLOCKS,    # Layout blocks
    SECTION_STREAMBLOCKS,   # Section blocks
    COMPONENT_STREAMBLOCKS, # All blocks
)
```

## Models API

### AratingaPage

Base page model.

```python
from aratinga.models import AratingaPage

# Fields
title            # CharField - Page title
slug             # SlugField - URL identifier
live             # BooleanField - Published status
first_published_at  # DateTimeField
last_published_at   # DateTimeField

# Methods
get_url()        # Get page URL
get_absolute_url()  # Absolute URL
specific()       # Get specific subclass
get_children()   # Get child pages
get_siblings()   # Get sibling pages
get_parent()     # Get parent page
```

### AratingaWebPage

General-purpose page type.

```python
from aratinga.models import AratingaWebPage

class CustomPage(AratingaWebPage):
    # Custom fields here
    pass

# Inherited fields from AratingaPage
# Plus: body (StreamField)
```

### AratingaArticlePage

Article/blog post page.

```python
from aratinga.models import AratingaArticlePage

article = AratingaArticlePage.objects.first()
article.author           # ForeignKey to User
article.author_display   # CharField - Override author name
article.featured_image   # ForeignKey to Image
article.caption          # TextField
article.body             # StreamField
```

### AratingaArticleIndexPage

Article listing and filtering.

```python
from aratinga.models import AratingaArticleIndexPage

index = AratingaArticleIndexPage.objects.first()
index.show_images        # BooleanField
index.show_meta          # BooleanField - Author/date
index.show_preview_text  # BooleanField
index.index_order_by     # CharField - Sort order
```

## QuertSet Methods

### Filtering

```python
from aratinga.models import AratingaPage

# Get live pages
pages = AratingaPage.objects.live()

# Get draft pages
pages = AratingaPage.objects.not_live()

# Filter by type
articles = AratingaArticlePage.objects.all()

# Filter by classifier
classified = AratingaPage.objects.filter(
    classifier_terms__name='Featured'
)

# Filter by tag
tagged = AratingaPage.objects.filter(
    tags__name='important'
)

# Search
results = AratingaPage.objects.live().search('keyword')
```

### Ordering

```python
# By title
pages = AratingaPage.objects.order_by('title')

# By publish date
pages = AratingaPage.objects.order_by('-first_published_at')

# By last update
pages = AratingaPage.objects.order_by('-last_published_at')

# Reverse order
pages = AratingaPage.objects.order_by('-title')
```

### Related Data

```python
# Load related data efficiently
pages = AratingaPage.objects.select_related('owner')
pages = AratingaPage.objects.prefetch_related('body')

# Combined
pages = AratingaPage.objects.select_related('owner').prefetch_related('body')
```

## Template Tags & Filters

### Load Tags

```django
{% load wagtailcore_tags %}
{% load wagtailimages_tags %}
{% load i18n %}
```

### Include Blocks

```django
{% for block in page.body %}
    {% include_block block %}
{% endfor %}
```

### Image Tags

```django
{% load wagtailimages_tags %}

{% image page.featured_image width-800 as featured %}
    <img src="{{ featured.url }}" alt="{{ page.title }}">
{% endimage %}
```

### Internationalization

```django
{% load i18n %}

{% trans "Translate this" %}
{% blocktrans %}Translate with {{variable}}{% endblocktrans %}
{% language 'es' %}Translated content{% endlanguage %}
```

## Settings

### Core Settings

```python
# settings/base.py

# Language
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
    ('pt-br', 'Português'),
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = 'media'
```

### Wagtail-Specific

```python
# Admin interface
AUTH_PASSWORD_VALIDATORS = [...]

# Image processing
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 20 * 1024 * 1024

# Search backend
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database'
    }
}
```

## Admin API

### ModelAdmin

Register custom models in admin:

```python
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import MyModel

@modeladmin_register
class MyModelAdmin(ModelAdmin):
    model = MyModel
    list_display = ('title', 'date')
    search_fields = ('title',)
```

## Signals & Hooks

### Pre/Post Save

```python
from django.db.models.signals import pre_save, post_save

@receiver(post_save, sender=AratingaPage)
def page_saved(sender, instance, created, **kwargs):
    if created:
        print(f"Created: {instance.title}")
```

### Wagtail Hooks

```python
from wagtail import hooks

@hooks.register('before_edit_page')
def before_edit(request, page):
    pass

@hooks.register('after_publish_page')
def after_publish(request, page):
    pass
```

## Common Patterns

### Get Page by URL

```python
from wagtail.models import Page

page = Page.objects.live().get(url_path='/about/')
```

### Create New Page

```python
from aratinga.models import AratingaWebPage

root = Page.get_first_root_node()
page = root.add_child(instance=AratingaWebPage(
    title='New Page',
    slug='new-page',
))
```

### Add Block Content

```python
from wagtail.blocks import StreamValue
from aratinga.blocks import RichTextBlock

page = AratingaWebPage.objects.first()
block = RichTextBlock().make_block_value('<p>Content</p>')
page.body = StreamValue(page.body.stream_block, [
    ('text', block)
])
page.save()
```

## Exceptions

### PageNotFound

```python
from wagtail.models import Page
from django.core.exceptions import Http404

try:
    page = Page.objects.live().get(slug='about')
except Page.DoesNotExist:
    raise Http404("Page not found")
```

## Internationalization API

### Getting Language

```python
from django.utils import translation

# Get current language
language = translation.get_language()

# Set language
translation.activate('pt-br')

# Deactivate language
translation.deactivate()
```

### Translating Strings

```python
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _lazy

# Eager translation
translated = _("Hello")

# Lazy translation (for models)
label = _lazy("My Label")
```

## Performance APIs

### Caching

```django
{% load cache %}

{% cache 3600 'cache_key' %}
    Cached content here
{% endcache %}
```

### Database Optimization

```python
from django.db.models import Prefetch
from wagtail.models import Page

# Efficient queries
pages = Page.objects.select_related('owner').prefetch_related('body')
```

## Additional Resources

- [Wagtail API Documentation](https://docs.wagtail.io/en/stable/reference/index.html)
- [Django API Reference](https://docs.djangoproject.com/en/stable/ref/)
- [StreamField Documentation](https://docs.wagtail.io/en/stable/reference/streamfield.html)

## Need Help?

- 📖 [Main Documentation](../index.md)
- 🧩 [Blocks Guide](../blocks/index.md)
- ⚙️ [Customization Guide](../advanced/customization.md)
- 💬 [GitHub Discussions](https://github.com/f4biosa/aratinga/discussions)
