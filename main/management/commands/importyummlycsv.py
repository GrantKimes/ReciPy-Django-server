from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from main.models import Recipe, Ingredient

import csv

filename = 'data/yummly_recipe_data.csv' # make this as an argument


class Command(BaseCommand):
    help = 'Imports a csv file into database'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)


    # Delete existing values in DB, should change to prompt to confirm deletion
    def delete_existing(self):
        self.stdout.write(self.style.NOTICE("Deleting {} recipes".format(Recipe.objects.count())))
        for recipe in Recipe.objects.all():
            recipe.delete()

        self.stdout.write(self.style.NOTICE("Deleting {} ingredients".format(Ingredient.objects.count())))
        for ingredient in Ingredient.objects.all():
            ingredient.delete()


    # For each ingredient in recipe, associate with an Ingredient model in DB
    def add_ingredients(self, recipe):
        # self.stdout.write("Ingredient list: {}".format(recipe.ingredient_list))

        for ingredient_name in recipe.ingredient_list.replace("'", "").split(", "):
            # self.stdout.write(ingredient_name)

            try:
                ingredient = Ingredient.objects.get(name=ingredient_name)
                # ingredient already exists in database
                # self.stdout.write("EXISTS: {}".format(ingredient_name))

            except ObjectDoesNotExist:
                # ingredient does not exist in database, add it
                # self.stdout.write("NOT EXISTS: {}".format(ingredient_name))
                ingredient = Ingredient()
                ingredient.name = ingredient_name
                ingredient.save()

            recipe.ingredients.add(ingredient)



    # Main method when command is called
    def handle(self, *args, **options):

        self.delete_existing()

        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter='|', quotechar='"')

            count = 0
            for row in reader:
                if row[4] == '': # If empty value for calories, default
                    row[4] = 0
                
                r = Recipe()
                r.url           = row[0]
                r.name          = row[1]
                r.source        = row[2]
                r.rating        = row[3]
                r.time_in_seconds = row[4]
                r.tags          = row[5]
                r.ingredient_list = row[6]
                r.isYummlyRecipe = True
                r.save()

                # for each ingredient in list, add to many to many field
                self.add_ingredients(r)


                count += 1
                if count >= 100: break



        self.stdout.write(self.style.SUCCESS('Finished importing {} into db ({} recipes, {} ingredients).'\
            .format(filename, Recipe.objects.count(), Ingredient.objects.count()) ))

