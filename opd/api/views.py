from django.contrib.auth import authenticate
from django.http.response import Http404
from rest_framework import serializers
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


# # NOTE: this is read_only (get request) portion of the doctors with the function based view
# @api_view(["GET"])
# def doctor_list(request):
#     if request.method == "GET":
#         doctors = Doctor.objects.all()
#         serializer = DoctorSerializer(doctors, many=True, context={"request": request})
#         return Response(serializer.data, status=status.HTTP_200_OK)


# NOTE: this has the same functionality as the doctor_list method as above but with less no of code
# class DoctorList(generics.ListAPIView):
#     queryset = Doctor.objects.all()
#     serializer_class = DoctorSerializer
#

# NOTE: this is the doctor detail profile using the APIView class inheritence
# class DoctorDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Doctor.objects.get(id=pk)
#         except Doctor.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk):
#         doctor = self.get_object(pk)
#         serializer = DoctorDetailSerializer(doctor, context={"request": request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk):
#         doctor = self.get_object(pk)
#         serializer = DoctorDetailSerializer(
#             doctor, request.data, context={"request": request}
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         doctor = self.get_object(pk)
#         doctor.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#


# class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Doctor.objects.all()
#     serializer_class = DoctorDetailSerializer
#


from .serializers import (
    DoctorSerializer,
    DoctorDetailSerializer,
    RegistrationSerializer,
)
from opd.models import Doctor


@api_view(["POST"])
def doctor_login(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credential"}, status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def doctor_logout(request):
    try:
        token = request.auth
        token.delete()
        return Response({"message": "Logout Successfull"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def doctor_registration(request):
    data = {}
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Registration Successfull"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    pass
