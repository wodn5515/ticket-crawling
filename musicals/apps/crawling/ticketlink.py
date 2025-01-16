from apps.crawling.base import BaseCrawling
from datetime import datetime
import requests


class TicketlinkCrawling(BaseCrawling):
    url = "https://www.ticketlink.co.kr/help/getNoticeList"
    page = 1

    def crawl_data(self):
        while True:
            # 10페이지가 넘어갈시 중단
            if self.page > 10:
                break

            params = self._get_parameter()
            response = requests.get(url=self.url, params=params)
            results = response.json()["result"]["result"]

            for result in results:
                datum = self._result_to_data(result)
                self.data.append(datum)

            self.page += 1

    def _get_parameter(self):
        return {"page": self.page, "noticeCategoryCode": "TICKET_OPEN"}

    def _result_to_data(self, result: dict):
        name = self._get_name(result)
        site = "ticketlink"
        link = self._get_link(result)
        thumbnail = None
        open_at = self._get_open_at(result)

        if open_at > datetime.now():
            is_published = True
        else:
            is_published = False

        return {
            "name": name,
            "site": site,
            "link": link,
            "thumbnail": thumbnail,
            "open_at": open_at,
            "is_published": is_published,
        }

    def _get_name(self, result: dict):
        return result["title"].replace("\u200b", "")

    def _get_link(self, result: dict):
        nid = result["noticeId"]
        return f"https://www.ticketlink.co.kr/help/notice/{nid}"

    def _get_open_at(self, result: dict):
        timestamp = result["ticketOpenDatetime"] / 1000
        dt = datetime.fromtimestamp(timestamp)
        return dt
