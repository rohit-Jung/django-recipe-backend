# Generated by Django 5.1 on 2024-09-09 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_recipe_food_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='food_category',
            new_name='category',
        ),
    ]
