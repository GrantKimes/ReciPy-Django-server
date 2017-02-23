from django.contrib import admin
from .models import YummlyRecipe, Ingredient

# Register your models here.

admin.site.register(YummlyRecipe)
admin.site.register(Ingredient)