from rest_framework import serializers
from recipes.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'username',
            'title',
            'prep_time_in_minutes',
            'cook_time_in_minutes',
            'public',
        ]
