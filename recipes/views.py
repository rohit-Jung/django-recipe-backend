# views.py
from email.mime import image
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Recipe, Review
from .serializers import RecipeSerializer, ReviewSerializer
from accounts.decorators import role_required
import json
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from .models import RecipeIngredient, Instruction


@api_view(['GET'])
def recipe_list(request):
    recipes = Recipe.objects.all()
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@role_required(['chef'])
def recipe_create(request):
    # Extract and parse data
    data = request.data

    try:
        # Handle JSON fields
        recipe_ingredients = json.loads(data.get('recipe_ingredients', '[]'))
        instructions = json.loads(data.get('instructions', '[]'))
        tags = json.loads(data.get('tags', '[]'))

        # Prepare final data by merging parsed fields with existing data
        recipe_create_data = {
            'name': data.get('name'),
            'description': data.get('description'),
            'servings': data.get('servings'),
            'prep_time': data.get('prep_time'),
            'cooking_time': data.get('cooking_time'),
            'image': data.get('image'),
            'tags': tags,
            'recipe_ingredients': recipe_ingredients,
            'instructions': instructions,
            'difficulty': data.get('difficulty'),
            'category': data.get('category')

        }

        print("data prepared", recipe_create_data)

        # Initialize serializer with the prepared data
        serializer = RecipeSerializer(data=recipe_create_data)

        if serializer.is_valid():
            # Set the user and save the recipe
            serializer.validated_data['user'] = request.user
            recipe = serializer.save()

            return Response({'success': True, 'recipe_id': recipe.id, 'recipe': RecipeSerializer(recipe).data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except json.JSONDecodeError as e:
        return Response({'error': f'Invalid JSON format: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_recipes(request):
    user = request.user
    try:
        recipes = Recipe.objects.filter(user=user)
    except Recipe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def each_recipe_detail(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = RecipeSerializer(recipe)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_recipe(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if recipe.user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)
    recipe.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@role_required(['chef'])

def update_recipe(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Check if the user is the owner of the recipe
    if recipe.user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    data = request.data
    try:
        image = data.get('image')
        if image == "undefined" or not image:
            image = recipe.image

        print(json.loads(data.get('tags')))
        print(data.get('tags'))
        recipe_update_data = {
            'name': data.get('name'),
            'description': data.get('description'),
            'servings': data.get('servings'),
            'prep_time': data.get('prep_time'),
            'cooking_time': data.get('cooking_time'),
            'image': image,  # Use existing image if not provided or invalid
            'tags': json.load(data.get('tags', '[]')),
            'recipe_ingredients': json.loads(data.get('recipe_ingredients', '[]')),
            'instructions': json.loads(data.get('instructions', '[]')),
            'difficulty': data.get('difficulty'),
            'category': data.get('category')
        }

        print("data prepared", recipe_update_data)

        serializer = RecipeSerializer(recipe, data=recipe_update_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
    except json.JSONDecodeError as e:
        return Response({'error': f'Invalid JSON format: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def review_list(request, recipe_id):
    reviews = Review.objects.filter(recipe_id=recipe_id)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        return Response({'error': 'Recipe not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ReviewSerializer(data=request.data, context={'request': request, 'recipe': recipe})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def review_detail(request, pk): 
    try:
        reviews = Review.objects.filter(recipe_id=pk)
        if not reviews.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ReviewSerializer(reviews, many=True) 
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_review(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if review.user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = ReviewSerializer(review, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if review.user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    review.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

