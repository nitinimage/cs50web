from django.urls import path

from . import views

# app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.page, name="page"),
    path("wiki/edit/<str:title>",views.edit_page,name="edit_page"),
    path("create",views.create, name="create"),
    path("create_error",views.create_error, name="create_error"),
    path("search",views.search, name="search"),
    path("random",views.random_page, name="random")
]


