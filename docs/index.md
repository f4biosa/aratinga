# Aratinga CMS

A powerful, flexible open-source CMS built on Django, Wagtail, and built-in page management features.

## Welcome

Aratinga is a PHP-Independent CMS that provides a comprehensive set of features for building modern websites. It's built on top of [Wagtail](https://wagtail.io/), Django's leading CMS framework, and adds rich functionality specifically designed for content management.

## Key Features

- 🎨 **Rich Block System** - Ready-made blocks for common content patterns (HTML, Content, Layout, Section)
- 📄 **Multiple Page Types** - Web Pages, Articles, and custom page types
- 🏷️ **Content Organization** - Classifiers and tags for flexible content management
- 🌍 **Multi-language Support** - Full internationalization (i18n) support
- 🎯 **SEO Optimized** - Built-in SEO fields and optimization tools
- 📱 **Responsive Design** - Bootstrap 5 templates out of the box
- ⚙️ **Highly Customizable** - Extend models, blocks, and templates easily

## Documentation

- [**Getting Started**](getting-started/index.md) - Installation and first project setup
- [**Concepts**](concepts/index.md) - Learn core CMS concepts
- [**Blocks**](blocks/index.md) - Complete guide to available blocks
- [**Models**](models/index.md) - Page types and page models
- [**API Reference**](api/index.md) - Complete API documentation
- [**Advanced Topics**](advanced/index.md) - Advanced customization and development

## Quick Start

### Installation

```bash
# Install Aratinga
pip install aratinga

# Create a new project
aratinga start myproject

# Apply migrations
cd myproject
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Access the admin interface at `http://localhost:8000/admin/`

## Architecture

Aratinga follows a clean separation between the reusable CMS package and project-specific implementations:

```
/aratinga/                    # CMS Package (library)
├── src/aratinga/
│   ├── blocks/               # Block definitions
│   ├── models/               # Data models
│   ├── locale/               # Translations
│   └── ...

/myproject/                   # Your Project (generated via `aratinga start`)
├── manage.py                 # Django management
├── themes/                   # Theme files
├── website/                  # Project app
└── settings/                 # Configuration
```

## Community & Support

- [GitHub](https://github.com/f4biosa/aratinga) - Source code and issue tracking
- [Discussions](https://github.com/f4biosa/aratinga/discussions) - Community conversations

---

**Last Updated**: March 2026
**Version**: Latest Development
