# Generated by Django 5.1.7 on 2025-03-29 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aratingaadmin', '0002_alter_themesettings_theme'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theme',
            name='is_active',
        ),
    ]
