from apps.crawling.base import BaseCrawling
from apps.show.models.ticketopen import TicketOpen
from bs4 import BeautifulSoup as bs
import requests
import re


class MelonCrawling(BaseCrawling):
    url = "https://ticket.melon.com/csoon/ajax/listTicketOpen.htm"
    page_index = 1
    order_type = 2
    genre_code = "GENRE_ALL"

    def crawl_data(self):
        hdrs = self._get_header()
        while True:
            request_url = self.url
            body = self._get_body()
            response = requests.post(request_url, headers=hdrs, data=body)
            soup = bs(response.text, "html.parser")

            results = soup.select("ul.list_ticket_cont > li")

            # 데이터가 없을경우 중단
            if not results or self.page_index > 100:
                break

            for result in results:
                datum = self._result_to_data(result)
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

    def _result_to_data(self, result):
        is_published = True

        name = self._get_name(result)
        site = "melon"
        link = self._get_link(result)
        thumbnail = self._get_thumbnail(result)
        has_detail_open_at, open_at = self._get_open_at(result)

        if open_at is None and has_detail_open_at is False:
            is_published = False

        return {
            "name": name,
            "site": site,
            "link": link,
            "thumbnail": thumbnail,
            "open_at": open_at,
            "is_published": is_published,
            "has_detail_open_at": has_detail_open_at,
        }

    def _get_open_at(self, result) -> tuple[bool, str | None]:
        open_at_text = result.select_one("span.date").text
        if re.match(r"오픈일정", open_at_text):
            return True, None
        elif re.match(r"추후공지", open_at_text):
            return False, None
        else:
            return False, self._date_converter(open_at_text)

    def _get_link(self, result):
        return (
            "https://ticket.melon.com/csoon"
            + result.select_one("a.tit").attrs.get("href")[1:]
        )

    def _get_name(self, result):
        return result.select_one("a.tit").text.strip()

    def _get_thumbnail(self, result):
        thumbnail = re.match(
            r"^[A-Za-z0-9:/.-]+\.(png|jpg|JPG|PNG)",
            result.select_one("a.poster > img").attrs.get("src"),
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
