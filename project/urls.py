"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from api.views import RecipeStepCreateView
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from recipes import views as recipes_views
from api import views as api_views

api_router = DefaultRouter()
api_router.register('recipes', api_views.RecipeViewSet, basename='recipe')

urlpatterns = [
    path("", recipes_views.homepage, name="homepage"),
    path("recipes/", recipes_views.recipe_list, name="recipe_list"),
    path(
        "recipes/<int:pk>/",
        recipes_views.recipe_detail,
        name="recipe_detail",
    ),
    path(
        "recipes/<int:recipe_pk>/edit/", recipes_views.edit_recipe, name="edit_recipe"
    ),
    path(
        "recipes/<int:recipe_pk>/delete/",
        recipes_views.delete_recipe,
        name="delete_recipe",
    ),
    path(
        "recipes/<int:recipe_pk>/copy/", recipes_views.copy_recipe, name="copy_recipe"
    ),
    path(
        "recipes/<int:recipe_pk>/favorite/",
        recipes_views.toggle_favorite_recipe,
        name="toggle_favorite_recipe",
    ),
    path("recipes/new/", recipes_views.AddRecipeView.as_view(), name="add_recipe"),
    path(
        "recipes/<int:recipe_pk>/add_ingredient/",
        recipes_views.add_ingredient,
        name="add_ingredient",
    ),
    path(
        "recipes/<int:recipe_pk>/add_recipe_step/",
        recipes_views.add_recipe_step,
        name="add_recipe_step",
    ),
    path("recipes/search/", recipes_views.search_recipes, name="search_recipes"),
    path("recipes/random/", recipes_views.show_random_recipe, name="random_recipe"),
    path(
        "mealplan/<int:year>/<int:month>/<int:day>/",
        recipes_views.show_meal_plan,
        name="show_meal_plan",
    ),
    path("mealplan/add-remove/", recipes_views.meal_plan_add_remove_recipe),
    path("tags/<str:tag_name>/", recipes_views.view_tag, name="view_tag"),
    path("admin/", admin.site.urls),
    path("accounts/", include("registration.backends.default.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path('api/recipes/<int:pk>/images/', api_views.RecipeImageView.as_view()),
    path('api/recipe_steps/', api_views.RecipeStepCreateView.as_view()),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include(api_router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
