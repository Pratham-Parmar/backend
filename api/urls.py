from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('search', views.search, name='search'),
    path('add', views.add, name='add'),
    path('ports', views.ports, name='ports'),
    path('rates', views.Rates, name='rates'),
    path('logout', views.logout_user, name='logout'),
]
