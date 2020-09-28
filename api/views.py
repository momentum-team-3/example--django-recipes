from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, ParseError
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from api.serializers import RecipeImageSerializer, RecipeSerializer, NewRecipeStepSerializer
from recipes.models import Recipe, RecipeImage
from django.shortcuts import get_object_or_404


# class RecipeListView(generics.ListCreateAPIView):
#     serializer_class = RecipeSerializer

#     def get_queryset(self):
#         return Recipe.objects.for_user(self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = RecipeSerializer

#     def get_queryset(self):
#         return self.request.user.recipes

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.action in ['list', 'create', 'retrieve']:
            return Recipe.objects.for_user(self.request.user)

        return self.request.user.recipes

class RecipeStepCreateView(generics.CreateAPIView):
    serializer_class = NewRecipeStepSerializer
    queryset = Recipe.objects.all()

    def perform_create(self, serializer):
        serializer.is_valid()
        recipe = serializer.validated_data['recipe']
        if self.request.user != recipe.user:
            raise PermissionDenied("You are not the owner of that recipe")
        serializer.save()


# class AltRecipeStepCreateView(APIView):
#     def post(self, request, recipe_pk):
#         recipe = get_object_or_404(request.user.recipes, pk=recipe_pk)
#         serializer = NewRecipeStepSerializer(data=request.data)
#         serializer.is_valid()
#         step = serializer.save(recipe=recipe)
#         return Response(NewRecipeStepSerializer(step).data)


class RecipeImageView(APIView):
    # Learned how to do this from
    # https://www.goodcode.io/articles/django-rest-framework-file-upload/

    parser_classes = (FileUploadParser,)

    def post(self, request, pk):
        recipe = get_object_or_404(self.request.user.recipes, pk=pk)
        # Read the uploaded file
        if 'file' not in request.data:
            raise ParseError("Empty content")

        file = request.data['file']
        image = RecipeImage(recipe=recipe)
        image.image.save(file.name, file, save=True)
        serializer = RecipeImageSerializer(instance=image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
