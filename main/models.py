from django.db import models

# Create your models here.


class Ingredient(models.Model):
	name 			= models.CharField(max_length=200)

	def __str__(self):
		return self.name



# Uneeded
class YummlyRecipeManager(models.Manager):
	def create_recipe(self, url, name, source, rating, time_in_seconds, tags, ingredient_list):
		recipe = self.create(url=url, name=name, source=source, rating=rating, time_in_seconds=time_in_seconds, tags=tags, ingredient_list=ingredient_list)
		recipe.save()
		return recipe

class YummlyRecipe(models.Model):
	url	 			= models.CharField(max_length=200) 
	name	 		= models.CharField(max_length=200) 
	source 			= models.CharField(max_length=200) 
	rating			= models.IntegerField()
	time_in_seconds	= models.IntegerField() 
	tags 			= models.TextField(blank=True)
	ingredient_list	= models.TextField(blank=True)

	ingredients 	= models.ManyToManyField(Ingredient)



	# instructions	= models.TextField(blank=True)
	# picture			= models.ImageField(max_length=200, blank=True, null=True)
	# tags			= models.CharField(max_length=200, blank=True)
	# user_created	= models.BooleanField()

	objects = YummlyRecipeManager()

	def __str__(self):
		return self.name



# Set up users

# class Review(models.Model):