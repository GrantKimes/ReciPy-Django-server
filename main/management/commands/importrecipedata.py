from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from main.models import Recipe, Ingredient

import csv
import time



class Command(BaseCommand):
	help = 'Imports recipes from a csv and links related recipes'
	recipe_file = 'data/final_recipes_v2.csv' 
	recommendation_file = 'data/final_recommendations_v2.csv'


	# Main method when command is called
	def handle(self, *args, **options):
		print("{} recipes exist in database.".format(Recipe.objects.count()))

		choice = input("Delete existing recipes and import from {}? [y/n] ".format(self.recipe_file))
		if choice == 'y':
			self.delete_existing_recipes()
			self.read_csv()

		# If already chose to delete and import recipes, automatically perform recommendations. 
		# If not, might want to just perform recommendations. 
		if choice != 'y': 
			choice = input("Import recommendations from {}? [y/n] ".format(self.recommendation_file))
		if choice == 'y':
			self.get_recommendations()


	# Read from csv file and create models in database 
	def read_csv(self):
		print('Creating recipes in database...', end='', flush=True)
		start_time = time.time()
		with open(self.recipe_file, 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='"')

			headers = next(reader)

			count = 0

			# Columns: id,bitter,meaty,salty,sour,sweet,piquant,ingredients,recipeName,smallImageUrls,totalTimeInSeconds,rating,sourceDisplayName
			for row in reader:
				# If image url is http:, change to https:
				image_url = row[9].split(' ')[0]
				if image_url[:5] == 'http:':
					image_url = "{}s{}".format(image_url[:4], image_url[4:])

				r = Recipe()
				r.yummly_url        = row[0]
				r.bitter            = row[1]
				r.meaty             = row[2]
				r.salty             = row[3]
				r.sour              = row[4]
				r.sweet             = row[5]
				r.piquant           = row[6]
				r.ingredient_list   = row[7].lower()
				r.name              = row[8]
				r.yummly_image_url  = image_url 
				# r.yummly_time_in_seconds   = row[10] if (row[10] != '') else 0
				r.yummly_rating     = row[11]
				r.yummly_source     = row[12]
				r.is_yummly_recipe 	= True
				r.save()

				# For each ingredient in list, add to many to many field
				# self.add_ingredients(r)
				# Now managed in Recipe post_save method


				count += 1
				if count % 100 == 0:
					print('.', end='', flush=True)

		print("")
		self.stdout.write(self.style.SUCCESS('Finished importing {} into db: {} recipes, {} ingredients (took {} minutes).'\
			.format(self.recipe_file, Recipe.objects.count(), Ingredient.objects.count(), int((time.time()-start_time)/60)) ))


	# Delete existing values in DB, should change to prompt to confirm deletion
	def delete_existing_recipes(self):
		print("Deleting {} recipes".format(Recipe.objects.count()), end='', flush=True)
		count = 0
		for recipe in Recipe.objects.all():
			recipe.delete()
			count += 1
			if count % 100 == 0: print('.', end='', flush=True)
		print("")

		print("Deleting {} ingredients".format(Ingredient.objects.count()), end='', flush=True)
		count = 0
		for ingredient in Ingredient.objects.all():
			ingredient.delete()
			count += 1
			if count % 100 == 0: print('.', end='', flush=True)
		print("")


	def get_recommendations(self):
		print('Linking recommendations...', end='', flush=True)
		start_time = time.time()
		with open(self.recommendation_file, 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='"')

			headers = next(reader)

			count = 0

			for row in reader:
				try:
					currRecipe = Recipe.objects.get(yummly_url=row[0])
					for i in range(1, 5):
						relatedRecipe = Recipe.objects.get(yummly_url=row[i])
						currRecipe.related_recipes.add(relatedRecipe)
				except Recipe.DoesNotExist:
					print("    - Couldn't find " + row[i])
					return 


				count += 1
				if count % 100 == 0:
					print('.', end='', flush=True)

			print("")
			self.stdout.write(self.style.SUCCESS('Finished linking recommended recipes (took {} minutes).'.format(int((time.time()-start_time)/60)) ))



























