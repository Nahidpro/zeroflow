from django.contrib import admin

import packages

from .models import Package
from django.utils import timezone

admin.site.register(Package)