# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import ShoppingList, IngredientItem
from .serializers import ShoppingListSerializer, IngredientItemSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def shoppinglist_list_create(request):
    if request.method == 'GET':
        shoppinglists = ShoppingList.objects.filter(user=request.user)
        serializer = ShoppingListSerializer(shoppinglists, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print(request.data)
        serializer = ShoppingListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def shoppinglist_detail(request, pk):
    try:
        shoppinglist = ShoppingList.objects.get(pk=pk, user=request.user)
        print(shoppinglist)
    except ShoppingList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ShoppingListSerializer(shoppinglist)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ShoppingListSerializer(shoppinglist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        
        shoppinglist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def delete_ingredient_item(request, item_id):
    try:
        # Get the IngredientItem object
        item = IngredientItem.objects.get(id=item_id)
        # Delete the item
        item.delete()
        return Response({'message': 'IngredientItem deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except IngredientItem.DoesNotExist:
        return Response({'error': 'IngredientItem not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PUT'])
def update_ingredient_item(request, item_id):
    try:
        item = IngredientItem.objects.get(id=item_id)

        serializer = IngredientItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except IngredientItem.DoesNotExist:
        return Response({'error': 'IngredientItem not found'}, status=status.HTTP_404_NOT_FOUND)