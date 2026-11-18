from django.urls import path
from .views import ChatbotAskView, ChatbotHistoryView

urlpatterns = [
    path("ask/", ChatbotAskView.as_view(), name="chatbot-ask"),
    path("history/", ChatbotHistoryView.as_view(), name="chatbot-history"),
]
