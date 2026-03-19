# Getting Started with Aratinga

Learn how to install Aratinga and create your first project.

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager
- A relational database (SQLite, PostgreSQL, MySQL)

### Install Aratinga

```bash
pip install aratinga
```

Or using `uv`:

```bash
uv pip install aratinga
```

### Create Your First Project

Use the `aratinga start` command to generate a new project:

```bash
aratinga start myproject
cd myproject
```

This creates a Django project pre-configured with Aratinga's features, including:

- Database configuration
- Installed apps and middleware
- Static and media file settings
- Theme and template directories
- Initial migrations

## Initial Setup

### Apply Database Migrations

```bash
python manage.py migrate
```

### Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Run the Development Server

```bash
python manage.py runserver
```

Access your site at:
- **Frontend**: http://localhost:8000/
- **Admin Interface**: http://localhost:8000/admin/

## Your First Page

1. **Log in** to the admin interface at `/admin/`
2. **Create a Page**:
   - Go to "Pages" in the sidebar
   - Click "Add a page"
   - Select "Web Page" as the page type
   - Fill in the title and slug
3. **Add Content**:
   - Navigate to the "Content" tab
   - Click "Add block" to add content blocks
   - See [Blocks Documentation](../blocks/index.md) for available types
4. **Publish**:
   - Click "Publish" to make the page live

## Project Structure

```
myproject/
├── manage.py              # Django management script
├── db.sqlite3            # Development database
├── static/               # Static files (CSS, JS, images)
├── media/                # User uploads
├── themes/               # Theme templates
│   └── bootstrap5/       # Default Bootstrap 5 theme
│       └── templates/
├── website/              # Your project app
│   ├── models.py        # Custom page models
│   ├── views.py         # Custom views
│   └── migrations/       # Database migrations
├── settings/             # Configuration
│   ├── base.py          # Base settings
│   ├── development.py   # Development settings
│   └── production.py    # Production settings
└── manage.py            # Django CLI
```

## Configuration

### settings/base.py

Key settings to configure:

```python
# Language
LANGUAGE_CODE = 'en-us'  # or 'pt-br'

# Timezone
TIME_ZONE = 'UTC'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Allowed hosts (in production)
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

## Next Steps

- 📖 [Learn Core Concepts](../concepts/index.md) - Understand Aratinga's architecture
- 🧩 [Explore Blocks](../blocks/index.md) - Available content blocks
- 📄 [Page Models](../models/index.md) - Different page types
- ⚙️ [Advanced Customization](../advanced/index.md) - Extend Aratinga

## Troubleshooting

### Port Already in Use

```bash
python manage.py runserver 8001
```

### Database Locked

Delete `db.sqlite3` and run migrations again:

```bash
rm db.sqlite3
python manage.py migrate
```

### Missing Static Files

```bash
python manage.py collectstatic --clear --noinput
```

## Getting Help

- Check the [Concepts](../concepts/index.md) guide
- Review the [Blocks Documentation](../blocks/index.md)
- Visit [GitHub Discussions](https://github.com/f4biosa/aratinga/discussions)
