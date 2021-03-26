from django.urls import path
from travler import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # Home Page
     path('', views.home, name='home page view'),
    # REST framework URLs
    path('api/token', TokenObtainPairView.as_view()),
    path('api/token/refresh', TokenRefreshView.as_view()),
    # Post Urls
    path('post/view/<str:pk>/', views.post_view, name='post view'),
    path('post/create/', views.post_create, name='post create'),
    path('post/edit/<str:pk>/', views.post_update, name='post update'),
    path('post/delete/<str:pk>/', views.post_delete, name='post delete'),

    # Message Urls
    path('message/view/<int:pk>/', views.message_read, name='message view'),
    path('message/create/', views.message_sent, name='message create'),
    path('message/edit/<int:pk>/', views.message_edit, name='message edit'),
    path('message/delete/<int:pk>/', views.message_delete, name='message delete'),

    # Work Place Url
    path('work_place/view/<int:pk>/', views.work_place_view, name='message view'),
    path('work_place/create/', views.work_place_create, name='message create'),
    path('work_place/edit/<int:pk>/', views.work_place_update, name='message edit'),
    path('work_place/delete/<int:pk>/', views.work_place_delete, name='message delete'),

    # Visit Url
    path('visit/view/<str:pk>/', views.visit_view, name="visit-list"),
    path('visit/create/', views.visit_create, name="create-visit"),
    path('visit/edit/<str:pk>/', views.visit_update, name="visit-update"),
    path('visit/delete/<str:pk>/', views.visit_delete, name='delete visit'),

    # location URLS
    path('location/view/<str:pk>/', views.location, name="location-list"),
    path('location/create/', views.location_create, name="create-location"),
    path('location/edit/<str:pk>/', views.location_update, name="location-update"),
    path('location/delete/<str:pk>/', views.location_delete, name="location-delete"),

    # user Profile
    path('userprofile/<int:pk>/', views.userprofile, name='user profile'),
    path('userCreate/', views.userprofile_create, name='user profile create'),
    path('userEdit/<int:pk>/', views.userprofile_edit, name='user profile edit'),
    path('userDelete/<int:pk>/', views.userprofile_delete, name='user profile delete'),
]