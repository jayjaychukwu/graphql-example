"""
URL configuration for graph_eg project.

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
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView  # View that handles the UI

from graph_eg.schema import schema  # schema we want to query

urlpatterns = [
    path("admin/", admin.site.urls),
    # this URL will provide a UI that is used to query the database and interact with the GraphQL API
    path("", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
