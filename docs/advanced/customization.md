# Advanced Customization

Extend Aratinga with custom blocks, models, and functionality.

## Creating Custom Blocks

### Basic Custom Block

```python
# website/blocks.py
from wagtail import blocks
from aratinga.blocks.base_blocks import BaseBlock
from wagtail.images.blocks import ImageChooserBlock

class GalleryGridBlock(BaseBlock):
    """Custom gallery block with custom styling"""

    title = blocks.CharBlock(required=False, label="Gallery Title")
    columns = blocks.ChoiceBlock(
        choices=[
            ('2', 'Two columns'),
            ('3', 'Three columns'),
            ('4', 'Four columns'),
        ],
        default='3',
        label="Number of Columns"
    )
    images = blocks.StreamBlock([
        ('image', ImageChooserBlock()),
    ])

    class Meta:
        template = 'blocks/gallery_grid_block.html'
        icon = 'image'
        label = 'Gallery Grid'
```

### Register Custom Block

```python
# website/models.py
from wagtail.fields import StreamField
from wagtail.models import Page
from .blocks import GalleryGridBlock

class HomePage(Page):
    body = StreamField([
        ('gallery_grid', GalleryGridBlock()),
        # ...other blocks...
    ])

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
```

### Create Custom Template

```django
{# themes/bootstrap5/templates/blocks/gallery_grid_block.html #}
<section class="gallery-section">
    {% if self.title %}
        <h2>{{ self.title }}</h2>
    {% endif %}

    <div class="row row-cols-{{ self.columns }} g-3">
        {% for block in self.images %}
            <div class="col">
                {% image block.value width-300 as img %}
                <img src="{{ img.url }}" alt="{{ img.title }}" class="img-fluid">
            </div>
        {% endfor %}
    </div>
</section>
```

## Extending Models

### Custom Page Type

```python
# website/models.py
from aratinga.models import AratingaWebPage
from django.db import models
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from aratinga.blocks import COMPONENT_STREAMBLOCKS

class EventPage(AratingaWebPage):
    """Custom event page with date and location"""

    event_date = models.DateField(blank=True, null=True)
    event_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    capacity = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_free = models.BooleanField(default=False)

    content_panels = AratingaWebPage.content_panels + [
        FieldPanel('event_date'),
        FieldPanel('event_time'),
        FieldPanel('location'),
        FieldPanel('address'),
        FieldPanel('capacity'),
        FieldPanel('price'),
        FieldPanel('is_free'),
    ]

    class Meta:
        verbose_name = "Event Page"
        verbose_name_plural = "Event Pages"
```

### Custom Classifier

```python
# website/models.py
from aratinga.models import AratingaPage

# In AratingaPage admin, select classifiers to tag pages
# Use in templates:
# {% if "Featured" in page.classifier_terms.all %}
#     <span class="badge">Featured</span>
# {% endif %}
```

## Template Customization

### Override Block Templates

1. Create template in your theme:
   ```
   themes/bootstrap5/templates/blocks/card_block.html
   ```

2. Override default template:
   ```django
   {# Custom card styling #}
   <div class="custom-card">
       {% if self.image %}
           {% image self.image width-400 as img %}
           <img src="{{ img.url }}" alt="">
       {% endif %}
       <h3>{{ self.title }}</h3>
       <p>{{ self.subtitle }}</p>
   </div>
   ```

### Override Page Templates

```
themes/bootstrap5/templates/pages/
├── base.html              # Page wrapper
├── web_page.html          # Web page template
├── article_page.html      # Article template
└── article_index_page.html # Article listing
```

## Template Filters & Tags

### Include Blocks

```django
{% for block in page.body %}
    {% include_block block %}
{% endfor %}
```

### Image Resizing

```django
{% load wagtailimages_tags %}
{% image page.featured_image width-800 as featured %}
    <img src="{{ featured.url }}" alt="{{ page.title }}">
{% endimage %}
```

### Querystring Filters

```django
{% load wagtailcore_tags %}
{{ page.get_children.live.order_by|truncatewords:10 }}
```

## Settings Customization

### settings/base.py

```python
# Custom block settings
ARATINGA_SETTINGS = {
    'CMS_FRONTEND_TEMPLATES_PAGES': {
        '*': [  # Global templates
            ('templates/pages/default.html', 'Default'),
        ],
        'homepage': [
            ('templates/pages/home.html', 'Home'),
        ],
        'eventpage': [
            ('templates/pages/event.html', 'Event'),
        ],
    },
    'CMS_FRONTEND_TEMPLATES_BLOCKS': {
        '*': [
            ('templates/blocks/default.html', 'Default'),
        ],
    },
}

# Classifiers
WAGTAIL_TAGGIT_MODEL = 'taggit.Tag'

# Image quality
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 20 * 1024 * 1024  # 20MB

# Pagination
DEFAULT_PAGE_SIZE = 20
```

## Signals & Hooks

### Pre/Post Save Hooks

```python
# website/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ArticlePage

@receiver(post_save, sender=ArticlePage)
def article_published(sender, instance, created, **kwargs):
    """Send notification when article is published"""
    if instance.live and not created:
        # Send notification email
        send_email(subject=f"New article: {instance.title}")
```

### Wagtail Hooks

```python
# website/wagtail_hooks.py
from wagtail import hooks

@hooks.register('before_edit_page')
def do_before_edit_page(request, page):
    """Called before page edit form renders"""
    pass

@hooks.register('after_publish_page')
def do_after_publish_page(request, page):
    """Called after page is published"""
    pass
```

## Performance Optimization

### Caching

```django
{% load cache %}

{% cache 3600 "article_list" %}
    {% for article in articles %}
        <article>{{ article.title }}</article>
    {% endfor %}
{% endcache %}
```

### Database Queries

```python
# Use select_related for foreign keys
pages = Page.objects.select_related('owner')

# Use prefetch_related for reverse FKs
pages = Page.objects.prefetch_related('body')

# Count queries in development
from django.test.utils import override_settings
with override_settings(DEBUG=True):
    from django.db import connection
    # ... your code ...
    print(f"Total queries: {len(connection.queries)}")
```

## Testing

### Unit Tests

```python
# website/tests.py
from django.test import TestCase
from wagtail.tests.utils import WagtailPageTests
from .models import ArticlePage

class ArticlePageTests(WagtailPageTests):
    def test_can_create_article(self):
        article = ArticlePage(
            title="Test Article",
            slug="test-article",
        )
        self.assertTrue(article.is_creatable)
```

### Fixtures

```python
# Create test data
from wagtail.models import Page

root = Page.get_first_root_node()
article_index = root.add_child(instance=ArticlePage(
    title="Articles",
    slug="articles",
))
```

## Deployment

### Production Settings

```python
# settings/production.py
DEBUG = False

ALLOWED_HOSTS = [
    'yourdomain.com',
    'www.yourdomain.com',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aratinga_prod',
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': 5432,
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

## Next Steps

- 🌍 [Internationalization](internationalization.md) - Multi-language support
- 🚀 [Performance](../api/index.md) - Optimization tips
- 📚 [API Reference](../api/index.md) - Complete API docs
