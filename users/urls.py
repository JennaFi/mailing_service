from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, reverse_lazy

from users import views
from users.apps import UsersConfig
from users.forms import UserPasswordResetForm, UserSetPasswordForm

from users.views import UserListView, UserRegisterView, email_verification, UserUpdateProfile
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserListView.as_view(), name='users_list'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>/', views.email_verification, name='email_confirm'),
    path('edit_profile/<int:pk>/edit/', UserUpdateProfile.as_view(), name='edit_profile'),
    path('password_reset/', PasswordResetView.as_view(template_name='password_reset_form.html',
                                                      form_class=UserPasswordResetForm,
                                                      email_template_name='password_reset_email.html',
                                                      success_url=reverse_lazy('users:password_reset_done'), ),
                                                      name='password_reset',
         ),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
                                                      name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
                                                         template_name='password_reset_confirm.html',
                                                         form_class=UserSetPasswordForm,
                                                         success_url=reverse_lazy('users:password_reset_complete'), ),
                                                         name='password_reset_confirm',
         ),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
                                                                       name='password_reset_complete',
         ),

    path('users/<int:pk>/block', views.UserBlockView.as_view(), name='user_block'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
