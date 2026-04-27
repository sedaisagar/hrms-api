from rest_framework import  serializers

from users.models import User, ClientProfile


class UserSerializer(serializers.ModelSerializer):
    has_client_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['password']

    def get_has_client_profile(self, instance: User):
        # return ClientProfile.objects.filter(user=instance).exists()
        try:
            return instance.client_profile is not None
        except:
            return False
        
class SocialLinkSerializer(serializers.Serializer):
    facebook = serializers.URLField()
    twitter = serializers.URLField()
    linkedin = serializers.URLField()
    whatsapp = serializers.URLField()
    instagram = serializers.URLField()
    pinterest = serializers.URLField()

class ClientProfileSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=False)

    class Meta:
        model = ClientProfile
        # fields = "__all__"
        exclude = ["client_id"]

    def validate(self, attrs):
        user : User = attrs.get("user")
        if user.role != "user":
            raise serializers.ValidationError({
                "user":["User with role user are only allowed to create client profile!"]
            })


        return super().validate(attrs)
    