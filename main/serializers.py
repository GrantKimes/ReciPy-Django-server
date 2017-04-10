from django.contrib.auth.models import User, Group 
from rest_framework import serializers 

from .models import Recipe, Ingredient, Profile, RecipeVote


############################################################
# Simple serializers, used for lists
############################################################

class IngredientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ingredient 
		fields = ('name',)


class RecipeSerializer(serializers.ModelSerializer):
	ingredients = IngredientSerializer(read_only=True, many=True)
	# related_recipes = RecipeSerializer(many=True)

	class Meta:
		model = Recipe 
		fields = ('id', 'name', 'is_yummly_recipe', 'is_user_recipe', 'ingredient_list',
			'ingredients', 'yummly_url', 'source', 'rating', 'time_in_seconds', 
			'yummly_image_url', 'date_created', 'date_modified',)


class ProfileSerializer(serializers.ModelSerializer):
	saved_recipes = RecipeSerializer(read_only=True, many=True)
	voted_recipes = RecipeSerializer(read_only=True, many=True)

	class Meta:
		model = Profile 
		fields = ('saved_recipes', 'voted_recipes',)


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'email',)


############################################################
# Detail serializers, show all info about a single object
############################################################

class RecipeDetailSerializer(serializers.ModelSerializer):
	ingredients = IngredientSerializer(read_only=True, many=True)
	related_recipes = RecipeSerializer(many=True)
	creator = UserSerializer()

	class Meta:
		model = Recipe 
		fields = ('id', 'name',  'creator', 'is_yummly_recipe', 'is_user_recipe', 'ingredient_list',
			'yummly_url', 'source', 'rating', 'time_in_seconds', 
			'yummly_image_url', 'bitter', 'meaty', 'salty', 'sour', 'sweet', 'piquant',
			'date_created', 'date_modified', 'ingredients', 'related_recipes',)

class RecipeCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Recipe 
		fields = ('id', 'name', 'ingredient_list',)

class UserDetailSerializer(serializers.ModelSerializer):
	profile = ProfileSerializer()

	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'profile',)









