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
	name	 		= models.CharField(max_length=200) 

	# Machine learning algorithm to determine similar recipes
	related_recipes	= models.ManyToManyField('self')

	is_yummly_recipe = models.BooleanField(default=False)
	is_user_uecipe	= models.BooleanField(default=False)

	ingredient_list	= models.TextField(blank=True) # String representation
	ingredients 	= models.ManyToManyField(Ingredient) # Foreign key model representation

	# Data included in Yummly API
	yummly_url	 	= models.CharField(max_length=200) 
	source 			= models.CharField(max_length=200) 
	rating			= models.IntegerField()
	time_in_seconds	= models.IntegerField() 
	yummly_image_url = models.CharField(max_length=200)

	# Taste profile from Yummly
	bitter			= models.FloatField(blank=True, default=0)
	meaty			= models.FloatField(blank=True, default=0)
	salty			= models.FloatField(blank=True, default=0)
	sour			= models.FloatField(blank=True, default=0)
	sweet			= models.FloatField(blank=True, default=0)
	piquant			= models.FloatField(blank=True, default=0)


	def __str__(self):
		return self.name


	# Timestamps
	date_created	= models.DateTimeField(editable=False)
	date_modified	= models.DateTimeField(editable=False)

	def save(self, *args, **kwargs):
		# On save, update timestamps
		if not self.id: # Being created
			self.date_created = timezone.now()
		self.date_modified = timezone.now()
		return super(Recipe, self).save(*args, **kwargs)


	def num_saves(self):
		count = self.profiles_saved.all().count()
		return count



# Each user has a profile with additional information
class Profile(models.Model):
	user 			= models.OneToOneField(User, on_delete=models.CASCADE)
	saved_recipes 	= models.ManyToManyField(Recipe, related_name='profiles_saved')
	voted_recipes	= models.ManyToManyField(Recipe, through='RecipeVote', related_name='profiles_voted')

	bio 			= models.TextField(max_length=500, blank=True)

	# when = models.DateTimeField('date created', auto_now_add=True) # Timestamp format for model creation


	def __str__(self):
		return self.user.username


	def liked_recipes(self):
		liked_recipes = self.voted_recipes.filter(recipevote__liked=True)
		return liked_recipes

	def disliked_recipes(self):
		disliked_recipes = self.voted_recipes.filter(recipevote__liked=False)
		return disliked_recipes



# Listeners to keep user profile in sync with its corresponding user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save() 



# Keeps track of like and dislike of a user for a recipe
class RecipeVote(models.Model):
	user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	recipe 		= models.ForeignKey(Recipe, on_delete=models.CASCADE)

	liked 		= models.NullBooleanField(default=None)
	# disliked	= models.NullBooleanField()

	date_modified = models.DateTimeField(auto_now=True)


	def __str__(self):
		if self.liked == True:
			s = " likes "
		elif self.liked == False:
			s = " dislikes "
		else:
			s = " neutral to "

		return str(self.user_profile) + s + str(self.recipe)


























