from django.db import models
from django.conf import settings
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    validate_slug)
from django.core.exceptions import ValidationError


class Unit(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=9)

    def clean(self):
        super().clean()

        if not self.name:
            raise ValidationError("Name cannot be empty.")
        if len(self.name) > 200:
            raise ValidationError("Name cannot exceed 200 characters.")
        if not self.symbol:
            raise ValidationError("Symbol cannot be empty.")
        if len(self.symbol) > 9:
            raise ValidationError("Symbol cannot exceed 9 characters.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.name)


class Category(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               null=True, blank=True)

    def clean(self):
        super().clean()

        if not self.name:
            raise ValidationError("Name cannot be empty.")
        if len(self.name) > 200:
            raise ValidationError("Name cannot exceed 200 characters.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    discount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    quantity_per_unit = models.DecimalField(max_digits=5, decimal_places=2)
    currency = models.CharField(max_length=3)
    categories = models.ManyToManyField(Category, through='ProductCategory')

    def clean(self):
        super().clean()

        if not self.name:
            raise ValidationError("Name cannot be empty.")
        if len(self.name) > 200:
            raise ValidationError("Name cannot exceed 200 characters.")
        if not self.description:
            raise ValidationError("Description cannot be empty.")
        if not self.price or self.price <= 0:
            raise ValidationError("Price must be greater than 0.")
        if not self.unit:
            raise ValidationError("Unit cannot be empty.")
        if not self.quantity_per_unit or self.quantity_per_unit <= 0:
            raise ValidationError("Quantity per unit must be greater than 0.")
        if not self.currency:
            raise ValidationError("Currency cannot be empty.")
        if len(self.currency) > 3:
            raise ValidationError("Currency cannot exceed 3 characters.")
        try:
            validate_slug(self.currency)
        except ValidationError as exc:
            raise ValidationError(
                "Currency must be a valid ISO 4217 code."
            ) from exc
        if self.discount < 0 or self.discount > 100:
            raise ValidationError("Discount must be between 0 and 100.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.name)


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Image(models.Model):
    image_file = models.ImageField(upload_to='product_images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    discount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
