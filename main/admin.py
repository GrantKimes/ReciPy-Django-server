from django.contrib import admin
from . import models

# Register your models here.

class RecipeAdmin(admin.ModelAdmin):
	search_fields = ['name']

admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.Ingredient)
admin.site.register(models.RecipeVote)
admin.site.register(models.Profile)