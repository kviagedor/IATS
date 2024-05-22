from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('employees/', views.employees, name="employees"),
    path('itassets/', views.itAsset, name="itassets"),
    path('asset/<str:asset_tag>', views.asset, name="asset"),
    path('emp/', views.universal_search, name="search_results"),
    path('upload-employee-csv/', views.upload_employee_csv, name='upload_employee_csv'),
    path('upload-it-asset-csv/', views.upload_it_asset_csv, name='upload_it_asset_csv'),
    path('asset_chart/', views.asset_chart, name='asset_chart'),
]