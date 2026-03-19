# Page Models

Aratinga provides pre-built page models for common website needs. Customize or extend them for your project.

## Base Model: AratingaPage

All pages inherit from `AratingaPage`, providing:

### Core Fields

- **Title** - Page name (required)
- **Slug** - URL-friendly identifier (required, auto-generated)
- **Status** - Draft or Published
- **Publish date** - Scheduled publishing
- **SEO Fields**:
  - Meta title
  - Meta description
  - Search preview

### Organization

- **Classifiers** - Flexible taxonomy system
- **Tags** - Simple text-based tags
- **Parent page** - Hierarchical structure

### Admin Interface

Organized into tabs:

- **Content** - Core page fields and body
- **Classify** - Tags and classifiers
- **Promote** - SEO and preview settings

## AratingaWebPage

General-purpose page for all website content.

### Features

- Rich StreamField body with all block types
- Flexible layout with cards, galleries, sections
- SEO optimization

### Usage

```python
# Create a web page in admin:
# 1. Pages → Add a page
# 2. Select "Web Page"
# 3. Add title and content blocks
# 4. Publish
```

### Template

Located at `themes/bootstrap5/templates/pages/web_page.html`

Render page content:

```django
{% for block in page.body %}
    {% include_block block %}
{% endfor %}
```

## AratingaArticlePage

Blog post / article with metadata.

### Additional Fields

- **Author** - Staff member (optional, auto-filled)
- **Author display** - Override author name
- **Publish date** - Article publication date
- **Featured image** - Hero image
- **Caption** - Image caption (optional)

### Page Sections

From the Promote tab:

- **Show images** - Display featured images in lists
- **Show author and date info** - Display metadata
- **Show preview text** - Show preview in listings

### Body Content

Simplified StreamField with content-focused blocks:

- Rich text, buttons, images, embeds
- Cards, carousels, galleries
- Quotes, tables

### Fields Example

```python
article = AratingaArticlePage()
article.title = "Understanding Aratinga"
article.author = User.objects.first()
article.body = [
    ('text', RichTextBlock().make_block_value(...)),
    ('image', ImageBlock().make_block_value(...)),
]
article.save()
```

## AratingaArticleIndexPage

Lists articles with filtering and pagination.

### Features

- Display latest articles from a section
- Filter by classifiers
- Pagination
- Featured articles section
- Shows/hides article metadata

### Configuration

From Promote tab:

- **Show images** - Display article featured images
- **Show author and date info** - Display article metadata
- **Show preview text** - Show article preview text
- **Index order** - Sort articles by:
  - Date published (newest/oldest)
  - Date updated (newest/oldest)
  - Title (alphabetical/reverse)
- **Subpages** - Show child articles

### Usage

1. Create an Article Index Page in admin
2. Add articles as child pages
3. Index automatically lists and filters articles

## Creating Custom Page Models

Extend `AratingaWebPage` or `AratingaArticlePage`:

```python
from aratinga.models import AratingaWebPage
from wagtail.fields import StreamField
from aratinga.blocks import COMPONENT_STREAMBLOCKS

class ServicePage(AratingaWebPage):
    """Custom service page model"""

    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration = models.CharField(max_length=100, blank=True)

    content_panels = AratingaWebPage.content_panels + [
        FieldPanel('price'),
        FieldPanel('duration'),
    ]

    class Meta:
        verbose_name = "Service Page"
        verbose_name_plural = "Service Pages"
```

Register in admin:

```python
from django.contrib import admin
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import ServicePage

@modeladmin_register
class ServicePageAdmin(ModelAdmin):
    model = ServicePage
```

## Page Hierarchy

Visualize and manage page structure:

```
Website Home /
├── About /about/
│   ├── Team /about/team/
│   └── History /about/history/
├── Services /services/
│   ├── Consulting /services/consulting/
│   └── Development /services/development/
└── Blog /blog/
    ├── Article 1 /blog/article-1/
    └── Article 2 /blog/article-2/
```

Move pages by:
1. Admin interface drag-and-drop
2. Edit page → Move to different parent

## Publishing Pages

### Workflow

1. **Draft** - Editable by authors, not publicly visible
2. **Scheduled** - Set to publish at specific date/time
3. **Published** - Live on website

### Actions

- **Save as draft** - Keep editing
- **Schedule publish** - Set publish date
- **Publish now** - Make live immediately
- **Unpublish** - Remove from public access

## SEO Optimization

Each page includes SEO fields:

### Meta Title

Override the page title in search results (60 characters recommended).

### Meta Description

Search result snippet (155 characters recommended).

### Preview

Real-time preview of search result appearance.

## Accessing Pages in Templates

```django
{# Get current page #}
{{ page.title }}
{{ page.get_url }}
{{ page.live_revision }}

{# Iterate child pages #}
{% for child in page.get_children.live.specific %}
    <a href="{{ child.get_url }}">{{ child.title }}</a>
{% endfor %}

{# Get siblings #}
{% for sibling in page.get_siblings.live %}
    <a href="{{ sibling.get_url }}">{{ sibling.title }}</a>
{% endfor %}
```

## Next Steps

- 📖 [Concepts](../concepts/index.md) - Understand page organization
- 🧩 [Blocks](../blocks/index.md) - Available content blocks
- ⚙️ [Customization](../advanced/customization.md) - Create custom models
- 🌍 [Internationalization](../advanced/internationalization.md) - Multi-language pages
