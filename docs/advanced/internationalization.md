# Internationalization (i18n)

Build multi-language websites with Aratinga's built-in internationalization support.

## Setup

### Configure Languages

In `settings/base.py`:

```python
from django.utils.translation import gettext_lazy as _

# Supported languages
LANGUAGES = [
    ('en', _('English')),
    ('pt-br', _('Portuguese (Brazil)')),
    ('es', _('Spanish')),
]

# Default language
LANGUAGE_CODE = 'en'

# Language cookie
LANGUAGE_COOKIE_AGE = 60 * 60 * 24 * 365  # One year
LANGUAGE_COOKIE_DOMAIN = None
LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_PATH = '/'

# Timezone
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True

# Locale paths
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
    os.path.join(BASE_DIR, 'website', 'locale'),
]
```

### Enable Locale Middleware

```python
MIDDLEWARE = [
    # ...
    'django.middleware.locale.LocaleMiddleware',
    # ...
]
```

## Mark Strings for Translation

### In Python Code

```python
from django.utils.translation import gettext_lazy as _

# Use gettext_lazy for model fields and module-level strings
label = _("My Translatable String")

class MyModel(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title")
    )
```

### In Block Definitions

```python
from wagtail import blocks
from django.utils.translation import gettext_lazy as _

class MyBlock(blocks.StructBlock):
    title = blocks.CharBlock(label=_("Title"))

    class Meta:
        label = _("My Block")
```

All Aratinga blocks are pre-translated with `_()` markers.

### In Templates

```django
{% load i18n %}

<p>{% trans "Hello, World!" %}</p>
<p>{% blocktrans %}You have {{count}} messages{% endblocktrans %}</p>
```

## Generate Translation Files

### Create Message Files

```bash
# Generate .po files for all configured languages
python manage.py makemessages -a

# Or for specific language
python manage.py makemessages -l pt_BR
python manage.py makemessages -l es
```

This creates files:
```
locale/
├── en/LC_MESSAGES/
│   └── django.po
├── pt_BR/LC_MESSAGES/
│   └── django.po
└── es/LC_MESSAGES/
    └── django.po
```

### Edit Translation Files

Use a .po editor like:
- [Poedit](https://www.poedit.net/)
- [Gtranslator](https://wiki.gnome.org/Apps/Gtranslator)
- [VS Code i18n extension](https://marketplace.visualstudio.com/items?itemName=lokalise.i18n-ally)

Or edit manually:

```po
#: src/aratinga/blocks/html_blocks.py:237
msgid "Author"
msgstr "Autor"

#: src/aratinga/blocks/content_blocks.py:49
msgid "Card"
msgstr "Cartão"
```

### Compile Translations

Convert .po files to binary .mo format:

```bash
# Compile all languages
python manage.py compilemessages

# Or specific language
python manage.py compilemessages -l pt_BR
```

This creates `.mo` files used by Django at runtime.

## Language Switching

### URL-Based Language Selection

```python
# urls.py
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
) + [
    path('i18n/', include('django.conf.urls.i18n')),
]
```

Access different languages:
- `http://localhost:8000/en/` - English
- `http://localhost:8000/pt-br/` - Portuguese

### Language Selector in Templates

```django
{% load i18n %}

<div class="language-selector">
    {% for code, name in LANGUAGES %}
        {% language code %}
            <a href="/{{ code }}{% trans current_path %}">
                {{ name }}
            </a>
        {% endlanguage %}
    {% endfor %}
</div>
```

Or with POST form:

```django
{% load i18n %}

<form action="{% url 'set_language' %}" method="post">
    {% csrf_token %}
    <input name="language" type="hidden" value="pt-br">
    <button type="submit">Português</button>
</form>
```

## Aratinga's Built-in Translations

Aratinga includes pre-translated strings for:

- Block names and labels
- Field names (Title, Body, Author, etc.)
- Form messages
- Classifiers and organization

Included languages:
- English (en)
- Portuguese (pt-br)

Extend by adding your custom language folders.

## Page-Specific Content Translation

### Using Wagtail Locales

Aratinga integrates with Wagtail's content translation:

````text
# Each page can have variants per language
# The page model supports:
# - locale (current language version)
# - translation_key (group across languages)

# In templates
{% if page.locale.language_code == 'en' %}
    <!-- English-specific content -->
{% endif %}
```

### Manual Multi-language Pages

Create separate page trees per language:

```
Website Root
├── English (/en/)
│   ├── About (/en/about/)
│   └── Services (/en/services/)
└── Portuguese (/pt-br/)
    ├── Sobre (/pt-br/sobre/)
    └── Serviços (/pt-br/servicos/)
```

## Template Language Tags

### Get Current Language

```django
{% load i18n %}

<!-- Current language code -->
{{ request.LANGUAGE_CODE }}

<!-- Current language name -->
{% get_current_language as language_code %}
{{ language_code }}

<!-- Get language name -->
{% get_language_info for code as lang %}
{{ lang.name }}
```

### Conditionally Translate Content

```django
{% load i18n %}

{% if request.LANGUAGE_CODE == 'pt-br' %}
    <p>Conteúdo em Português</p>
{% else %}
    <p>English Content</p>
{% endif %}
```

## DateFormat & Numbers

Format dates and numbers based on language:

```django
{% load humanize %}

<!-- Date formatting by language -->
{{ article.created_at|date:"DATE_FORMAT" }}

<!-- Number formatting -->
{{ price|floatformat:2 }}
```

## Translation Files Structure

```
locale/
├── en/
│   └── LC_MESSAGES/
│       ├── django.po      # Translation file
│       └── django.mo      # Compiled binary
├── pt_BR/
│   └── LC_MESSAGES/
│       ├── django.po
│       └── django.mo
└── es/
    └── LC_MESSAGES/
        ├── django.po
        └── django.mo
```

## Deployment

### Production Translations

1. **Generate and compile** locally:
   ```bash
   python manage.py makemessages -a
   # Edit .po files...
   python manage.py compilemessages
   ```

2. **Commit to version control**:
   ```bash
   git add locale/
   git commit -m "Update translations"
   ```

3. **Deploy and compile on server**:
   ```bash
   python manage.py compilemessages
   ```

## Locale Switching Strategies

### Cookie-Based (Recommended)

User language preference stored in cookie

### Session-Based

Language preference stored in session

### URL-Based

Language in URL path (`/en/`, `/pt-br/`)

### Header-Based

Accept-Language HTTP header

## Best Practices

1. **Mark early** - Use `_()` when creating strings
2. **Keep it simple** - Avoid complex pluralization
3. **Context matters** - Use contexts for ambiguous strings
   ```python
   _("Open")  # Could be a door or file
   pgettext("software", "Open")
   ```
4. **Translate UI sources** - Everything users see
5. **Extract regularly** - Keep translation files updated
6. **Version control** - Commit .po/.mo files
7. **Test all languages** - Ensure translation works in templates

## Common Issues

### Translations Not Appearing

1. Check `.mo` files compiled:
   ```bash
   ls -la locale/pt_BR/LC_MESSAGES/django.mo
   ```
2. Clear browser cache
3. Restart development server
4. Check `LANGUAGE_CODE` setting

### Missing Translations

Generate updated files:
```bash
python manage.py makemessages -a --keep-pot
```

### Plural Forms

```python
from django.utils.translation import ngettext

count = 5
msg = ngettext(
    'You have %(count)d message',
    'You have %(count)d messages',
    count
) % {'count': count}
```

## Next Steps

- ⚙️ [Customization](customization.md) - Extend functionality
- 📚 [API Reference](../api/index.md) - Complete API
- 🚀 [Deployment](../advanced/index.md) - Production setup
