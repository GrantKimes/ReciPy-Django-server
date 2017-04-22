from django.db import migrations, models
from django.contrib.postgres.operations import TrigramExtension

class Migration(migrations.Migration):

	dependencies = [
		('main', '0025_auto_20170421_2118'),
	]

	operations = [
		TrigramExtension(),
	]