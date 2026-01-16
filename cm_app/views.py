from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from .utils.emailUtils import *
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import make_password
from .models import *
from .serializers import *
# Code Added by Tejasve on 26-05-2024
# Reason - for functionality of Password Reset
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
User = get_user_model()

# End of Code Added by Tejasve on 26-05-2024
# Reason - for functionality of Password Reset


class SignupAPIView(APIView):
    def post(self, request):

        data = {
            "username": request.data["email"],
            "email": request.data["email"],
            "password": make_password(request.data["password"]),
            "confirm_password": request.data["confirm_password"],
            "contact_number": request.data["contact_number"],
            "first_name": request.data["first_name"],
            "last_name": request.data["last_name"],
        }
        userSerializer = UserSerializer(data=data)

        try:
            if userSerializer.is_valid(raise_exception=True):
                userSerializer.save()
                return Response("Registration done successfully", 200)
        except Exception as e:
            if "email" in userSerializer.errors.keys():
                return Response("Email already registered", 500)
            return Response(userSerializer.errors, 500)


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                refresh = RefreshToken.for_user(user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {"first_name": user.first_name,
                             "last_name": user.last_name,
                             "email": user.email,
                             "contact_number": user.contact_number}
                })
            else:
                return Response("Invalid username or password", 401)
        except:
            return Response("User not found", 404)


class TokenAPIVIew(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            refresh = RefreshToken(refresh_token)

            return Response({
                'refresh':     str(refresh),
                'access': str(refresh.access_token),
            })
        except Exception as e:
            return Response({
                "message": "Token expired"
            }, 500)


class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        userSerializer = UserSerializer(request.user)
        return Response({
            "user": {"first_name": userSerializer.data['first_name'],
                     "last_name": userSerializer.data['last_name'],
                     "email": userSerializer.data['email'],
                     "contact_number": userSerializer.data['contact_number']}
        }, 200)


# Code added by Tejasve Gupta on 26-05-2024
# Reason - Functionality of Forget Password
class PasswordResetAPIView(APIView):
    def post(self, request):
        if request.data["postFor"] == "email":
            email = request.data["data"]["email"]
            try:
                user = User.objects.get(email=email)
                otp = generate_otp()
                user.otp = otp
                user.save()
                send_otp(email, otp)
                return JsonResponse({'msg': 'OTP sent successfully'})
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

        else:

            otp = request.data["data"]['otp']
            email = request.data["data"]['email']
            user = User.objects.filter(email=email, otp=otp).first()
            if not user:
                return Response({"error": "Invalid OTP or User not found"}, status=400)
            user.otp = None
            user.save()
            return Response({"msg": "OTP verified successfully"}, status=200)

    def put(self, request):

        email = request.data['email']
        password = request.data['password']

        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return JsonResponse({'msg': 'Password updated successfully'})
        except Exception as e:
            return JsonResponse({'error': 'Invalid OTP'}, status=400)
# End of Code added by Tejasve Gupta on 26-05-2024
# Reason - Functionality of Forget Password


class JobListingListAPIView(APIView):
    # queryset = JobListing.objects.all()
    # serializer_class = JobListingSerializer

    def get(self, request, *args, **kwargs):
        job_listings = JobListing.objects.all()  # Retrieve all job listings
        serializer = JobListingSerializer(job_listings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST method for creating a new job listing
    def post(self, request, *args, **kwargs):
        serializer = JobListingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the job listing if data is valid
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class JobDetailAPIView(APIView):

#     def get(self, request, *args, **kwargs):
#         # Get the 'id' from query params
#         job_id = request.query_params.get('id', 3)
#         if job_id is None:
#             return Response({"error": "Job ID is required."}, status=status.HTTP_400_BAD_REQUEST)

#         # Retrieve the job by id or return a 404 if not found
#         job_listing = get_object_or_404(JobListing, id=job_id)
#         serializer = JobListingSerializer(job_listing)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class ParticularJobDetailAPIView(APIView):
    def get(self, request, id):
        try:
            # Fetch the job by its ID
            job = JobListing.objects.get(id=id)
        except JobListing.DoesNotExist:
            return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the job object
        serializer = ParticularJobListingSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)