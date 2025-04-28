from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('order/create/', views.create_order, name='create_order'),
    path('orders/user/', views.user_orders, name='user_orders'),
    path('orders/<uuid:order_id>/', views.order_detail, name='order_detail'),
    path('orders/cancel/<uuid:order_id>/', views.cancel_order, name='cancel_order'),
    path('orders/search/', views.search_orders, name='search_orders'),
    path('orders/search/results/', views.search_orders_results, name='search_orders_results'),
    path('admin/orders/all/', views.all_orders, name='all_orders'), # URL สำหรับผู้ดูแลระบบ
]