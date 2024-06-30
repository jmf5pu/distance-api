from django.urls import path
import app.views as views

urlpatterns = [
    path('get_geocode/', views.get_geocode),
    path('reverse_geocode/', views.reverse_geocode),
    path('calculate_geometric_distance/', views.calculate_geometric_distance)
]
