from rest_framework import serializers
from .models import ShoppingList, IngredientItem

class IngredientItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    
    class Meta:
        model = IngredientItem
        fields = ['id', 'ingredient', 'quantity', 'measurement', 'checked']

class ShoppingListSerializer(serializers.ModelSerializer):
    ingredient_items = IngredientItemSerializer(many=True)

    class Meta:
        model = ShoppingList
        fields = ['id', 'user', 'title',  'ingredient_items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('ingredient_items', [])
        
        # Create the ShoppingList instance
        shopping_list = ShoppingList.objects.create(**validated_data)
        
        # Create IngredientItem instances
        for item_data in items_data:
            IngredientItem.objects.create(
                shopping_list=shopping_list,
                **item_data
            )
        
        return shopping_list

    def update(self, instance, validated_data):
        items_data = validated_data.pop('ingredient_items', [])

        # Update ShoppingList fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        existing_items = {item.id: item for item in instance.items.all()}

        # Update IngredientItems
        for item_data in items_data:
            item_id = item_data.get('id')
            if item_id and item_id in existing_items:
                item = existing_items.pop(item_id)
                for attr, value in item_data.items():
                    setattr(item, attr, value)
                item.save()
            else:
                IngredientItem.objects.create(shopping_list=instance, **item_data)

        # Delete the existing
        if existing_items:
            IngredientItem.objects.filter(id__in=existing_items.keys()).delete()

        return instance