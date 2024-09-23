from django.contrib import admin
from .models import Recipe, RecipeIngredient, Instruction, Review

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1 

class InstructionInline(admin.TabularInline):
    model = Instruction
    extra = 1  

# Custom admin class for the Recipe model
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'servings', 'prep_time', 'cooking_time', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    inlines = [RecipeIngredientInline, InstructionInline]  # Adding the inlines to Recipe admin page

# Register the other models individually
@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'quantity', 'measurement', 'recipe')
    search_fields = ('ingredient',)
    list_filter = ('recipe',)

@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'description', 'recipe')
    search_fields = ('description',)
    list_filter = ('recipe',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'rating', 'comment', 'created_at')
    search_fields = ('comment',)
    list_filter = ('recipe', 'user', 'rating')
