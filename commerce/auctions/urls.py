from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.sell, name="add_product"),
    path("product/<int:prod_id>",views.prod_view,name="Prod_page"),
    path("my_list",views.mylist_page,name="mylist_page"),
    path("update/<int:prod_id>",views.update_prod,name="update_prod"),
    path("watchlist",views.watchList,name = "watchlist"),
    path("addtowatch/<int:prod_id>",views.addToWatchlist,name = "add_to_watchList")
]
