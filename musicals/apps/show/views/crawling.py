from rest_framework.views import APIView
from rest_framework.response import Response
from apps.crawling.client import CrawlingClient


class CrawlingView(APIView):
    def get(self, request):
        crawling_client = CrawlingClient()
        crawling_client.excute_all()
        return Response({"message": "done"})
