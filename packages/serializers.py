from django.utils import timezone

from rest_framework import serializers
from django.core.validators import EmailValidator
from .models import Package
import re
import logging

logger = logging.getLogger(__name__)


from django.utils import timezone
from rest_framework import serializers
from .models import Package

from rest_framework import serializers
from django.utils import timezone
from .models import Package

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from .models import Package

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = [
            'id',
            'tracking_number',
            'issued_by',
            'sender_name',
            'sender_address',
            'sender_city',
            'sender_zip_code',
            'sender_phone_number',
            'sender_email',
            'weight',
            'destination',
            'status',
            'created_at',
            'updated_at',
            'delivered_at',
            'package_type',
            'receiver_name',
            'receiver_address',
            'receiver_city',
            'receiver_zip_code',
            'receiver_phone_number',
            'receiver_email',
            'notes',
            'charge',
        ]
        read_only_fields = [
            'tracking_number',
            'created_at',
            'updated_at',
            'issued_by',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            if isinstance(self.instance, Package):
                if self.instance and self.instance.issued_by == request.user:
                    self.fields['status'].read_only = False
            elif not request.user.is_staff:
                self.fields['status'].read_only = True

            if not request.user.is_staff:
                self.fields['charge'].read_only = True

    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight must be greater than zero.")
        return value

    def validate_charge(self, value):
        if value < 0:
            raise serializers.ValidationError("Charge cannot be negative.")
        return value

    def validate_status(self, value):
        
        if self.instance and self.instance.status == 'delivered' and value != 'delivered':
            raise serializers.ValidationError("Cannot change the status of a delivered package.")
        return value

    def validate(self, data):
        
        if not self.instance:
            if data.get('status') == 'delivered':
                data['delivered_at'] = timezone.now()
        else:
            if data.get('status') == 'delivered' and not self.instance.delivered_at:
                data['delivered_at'] = timezone.now()
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['issued_by'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        logger.debug(f"update: instance={instance}, validated_data={validated_data}")
        request = self.context.get('request')
        user = request.user

        if user != instance.issued_by and not user.is_staff: 
            raise PermissionDenied("You do not have permission to modify this package.")

        if validated_data.get('status') == 'delivered' and not instance.delivered_at:
            validated_data['delivered_at'] = timezone.now()

        return super().update(instance, validated_data)


