from accounts.serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions, status, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from djoser.views import UserViewSet as DjoserUserViewSet
from djoser.views import UserViewSet
from rest_framework_simplejwt.tokens import RefreshToken,OutstandingToken,BlacklistedToken
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.authentication import JWTAuthentication


from .models import User, Profile
from .serializers import UserSerializer, ProfileSerializer
from permission.permissions import OwnProfilePermission


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
 
class ActivateUser(DjoserUserViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]
    @action(detail=True, methods=['post'])
    def activation(self, request, *args, **kwargs):
        self.action == "activation"
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.user
            super().activation(request, *args, **kwargs)
            response = {
                'detail': 'Account Activated',
                'data': 'Account Activated',
                'user': UserSerializer(user).data,
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        
        except ObjectDoesNotExist:
            return Response({'detail': 'User with this UID does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    
class ProfileView(APIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['get', 'put', 'head']
    permission_classes = [permissions.IsAuthenticated, OwnProfilePermission]
    
    def get(self, request, format=None):
        profile = self.queryset.get(user=request.user)
        serializer = self.serializer_class(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        profile = self.queryset.get(user=request.user)
        serializer = self.serializer_class(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            if request.session:
                request.session.flush()
            else:
                refresh_token = request.data["refresh"]
                token = RefreshToken(refresh_token)
                token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class LogoutAllView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)