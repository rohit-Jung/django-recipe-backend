# Generated by Django 5.1 on 2024-09-03 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_remove_recipe_tags_alter_recipe_image_delete_tag_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='image',
        ),
        migrations.AddField(
            model_name='recipe',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
