# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import MealPlan
from .serializers import MealPlanSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def mealplan_list_create(request):
    if request.method == 'GET':
        mealplans = MealPlan.objects.filter(user=request.user)
        serializer = MealPlanSerializer(mealplans, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MealPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def mealplan_detail(request, pk):
    try:
        mealplan = MealPlan.objects.get(pk=pk, user=request.user)
    except MealPlan.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MealPlanSerializer(mealplan)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MealPlanSerializer(mealplan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        mealplan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
