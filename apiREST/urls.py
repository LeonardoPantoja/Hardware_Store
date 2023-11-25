from rest_framework import routers
from .api import ProductCategoryViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register(r'productcategory', ProductCategoryViewSet)
router.register(r'product', ProductViewSet )

urlpatterns = router.urls