from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_asset, name='upload_asset'),
    path('edit/<str:asset_id>/', views.edit_asset, name='edit_asset'),
]
