from datetime import datetime, date, timedelta
from apps.show.models.ticketopen import TicketOpen


class TicketOpenService:
    model = TicketOpen

    def __init__(self, period_str):
        self.period_str = period_str

    def _get_period(self):
        today = date.today()
        if self.period_str == "today":
            start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            end_datetime = today.strftime("%Y-%m-%d") + " 23:59:59"
        elif self.period_str == "week":
            start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            end_date = today + timedelta(days=7)
            end_datetime = end_date.strftime("%Y-%m-%d") + " 23:59:59"

        return start_datetime, end_datetime

    def get_ticketopens(self):
        start_dt, end_dt = self._get_period()
        queryset = self._select_ticketopens(start_dt, end_dt)
        results = self._list_serializer(queryset)
        return results

    def _select_ticketopens(self, start_dt, end_dt):
        results = self.model.objects.filter(
            open_at__gte=start_dt, open_at__lte=end_dt, is_published=True
        ).order_by("open_at")
        return results

    def _list_serializer(self, queryset):
        results = {
            "results": [self._instance_serializer(instance) for instance in queryset]
        }
        return results

    def _instance_serializer(self, instance: TicketOpen):
        data = {
            "id": instance.pk,
            "name": instance.name,
            "open_at": instance.open_at.strftime("%m월 %d일 %H시 %M시"),
            "link": instance.link,
        }
        return data
