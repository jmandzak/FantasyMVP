# Create your views here.
from django.shortcuts import render


def home(request):
    return render(request, "draft/home.html")


def mock_draft(request):
    return render(request, "draft/mock_draft.html")


def live_draft(request):
    return render(request, "draft/live_draft.html")


def statistics(request):
    return render(request, "draft/statistics.html")
