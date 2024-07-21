from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("mock-draft/", views.mock_draft, name="mock_draft"),
    path("live-draft/", views.live_draft, name="live_draft"),
    path("all-statistics/", views.all_statistics, name="all_statistics"),
    path("qb-statistics/", views.qb_statistics, name="qb_statistics"),
    path("rb-statistics/", views.rb_statistics, name="rb_statistics"),
    path("wr-statistics/", views.wr_statistics, name="wr_statistics"),
    path("te-statistics/", views.te_statistics, name="te_statistics"),
    path("k-statistics/", views.k_statistics, name="k_statistics"),
    path("def-statistics/", views.def_statistics, name="def_statistics"),
]
