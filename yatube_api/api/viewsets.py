from rest_framework import mixins, viewsets


class ListCreateViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """Позволяет получать список объектов и создавать новые объекты."""
    pass
