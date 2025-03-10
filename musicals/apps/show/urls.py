from django.urls import path
from apps.show.views.crawling import CrawlingView
from apps.show.views.ticketopen import TicketOpenView

urlpatterns = [
    path("crawling", CrawlingView.as_view(), name="crawling"),
    path("opens", TicketOpenView.as_view(), name="ticketopen"),
]
