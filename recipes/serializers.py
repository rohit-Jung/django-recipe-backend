
from rest_framework import serializers
from .models import Recipe, RecipeIngredient, Instruction, Review
from accounts.serializers import CustomUserSerializer
from rest_framework.exceptions import ValidationError
import json

class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'quantity', 'measurement', 'recipe']
        
        read_only_fields = ('recipe', )

class InstructionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Instruction
        fields = ['id', 'step_number', 'description', 'recipe']

        read_only_fields = ('recipe', )

class RecipeSerializer(serializers.ModelSerializer):
    recipe_ingredients = RecipeIngredientSerializer(many=True)
    instructions = InstructionSerializer(many=True)
    image_url = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'description', 'servings', 'prep_time', 
            'cooking_time', 'image', 'tags', 'recipe_ingredients', 
            'instructions', 'difficulty', 'image_url', 'user', 'created_at', 'category'
        ]
        read_only_fields = ['id', 'image_url', 'user', 'created_at']

    def get_image_url(self, obj):
        return obj.get_image_url()
    
    def get_tags(self, obj):
        raw_tags = obj.tags 
        if isinstance(raw_tags, str):
            clean_tags = raw_tags.strip("[]").replace("'", "").replace('"', '')
            return [tag.strip() for tag in clean_tags.split(',')]
        return raw_tags  

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients', [])
        instructions_data = validated_data.pop('instructions', [])
        
        recipe = Recipe.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(recipe=recipe, **ingredient_data)
        
        for instruction_data in instructions_data:
            Instruction.objects.create(recipe=recipe, **instruction_data)

        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients', [])
        instructions_data = validated_data.pop('instructions', [])
        print(validated_data)
        for attr, value in validated_data.items():
            # Only update image if provided
            if attr == 'image' and (not value or value == 'undefined'):
                continue  # Skip updating image if not provided
            setattr(instance, attr, value)

        instance.save()

        existing_ingredients = {ingredient.id: ingredient for ingredient in instance.recipe_ingredients.all()}
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            if ingredient_id and ingredient_id in existing_ingredients:
                ingredient = existing_ingredients.pop(ingredient_id)
                for attr, value in ingredient_data.items():
                    setattr(ingredient, attr, value)
                ingredient.save()
            else:
                RecipeIngredient.objects.create(recipe=instance, **ingredient_data)

        if existing_ingredients:
            RecipeIngredient.objects.filter(id__in=existing_ingredients.keys()).delete()

        existing_instructions = {instruction.id: instruction for instruction in instance.instructions.all()}
        for instruction_data in instructions_data:
            instruction_id = instruction_data.get('id')
            if instruction_id and instruction_id in existing_instructions:
                instruction = existing_instructions.pop(instruction_id)
                for attr, value in instruction_data.items():
                    setattr(instruction, attr, value)
                instruction.save()
            else:
                Instruction.objects.create(recipe=instance, **instruction_data)

        if existing_instructions:
            Instruction.objects.filter(id__in=existing_instructions.keys()).delete()

        return instance

class ReviewSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'recipe', 'user', 'rating', 'comment', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['recipe'] = self.context['recipe'] 

        return Review.objects.create(**validated_data)
