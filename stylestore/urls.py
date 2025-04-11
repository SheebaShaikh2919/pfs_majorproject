from django.contrib import admin
from django.urls import path, include 

# from django.http import HttpResponse
# from . import errorhandlers
# from django.contrib.auth.decorators import login_required
# from auth import views as auth_views

urlpatterns = [
    path('', include('main.urls')),
    path('auth/', include('auth.urls')),
    # path('admin/login/', auth_views.login),
    path('admin/', admin.site.urls),
]

handler404 = 'stylestore.errorhandlers.handler404'

# lambda request: admin.site.urls if request.user.is_superuser else HttpResponse(status=404)
# errorhandlers.handler404(request, None)

# https://pypi.org/project/django-decorator-include/


