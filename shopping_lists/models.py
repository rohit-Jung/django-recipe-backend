from django.db import models
from accounts.models import CustomUser

class ShoppingList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class IngredientItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, related_name='ingredient_items', on_delete=models.CASCADE)
    quantity = models.CharField(max_length=20)  
    measurement = models.CharField(max_length=50)  
    ingredient = models.CharField(max_length=100)  
    checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item} ({self.quantity} {self.measurement}) in {self.shopping_list.title}"
