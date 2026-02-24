from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Account
from .serializers import AccountSerializer


class AccountViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
