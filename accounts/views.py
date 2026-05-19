import logging

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import LoginSerializer, LogoutSerializer, RegisterSerializer
from app.utils.email_service import EmailService

logger = logging.getLogger(__name__)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        serialized_user = RegisterSerializer(user).data
        EmailService.send(
            subject="Welcome",
            recipient=user.email,
            template_name="emails/account/create_account.html",
            context={
                "name": user.full_name or "Customer",
                "email": user.email,
                "login_url": f"{settings.FRONTEND_BASE_URL}/accounts/login",
            },
        )

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
    permission_classes = [AllowAny]

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
            logger.exception(f"Exception in Logout API - {error}")
            return Response(
                {"message": "Something went wrong", "error": str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
