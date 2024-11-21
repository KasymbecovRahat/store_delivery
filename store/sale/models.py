from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField

USERS_STATUS = (
    ('Владелец', 'Владелец'),
    ('Клиент', 'Клиент'),
    ('Курьер', 'Курьер')
)

ORDER_STATUS = (
    ('Ожидает  обработки', 'Ожидает  обработки'),
    ('В процессе доставки', 'В процессе доставки'),
    ('Доставлен', 'Доставлен'),
    ('Отменен', 'Отменен')
)

COURIER_STATUS = (
    ('Доступен', 'Доступен'),
    ('Занят', 'Занят')
)


class UserProfile(AbstractUser):
    phonenumber = PhoneNumberField(region='KG')
    user_role = models.CharField(max_length=12, choices=USERS_STATUS, default='client')


class Store(models.Model):
    store_name = models.CharField(max_length=20)
    store_description = models.TextField(null=True, blank=True)
    contact_info = models.TextField()
    address = models.CharField(max_length=20)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store_image = models.ImageField(upload_to='store_photo')

    def __str__(self):
        return f'{self.store_name}, {self.address}'


class Category(models.Model):
    category_name = models.CharField(max_length=20)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='category')


class Product(models.Model):
    product_name = models.CharField(max_length=30)
    product_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product')
    product_photo = models.ImageField(upload_to='product_image/')
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')


    def __str__(self):
        return f'{self.product_name} {self.store}'

    def get_average_raitings(self):
        raitings = self.raitings.all()
        if raitings.exists():
            return round(sum(rating.stars for rating in raitings) / raitings.count(), 1)
        return 0


class Orders(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders_product')
    client_orders = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_orders')
    courier_orders = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courier_orders')
    orders_status = models.CharField(max_length=20, choices=ORDER_STATUS)
    orders_created = models.DateTimeField(auto_now_add=True)
    delivery_adress = models.TextField()

    def __str__(self):
        return f'{self.product} {self.client_orders} {self.orders_status}'


class Courier(models.Model):
    courier_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status_courier = models.CharField(max_length=12, choices=COURIER_STATUS)
    current_orders = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='courier')

    def __str__(self):
        return f'{self.courier_user}'


class Rating(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store_review = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='review_store')
    courier_review = models.ForeignKey(Courier, on_delete=models.CASCADE, related_name='review_courier')
    product_review = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='raitings')
    comment = models.TextField()
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='Рейтинг')

    def __str__(self):
        return f'{self.author} {self.stars} {self.comment}'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart')
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class CarItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity








































