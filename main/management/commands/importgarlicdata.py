from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from main.models import Recipe, Ingredient

import csv

filename = 'data/garlic_ingredients.csv' 

class Command(BaseCommand):
    help = 'Imports a csv file into database'

    # Main method when command is called
    def handle(self, *args, **options):
    	self.delete_existing_recipes()
    	self.read_file()


    def read_file(self):
    	with open(filename, 'r') as csvfile:
    		reader = csv.reader(csvfile, delimiter='|', quotechar='"')

    		count = 0
    		for row in reader:
    			count += 1
    			if count == 1: # First row is column names
    				continue

    			r = Recipe()
    			




    # Delete existing values in DB, should change to prompt to confirm deletion
    def delete_existing_recipes(self):
        self.stdout.write(self.style.NOTICE("Deleting {} recipes".format(YummlyRecipe.objects.count())))
        for recipe in Recipe.objects.all():
            recipe.delete()

        self.stdout.write(self.style.NOTICE("Deleting {} ingredients".format(Ingredient.objects.count())))
        for ingredient in Ingredient.objects.all():
            ingredient.delete()
