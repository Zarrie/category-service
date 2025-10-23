from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, CategorySimilarityViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("similarities", CategorySimilarityViewSet, basename="similarities")

urlpatterns = router.urls