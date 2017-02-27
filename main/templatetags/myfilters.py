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

