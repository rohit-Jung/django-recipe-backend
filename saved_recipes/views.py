from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import SavedRecipe, Recipe
from .serializers import SavedRecipeSerializer

# List and create saved recipes
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saved_recipe_list(request):
    if request.method == 'GET':
        saved_recipes = SavedRecipe.objects.filter(user=request.user)
        serializer = SavedRecipeSerializer(saved_recipes, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def saved_recipe_list_create(request):
        recipe_id = request.data.get('recipe_id')
        print(request.data)
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            return Response({'error': 'Recipe not found.'}, status=status.HTTP_404_NOT_FOUND)

        if SavedRecipe.objects.filter(user=request.user, recipe=recipe).exists():
            return Response("Already Saved Recipes", status=status.HTTP_409_CONFLICT)
        
        data = {
            'recipe': recipe.id,
            'user': request.user.id,  
        }

        serializer = SavedRecipeSerializer(data=data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete a saved recipe
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def saved_recipe_detail(request, pk):
    if request.method == 'GET':
        try:
            saved_recipe = SavedRecipe.objects.get(recipe_id=pk, user=request.user)
        except SavedRecipe.DoesNotExist:
            return Response({'error': 'Saved recipe not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SavedRecipeSerializer(saved_recipe)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        try:
            saved_recipe = SavedRecipe.objects.get(pk=pk, user=request.user)
        except SavedRecipe.DoesNotExist:
            return Response({'error': 'Saved recipe not found.'}, status=status.HTTP_404_NOT_FOUND)
        saved_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
