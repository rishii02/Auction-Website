from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create',views.create,name="create"),
    path("viewdetails/<int:pk>/",views.view,name="view"),
    path("add_item/<int:pk>/",views.add_item,name="add_item"),
    path("watch",views.watch,name="watch"),
    path("delete_item/<int:pk>",views.delete_item,name="delete_item"),
    path("delete/<int:pk>",views.delete,name="delete"),
    path("add_coment/<int:pk>",views.add_comment,name="add_comment"),
    path("view_comments<int:pk>",views.view_comments,name="view_comments"),
    path("category",views.category,name="category")
]
