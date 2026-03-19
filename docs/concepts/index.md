# Core Concepts

Understand the fundamental concepts behind Aratinga CMS.

## Pages

Pages are the main content containers in Aratinga. Each page has:

- **Title** - The page name (shown in navigation and meta tags)
- **Slug** - URL-friendly identifier (e.g., `about-us`)
- **Status** - Draft or Published
- **Body** - StreamField containing blocks of content
- **SEO Fields** - Meta description, title, etc.
- **Classifications** - Classifiers and tags for organization

### Page Hierarchy

Pages form a tree structure:

```
Website Home (/)
├── About Us (/about-us/)
│   ├── Team (/about-us/team/)
│   └── History (/about-us/history/)
├── Services (/services/)
│   ├── Consulting (/services/consulting/)
│   └── Development (/services/development/)
└── Blog (/blog/)
    ├── Article 1 (/blog/article-1/)
    └── Article 2 (/blog/article-2/)
```

## Blocks

Blocks are the building blocks of page content. They represent different types of content elements:

### Block Categories

- **HTML Blocks** - Rich text, buttons, images, embeds, quotes, tables
- **Content Blocks** - Cards, carousels, galleries
- **Layout Blocks** - Grid rows, columns, card grids
- **Section Blocks** - Hero sections, promotional blocks, featured sections

See [Blocks Documentation](../blocks/index.md) for detailed information.

## StreamField

A StreamField is a Django field that allows editors to add multiple blocks to a page in any order.

```python
body = StreamField(
    [
        ("text", RichTextBlock()),
        ("image", ImageBlock()),
        ("card", CardBlock()),
    ]
)
```

Editors see each block represented in the admin interface with drag-and-drop reordering.

## Page Types

Aratinga provides several built-in page types:

### AratingaPage (Abstract)

The base class for all pages. Provides:

- Basic page fields (title, slug, etc.)
- Classification and tagging
- SEO optimization fields

### AratingaWebPage

General-purpose page for website content. Includes:

- Rich body StreamField with multiple block types
- Flexible layout options

### AratingaArticlePage

Optimized for blog posts and articles. Includes:

- Article-specific metadata (author, publish date)
- Featured image
- Article-specific body blocks

### AratingaArticleIndexPage

Lists and filters articles. Provides:

- Article listing
- Filtering by classifiers
- Pagination
- Featured articles

## Classifiers

Classifiers are flexible taxonomy tools for organizing content:

- Group pages by category, topic, or any custom dimension
- Link multiple pages to the same classifier term
- Use in templates to:
  - Display related content
  - Filter content on index pages
  - Generate navigation menus

Example:

```python
# In templates
{% for page in articles %}
    {% if "News" in page.classifier_terms.all %}
        <article>{{ page.title }}</article>
    {% endif %}
{% endfor %}
```

## Tags

Simple text-based tags for marking pages:

```python
page.tags.add("featured", "trending", "important")
```

Use for:

- Content flagging
- Simple categorization
- Search filters

## Theme System

Aratinga ships with Bootstrap 5 theme but is theme-agnostic:

```
themes/
└── bootstrap5/
    └── templates/
        ├── base.html
        ├── pages/
        │   ├── web_page.html
        │   └── article_page.html
        ├── blocks/
        │   ├── rich_text_block.html
        │   ├── image_block.html
        │   └── card_block.html
        └── partials/
            └── navigation.html
```

Customize by:

1. Creating a new theme directory
2. Overriding template files
3. Adding custom CSS/JS

## Internationalization (i18n)

Aratinga supports multiple languages out of the box:

```python
# In settings/base.py
LANGUAGES = [
    ('en', 'English'),
    ('pt-br', 'Português'),
]

LANGUAGE_CODE = 'en'
```

All UI strings are translatable using Django's translation system:

```python
from django.utils.translation import gettext_lazy as _

label = _("My Translatable String")
```

Manage translations in `/locale/` directories.

## Models vs Blocks

- **Model Fields** - Fixed page structure (title, slug, author)
- **Blocks** - Flexible content within StreamField

Models define the schema, blocks define the content.

## Admin Interface

The Aratinga admin interface provides:

- **Page Management** - Create, edit, publish pages
- **Block Editor** - Drag-and-drop content blocks
- **Classification** - Tag and filter content
- **Preview** - Preview pages before publishing
- **Scheduling** - Schedule page publishing
- **Versioning** - Track page revisions

## Next Steps

- ✅ [Getting Started](../getting-started/index.md)
- 🧩 [Blocks Documentation](../blocks/index.md)
- 📄 [Page Models](../models/index.md)
- ⚙️ [Advanced Topics](../advanced/index.md)
