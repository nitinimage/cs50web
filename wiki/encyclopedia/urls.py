from django.urls import path

from . import views

# app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.page, name="page"),
    path("wiki/edit/<str:title>",views.edit_page,name="edit_page"),
    path("wiki/delete/<str:title>",views.delete_page,name="delete_page"),
    path("create",views.create, name="create"),
    path("error/<str:error>",views.error, name="error"),
    path("search",views.search, name="search"),
    path("random",views.random_page, name="random")
]


