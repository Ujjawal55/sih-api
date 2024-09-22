from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def home_page(request):
    return Response("<h2>home page</h2>")
