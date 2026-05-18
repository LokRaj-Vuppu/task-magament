from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import LoginSerializer, LogoutSerializer, RegisterSerializer

# from accounts.tasks import send_email_on_account_registration
from app.utils.email_service import EmailService


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        serialized_user = RegisterSerializer(user).data
        # Send email from celery
        EmailService.send(
            subject="Welcome",
            recipient=user.email,
            template_name="emails/account/create_account.html",
            context={
                "name": user.full_name or "Customer",
                "email": user.email,
                "login_url": "http://localhost:8000/accounts/login",
            },
        )
        # send_email_on_account_registration.delay(user.email, user.full_name)

        return Response(
            {
                "message": "User registered successfully",
                "token_details": {
                    "access": serialized_user["access"],
                    "refresh": serialized_user["refresh"],
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(
            {"message": "Login Successful", "token_details": serializer.validated_data},
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = LogoutSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as error:
            print(f"Exception in Logput API - {error}")
            return Response(
                {"message": "Something went wrong", "error": str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
