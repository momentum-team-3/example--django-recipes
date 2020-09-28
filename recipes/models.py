from django.db import models
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
from users.models import User
from ordered_model.models import OrderedModel
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill



class Tag(models.Model):
    tag = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tag


def make_fake_recipe(user):
    from faker import Faker
    import random

    f = Faker()
    recipe = Recipe(
        title=(" ".join(f.words(3))),
        user=user,
        prep_time_in_minutes=random.randint(10, 60),
        cook_time_in_minutes=random.randint(10, 120),
        public=(random.random() < 0.8),
    )
    recipe.save()
    for _ in range(random.randint(2, 8)):
        ingredient = Ingredient(
            recipe=recipe, amount=str(random.randint(1, 10)), item=f.word()
        )
        ingredient.save()
    for i in range(random.randint(3, 6)):
        step = RecipeStep(recipe=recipe, text=f.paragraph())
        step.order = i + 1
        step.save()


class RecipeQuerySet(models.QuerySet):
    def for_user(self, user):
        if user.is_authenticated:
            recipes = self.filter(Q(public=True) | Q(user=user))
        else:
            recipes = self.filter(public=True)
        return recipes

    def search(self, search_term):
        recipes = self.annotate(
            search=SearchVector(
                "title", "ingredients__item", "steps__text", "tags__tag"
            )
        )
        recipes = recipes.filter(search=search_term).distinct("pk")
        return recipes

    def public(self):
        return self.filter(public=True)


class Recipe(models.Model):
    objects = RecipeQuerySet.as_manager()

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length=255)
    prep_time_in_minutes = models.PositiveIntegerField(null=True, blank=True)
    cook_time_in_minutes = models.PositiveIntegerField(null=True, blank=True)
    tags = models.ManyToManyField(to=Tag, related_name="recipes", blank=True)
    original_recipe = models.ForeignKey(
        to="self", on_delete=models.SET_NULL, null=True, blank=True
    )
    public = models.BooleanField(default=True)
    favorited_by = models.ManyToManyField(
        to=User, related_name="favorite_recipes", blank=True
    )

    def get_tag_names(self):
        tag_names = []
        for tag in self.tags.all():
            tag_names.append(tag.tag)

        return " ".join(tag_names)

    def set_tag_names(self, tag_names):
        """
        Given a string of tag names separated by spaces,
        create any tags that do not currently exist, and associate all
        of these tags with the recipe.
        """
        tag_names = tag_names.split()
        tags = []
        for tag_name in tag_names:
            tag = Tag.objects.filter(tag=tag_name).first()
            if tag is None:
                tag = Tag.objects.create(tag=tag_name)
            tags.append(tag)
        self.tags.set(tags)

    def total_time_in_minutes(self):
        if self.cook_time_in_minutes is None or self.prep_time_in_minutes is None:
            return None
        return self.cook_time_in_minutes + self.prep_time_in_minutes

    def __str__(self):
        return self.title


class RecipeImage(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name="images")
    alt_text = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="recipe_images/", null=True, blank=True)
    image_medium = ImageSpecField(source='image', processors=[ResizeToFit(300, 300)], format='JPEG', options={'quality': 80})
    image_thumb = ImageSpecField(source='image', processors=[ResizeToFill(150, 150)], format='JPEG', options={'quality': 80})


class Ingredient(models.Model):
    recipe = models.ForeignKey(
        to=Recipe, on_delete=models.CASCADE, related_name="ingredients"
    )
    amount = models.CharField(max_length=20)
    item = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.amount} {self.item}"


class RecipeStep(OrderedModel):
    recipe = models.ForeignKey(
        to=Recipe, on_delete=models.CASCADE, related_name="steps"
    )
    text = models.TextField()
    order_with_respect_to = "recipe"

    def __str__(self):
        return f"{self.order} {self.text}"


class MealPlan(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="meal_plans"
    )
    date = models.DateField(verbose_name="Date for plan")
    recipes = models.ManyToManyField(to=Recipe, related_name="meal_plans")

    class Meta:
        unique_together = [
            "user",
            "date",
        ]


def search_recipes_for_user(user, search_term):
    recipes = get_available_recipes_for_user(Recipe.objects, user)
    # recipes = recipes.annotate(
    #     search=SearchVector("title", "ingredients__item", "steps__text", "tags__tag")
    # )
    recipes = recipes.filter(search=search_term).distinct("pk")
    # recipes = recipes.filter(title__search=search_term).distinct()
    return recipes


def get_available_recipes_for_user(queryset, user):
    if user.is_authenticated:
        recipes = queryset.filter(Q(public=True) | Q(user=user))
    else:
        recipes = queryset.filter(public=True)
    return recipes
