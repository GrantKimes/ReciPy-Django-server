from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.utils import timezone 


import logging
logger = logging.getLogger('main')


class Ingredient(models.Model):
	raw_name 	= models.CharField(max_length=200) # Lowercase and hyphens in between words
	name 		= models.CharField(max_length=200) # Capitalized and with spaces

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = self.raw_name.replace('-', ' ').title()
		return super(Ingredient, self).save(*args, **kwargs)


# Encompasses recipes from external API source, as well as user uploaded
class Recipe(models.Model):
	name	 		= models.CharField(max_length=300) 
	creator 		= models.ForeignKey('Profile', related_name='created_recipes', null=True, blank=True)
	is_yummly_recipe = models.BooleanField(default=False)
	is_user_recipe	= models.BooleanField(default=False)
	ingredient_list	= models.TextField() # String representation
	ingredients 	= models.ManyToManyField(Ingredient) # Foreign key model representation
	instructions	= models.TextField()
	photo			= models.ImageField(upload_to='recipe_photos/', null=True, blank=True)

	# Machine learning algorithm to determine similar recipes
	related_recipes	= models.ManyToManyField('self', blank=True)

	# Data included in Yummly API
	yummly_url	 	= models.CharField(max_length=300, blank=True) 
	yummly_source 	= models.CharField(max_length=300, blank=True) 
	yummly_rating	= models.IntegerField(default=0, blank=True)
	yummly_time_in_seconds	= models.IntegerField(default=0, blank=True) 
	yummly_image_url = models.CharField(max_length=300, blank=True)

	# Taste profile from Yummly
	bitter			= models.FloatField(blank=True, default=0)
	meaty			= models.FloatField(blank=True, default=0)
	salty			= models.FloatField(blank=True, default=0)
	sour			= models.FloatField(blank=True, default=0)
	sweet			= models.FloatField(blank=True, default=0)
	piquant			= models.FloatField(blank=True, default=0)

	# Timestamps
	date_created	= models.DateTimeField(editable=False)
	date_modified	= models.DateTimeField(editable=False)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.__update_timestamps()
		return super(Recipe, self).save(*args, **kwargs)

	def __update_timestamps(self):
		if not self.id: # Being created
			self.date_created = timezone.now()
		self.date_modified = timezone.now()

	def _post_save_link_ingredients(self):
		for ingredient_name in self.ingredient_list.split(' '):
			try:
				ingredient = Ingredient.objects.get(raw_name=ingredient_name)
			except Ingredient.DoesNotExist:
				ingredient = Ingredient.objects.create(raw_name=ingredient_name)

			if ingredient not in self.ingredients.all():
				self.ingredients.add(ingredient)

	def num_saves(self):
		count = self.profiles_saved.all().count()
		return count

@receiver(post_save, sender=Recipe)
def recipe_saved(sender, instance, created, **kwargs):
	instance._post_save_link_ingredients()


# Each user has a profile with additional information
class Profile(models.Model):
	user 			= models.OneToOneField(User, on_delete=models.CASCADE)
	bio 			= models.TextField(max_length=500, blank=True)
	saved_recipes 	= models.ManyToManyField(Recipe, related_name='profiles_saved', blank=True)
	
	# voted_recipes	= models.ManyToManyField(Recipe, through='RecipeVote', related_name='profiles_voted')
	liked_recipes	= models.ManyToManyField(Recipe, related_name='profiles_liked', blank=True)
	disliked_recipes = models.ManyToManyField(Recipe, related_name='profiles_disliked', blank=True)

	date_created 	= models.DateTimeField(auto_now_add=True) 
	date_modified 	= models.DateTimeField(auto_now=True) 


	def __str__(self):
		return self.user.username + "'s profile"


	# def liked_recipes(self):
	# 	liked_recipes = self.voted_recipes.filter(recipevote__liked=True)
	# 	return liked_recipes

	# def disliked_recipes(self):
	# 	disliked_recipes = self.voted_recipes.filter(recipevote__liked=False)
	# 	return disliked_recipes



# Listeners to keep user profile in sync with its corresponding user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	profile = instance.profile 
	# profile.liked_recipes = profile.voted_recipes.filter(recipevote__liked=True)
	# profile.disliked_recipes = profile.voted_recipes.filter(recipevote__liked=False)
	profile.save() 



# Keeps track of like and dislike of a user for a recipe
class RecipeVote(models.Model):
	user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	recipe 		= models.ForeignKey(Recipe, on_delete=models.CASCADE)

	liked 		= models.NullBooleanField(default=None)
	# disliked	= models.NullBooleanField()

	date_modified = models.DateTimeField(auto_now=True)


	def __str__(self):
		if self.liked == True: 		s = " likes "
		elif self.liked == False: 	s = " dislikes "
		else: 						s = " neutral to "

		return str(self.user_profile) + s + str(self.recipe)


























