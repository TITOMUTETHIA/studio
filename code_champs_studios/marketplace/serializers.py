from rest_framework import serializers
from .models import Model3D, Order
from accounts.models import CustomUser

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "is_creator", "bio", "avatar"]

# Model3D Serializer
class Model3DSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Model3D
        fields = [
            "id",
            "owner",
            "title",
            "description",
            "file",
            "thumbnail",
            "price",
            "license_type",
            "approved",
            "created_at",
        ]

# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    model = Model3DSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "buyer", "model", "amount_cents", "fulfilled", "created_at"]
