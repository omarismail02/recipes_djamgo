from django.contrib import admin
from .models import Recipe,LikedRecipes

admin.site.register(Recipe)
admin.site.register(LikedRecipes)
