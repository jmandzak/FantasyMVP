from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("mock-draft/", views.mock_draft, name="mock_draft"),
    path("live-draft/", views.live_draft, name="live_draft"),
    path("statistics/", views.statistics, name="statistics"),
]
