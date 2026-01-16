from django.urls import path

from .views import *
urlpatterns = [
    path('signup/', SignupAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('refresh/', TokenAPIVIew.as_view()),
    path('user/', UserAPIView.as_view()),
    # Code Added by Tejasve on 26-05-2024
    # Reason - for functionality of Password Reset
    path('send-otp/', PasswordResetAPIView.as_view(), name='send_otp'),
    path('update-password/', PasswordResetAPIView.as_view(), name='update_password'),
    path('verify-otp/', PasswordResetAPIView.as_view(), name='verify_otp'),
    # End of Code Added by Tejasve on 26-05-2024
    # Reason - for functionality of Password Reset
    path('it-jobs/', JobListingListAPIView.as_view(), name='it-job-listing-list'),
    # path('job-detail/', JobDetailAPIView.as_view(), name='job-detail'),

    path('particular-job-details/<int:id>/', ParticularJobDetailAPIView.as_view(), name='Particular-job-detail'),

]
