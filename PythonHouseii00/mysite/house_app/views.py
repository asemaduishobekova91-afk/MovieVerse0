from .models import UserProfile, Region, City, District, Property, PropertyImage, Review
from .serializers import (UserProfileSerializer,UserSerializer,LoginSerializer,
                          RegionListSerializer, CityListSerializer,CityDetailSerializer,
                          DistrictListSerializer,PropertyListSerializer,PropertyDetailSerializer,
                          PropertyCreateSerializer,PropertyImageSerializer,ReviewCreateSerializer,
                          ReviewListSerializer,)
from rest_framework import viewsets, generics, status
from .filters import PropertyFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import PropertyPagination
from .permissions import CheckSeller, CheckBuyer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout


class UserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "Вы вышли из системы"})

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(username=self.request.user.username)


class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['region_name']


class CityListView(generics.ListAPIView):
    queryset = City.objects.select_related('region_name').all()
    serializer_class = CityListSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['city_name']
    filterset_fields = ['region_name']


class CityDetailView(generics.RetrieveAPIView):
    queryset = City.objects.select_related('region_name').all()
    serializer_class = CityDetailSerializer


class DistrictListView(generics.ListAPIView):
    queryset = District.objects.select_related('city').all()
    serializer_class = DistrictListSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['district_name']
    filterset_fields = ['city']


class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.select_related('region_name', 'city', 'seller').all()
    serializer_class = PropertyListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['title', 'address', 'city__city_name']
    ordering_fields = ['price', 'area', 'rooms', 'id']
    pagination_class = PropertyPagination


class PropertyDetailView(generics.RetrieveAPIView):
    queryset = Property.objects.select_related('region_name', 'city', 'seller').all()
    serializer_class = PropertyDetailSerializer


class PropertyCreateView(generics.CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyCreateSerializer
    permission_classes = [CheckSeller]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class PropertyUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.select_related('region_name', 'city', 'seller').all()
    serializer_class = PropertyCreateSerializer



class PropertyImageCreateView(generics.CreateAPIView):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer


class PropertyImageDeleteView(generics.DestroyAPIView):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer


class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.select_related('author', 'seller', 'property').all()
    serializer_class = ReviewListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['property', 'seller']
    ordering_fields = ['created_date', 'rating']


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [CheckBuyer]

    def perform_create(self, serializer):
        prop = serializer.validated_data.get("property")
        serializer.save(author=self.request.user, seller=prop.seller)
