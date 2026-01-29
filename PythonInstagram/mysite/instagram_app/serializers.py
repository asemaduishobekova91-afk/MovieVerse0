from rest_framework import serializers
from .models import (UserProfile, Follow, City,
                     HashTag, Post, PostContent,
                     PostLike, Review, ReviewLike)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  )
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
        raise serializers.ValidationError("Неверные учетные данные")

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


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'user_photo', 'is_official']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = '__all__'


class PostContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = ['content']


class PostLikeSerializer(serializers.ModelSerializer):
    user = UserNameSerializer()

    class Meta:
        model = PostLike
        fields = ['user', 'like']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserNameSerializer()
    class Meta:
        model = Review
        fields = ['user', 'parent', 'comment', 'created_date']


class PostListSerializer(serializers.ModelSerializer):
    content = PostContentSerializer(many=True, read_only=True)
    user = UserNameSerializer()

    class Meta:
        model = Post
        fields = [ 'user', 'id', 'content']



class PostDetailSerializer(serializers.ModelSerializer):
    user = UserNameSerializer()
    content = PostContentSerializer(many=True, read_only=True)
    like =  PostLikeSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id','user', 'content', 'description', 'created_date', 'like'
                  ,'reviews']


class ReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewLike
        fields = '__all__'

class CreatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'