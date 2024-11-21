from rest_framework import viewsets, permissions, status, generics
from .models import *
from .serialazers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filter import *
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .permission import *


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerialazer()


class StoreListViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreListSerialazer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['store_name']
    filterset_class = StoreFilterSet
    permission_classes = [CheckCrud, CheckOwnerStore]


class StoreDetailListViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerialazer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['store_name']
    filterset_class = StoreFilterSet
    permission_classes = [CheckCrud, CheckOwnerStore, permissions.IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerialazer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['product_name']
    filterset_class = ProductFilterSet
    ordering_fields = ['price']
    permission_classes = [CheckCrud, permissions.IsAuthenticatedOrReadOnly]


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerialazer
    permission_classes = [CheckCrud, CheckClientOrders, CheckOrders, permissions.IsAuthenticatedOrReadOnly,
                          CheckClient]


class CourierViewSet(viewsets.ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerialazer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerialazer
    permission_classes = [CheckOwner, permissions.IsAuthenticatedOrReadOnly]


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerialazer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CarItemViewSet(viewsets.ModelViewSet):
    queryset = CarItem.objects.all()
    serializer_class = CartItemSerialazer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerialazer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
