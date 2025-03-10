from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserDetailSerializer
from .models import UserAccount
from rest_framework.exceptions import ValidationError
from .serializers import UserUpdateSerializer
from django.contrib.auth import get_user_model
import logging
UserAccount = get_user_model()
logger = logging.getLogger(__name__) 

def Hello(request):
    return HttpResponse("Welcome to Zero Flow!  We are a reliable courier service committed to delivering your packages safely and on time.")

class UserRegistrationView(generics.CreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            logger.info(f"User registered successfully: {user.username}")
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            logger.warning(f"User registration validation error: {e.detail}")
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"User registration error: {e}", exc_info=True)
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class  UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            response_data = {
                "message": "Profile updated successfully.",
                "user": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except ValidationError as e: 
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Error updating user profile.")
            return Response({"error": "An error occurred while updating your profile."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_update(self, serializer):
        serializer.save()