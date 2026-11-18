"""
URL configuration for AI-Powered University Student Assistant (SWE488).
"""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health_check(request):
    return JsonResponse(
        {
            "status": "ok",
            "project": "AI-Powered University Student Assistant (SWE488)",
            "endpoints": {
                "auth": "/api/auth/",
                "courses_exams_announcements": "/api/",
                "chatbot": "/api/chatbot/",
                "admin": "/admin/",
            },
        }
    )


urlpatterns = [
    path("", health_check, name="health-check"),
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.users.urls")),
    path("api/", include("apps.courses.urls")),
    path("api/chatbot/", include("apps.chatbot.urls")),
]
