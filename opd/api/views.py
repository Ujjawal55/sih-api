from django.http.response import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DoctorSerializer, DoctorDetailSerializer
from opd.models import Doctor
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


@api_view(["GET"])
def doctor_list(request):
    if request.method == "GET":
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorDetail(APIView):
    def get_object(self, pk):
        try:
            return Doctor.objects.get(id=pk)
        except Doctor.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        doctor = self.get_object(pk)
        serializer = DoctorDetailSerializer(doctor, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        doctor = self.get_object(pk)
        serializer = DoctorDetailSerializer(
            doctor, request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        doctor = self.get_object(pk)
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
