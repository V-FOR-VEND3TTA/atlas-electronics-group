from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField

class StoreLocation(models.Model):
    """NY, London, Singapore (timezones, currencies configured elsewhere)"""
    code = models.CharField(max_length=10, unique=True)  # e.g. NY, LON, SIN
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    currency = models.CharField(max_length=3, default="USD")  # adapt per location

    def __str__(self):
        return f"{self.name} ({self.code})"


class Vendor(models.Model):  # manufacturer / supplier
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    price = MoneyField(max_digits=12, decimal_places=2, default_currency="USD")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"


class ProductInventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventories")
    location = models.ForeignKey(StoreLocation, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ("product", "location")

    def __str__(self):
        return f"{self.product.sku} @ {self.location.code} = {self.quantity}"
