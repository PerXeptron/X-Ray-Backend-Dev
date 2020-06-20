from rest_framework import serializers

from samplexray.models import XRaySample

from django.contrib.auth.models import User


class XRaySampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = XRaySample
        fields = ['id', 'title', 'image', 'date_posted', 'userperson', 
            'atelectasis', 'cardiomegaly', 'consolidation', 'edema', 'pleural_effusion']

class RegistrationSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type' : 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only':True}
        }

    def save(self):
        user = User(
                username=self.validated_data['username'],
                )
        
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2 :
            raise serializers.ValidationError({'password': 'Passwords Must Match'})

        user.set_password(password)
        user.save()
        return user