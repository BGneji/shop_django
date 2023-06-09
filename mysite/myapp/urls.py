from django.urls import path
from . import views

from .views import ProductListView, ProductDetailView, ProductDeleteView, PaymentSuccessView, PaymentFailedView, \
    create_checkout_session

app_name = " "

urlpatterns = [
    # http://127.0.0.1:8000/myapp/hello/
    # path('', views.index, name='index'),
    path('', ProductListView.as_view(), name='index'),
    # path('<int:my_id>/', views.indexItem, name='detail'),
    path('<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('add_item/', views.add_item, name='add_item'),
    path('update_item/<int:my_id>/', views.update_item, name='update_item'),
    # path('delete_item/<int:my_id>/', views.delete_item, name='delete_item'),
    path('delete_item/<int:pk>/', ProductDeleteView.as_view(), name='delete_item'),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('failed/', PaymentFailedView.as_view(), name='failed'),
    path("api/checkout-session/<int:id>/", create_checkout_session, name="api_checkout_session"),


]