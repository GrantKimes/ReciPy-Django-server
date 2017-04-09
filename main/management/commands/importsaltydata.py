from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from main.models import Recipe, Ingredient

import csv



class Command(BaseCommand):
	help = 'Imports a csv file into database'
	filename = 'data/salty_recipes_2.csv' 

	# Main method when command is called
	def handle(self, *args, **options):
		print("{} recipes exist in database.".format(Recipe.objects.count()))

		choice = input("Delete existing recipes and import from {}? [y/n] ".format(self.filename))
		if choice == 'y':
			self.delete_existing_recipes()
			self.read_csv()

		# If already chose to delete and import recipes, automatically perform recommendations. 
		# If not, might want to just perform recommendations. 
		if choice != 'y': 
			choice = input("Import recommendations from data/id_recc_pairing.csv? [y/n] ")
		if choice == 'y':
			self.get_recommendations()


	# Read from csv file and create models in database 
	def read_csv(self):
		print('Creating recipes in database...', end='', flush=True)
		with open(self.filename, 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='"')

			headers = next(reader)

			count = 0

			# id,bitter,meaty,salty,sour,sweet,piquant,ingredients,recipeName,smallImageUrls,totalTimeInSeconds,rating,sourceDisplayName
			for row in reader:
				row[9] = row[9].split(' ')[0] # Only use first image url in array, there's only ever one


				r = Recipe()
				r.yummly_url        = row[0]
				r.bitter            = row[1]
				r.meaty             = row[2]
				r.salty             = row[3]
				r.sour              = row[4]
				r.sweet             = row[5]
				r.piquant           = row[6]
				r.ingredient_list   = row[7].lower()
				r.name              = row[8].replace('"', '')
				r.yummly_image_url  = row[9]
				r.time_in_seconds   = 0 #row[10]
				r.rating            = 0 #row[11]
				r.source            = row[12]
				r.is_yummly_recipe = True
				r.save()

				# for each ingredient in list, add to many to many field
				self.add_ingredients(r)


				count += 1
				if count % 100 == 0:
					print('.', end='', flush=True)

		print("")
		self.stdout.write(self.style.SUCCESS('Finished importing {} into db ({} recipes, {} ingredients).'\
			.format(self.filename, Recipe.objects.count(), Ingredient.objects.count()) ))


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

	# For each ingredient in ingredient list string, associate with an Ingredient model in DB
	def add_ingredients(self, recipe):
		for ingredient_name in recipe.ingredient_list.split(" "):
			# If ingredient model already exists in database, add to recipe. Otherwise, create ingredient
			try:
				ingredient = Ingredient.objects.get(raw_name=ingredient_name)

			except ObjectDoesNotExist:
				ingredient = Ingredient()
				ingredient.raw_name = ingredient_name
				ingredient.save()

			recipe.ingredients.add(ingredient)


	def get_recommendations(self):
		print('Linking recommendations...', end='', flush=True)
		with open('data/id_recc_pairing.csv', 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='"')

			headers = next(reader)

			count = 0

			for row in reader:
				try:
					currRecipe = Recipe.objects.get(yummly_url=row[0])
					# print("  + Found " + str(currRecipe))
					for i in range(1, 4):
						# print("  Looking for related recipe " + row[i])
						relatedRecipe = Recipe.objects.get(yummly_url=row[i])
						# print("    + Found related recipe " + str(relatedRecipe))
						currRecipe.related_recipes.add(relatedRecipe)
					# print(currRecipe)
				except Recipe.DoesNotExist:
					print("    - Couldn't find " + row[i])
					return 


				count += 1
				if count % 100 == 0:
					print('.', end='', flush=True)

			print("")
			self.stdout.write(self.style.SUCCESS('Finished linking recommended recipes.'))



























