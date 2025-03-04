from django.urls import path
from .views.crawling import CrawlingView

urlpatterns = [
    path("crawling", CrawlingView.as_view(), name="crawling"),
]
