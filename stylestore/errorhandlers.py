from django.shortcuts import render
from main import views

def handler404(request, exception, template_name='errorhandlers/404.html'):
    context = {}

    get_cart = views.getCart(request)
    if get_cart:
        context = {**context, **get_cart}

    response = render(request, template_name, context)
    response.status_code = 404
    return response

