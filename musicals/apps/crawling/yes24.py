from apps.crawling.base import BaseCrawling
from bs4 import BeautifulSoup as bs
import requests
import re


class Yes24Crawling(BaseCrawling):
    url = "http://ticket.yes24.com/New/Notice/Ajax/axList.aspx"
    page = 1
    order = 2
    search_type = "All"
    size = 40

    def crawl_data(self):
        hdrs = self._get_header()
        while True:
            request_url = self.url
            body = self._get_body()
            response = requests.post(request_url, headers=hdrs, data=body)
            soup = bs(response.text, "html.parser")

            results = soup.select("div.noti-tbl > table > tbody > tr")[1:]

            # 데이터가 없을경우 중단
            if not results or self.page > 5:
                break

            for result in results[1:]:
                datum = self._result_to_data(result)
                self.data.append(datum)

            self.page += 1

    def _get_body(self):
        body = {
            "page": self.page,
            "size": self.size,
            "order": self.order,
            "searchType": self.search_type,
        }
        return body

    def _result_to_data(self, result):
        is_published = True

        name = self._get_name(result)
        site = "yes24"
        link = self._get_link(result)
        thumbnail = None
        open_at = self._get_open_at(result)
        has_detail_open_at = self._get_has_detail_open_at(result)

        return {
            "name": name,
            "site": site,
            "link": link,
            "thumbnail": thumbnail,
            "open_at": open_at,
            "is_published": is_published,
            "has_detail_open_at": has_detail_open_at,
        }

    def _get_open_at(self, result) -> str:
        open_at_text = result.select("td")[2].text.strip()
        return self._date_converter(open_at_text)

    def _get_has_detail_open_at(self, result) -> bool:
        return True if result.select("td")[2].select("a") else False

    def _get_link(self, result):
        return "http://ticket.yes24.com/New/Notice/NoticeMain.aspx" + result.select(
            "td"
        )[1].select_one("a").attrs.get("href")

    def _get_name(self, result):
        return result.select("td")[1].select("em")[-1].text

    def _date_converter(self, open_at_text):
        dt = re.sub(r"[(가-힣)]", "", open_at_text)
        date, time = dt.split(" ")
        year, month, day = map(int, date.split("."))
        hour, minute = map(int, time.split(":"))

        return f"{year}-{month}-{day} {hour}:{minute}:00"
