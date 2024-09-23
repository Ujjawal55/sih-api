from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DoctorSerializer
from opd.models import Doctor


@api_view(["GET"])
def doctor_list(request):
    if request.method == "GET":
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
