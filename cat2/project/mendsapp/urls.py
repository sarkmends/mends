from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/add_category/', views.add_category, name='add_category'),  # Corrected path
    path('home/add_image/', views.add_image, name='add_image'),
    path('home/view/', views.view, name='view'),
    path('home/view_category/<str:category_name>/', views.view_cate, name='view_cate'),
    path('search/', views.search, name='search'),
    path('download/<int:image_id>/', views.download_image, name='download_image')

]
