"""
This module defines the data models for the products application.

It includes models for units of measure (Unit), product categories (Category),
products (Product), product-category relationships (ProductCategory),
product images (Image), shopping carts (Cart), cart items (CartItem),
and user wishlists (Wishlist).

Each model is a subclass of django.db.models.Model and defines
a set of fields that represent the attributes of the model.
Each model may also define methods for performing operations related to
the model, such as validating the model's fields (clean) or
adding a product to a wishlist (add_product).

The models in this module are used to create the database
schema for the products application.
They are also used by the Django ORM to query the database
and create, read, update, and delete records.

This module also imports several modules from Django for
use in the models, including models (for creating model classes),
settings (for accessing Django settings), validators (for validating
model fields), and exceptions (for raising exceptions in the models).
"""
from django.db import models
from django.conf import settings
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    validate_slug)
from django.core.exceptions import ValidationError


class Unit(models.Model):
    """
    Represents a unit of measure for a product.

    Attributes:
        name (CharField): The name of the unit.
        symbol (CharField): The symbol of the unit.
    """
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
    """
    Represents a product category.

    Attributes:
        name (CharField): The name of the category.
        parent (ForeignKey): The parent category, if any.
    """
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
    """
    Represents a product.

    Attributes:
        name (CharField): The name of the product.
        description (TextField): The description of the product.
        price (DecimalField): The price of the product.
        discount (IntegerField): The discount on the product.
        unit (ForeignKey): The unit of measure for the product.
        quantity_per_unit (DecimalField): The quantity per unit of the product.
        currency (CharField): The currency of the product.
        categories (ManyToManyField): The categories the product belongs to.
    """
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

    def delete(self, *args, **kwargs):
        try:
            image = Image.objects.get(product=self)
            if image.image_file:
                image.image_file.delete(save=False)
            image.delete()
        except Image.DoesNotExist:
            pass
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.name)


class ProductCategory(models.Model):
    """
    Represents the many-to-many relationship between products and categories.

    Attributes:
        product (ForeignKey): The product.
        category (ForeignKey): The category.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Image(models.Model):
    """
    Represents an image of a product.

    Attributes:
        image_file (ImageField): The image file.
        product (ForeignKey): The product the image is of.
    """
    image_file = models.ImageField(upload_to='product_images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def clean(self):
        super().clean()

        if not self.image_file:
            raise ValidationError("Image file cannot be empty.")
        if not self.product:
            raise ValidationError("Product cannot be empty.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.product.name} Image'


class Cart(models.Model):
    """
    Represents a user's shopping cart.

    Attributes:
        user (ForeignKey): The user who owns the cart.
        created_at (DateTimeField): The date and time the cart was created.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    """
    Represents an item in a shopping cart.

    Attributes:
        cart (ForeignKey): The cart the item is in.
        product (ForeignKey): The product the item is.
        quantity (IntegerField): The quantity of the product in the cart.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def clean(self) -> None:
        super().clean()

        if not self.cart:
            raise ValidationError("Cart cannot be empty.")
        if not self.product:
            raise ValidationError("Product cannot be empty.")
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Wishlist(models.Model):
    """
    Represents a user's wishlist.

    Attributes:
        user (ForeignKey): The user who owns the wishlist.
        products (ManyToManyField): The products in the wishlist.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def clean(self) -> None:
        super().clean()

        if not self.user:
            raise ValidationError("User cannot be empty.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def add_product(self, product):
        """
        Adds a product to the wishlist.

        Args:
            product (Product): The product to add.
        """
        if not isinstance(product, Product):
            raise ValueError(
                "Only real products can be added to the wishlist."
            )
        self.products.add(product)
