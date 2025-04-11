from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from cloudinary.models import CloudinaryField


# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, email, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    GENDERS = (
        ('f', 'Female'),
        ('m', 'Male'),
        ('u', 'Undisclosed'),
    )
    gender = models.CharField(max_length=1, choices=GENDERS, null=True, blank=True)

    REQUIRED_FIELDS = ['email', 'phone_number']
    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "CustomUsers"

# Address Model
class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    line_1 = models.CharField(max_length=50)
    line_2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    pin_code = models.CharField(max_length=10)
    
    is_shipping = models.BooleanField(default=False)
    is_billing = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.line_1}, {self.city}"

    class Meta:
        verbose_name_plural = "Addresses"

# Coupon Model
class Coupon(models.Model):
    name = models.CharField(max_length=6)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_valid = models.BooleanField(default=True)
    discount_percentage = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Coupons"

# Styles Model

    
class Styles(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    image_model = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Styles"

# Templates Model
class Templates(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    unit_price = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Templates"

# Orders Model
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    coupon_used = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.FloatField(default=0.0)

    PAYMENT_TYPES = (
        ('c', 'Cash on delivery'),
        ('d', 'Debit Card'),
        ('p', 'PayTM'),
    )
    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPES)
    payment_status = models.BooleanField(default=False)

    ordered_at = models.DateTimeField(auto_now_add=True)
    expected_delivery = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='shipping_orders')
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='billing_orders')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    class Meta:
        verbose_name_plural = "Orders"

# Complete Design Model
class CompleteDesign(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)

    content_image = models.URLField()  # Uploaded image
    style = models.ForeignKey(Styles, on_delete=models.CASCADE)
    result_design = models.URLField()  # Output after style transfer

    styled_templates = models.JSONField(default=dict)  # Stores template name + styled image URL

    def __str__(self):
        return f"Design {self.id} by {self.user.username}"

    class Meta:
        verbose_name_plural = "CompleteDesigns"

# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_purchased = models.BooleanField(default=False)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)

    complete_design = models.ForeignKey(CompleteDesign, on_delete=models.CASCADE)

    template = models.ForeignKey(Templates, on_delete=models.CASCADE)
    styled_template_url = models.URLField()  # Final product image with style on template

    quantity = models.IntegerField(default=1)
    unit_price = models.FloatField()

    added_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart item {self.id} for {self.user.username}"

    class Meta:
        verbose_name_plural = "Cart"
