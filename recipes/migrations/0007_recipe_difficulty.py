# Generated by Django 5.1 on 2024-09-06 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_remove_recipe_image_url_recipe_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='difficulty',
            field=models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('difficult', 'Difficult'), ('exteme', 'Extreme')], default='medium', max_length=20),
        ),
    ]
