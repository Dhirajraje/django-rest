from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from sales.views import add_sale, get_sales, get_sales_aggr, upload_sales_excel


urlpatterns = [
    path('getSales/', get_sales),
    path('addSales/', add_sale),
    path('getAggrSale/', get_sales_aggr),
    path('uploadSales/', upload_sales_excel),
]
