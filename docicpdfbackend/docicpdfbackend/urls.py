from django.contrib import admin
from django.template.context_processors import static
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('gestionuser.urls')),
    path('accounts/', include('allauth.urls')),
    path('pdf/',include('gestionpdf.urls')),

]
