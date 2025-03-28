# Generated by Django 5.1.2 on 2024-10-16 18:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aratinga', '0001_initial'),
        ('wagtailcore', '0094_alter_page_locale'),
        ('wagtailimages', '0026_delete_uploadedimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_suffix', models.CharField(default='The Wagtail Bakery', help_text="The suffix for the title meta tag e.g. ' | The Wagtail Bakery'", max_length=255, verbose_name='Title suffix')),
                ('favicon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='favicon', to='wagtailimages.image', verbose_name='Favicon')),
                ('logo', models.ForeignKey(blank=True, help_text='Brand logo used in the navbar and throughout the site', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Logo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('genericsettings_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='aratinga.genericsettings')),
                ('from_email_address', models.CharField(blank=True, help_text='The default email address this site appears to send from. For example: "sender@example.com" or "Sender Name <sender@example.com>" (without quotes)', max_length=255, verbose_name='From email address')),
                ('search_num_results', models.PositiveIntegerField(default=10, verbose_name='Number of results per page')),
                ('external_new_tab', models.BooleanField(default=False, verbose_name='Open all external links in new tab')),
                ('google_maps_api_key', models.CharField(blank=True, help_text='The API Key used for Google Maps.', max_length=255, verbose_name='Google Maps API Key')),
                ('mailchimp_api_key', models.CharField(blank=True, help_text='The API Key used for Mailchimp.', max_length=255, verbose_name='Mailchimp API Key')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'verbose_name': 'CMS Settings',
            },
            bases=('aratinga.genericsettings', models.Model),
        ),
    ]
