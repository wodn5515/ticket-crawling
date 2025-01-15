from apps.crawling.base import BaseCrwaling
from apps.show.models.ticketopen import TicketOpen
from bs4 import BeautifulSoup as bs
import requests
import re


class MelonCrwaling(BaseCrwaling):
    url = "https://ticket.melon.com/csoon/ajax/listTicketOpen.htm"
    page_index = 1
    order_type = 2
    genre_code = "GENRE_ALL"
    data = []

    def crawl_data(self):
        hdrs = self._get_header()
        while True:
            request_url = self.url
            body = self._get_body()
            response = requests.post(request_url, headers=hdrs, data=body)
            soup = bs(response.text, "html.parser")

            elements = soup.select("ul.list_ticket_cont > li")

            # 데이터가 없을경우 중단
            if not elements:
                break

            for element in elements:
                datum = self._element_to_data(element)
                self.data.append(datum)

            self.page_index += 10

    def _get_header(self):
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        return {"User-Agent": user_agent}

    def _get_body(self):
        body = {
            "pageIndex": self.page_index,
            "orderType": self.order_type,
            "schGcode": self.genre_code,
        }
        return body

    def _element_to_data(self, element):
        name = self._get_name(element)
        site = "melon"
        link = self._get_link(element)
        thumbnail = self._get_thumbnail(element)
        open_at = self._get_open_at(element)

        if open_at is False:
            is_published = False
            open_at = None
        else:
            is_published = True

        return {
            "name": name,
            "site": site,
            "link": link,
            "thumbnail": thumbnail,
            "open_at": open_at,
            "is_published": is_published,
        }

    def _get_open_at(self, element):
        open_at_text = element.select_one("span.date").text
        if re.match(r"오픈일정", open_at_text):
            return None
        elif re.match(r"추후공지", open_at_text):
            return False
        else:
            return self._date_converter(open_at_text)

    def _get_link(self, element):
        return (
            "https://ticket.melon.com/csoon"
            + element.select_one("a.tit").attrs.get("href")[1:]
        )

    def _get_name(self, element):
        return element.select_one("a.tit").text.strip()

    def _get_thumbnail(self, element):
        thumbnail = re.match(
            r"^[A-Za-z0-9:/.-]+\.(png|jpg|JPG|PNG)",
            element.select_one("a.poster > img").attrs.get("src"),
        )
        if thumbnail:
            return thumbnail.group()
        else:
            return None

    def _date_converter(self, open_at_text):
        dt = re.sub(r"[(가-힣)]", "", open_at_text)
        date, time = dt.split(" ")
        year, month, day = map(int, date.split("."))
        hour, minute = map(int, time.split(":"))

        return f"{year}-{month}-{day} {hour}:{minute}:00"

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
