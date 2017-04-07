from django.contrib.auth.models import User, Group 
from rest_framework import serializers 

from .models import Recipe, Ingredient 


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Ingredient 
		fields = ('name',)


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
	ingredients = IngredientSerializer(read_only=True, many=True)

	class Meta:
		model = Recipe 
		fields = ('id', 'name', 'source', 'rating', 'time_in_seconds',
			'tags', 'ingredient_list', 'isYummlyRecipe', 'isUserRecipe',
			'ingredients',)


# class UserSerializer(serializers.HyperlinkedModelSerializer):
# 	class Meta:
# 		model = User
# 		fields = ('url', 'username', 'email', 'groups',)

