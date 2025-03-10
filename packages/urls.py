from django.urls import path
from .views import (
    PackageCreateView,
    PackageListView,
    PackageDetailView,
    PackageDeleteView,
    PackageRestoreView,
)

urlpatterns = [
    path('', PackageListView.as_view(), name='package-list'),
    path('create/', PackageCreateView.as_view(), name='package-create'),
    path('<str:tracking_number>/', PackageDetailView.as_view(), name='package-detail'),
    path('<str:tracking_number>/delete/', PackageDeleteView.as_view(), name='package-delete'),
    path('<str:tracking_number>/restore/', PackageRestoreView.as_view(), name='package-restore'),
]