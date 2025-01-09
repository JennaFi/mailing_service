from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from users.apps import UsersConfig

from users.views import UserListView, UserRegisterView, email_verification, UserUpdateProfile
from django.contrib.auth.views import LoginView, LogoutView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserListView.as_view(), name='users'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="mailing:main_page"), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('email_confirm/<str:token>', email_verification, name='email_confirm'),
    path('edit_profile/', UserUpdateProfile.as_view(), name='edit_profile'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
