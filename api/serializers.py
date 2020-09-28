from rest_framework import serializers
from recipes.models import Recipe, RecipeImage, RecipeStep, Ingredient

class NestedIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['amount', 'item']

class NestedRecipeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = ['text', 'order']

class RecipeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    ingredients = NestedIngredientSerializer(many=True, read_only=True)
    steps = NestedRecipeStepSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'username',
            'title',
            'prep_time_in_minutes',
            'cook_time_in_minutes',
            'public',
            'ingredients',
            'steps',
        ]

class RecipeImageSerializer(serializers.ModelSerializer):
    image_thumb = serializers.ImageField()

    class Meta:
        model = RecipeImage
        fields = ['pk', 'recipe', 'image', 'image_thumb']

class NewRecipeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = ['pk', 'recipe', 'text',]
