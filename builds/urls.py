from django.urls import path
from . import views

app_name = 'builds'

urlpatterns = [
    # Authentication
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
    path('auth/profile/', views.UserProfileView.as_view(), name='profile'),
    path('auth/logout/', views.UserLogoutView.as_view(), name='logout'),
    path('auth/signup/', views.UserSignUpView.as_view(), name='signup'),
    
    # Build management
    path('', views.BuildListView.as_view(), name='build_list'),
    path('create/', views.BuildCreateView.as_view(), name='build_create'),
    
    # Build detail views (slug-based is preferred, pk-based for backwards compatibility)
    path('<slug:slug>/', views.BuildDetailView.as_view(), name='build_detail_slug'),
    path('<int:pk>/', views.BuildDetailPkView.as_view(), name='build_detail'),
    
    # Build operations
    path('<slug:slug>/edit/', views.BuildUpdateView.as_view(), name='build_update'),
    path('<slug:slug>/delete/', views.BuildDeleteView.as_view(), name='build_delete'),
    
    # Part management in builds
    path('<slug:slug>/add-part/', views.AddPartToBuildView.as_view(), name='add_part'),
    path('item/<int:item_pk>/edit/', views.UpdateBuildItemView.as_view(), name='update_item'),
    path('item/<int:item_pk>/delete/', views.DeleteBuildItemView.as_view(), name='delete_item'),
    
    # API endpoints
    path('api/parts/', views.parts_api, name='parts_api'),
    path('api/toggle-favorite-build/<slug:slug>/', views.ToggleFavoriteBuildView.as_view(), name='toggle_favorite_build'),
    path('api/toggle-favorite-part/<int:pk>/', views.ToggleFavoritePartView.as_view(), name='toggle_favorite_part'),
]
