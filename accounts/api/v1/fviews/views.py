from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from accounts.api.v1.fserializer.serializer import CustomAuthTokenSerializer
from rest_framework.authtoken.models import Token

class CustomObtainToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data = request.data,
            contect ={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.valid_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({"token":token.key, 'user_id':user.pk, "email":user.email})