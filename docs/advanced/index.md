# Advanced Topics

Go deeper with Aratinga's advanced customization and deployment options.

## Topics

- **[Customization](customization.md)** - Create custom blocks and models
- **[Internationalization (i18n)](internationalization.md)** - Multi-language support
- **[Extending](extending.md)** - Hooks, signals, and plugins (coming soon)
- **[Performance](performance.md)** - Optimization and caching (coming soon)
- **[Deployment](deployment.md)** - Production setup and best practices (coming soon)

## Quick Links

### Create Custom Blocks

```python
from wagtail import blocks
from aratinga.blocks.base_blocks import BaseBlock

class MyBlock(BaseBlock):
    title = blocks.CharBlock()
    class Meta:
        template = 'blocks/my_block.html'
        label = 'My Block'
```

See [Customization](customization.md) for details.

### Extend Page Models

```python
from aratinga.models import AratingaWebPage

class ServicePage(AratingaWebPage):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        verbose_name = "Service"
```

See [Customization](customization.md) for details.

### Add Multi-Language Support

```python
LANGUAGES = [
    ('en', 'English'),
    ('pt-br', 'Português'),
]

python manage.py makemessages -a
python manage.py compilemessages
```

See [Internationalization](internationalization.md) for details.

## Best Practices

- ✅ Start with extending existing models
- ✅ Create reusable custom blocks
- ✅ Test in development before production
- ✅ Keep custom code organized
- ✅ Document custom functionality

## Common Patterns

### Custom Admin Actions

```python
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

@modeladmin_register
class MyAdmin(ModelAdmin):
    model = MyModel
    list_display = ('title', 'created_at')
```

### Wagtail Hooks

```python
from wagtail import hooks

@hooks.register('before_edit_page')
def do_something(request, page):
    pass
```

### Template Filters

```python
from django import template
register = template.Library()

@register.filter
def my_filter(value):
    return value.upper()
```

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Wagtail Documentation](https://docs.wagtail.io/)
- [Aratinga GitHub](https://github.com/f4biosa/aratinga)

## Support

- 💬 [GitHub Discussions](https://github.com/f4biosa/aratinga/discussions)
- 🐛 [Issue Tracker](https://github.com/f4biosa/aratinga/issues)
- 📖 [Main Documentation](../index.md)
