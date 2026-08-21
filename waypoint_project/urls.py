from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('report/', views.report, name='report'),
    path('search/', views.search, name='search'),
    path('catalog/', views.catalog, name='catalog'),
    path('trails/', include('trails.urls')),  # <-- ADD THIS (we'll create trails/urls.py next)
    path('park/<int:park_id>/', views.park_trails, name='park_trails'),
]   