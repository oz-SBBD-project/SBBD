from rest_framework.routers import DefaultRouter

from .views import AccountViewSet, TransactionViewSet

router = DefaultRouter()
router.register("accounts", AccountViewSet, basename="accounts")
router.register("transactions", TransactionViewSet, basename="transactions")

urlpatterns = router.urls
