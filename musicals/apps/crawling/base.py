from abc import ABCMeta, abstractmethod
from apps.show.models.ticketopen import TicketOpen


class BaseCrawling(metaclass=ABCMeta):
    data = []

    @abstractmethod
    def crawl_data(self):
        pass

    def _get_header(self) -> dict:
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        return {"User-Agent": user_agent}

    def data_to_db(self):
        entities = []

        for datum in self.data:
            ticket_open = TicketOpen(**datum)
            entities.append(ticket_open)

        TicketOpen.objects.bulk_create(entities, ignore_conflicts=True)
