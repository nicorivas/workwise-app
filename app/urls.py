"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .api import *
from .routing import router

urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path("logout", views.logout_view, name="logout"),
    path("", views.main, name="main"),
    path("explorer/", include("explorer.urls")),
    path("actions/", include("actions.urls")),
    path("company/", include("company.urls")),
    path("agents/", include("agents.urls")),
    path("projects/", include("projects.urls")),
    path("document/", include("document.urls")),
    path("instruction/", include("instruction.urls")),
    path("chat/", include("chat.urls")),
    path("task/", include("task.urls")),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
    path('header-company/', views.header_company, name="header_company"),
    path('test/', views.test, name="test"),
    path('component/<str:component>/', views.component, name="component_selector"),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('socket-test/', views.socket_test, name="socket-test"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)