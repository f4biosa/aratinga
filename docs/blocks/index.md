# Blocks Guide

Aratinga provides a comprehensive set of pre-built blocks for creating rich page content.

## Overview

Blocks are organized into four categories:

| Category | Purpose | Blocks |
|----------|---------|--------|
| **HTML Blocks** | Basic HTML elements | Rich Text, Buttons, Images, Embeds, Quotes, Tables |
| **Content Blocks** | Complex content patterns | Cards, Carousels, Image Galleries |
| **Layout Blocks** | Structural elements | Grid Rows, Columns, Card Grids |
| **Section Blocks** | Full-width sections | Hero, Promo, Featured Section |

## HTML Blocks

Simple, non-nested blocks for common content elements.

### Rich Text

Multi-format text editor with formatting options:

- Bold, Italic, Underline, Strikethrough
- Headings (H2-H6)
- Lists (bullet, numbered)
- Links
- Document links
- Horizontal rule

**Use for**: Article body, descriptions, instructions

### Button Link

Styled button linking to pages, documents, or external URLs.

**Fields**:
- Page link (internal pages)
- Document link (uploaded files)
- External link (URLs)
- Button title (display text)
- Button style (primary, secondary, danger, etc.)

**Use for**: Calls-to-action, navigation

### Image

Responsive image with alt text.

**Fields**:
- Image (required)
- Alt text (accessibility)

**Use for**: Hero images, article headers, illustrations

### Image Link

Clickable image linking to pages, documents, or external URLs.

**Fields**:
- Image (required)
- Alt text (required)
- Page link / Document link / External link
- Link title

**Use for**: Linked product images, banner ads

### Embed Video

YouTube, Vimeo, or other embeddable media.

**Fields**:
- URL (required) - Link to video or media

**Use for**: Video tutorials, interviews, presentations

### Quote

Blockquote with optional attribution.

**Fields**:
- Text (required)
- Author (optional)

**Use for**: Testimonials, famous quotes, callouts

### Download Block

Button for downloading files.

**Fields**:
- Document (required)
- Button style
- Button size

**Use for**: PDF downloads, document libraries

### Google Map

Embedded interactive map.

**Fields**:
- Search query - Address or business name
- Map title - Screen reader text
- Google place ID - Specific location
- Map zoom level

**Use for**: Location pages, contact information

### Page List

Latest pages from a section with filtering.

**Fields**:
- Parent page (required) - Show children of this page
- Classified as (optional) - Filter by classifier
- Number of pages to show

**Use for**: Blog index, resource lists, related content

### Page Preview

Mini preview card of a single page.

**Fields**:
- Page to preview (required)

**Use for**: Featured articles, recommended reading

### Table

Data table with sorting options.

**Fields**:
- Table data (required)

**Use for**: Pricing tables, feature comparisons, data

## Content Blocks

Nestable blocks containing multiple items.

### Card

Information card with image, title, body, and links.

**Fields**:
- Image (optional)
- Title (optional)
- Subtitle (optional)
- Body (optional) - Rich text
- Links (optional) - Buttons

**Use for**: Team members, testimonials, product cards

### Carousel

Rotating image carousel from a snippet.

**Fields**:
- Carousel (required)

**Use for**: Featured images, sliding gallery

### Image Gallery

Modal gallery from an image collection.

**Fields**:
- Image Collection (required)

**Use for**: Photo galleries, portfolio showcases

## Layout Blocks

Structural blocks that contain other blocks.

### Grid / Responsive Grid Row

Responsive grid system using Bootstrap columns.

**Fields**:
- Column configuration
- Full width toggle
- Content blocks

**Use for**: Creating responsive layouts

### Column

Single column within a grid row.

**Fields**:
- Column size (auto, 1/2, 1/3, 2/3, 1/4, 3/4, etc.)
- Content

**Use for**: Multi-column layouts

### Card Grid

Grid layout displaying cards in a masonry or deck layout.

**Fields**:
- Full width toggle
- Card blocks

**Use for**: Product grids, team directories

## Section Blocks

Full-width prominent sections.

### Hero Section

Large banner with image, title, text, and CTA.

**Fields**:
- Image (required)
- Title (optional)
- Text (optional)
- Call to action label (optional)
- Call to action page (optional)
- Parallax effect toggle
- Background color
- Text color

**Use for**: Page headers, main banners

### Promo Section

Promotional section with image and rich text.

**Fields**:
- Image (required)
- Title (optional)
- Text (optional) - Rich text

**Use for**: Special announcements, highlights

### Featured Section

Displays up to 3 child pages in a grid.

**Fields**:
- Title (optional)
- Featured section (optional) - Parent page

**Use for**: Highlighting section content

## Block Grouping

Blocks are organized into groups in the editor for easier navigation:

- **Content** - Card, Carousel, Image Gallery
- **Section** - Hero, Promo, Featured Section
- **HTML** - All HTML blocks

## Creating Custom Blocks

Extend Aratinga by creating custom blocks:

```python
from wagtail import blocks
from aratinga.blocks.base_blocks import BaseBlock

class TestimonialBlock(BaseBlock):
    """Custom testimonial block"""

    quote = blocks.TextBlock(required=True, label="Quote")
    author = blocks.CharBlock(required=True, label="Author")
    role = blocks.CharBlock(required=False, label="Role")
    image = ImageChooserBlock(required=False, label="Photo")

    class Meta:
        template = "blocks/testimonial_block.html"
        icon = "quote"
        label = "Testimonial"
```

Then register in your StreamField:

```python
body = StreamField([
    ('testimonial', TestimonialBlock()),
    # ...other blocks...
])
```

See [Advanced Topics](../advanced/index.md) for more details.

## Best Practices

1. **Use semantic HTML** - Choose the most appropriate block type
2. **Keep blocks simple** - Don't nest too deeply
3. **Write alt text** - For accessibility on all images
4. **Link meaningfully** - Use descriptive link text
5. **Preview before publishing** - Check mobile responsiveness
6. **Reuse patterns** - Create card-based layouts for consistency
7. **Performance** - Limit large gallery sizes, optimize images

## Next Steps

- 📄 [Page Models](../models/index.md) - Learn about page types
- ⚙️ [Customization](../advanced/customization.md) - Create custom blocks
