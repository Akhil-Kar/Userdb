from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin_login/', views.adminDash),
    path('addadmin/', views.addAdmin),
    path('adduser/', views.addUsers),
    path('addMultiUser/', views.addMultipleUser),
    path('userinfo/', views.userInfo),
    path('logout/', views.logout_view)
]