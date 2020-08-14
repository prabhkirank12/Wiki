from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("create", views.create, name="create"),
    path("search", views.search, name="search"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("randomPage", views.randomPage, name="randomPage")
]
