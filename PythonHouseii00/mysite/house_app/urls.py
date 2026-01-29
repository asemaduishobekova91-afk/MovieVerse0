from django.urls import path
from .  import views


urlpatterns = [
    path('register/', views.UserAPIView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileViewSet.as_view({'get': 'list', 'put': 'update', 'patch': 'partial_update'}), name='profile'),

    path('regions/', views.RegionListView.as_view(), name='region-list'),
    path('cities/', views.CityListView.as_view(), name='city-list'),
    path('cities/<int:pk>/', views.CityDetailView.as_view(), name='city-detail'),
    path('districts/', views.DistrictListView.as_view(), name='district-list'),
    path('properties/', views.PropertyListView.as_view(), name='property-list'),
    path('properties/<int:pk>/', views.PropertyDetailView.as_view(), name='property-detail'),
    path('properties/create/', views.PropertyCreateView.as_view(), name='property-create'),
    path('properties/<int:pk>/edit/', views.PropertyUpdateDeleteView.as_view(), name='property-edit-delete'),
    path('property-images/create/', views.PropertyImageCreateView.as_view(), name='property-image-create'),
    path('property-images/<int:pk>/delete/', views.PropertyImageDeleteView.as_view(), name='property-image-delete'),
    path('reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('reviews/create/', views.ReviewCreateView.as_view(), name='review-create'),
]
