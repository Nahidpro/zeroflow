from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid
import re
import logging

logger = logging.getLogger(__name__)

def generate_tracking_number():
    date_prefix = timezone.now().strftime("%Y%m%d")
    uuid_part = str(uuid.uuid4()).upper().replace("-", "")[:8]
    return f"{date_prefix}-{uuid_part}"

class ActivePackageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class DeletedPackageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=False)

class Package(models.Model):
    tracking_number = models.CharField(max_length=50, unique=True, default=generate_tracking_number, editable=False)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, 
                                  related_name='issued_packages', help_text="Employee who issued the package")
    
    # Sender Information
    sender_name = models.CharField(max_length=200, help_text="Sender's full name")
    sender_address = models.TextField(help_text="Sender's address")
    sender_city = models.CharField(max_length=100, blank=True, null=True, help_text="Sender's city")
    sender_zip_code = models.CharField(max_length=20, blank=True, null=True, help_text="Sender's zip code")
    sender_phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Sender's phone number")
    sender_email = models.EmailField(blank=True, null=True, help_text="Sender's email")

    # Package Details
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    destination = models.CharField(max_length=200)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    package_type = models.CharField(max_length=50, blank=True, null=True)
    charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, 
                               help_text="Charge for the package delivery")
    
    # Receiver Information
    receiver_name = models.CharField(max_length=200)
    receiver_address = models.TextField()
    receiver_city = models.CharField(max_length=100, blank=True, null=True)
    receiver_zip_code = models.CharField(max_length=20, blank=True, null=True)
    receiver_phone_number = models.CharField(max_length=20, blank=True, null=True)
    receiver_email = models.EmailField(blank=True, null=True)
    
    # Tracking Info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True, help_text="Internal notes about the package")

    objects = models.Manager()
    active_packages = ActivePackageManager()
    deleted_packages = DeletedPackageManager()

    class Meta:
        indexes = [
            models.Index(fields=['tracking_number']),
            models.Index(fields=['status', 'deleted_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.tracking_number

    def clean(self):
        logger.debug(f"clean: status={self.status}, delivered_at={self.delivered_at}")
        if self.status == 'delivered' and not self.delivered_at:
            self.delivered_at = timezone.now()
        elif self.status != 'delivered' and self.delivered_at:
            self.delivered_at = None

    def save(self, *args, **kwargs):
        logger.debug(f"save: status={self.status}, delivered_at={self.delivered_at}")
        self.full_clean()
        super().save(*args, **kwargs)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()  



