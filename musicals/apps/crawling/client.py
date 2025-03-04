from apps.crawling.base import BaseCrawling
from apps.crawling.melon import MelonCrawling
from apps.crawling.yes24 import Yes24Crawling
from apps.crawling.ticketlink import TicketlinkCrawling


class CrawlingClient:
    def __init__(self):
        pass

    def excute(self, crawling_class: BaseCrawling):
        client = crawling_class()
        client.crawl_data()
        client.data_to_db()

    def excute_all(self):
        self.crawling_classes = [
            MelonCrawling,
            Yes24Crawling,
            TicketlinkCrawling,
        ]
        for crawling_class in self.crawling_classes:
            self.excute(crawling_class)
