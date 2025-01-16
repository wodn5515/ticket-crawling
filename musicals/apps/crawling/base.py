from abc import ABCMeta, abstractmethod
from apps.show.models.ticketopen import TicketOpen


class BaseCrawling(metaclass=ABCMeta):
    data = []

    @abstractmethod
    def crawl_data(self):
        pass

    def data_to_db(self):
        entities = []

        for datum in self.data:
            ticket_open = TicketOpen(
                name=datum["name"],
                site=datum["site"],
                link=datum["link"],
                thumbnail=datum["thumbnail"],
                open_at=datum["open_at"],
                is_published=datum["is_published"],
            )
            entities.append(ticket_open)

        TicketOpen.objects.bulk_create(entities, ignore_conflicts=True)
