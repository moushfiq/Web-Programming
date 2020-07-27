from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("random", views.random, name="random"),
    path("wiki/<str:title>", views.info, name="info"),
    path("edit/<str:title>", views.edit, name="edit")
]
