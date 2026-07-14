"""URL routes for chat functionality."""
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('conversations/', views.ConversationListView.as_view(), name='conversation-list'),
    path('conversations/<int:conversation_id>/messages/', views.ConversationMessagesView.as_view(), name='conversation-messages'),
    path('conversations/<int:conversation_id>/read/', views.MarkMessagesReadView.as_view(), name='mark-read'),
    path('send/', views.SendMessageView.as_view(), name='send-message'),
    path('unread/', views.UnreadCountView.as_view(), name='unread-count'),
]
