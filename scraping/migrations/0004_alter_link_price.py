# Generated by Django 4.1.5 on 2023-02-04 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0003_alter_link_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='price',
            field=models.FloatField(blank=True, help_text='Цена', null=True),
        ),
    ]
