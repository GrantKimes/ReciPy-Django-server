from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 



class Ingredient(models.Model):
	name 	= models.CharField(max_length=200)

	def __str__(self):
		return self.name


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

	def __str__(self):
		return self.name



class UserRecipe(models.Model):
	name	 		= models.CharField(max_length=200) 
	ingredients 	= models.ManyToManyField(Ingredient)
	instructions 	= models.TextField(blank=True)
	# pictures



# Each user has a profile with additional information
class Profile(models.Model):
	user 			= models.OneToOneField(User, on_delete=models.CASCADE)
	liked_recipes 	= models.ManyToManyField(YummlyRecipe)

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
