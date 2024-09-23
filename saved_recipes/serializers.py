from rest_framework import serializers
from .models import SavedRecipe
from recipes.serializers import RecipeSerializer  # Ensure this serializer includes recipe details
from recipes.models import Recipe

class SavedRecipeSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())  # Use PK for input

    class Meta:
        model = SavedRecipe
        fields = ['id', 'user', 'recipe', 'saved_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Include RecipeSerializer for detailed output
        representation['recipe'] = RecipeSerializer(instance.recipe).data
        return representation
