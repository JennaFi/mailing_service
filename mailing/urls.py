from django.conf.urls.static import static
from django.urls import path, include
from mailing.apps import MailingConfig
from mailing.views import MainView, RecipientListView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView, \
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, MailingListView, MailingDetailView, \
    MailingCreateView, MailingUpdateView, MailingDeleteView, MailingAttemptsListView, UserMailingView
from mailing_service import settings

app_name = MailingConfig.name

urlpatterns = [
    path('', MainView.as_view(), name='main_page'),
    path('recipient_list/', RecipientListView.as_view(), name='recipient_list'),
    path('recipient/create/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient/<int:pk>/update/', RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/<int:pk>/delete/', RecipientDeleteView.as_view(), name='recipient_delete'),
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing_attempts_list/', MailingAttemptsListView.as_view(), name='mailing_attempts_list'),
    path('user_mailing/', UserMailingView.as_view(), name='user_mailing')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
