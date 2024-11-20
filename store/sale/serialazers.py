from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name',
                  'last_name', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerialazer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class CategorySerialazer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerialazer(serializers.ModelSerializer):
    average_raitings = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['product_name', 'price', 'product_photo', 'average_raitings',
                  'product_description', ]

    def get_average_raitings(self, obj):
        return obj.get_average_raitings()


class StoreSerialazer(serializers.ModelSerializer):
    average_raitings = serializers.SerializerMethodField()
    product = ProductSerialazer(read_only=True, many=True)
    category = CategorySerialazer(read_only=True, many=True)

    class Meta:
        model = Store
        fields = ['store_name', 'average_raitings', 'store_description', 'contact_info',
                  'address', 'owner', 'product', 'category']


    def get_average_raitings(self,obj):
        return obj.get_average_raitings()


class OrdersSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class CourierSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'


class RatingSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class CartItemSerialazer(serializers.ModelSerializer):
    product = ProductSerialazer(many=True,read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),write_only=True,source='product')

    class Meta:
        model = CarItem
        fields = ['id', 'product', 'product_id', 'quantity', 'get_total_price']


class CartSerialazer(serializers.ModelSerializer):
    items = CartItemSerialazer(read_only=True,many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

        def get_total_price(self,obj):
            return obj.get_total_price()

