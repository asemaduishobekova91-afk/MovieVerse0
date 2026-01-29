from django.contrib.auth import authenticate
from rest_framework import serializers
from django.db.models import Avg
from .models import UserProfile, Region, City, District, Property, PropertyImage, Review
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username','email','password','first_name','last_name',
            'phone_number','role',)
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
            self.instance = user
            return data
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'id': instance.id,
                'username': instance.username,
                'email': instance.email,
                'role': getattr(instance, "role", None),
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number', 'role']


class UserProfileReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username']


class RegionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'region_name']


class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name', 'region_name']


class CityPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name']


class CityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name', 'region_name']


class DistrictListSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'district_name', 'city']


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']


class ReviewListSerializer(serializers.ModelSerializer):
    author = UserProfileReviewSerializer(read_only=True)
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'author', 'rating', 'comment', 'created_date']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['property', 'rating', 'comment']


class PropertyListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    city = CityPropertySerializer(read_only=True)
    region_name = RegionListSerializer(read_only=True)
    seller = UserProfileShortSerializer(read_only=True)

    class Meta:
        model = Property
        fields = ['id','images','title','description','price','area','rooms','property_type',
            'condition','region_name','city','address','seller','avg_rating',]

    def get_images(self, obj):
        images = obj.images.all()
        return PropertyImageSerializer(images, many=True, context=self.context).data

    def get_avg_rating(self, obj):
        avg = obj.reviews.aggregate(avg=Avg('rating'))['avg']
        return avg


class PropertyDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    city = CityPropertySerializer(read_only=True)
    region_name = RegionListSerializer(read_only=True)
    seller = UserProfileShortSerializer(read_only=True)
    reviews = ReviewListSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = ['id','title','description','price','area','rooms','floor',
                  'total_floors','property_type','condition','documents',
                  'region_name','city','address','seller','images','reviews',]

    def get_images(self, obj):
        images = obj.images.all()
        return PropertyImageSerializer(images, many=True, context=self.context).data


class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['title','description',
            'property_type','region_name','city','address','area','price',
            'rooms','floor','total_floors','condition','documents',]
