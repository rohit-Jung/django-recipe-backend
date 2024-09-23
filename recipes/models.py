from django.db import models
from accounts.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator
import json
from django.conf import settings


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', related_name='recipe_ingredients', on_delete=models.CASCADE)
    ingredient = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    measurement = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.quantity} {self.measurement} of {self.ingredient}'

class Instruction(models.Model):
    recipe = models.ForeignKey('Recipe', related_name='instructions', on_delete=models.CASCADE)
    step_number = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return f'Step {self.step_number} for {self.recipe.name}'

class Recipe(models.Model):
    DIFFICULTY = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('difficult', 'Difficult'),
        ('extreme', 'Extreme')
    )
    
    FOOD_CATEGORY = (
        ('appetizer', 'Appetizer'),
        ('main_course', 'Main Course'),
        ('dessert', 'Dessert'),
        ('salad', 'Salad'),
        ('snack', 'Snack'),
        ('soup', 'Soup'),
        ('drink', 'Drink'),
        ('breakfast', 'Breakfast'),
        ('side_dish', 'Side Dish'),
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    servings = models.CharField(max_length=50)
    prep_time = models.CharField(max_length=50)
    cooking_time = models.CharField(max_length=50)
    image = models.ImageField(upload_to="recipe-images/", null=True, blank=True)  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tags = models.TextField(blank=True, default="[]") 
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY, default='medium')
    category = models.CharField(max_length=20, choices=FOOD_CATEGORY, default='main_course')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def recipe_ingredient(self):
        return self.recipe_ingredient_set.all()
    
    @property
    def instructions(self):
        return self.instructions.all()

    def get_image_url(self):
        if self.image:
            return f"{settings.BACKEND_URL}{self.image.url}"
        return None

    def __str__(self):
        return self.name

class Review(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'
