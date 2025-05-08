from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework import status



class CustomAuthTokenSerializer(serializers.Serializer):
    
    email = serializers.CharField(label=("email"),write_only=True)
    password = serializers.CharField(label=("password"),
                                     style={"input_type":"password"},
                                     trim_whitespace=False,
                                     write_only=True)
    token = serializers.CharField(label = ("token"),read_only=True)
    def validate(self, attrs):
        username = attrs.get("email") 
        password = attrs.get("password")
        
        if username & password:
            user = authenticate(request= self.context.get("request"),username=username,password=password)
            
            if not user:
                messages = ("Unable to log in with provided credentials.")    
                raise serializers.ValidationError(messages,code='authorization')
            
            if not user.is_verified:
                messages = ('user is not verifying.') 
                raise serializers.ValidationError(messages, code='Verifying')
        else:
            messages = ('Must include "username" and "password" .')
            raise serializers.ValidationError(messages,code='authorization' ) 
               
        attrs['user'] = user    
        return attrs
    