from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.show.services.ticketopen import TicketOpenService


class TicketOpenView(APIView):
    def get(self, request, *args, **kwargs):
        period_str = self.request.GET.get("period", "today")

        service = TicketOpenService(period_str=period_str)
        results = service.get_ticketopens()

        return Response(status=status.HTTP_200_OK, data=results)
