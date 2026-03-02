from django.urls import path
from . import views

urlpatterns = [ 
    # Order List
    path('', views.order_list, name='list'),

    # Order Detail
    path('<int:order_id>/', views.order_detail, name='detail'),

    # Order Success
    path('success/', views.order_success, name='success'),
]