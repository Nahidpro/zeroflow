from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Package
from .serializers import PackageSerializer
from .permissions import IsAdminOrIssuedBy
from .pagination import PackagePagination
import logging

logger = logging.getLogger(__name__)

class PackageCreateView(generics.CreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Package created successfully.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

class PackageListView(generics.ListAPIView):
    serializer_class = PackageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PackagePagination  

    def get_queryset(self):
        qs = Package.active_packages.all().select_related('issued_by')
        if not self.request.user.is_staff:
            qs = qs.filter(issued_by=self.request.user)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "count": self.paginator.page.paginator.count,  
                "data": serializer.data
            })

        # If pagination is disabled
        serializer = self.get_serializer(queryset, many=True)
        return response.Response({
            "count": queryset.count(),
            "data": serializer.data
        })


class PackageDetailView(generics.RetrieveUpdateAPIView):
    queryset = Package.active_packages.all()
    serializer_class = PackageSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrIssuedBy]
    lookup_field = 'tracking_number'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"message": "Package details", "data": serializer.data})

    def update(self, request, *args, **kwargs):
        logger.debug(f"update view: request.data={request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({"message": "Package updated successfully.", "data": serializer.data})

class PackageDeleteView(generics.DestroyAPIView):
    queryset = Package.active_packages.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminOrIssuedBy]
    lookup_field = 'tracking_number'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response({"message": "Package successfully deleted."}, status=status.HTTP_204_NO_CONTENT)

class PackageRestoreView(generics.UpdateAPIView):
    queryset = Package.deleted_packages.all()
    serializer_class = PackageSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrIssuedBy]
    lookup_field = 'tracking_number'

    def get_object(self):
        tracking_number = self.kwargs['tracking_number']
        try:
            return self.queryset.get(tracking_number=tracking_number)
        except Package.DoesNotExist:
            raise NotFound("Package not found")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        self.check_object_permissions(request, instance)

        instance.restore()
        return Response({"message": "Package successfully restored."}, status=status.HTTP_200_OK)