"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from tutorial.views import *
from django.conf.urls.static import static
from tutorial import settings
from wallet import urls as apiEndpoint

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', index),
                  path('myfiles/<str:address>/', myfiles),
                  url(r'api/v1/', include(apiEndpoint)),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
