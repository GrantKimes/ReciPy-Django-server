from django import template 

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
	return value.as_widget(attrs={'class': arg})

@register.filter(name='bootstrap_alerts')
def bootstrap_alerts(value):
	if value == 'error':
		return 'danger'
	else:
		return value

@register.filter(name='list_ingredients')
def list_ingredients(ingredientList):
	result = '<ul class="list-group">'
	for ingredient in ingredientList:
		result += '<li class="list-group-item">{}</li>'.format(ingredient.name)
	result += '</ul>'

	result = ''
	for ingredient in ingredientList:
		result += ingredient.name + ', '

	result = result[:-2]
	return result