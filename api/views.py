from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, ParseError
from rest_framework.response import Response

from api.serializers import RecipeSerializer
from recipes.models import Recipe
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

class RecipeImageView(APIView):
    # Learned how to do this from
    # https://www.goodcode.io/articles/django-rest-framework-file-upload/

    parser_classes = (FileUploadParser,)

    def put(self, request, pk):
        recipe = get_object_or_404(self.request.user.recipes, pk=pk)
        # Read the uploaded file
        if 'file' not in request.data:
            raise ParseError("Empty content")

        file = request.data['file']
        recipe.image.save(file.name, file, save=True)
        return Response(status=status.HTTP_200_OK)


        # Set image on the recipe to the uploaded file
        # Save the recipe
        # Let the user know things are good
