from django.urls import path
from users.apps import UsersConfig
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import UsersListAPIView, UserCreateAPIView, UserUpdateAPIView, UserDeleteAPIView, UserDetailAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("users/", UsersListAPIView.as_view(), name="list_view"),
    path("users/create/", UserCreateAPIView.as_view(), name="create_view"),
    path("users/update/<int:pk>/", UserUpdateAPIView.as_view(), name="update_view"),
    path("users/delete/<int:pk>/", UserDeleteAPIView.as_view(), name="delete_view"),
    path("users/detail/<int:pk>/", UserDetailAPIView.as_view(), name="detail_view"),
]
