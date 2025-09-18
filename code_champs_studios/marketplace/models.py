# marketplace/models.py
import uuid, os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

def model_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"models/{instance.creator.id}/{uuid.uuid4()}.{ext}"

ALLOWED_EXTENSIONS = ['glb','gltf','fbx','obj','blend']

class User(AbstractUser):
    is_creator = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    stripe_account_id = models.CharField(max_length=255, blank=True, null=True)
    # points/badges can be added separately

class LicenseType(models.TextChoices):
    PERSONAL = "personal", _("Personal")
    COMMERCIAL = "commercial", _("Commercial")

class Model3D(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='models')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)
    file = models.FileField(
        upload_to=model_upload_path,
        validators=[FileExtensionValidator(ALLOWED_EXTENSIONS)]
    )
    preview_image = models.ImageField(upload_to='previews/', blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)  # 0 = free
    license_type = models.CharField(max_length=32, choices=LicenseType.choices, default=LicenseType.PERSONAL)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    downloads = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_models', blank=True)
    tags = models.JSONField(default=list, blank=True)

    def is_free(self):
        return float(self.price) == 0.0

    def __str__(self):
        return f"{self.title} by {self.creator}"

class Order(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    model = models.ForeignKey(Model3D, on_delete=models.CASCADE, related_name='orders')
    license_type = models.CharField(max_length=32, choices=LicenseType.choices)
    amount_cents = models.PositiveIntegerField()  # store cents
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)
    download_url = models.URLField(blank=True, null=True)
