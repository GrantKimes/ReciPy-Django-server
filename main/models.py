from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.utils import timezone 



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

	related_recipes	= models.ManyToManyField('self')

	isYummlyRecipe	= models.BooleanField(default=False)
	isUserRecipe	= models.BooleanField(default=False)

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
	dateCreated		= models.DateTimeField(editable=False)
	dateModified	= models.DateTimeField(editable=False)

	def save(self, *args, **kwargs):
		# On save, update timestamps
		if not self.id:
			self.dateCreated = timezone.now()
		self.dateModified = timezone.now()
		return super(Recipe, self).save(*args, **kwargs)



# Each user has a profile with additional information
class Profile(models.Model):
	user 			= models.OneToOneField(User, on_delete=models.CASCADE)
	liked_recipes 	= models.ManyToManyField(Recipe)

	bio 			= models.TextField(max_length=500, blank=True)

	# when = models.DateTimeField('date created', auto_now_add=True) # Timestamp format for model creation


	def __str__(self):
		return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save() 
