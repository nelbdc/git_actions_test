from rest_framework import routers
from .views import CompanyView

companies_router = routers.DefaultRouter()
companies_router.register("companies", viewset=CompanyView,basename="companies")
