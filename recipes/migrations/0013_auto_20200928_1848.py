# Generated by Django 3.1.1 on 2020-09-28 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_recipe_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='image',
        ),
        migrations.CreateModel(
            name='RecipeImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alt_text', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='recipe_images/')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='recipes.recipe')),
            ],
        ),
    ]
