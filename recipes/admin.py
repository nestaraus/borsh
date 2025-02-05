from django.contrib import admin
from .models import Recipe, Category

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'cooking_time')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)